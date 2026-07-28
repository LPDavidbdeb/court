# case_manager/exhibit_renderers/text_layout.py

"""
Mise en page de texte long et **fidélité des caractères**, partagées par les
renderers qui composent une pièce à partir du modèle plutôt que d'assembler
des fichiers existants.

Les polices Base-14 du PDF (`helv`, `hebo`) ne couvrent pas tout le
répertoire français : « œ » y devient « ? », sans le moindre avertissement.
Pour une pièce, une substitution silencieuse est inacceptable. Chaque
insertion choisit donc la police la plus simple qui restitue le texte
**caractère pour caractère**, et bascule au besoin sur une police Unicode
intégrée. Si aucune police disponible ne peut rendre un caractère, le rendu
**échoue** plutôt que de produire une altération invisible.
"""

from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path

import fitz

from django.conf import settings

from .common import (
    FONT_BOLD,
    FONT_NORMAL,
    MARGIN_BOTTOM,
    MARGIN_TOP,
    PAGE_HEIGHT,
    PAGE_WIDTH,
    add_page,
)


# Espacement vertical entre deux blocs.
PARAGRAPH_SPACING = 8

# Interligne du corps de texte, en multiples de la taille de police. La
# police intégrée a un leading plus compact que la Base-14 : le fixer
# explicitement rend la mise en page indépendante de la police retenue.
LINE_HEIGHT = 1.35

# Alias interne de la police Unicode intégrée.
UNICODE_FONT_ALIAS = "docuni"

# Caractères invisibles retirés avant rendu : aucun contenu sémantique,
# aucune police ne les restitue.
INVISIBLE_CHARS = "\u200b\u200c\u200d\ufeff"

# Polices candidates, par ordre de préférence. `settings.EXHIBIT_FONT_FILE`
# a priorité si elle est définie.
FONT_CANDIDATES = (
    # macOS
    "/System/Library/Fonts/Helvetica.ttc",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    "/System/Library/Fonts/Geneva.ttf",
    # Linux
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/TTF/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    # Windows
    "C:/Windows/Fonts/arial.ttf",
)


# ---------------------------------------------------------------------------
# Fidélité des caractères
# ---------------------------------------------------------------------------

def _roundtrip_ok(char: str, fontname: str, fontfile: str | None) -> bool:
    """
    Écrit `char` puis le relit : seul un aller-retour identique prouve que la
    police restitue réellement le caractère.
    """
    doc = fitz.open()
    page = doc.new_page(width=PAGE_WIDTH, height=PAGE_HEIGHT)

    try:
        page.insert_text(
            (72, 72),
            char,
            fontsize=12,
            fontname=fontname,
            fontfile=fontfile,
        )
        extracted = page.get_text().strip()
    except Exception:
        return False
    finally:
        doc.close()

    return extracted == char


@lru_cache(maxsize=None)
def char_supported(char: str, fontname: str, fontfile: str | None) -> bool:
    return _roundtrip_ok(char, fontname, fontfile)


@lru_cache(maxsize=1)
def unicode_font() -> str | None:
    """
    Première police candidate qui restitue fidèlement une sonde française.
    Retourne son chemin, ou None si aucune n'est disponible.
    """
    probe = "œŒàâçèéêëîïôùûüÀÉÈÊÇÔÛ«»…—–’"

    configured = getattr(settings, "EXHIBIT_FONT_FILE", None)

    candidates = (
        (str(configured),) if configured else ()
    ) + FONT_CANDIDATES

    for path in candidates:
        if not Path(path).exists():
            continue

        if all(
            _roundtrip_ok(c, UNICODE_FONT_ALIAS, path)
            for c in probe
        ):
            return path

    return None


def pick_font(text: str, preferred: str) -> tuple[str, str | None]:
    """
    Retourne (fontname, fontfile) : la police qui rend le plus fidèlement
    `text`.

    Le corps du texte passe systématiquement par la police Unicode dès
    qu'elle est disponible : mélanger Base-14 et police intégrée d'un bloc à
    l'autre produirait des interlignages différents pour un même niveau. Les
    libellés courts (numéros, titres en gras) conservent la Base-14 tant
    qu'elle les restitue fidèlement.
    """
    chars = {c for c in text if c.strip()}

    fontfile = unicode_font()

    if preferred == FONT_NORMAL and fontfile is not None:
        return UNICODE_FONT_ALIAS, fontfile

    if all(char_supported(c, preferred, None) for c in chars):
        return preferred, None

    if fontfile is not None:
        return UNICODE_FONT_ALIAS, fontfile

    return preferred, None


def substitute_unsupported(
    text: str,
    fontname: str,
    fontfile: str | None,
) -> tuple[str, list[str]]:
    """
    Remplace les caractères que la police ne restitue pas — émojis, symboles
    hors répertoire — par un marqueur explicite `[U+XXXX]`.

    Une pièce ne doit jamais subir d'altération **silencieuse** : la
    substitution est donc visible dans le texte et retournée à l'appelant,
    qui doit la documenter.
    """
    unsupported = {
        c
        for c in set(text)
        if c.strip() and not char_supported(c, fontname, fontfile)
    }

    if not unsupported:
        return text, []

    for char in unsupported:
        text = text.replace(char, f"[U+{ord(char):04X}]")

    return text, sorted(unsupported)


def clean(text: str) -> str:
    """
    Retire les caractères invisibles. Aucune autre normalisation : le libellé
    doit rester celui de la base.
    """
    if not text:
        return ""

    return text.translate({ord(c): None for c in INVISIBLE_CHARS})


def prepare(text: str, preferred: str) -> tuple[str, str, str | None, list[str]]:
    """
    Prépare un fragment pour l'insertion : nettoyage, choix de police et
    substitution documentée des caractères non rendus.

    Retourne (texte, fontname, fontfile, caractères substitués).
    """
    text = clean(text)

    fontname, fontfile = pick_font(text, preferred)

    text, substitutions = substitute_unsupported(text, fontname, fontfile)

    return text, fontname, fontfile, substitutions


# ---------------------------------------------------------------------------
# Mise en page
# ---------------------------------------------------------------------------

def fits(
    text: str,
    rect: fitz.Rect,
    fontsize: float,
    fontname: str,
    fontfile: str | None,
) -> bool:
    doc = fitz.open()
    page = doc.new_page(width=PAGE_WIDTH, height=PAGE_HEIGHT)

    unused = page.insert_textbox(
        rect,
        text,
        fontsize=fontsize,
        fontname=fontname,
        fontfile=fontfile,
        lineheight=LINE_HEIGHT,
        align=fitz.TEXT_ALIGN_LEFT,
    )

    doc.close()

    return unused >= 0


def largest_prefix(
    tokens: list[str],
    rect: fitz.Rect,
    fontsize: float,
    fontname: str,
    fontfile: str | None,
) -> int:
    """
    Nombre de tokens de tête dont la concaténation tient dans `rect`
    (recherche par dichotomie ; la propriété est monotone).
    """
    lo, hi, best = 0, len(tokens), 0

    while lo <= hi:
        mid = (lo + hi) // 2

        if mid == 0 or fits(
            "".join(tokens[:mid]), rect, fontsize, fontname, fontfile
        ):
            best, lo = mid, mid + 1
        else:
            hi = mid - 1

    return best


class Flow:
    """
    Curseur de mise en page : page courante et ordonnée du prochain bloc.
    """

    def __init__(self, doc: fitz.Document):
        self.doc = doc
        self.page = add_page(doc)
        self.y = MARGIN_TOP

        # Caractères remplacés par un marqueur faute de police les rendant.
        # L'appelant doit les documenter dans la pièce.
        self.substitutions: set[str] = set()

    @property
    def bottom(self) -> float:
        return self.page.rect.height - MARGIN_BOTTOM

    def new_page(self) -> None:
        self.page = add_page(self.doc)
        self.y = MARGIN_TOP

    def space_left(self) -> float:
        return self.bottom - self.y

    def ensure(self, height: float) -> None:
        """
        Garantit `height` points disponibles, en changeant de page au besoin.
        """
        if self.space_left() < height:
            self.new_page()

    def rule(self, x0: float, x1: float, *, gap: float = 4) -> None:
        self.y += gap

        self.page.draw_line(
            fitz.Point(x0, self.y),
            fitz.Point(x1, self.y),
            width=0.4,
            color=(0.6, 0.6, 0.6),
        )

        self.y += gap

    def insert(
        self,
        text: str,
        *,
        x0: float,
        x1: float,
        fontsize: float,
        preferred: str = FONT_NORMAL,
    ) -> None:
        """
        Insère `text` dans la colonne [x0, x1], en paginant si nécessaire et
        sans jamais perdre de contenu.
        """
        text, fontname, fontfile, substitutions = prepare(text, preferred)

        if not text.strip():
            return

        self.substitutions.update(substitutions)

        tokens = re.split(r"(\s+)", text)
        i = 0

        while i < len(tokens):
            rect = fitz.Rect(x0, self.y, x1, self.bottom)

            n = largest_prefix(
                tokens[i:], rect, fontsize, fontname, fontfile
            )

            if n == 0:
                if self.y > MARGIN_TOP:
                    self.new_page()
                    continue

                # Un token seul déborde une page vide : forcer la progression.
                n = 1

            unused = self.page.insert_textbox(
                rect,
                "".join(tokens[i:i + n]),
                fontsize=fontsize,
                fontname=fontname,
                fontfile=fontfile,
                lineheight=LINE_HEIGHT,
                align=fitz.TEXT_ALIGN_LEFT,
            )

            self.y += rect.height - max(unused, 0)

            i += n

            if i < len(tokens):
                self.new_page()

    def label(
        self,
        text: str,
        *,
        x: float,
        fontsize: float,
        preferred: str = FONT_BOLD,
    ) -> None:
        """
        Écrit un libellé court sur une seule ligne, sans pagination.
        """
        text, fontname, fontfile, substitutions = prepare(text, preferred)

        if not text.strip():
            return

        self.substitutions.update(substitutions)

        self.page.insert_text(
            (x, self.y + fontsize),
            text,
            fontsize=fontsize,
            fontname=fontname,
            fontfile=fontfile,
        )
