# case_manager/management/commands/build_cahier_pieces.py

from __future__ import annotations

import json
import re
import shutil
from dataclasses import dataclass
from pathlib import Path

import fitz

from django.conf import settings
from django.core.management.base import (
    BaseCommand,
    CommandError,
)

from case_manager.management.commands.sync_pieces import (
    BORDEREAU_PATH,
    parse_bordereau,
)


# ---------------------------------------------------------------------------
# Répertoires
# ---------------------------------------------------------------------------

BASE_DIR = Path(settings.BASE_DIR)

PIECES_PDF_DIR = BASE_DIR / "pieces_pdf"
PIECES_MANIFEST_PATH = PIECES_PDF_DIR / "manifest.json"

OUTPUT_DIR = BASE_DIR / "cahier_pieces"
STAGING_DIR = BASE_DIR / ".cahier_pieces_build"
BACKUP_DIR = BASE_DIR / ".cahier_pieces_backup"


# ---------------------------------------------------------------------------
# Fichiers générés
# ---------------------------------------------------------------------------

CAHIER_FILENAME = "cahier_pieces.pdf"
INDEX_FILENAME = "index_pieces.pdf"
MANIFEST_FILENAME = "manifest_cahier.json"


# ---------------------------------------------------------------------------
# Mise en page
#
# Même format que le pipeline actuel : Letter 612 x 792 points.
# ---------------------------------------------------------------------------

PAGE_WIDTH = 612
PAGE_HEIGHT = 792

MARGIN_LEFT = 48
MARGIN_RIGHT = 48
MARGIN_TOP = 48
MARGIN_BOTTOM = 48

FONT_NORMAL = "helv"
FONT_BOLD = "hebo"

INDEX_FONT_SIZE = 9
INDEX_LINE_HEIGHT = 12

COTE_X = 54
DESCRIPTION_X = 105
DESCRIPTION_RIGHT = 490
PAGE_NUMBER_RIGHT = 555


# ---------------------------------------------------------------------------
# Informations du dossier
#
# Ces constantes peuvent éventuellement être déplacées dans settings.py
# ou dans un modèle Case.
# ---------------------------------------------------------------------------

COURT_NAME = "COUR SUPÉRIEURE"
COURT_CHAMBER = "Chambre civile"
COURT_DISTRICT = "District de Longueuil"

CASE_TITLE = (
    "LOUIS-PHILIPPE DAVID"
)

CASE_VERSUS = (
    "c. ÉLISE MARIE AYOUB ET MARIE-JOSÉE AYOUB"
)

BOOK_TITLE = "CAHIER DES PIÈCES"


# ---------------------------------------------------------------------------
# Structure interne
# ---------------------------------------------------------------------------

@dataclass
class ExhibitEntry:
    cote: str
    description: str
    pdf_path: Path
    page_count: int
    placeholder: bool
    source_type: str
    source_ids: list[str]

    start_page: int = 0
    end_page: int = 0


# ---------------------------------------------------------------------------
# Utilitaires
# ---------------------------------------------------------------------------

def cote_sort_key(cote: str) -> tuple[int, str]:
    """
    Trie P-1, P-2, ..., P-10 correctement.

    Les cotes non standard sont repoussées à la fin.
    """
    match = re.fullmatch(
        r"P-(\d+)",
        cote.strip(),
        re.IGNORECASE,
    )

    if not match:
        return (10**9, cote)

    return (int(match.group(1)), cote)


def sanitize_pdf_text(value: str) -> str:
    """
    Normalise certains caractères Unicode qui peuvent être mal rendus
    par les polices PDF standard de PyMuPDF.

    Les accents français sont conservés.
    """
    if not value:
        return ""

    replacements = {
        "\u00a0": " ",   # espace insécable
        "–": "-",
        "—": "-",
        "→": "->",
        "←": "<-",
        "“": '"',
        "”": '"',
        "’": "'",
        "…": "...",
    }

    for old, new in replacements.items():
        value = value.replace(old, new)

    return " ".join(
        value.split()
    )


def pdf_page_count(path: Path) -> int:
    """
    Retourne le nombre réel de pages d'un PDF.
    """
    doc = fitz.open(str(path))

    try:
        return doc.page_count
    finally:
        doc.close()


def text_width(
    text: str,
    *,
    fontsize: float,
    fontname: str = FONT_NORMAL,
) -> float:
    return fitz.get_text_length(
        text,
        fontsize=fontsize,
        fontname=fontname,
    )


def wrap_text(
    text: str,
    *,
    max_width: float,
    fontsize: float,
    fontname: str = FONT_NORMAL,
) -> list[str]:
    """
    Retourne une liste de lignes qui tiennent dans max_width.
    """
    text = sanitize_pdf_text(text)

    if not text:
        return [""]

    words = text.split()

    lines: list[str] = []
    current = ""

    for word in words:
        candidate = (
            f"{current} {word}".strip()
            if current
            else word
        )

        if text_width(
            candidate,
            fontsize=fontsize,
            fontname=fontname,
        ) <= max_width:
            current = candidate
            continue

        if current:
            lines.append(current)

        current = word

    if current:
        lines.append(current)

    return lines or [""]


# ---------------------------------------------------------------------------
# Lecture et validation des 105 pièces
# ---------------------------------------------------------------------------

def load_exhibit_entries() -> list[ExhibitEntry]:
    """
    Construit la liste canonique des pièces à partir :

        legal/bordereau_pieces.md
        +
        pieces_pdf/manifest.json
        +
        pieces_pdf/P-x.pdf

    Toute cote en erreur ou tout PDF manquant bloque la construction
    du cahier.

    Les placeholders sont toutefois autorisés.
    """

    if not PIECES_MANIFEST_PATH.exists():
        raise CommandError(
            "Manifest des pièces introuvable : "
            f"{PIECES_MANIFEST_PATH}"
        )

    manifest = json.loads(
        PIECES_MANIFEST_PATH.read_text(
            encoding="utf-8"
        )
    )

    summary = manifest.get(
        "_summary",
        {},
    )

    if summary.get(
        "error_count",
        0,
    ) > 0:
        raise CommandError(
            "Le manifest pieces_pdf contient "
            f"{summary['error_count']} erreur(s). "
            "Le cahier ne sera pas construit."
        )

    rows = parse_bordereau(
        BORDEREAU_PATH
    )

    rows = sorted(
        rows,
        key=lambda row: cote_sort_key(
            row.cote
        ),
    )

    seen: set[str] = set()
    entries: list[ExhibitEntry] = []

    for row in rows:
        cote = row.cote

        if cote in seen:
            raise CommandError(
                f"Cote dupliquée dans le bordereau : {cote}"
            )

        seen.add(cote)

        piece_meta = manifest.get(
            cote
        )

        if not piece_meta:
            raise CommandError(
                f"{cote} absente de "
                "pieces_pdf/manifest.json."
            )

        if piece_meta.get(
            "status"
        ) != "ok":
            raise CommandError(
                f"{cote} n'a pas le statut ok."
            )

        output_name = (
            piece_meta.get("output")
            or f"{cote}.pdf"
        )

        pdf_path = (
            PIECES_PDF_DIR
            / output_name
        )

        if not pdf_path.exists():
            raise CommandError(
                f"PDF introuvable pour {cote} : "
                f"{pdf_path}"
            )

        count = pdf_page_count(
            pdf_path
        )

        if count < 1:
            raise CommandError(
                f"{cote} contient zéro page."
            )

        entries.append(
            ExhibitEntry(
                cote=cote,
                description=row.description,
                pdf_path=pdf_path,
                page_count=count,
                placeholder=bool(
                    piece_meta.get(
                        "placeholder",
                        False,
                    )
                ),
                source_type=(
                    piece_meta.get(
                        "source_type",
                        ""
                    )
                ),
                source_ids=list(
                    piece_meta.get(
                        "source_ids",
                        []
                    )
                ),
            )
        )

    manifest_exhibit_count = (
        summary.get(
            "exhibit_count"
        )
    )

    if (
        manifest_exhibit_count is not None
        and manifest_exhibit_count
        != len(entries)
    ):
        raise CommandError(
            "Incohérence entre le bordereau "
            "et le manifest : "
            f"{len(entries)} cotes dans le bordereau, "
            f"{manifest_exhibit_count} dans le manifest."
        )

    return entries


# ---------------------------------------------------------------------------
# Index
# ---------------------------------------------------------------------------

def add_index_page_header(
    doc: fitz.Document,
    page_number: int,
) -> tuple[fitz.Page, float]:
    """
    Crée une nouvelle page d'index et retourne :
        page
        position Y de la première entrée
    """

    page = doc.new_page(
        width=PAGE_WIDTH,
        height=PAGE_HEIGHT,
    )

    page.insert_text(
        (MARGIN_LEFT, MARGIN_TOP),
        "INDEX DES PIÈCES",
        fontsize=16,
        fontname=FONT_BOLD,
    )

    page.insert_text(
        (
            MARGIN_LEFT,
            MARGIN_TOP + 22,
        ),
        f"Page d'index {page_number}",
        fontsize=8,
        fontname=FONT_NORMAL,
    )

    header_y = MARGIN_TOP + 55

    page.insert_text(
        (COTE_X, header_y),
        "Cote",
        fontsize=9,
        fontname=FONT_BOLD,
    )

    page.insert_text(
        (
            DESCRIPTION_X,
            header_y,
        ),
        "Description",
        fontsize=9,
        fontname=FONT_BOLD,
    )

    page_text = "Page"

    width = text_width(
        page_text,
        fontsize=9,
        fontname=FONT_BOLD,
    )

    page.insert_text(
        (
            PAGE_NUMBER_RIGHT - width,
            header_y,
        ),
        page_text,
        fontsize=9,
        fontname=FONT_BOLD,
    )

    page.draw_line(
        (
            MARGIN_LEFT,
            header_y + 8,
        ),
        (
            PAGE_WIDTH - MARGIN_RIGHT,
            header_y + 8,
        ),
        width=0.5,
    )

    return (
        page,
        header_y + 28,
    )


def render_index_document(
    entries: list[ExhibitEntry],
    *,
    mark_placeholders: bool,
) -> tuple[
    fitz.Document,
    list[tuple[int, fitz.Rect, int]],
]:
    """
    Génère l'index.

    Retourne :
        - le document PDF de l'index;
        - la liste des zones cliquables :
          (
              page_index_dans_index,
              rectangle,
              page_cible_du_cahier
          )

    Les liens seront ajoutés après la fusion finale.
    """

    doc = fitz.open()

    link_specs: list[
        tuple[int, fitz.Rect, int]
    ] = []

    page_number = 1

    page, y = add_index_page_header(
        doc,
        page_number,
    )

    description_width = (
        DESCRIPTION_RIGHT
        - DESCRIPTION_X
    )

    for entry in entries:
        display_description = (
            entry.description
        )

        if (
            mark_placeholders
            and entry.placeholder
        ):
            display_description += (
                " [REPRÉSENTATION TEMPORAIRE]"
            )

        lines = wrap_text(
            display_description,
            max_width=description_width,
            fontsize=INDEX_FONT_SIZE,
        )

        row_height = max(
            1,
            len(lines),
        ) * INDEX_LINE_HEIGHT + 7

        if (
            y + row_height
            > PAGE_HEIGHT - MARGIN_BOTTOM
        ):
            page_number += 1

            page, y = (
                add_index_page_header(
                    doc,
                    page_number,
                )
            )

        row_top = y - 10

        page.insert_text(
            (
                COTE_X,
                y,
            ),
            entry.cote,
            fontsize=INDEX_FONT_SIZE,
            fontname=FONT_BOLD,
        )

        for line_index, line in enumerate(
            lines
        ):
            page.insert_text(
                (
                    DESCRIPTION_X,
                    y
                    + line_index
                    * INDEX_LINE_HEIGHT,
                ),
                sanitize_pdf_text(
                    line
                ),
                fontsize=INDEX_FONT_SIZE,
                fontname=FONT_NORMAL,
            )

        if entry.start_page > 0:
            page_value = str(
                entry.start_page
            )

            width = text_width(
                page_value,
                fontsize=INDEX_FONT_SIZE,
                fontname=FONT_NORMAL,
            )

            page.insert_text(
                (
                    PAGE_NUMBER_RIGHT
                    - width,
                    y,
                ),
                page_value,
                fontsize=INDEX_FONT_SIZE,
                fontname=FONT_NORMAL,
            )

        # Ligne discrète entre les entrées.
        page.draw_line(
            (
                DESCRIPTION_X,
                y + row_height - 7,
            ),
            (
                PAGE_NUMBER_RIGHT,
                y + row_height - 7,
            ),
            width=0.15,
        )

        row_rect = fitz.Rect(
            MARGIN_LEFT,
            row_top,
            PAGE_WIDTH - MARGIN_RIGHT,
            y + row_height - 3,
        )

        if entry.start_page > 0:
            link_specs.append(
                (
                    page.number,
                    row_rect,
                    entry.start_page,
                )
            )

        y += row_height

    return doc, link_specs


# ---------------------------------------------------------------------------
# Page titre
# ---------------------------------------------------------------------------

def insert_centered_text(
    page: fitz.Page,
    text: str,
    y: float,
    *,
    fontsize: float,
    fontname: str,
) -> None:
    width = PAGE_WIDTH - 2 * MARGIN_LEFT

    page.insert_textbox(
        fitz.Rect(
            MARGIN_LEFT,
            y,
            PAGE_WIDTH - MARGIN_RIGHT,
            y + 60,
        ),
        sanitize_pdf_text(text),
        fontsize=fontsize,
        fontname=fontname,
        align=fitz.TEXT_ALIGN_CENTER,
    )


def add_cahier_cover(
    doc: fitz.Document,
    *,
    exhibit_count: int,
    placeholder_count: int,
) -> None:
    page = doc.new_page(
        width=PAGE_WIDTH,
        height=PAGE_HEIGHT,
    )

    insert_centered_text(
        page,
        COURT_NAME,
        70,
        fontsize=15,
        fontname=FONT_BOLD,
    )

    insert_centered_text(
        page,
        COURT_CHAMBER,
        100,
        fontsize=10,
        fontname=FONT_NORMAL,
    )

    insert_centered_text(
        page,
        COURT_DISTRICT,
        125,
        fontsize=10,
        fontname=FONT_NORMAL,
    )

    insert_centered_text(
        page,
        CASE_TITLE,
        220,
        fontsize=13,
        fontname=FONT_BOLD,
    )

    insert_centered_text(
        page,
        CASE_VERSUS,
        255,
        fontsize=11,
        fontname=FONT_NORMAL,
    )

    insert_centered_text(
        page,
        BOOK_TITLE,
        365,
        fontsize=22,
        fontname=FONT_BOLD,
    )

    insert_centered_text(
        page,
        f"P-1 à P-{exhibit_count}",
        410,
        fontsize=14,
        fontname=FONT_NORMAL,
    )

    if placeholder_count:
        insert_centered_text(
            page,
            (
                f"Version de travail - "
                f"{placeholder_count} représentation(s) "
                "temporaire(s)"
            ),
            650,
            fontsize=8,
            fontname=FONT_NORMAL,
        )


# ---------------------------------------------------------------------------
# Pagination continue
# ---------------------------------------------------------------------------

def stamp_page_numbers(
    doc: fitz.Document,
) -> None:
    """
    Ajoute une pagination continue au cahier complet.

    Les PDF individuels dans pieces_pdf/ ne sont jamais modifiés.
    """

    total = doc.page_count

    for index in range(
        total
    ):
        page = doc[index]

        label = (
            f"Page {index + 1} de {total}"
        )

        width = text_width(
            label,
            fontsize=8,
        )

        page.insert_text(
            (
                (
                    PAGE_WIDTH
                    - width
                )
                / 2,
                PAGE_HEIGHT - 18,
            ),
            label,
            fontsize=8,
            fontname=FONT_NORMAL,
        )


# ---------------------------------------------------------------------------
# Signets PDF
# ---------------------------------------------------------------------------

def build_toc(
    entries: list[ExhibitEntry],
    *,
    index_page_count: int,
) -> list[list]:
    """
    PyMuPDF utilise des pages 1-based dans set_toc().
    """

    toc: list[list] = [
        [
            1,
            "Page titre",
            1,
        ],
        [
            1,
            "Index des pièces",
            2,
        ],
    ]

    if entries:
        toc.append(
            [
                1,
                "Pièces",
                entries[0].start_page,
            ]
        )

    for entry in entries:
        title = sanitize_pdf_text(
            entry.description
        )

        if len(title) > 100:
            title = (
                title[:97]
                + "..."
            )

        toc.append(
            [
                2,
                (
                    f"{entry.cote} - "
                    f"{title}"
                ),
                entry.start_page,
            ]
        )

    return toc


# ---------------------------------------------------------------------------
# Manifest du cahier
# ---------------------------------------------------------------------------

def build_cahier_manifest(
    entries: list[ExhibitEntry],
    *,
    index_page_count: int,
    total_pages: int,
) -> dict:

    placeholder_count = sum(
        1
        for entry in entries
        if entry.placeholder
    )

    pieces_page_count = sum(
        entry.page_count
        for entry in entries
    )

    manifest: dict = {
        "_summary": {
            "exhibit_count": len(
                entries
            ),
            "placeholder_count": (
                placeholder_count
            ),
            "cover_page_count": 1,
            "index_page_count": (
                index_page_count
            ),
            "pieces_page_count": (
                pieces_page_count
            ),
            "total_page_count": (
                total_pages
            ),
            "source_manifest": (
                "pieces_pdf/manifest.json"
            ),
            "source_bordereau": str(
                BORDEREAU_PATH.relative_to(
                    BASE_DIR
                )
            ),
        }
    }

    for entry in entries:
        manifest[
            entry.cote
        ] = {
            "description": (
                entry.description
            ),
            "source_pdf": (
                entry.pdf_path.name
            ),
            "source_type": (
                entry.source_type
            ),
            "source_ids": (
                entry.source_ids
            ),
            "source_page_count": (
                entry.page_count
            ),
            "start_page": (
                entry.start_page
            ),
            "end_page": (
                entry.end_page
            ),
            "placeholder": (
                entry.placeholder
            ),
        }

    return manifest


# ---------------------------------------------------------------------------
# Validation finale
# ---------------------------------------------------------------------------

def validate_final_cahier(
    path: Path,
    *,
    expected_pages: int,
    expected_exhibits: int,
) -> None:

    doc = fitz.open(
        str(path)
    )

    try:
        if doc.page_count != expected_pages:
            raise CommandError(
                "Nombre de pages du cahier incohérent : "
                f"{doc.page_count} obtenu, "
                f"{expected_pages} attendu."
            )

        toc = doc.get_toc()

        # 3 entrées structurelles :
        # page titre, index, pièces
        expected_toc_minimum = (
            expected_exhibits
            + 3
        )

        if (
            len(toc)
            < expected_toc_minimum
        ):
            raise CommandError(
                "Le nombre de signets du cahier "
                "est inférieur au nombre attendu."
            )

    finally:
        doc.close()


# ---------------------------------------------------------------------------
# Commande Django
# ---------------------------------------------------------------------------

class Command(
    BaseCommand
):

    help = (
        "Construit un cahier consolidé à partir "
        "des PDF normalisés de pieces_pdf/."
    )

    def add_arguments(
        self,
        parser,
    ):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help=(
                "Valide les pièces et calcule "
                "la pagination sans produire le cahier."
            ),
        )

        parser.add_argument(
            "--mark-placeholders",
            action="store_true",
            help=(
                "Ajoute une mention temporaire dans "
                "l'index pour les pièces placeholder."
            ),
        )

        parser.add_argument(
            "--no-page-numbers",
            action="store_true",
            help=(
                "N'ajoute pas la pagination continue "
                "au pied des pages du cahier."
            ),
        )

    def handle(
        self,
        *args,
        **options,
    ):
        dry_run = options[
            "dry_run"
        ]

        mark_placeholders = options[
            "mark_placeholders"
        ]

        no_page_numbers = options[
            "no_page_numbers"
        ]

        # ---------------------------------------------------------------
        # 1. Charger et valider les pièces
        # ---------------------------------------------------------------

        entries = (
            load_exhibit_entries()
        )

        placeholder_count = sum(
            1
            for entry in entries
            if entry.placeholder
        )

        self.stdout.write(
            f"{len(entries)} pièce(s) "
            "validée(s)."
        )

        if placeholder_count:
            self.stdout.write(
                self.style.WARNING(
                    f"{placeholder_count} "
                    "placeholder(s) seront "
                    "inclus dans le cahier."
                )
            )

        # ---------------------------------------------------------------
        # 2. Première passe :
        #    déterminer combien de pages occupe l'index.
        #
        # Les pages de départ sont temporairement à zéro.
        # Leur valeur ne change pas la hauteur des lignes de l'index.
        # ---------------------------------------------------------------

        probe_index, _ = (
            render_index_document(
                entries,
                mark_placeholders=(
                    mark_placeholders
                ),
            )
        )

        index_page_count = (
            probe_index.page_count
        )

        probe_index.close()

        # ---------------------------------------------------------------
        # 3. Calculer les pages finales.
        #
        # Page 1       = couverture
        # Pages 2...N  = index
        # Page N+2     = première pièce
        # ---------------------------------------------------------------

        next_page = (
            1
            + index_page_count
            + 1
        )

        for entry in entries:
            entry.start_page = (
                next_page
            )

            entry.end_page = (
                entry.start_page
                + entry.page_count
                - 1
            )

            next_page = (
                entry.end_page
                + 1
            )

        expected_total_pages = (
            next_page
            - 1
        )

        pieces_page_count = sum(
            entry.page_count
            for entry in entries
        )

        self.stdout.write(
            (
                f"Index : "
                f"{index_page_count} page(s)"
            )
        )

        self.stdout.write(
            (
                f"Pièces : "
                f"{pieces_page_count} page(s)"
            )
        )

        self.stdout.write(
            (
                f"Cahier final prévu : "
                f"{expected_total_pages} page(s)"
            )
        )

        if dry_run:
            self.stdout.write(
                self.style.SUCCESS(
                    "Dry-run terminé. "
                    "Aucun fichier généré."
                )
            )
            return

        # ---------------------------------------------------------------
        # 4. Préparer staging.
        # ---------------------------------------------------------------

        if STAGING_DIR.exists():
            shutil.rmtree(
                STAGING_DIR
            )

        STAGING_DIR.mkdir(
            parents=True
        )

        try:
            # -----------------------------------------------------------
            # 5. Générer l'index final avec les vraies pages.
            # -----------------------------------------------------------

            index_doc, index_links = (
                render_index_document(
                    entries,
                    mark_placeholders=(
                        mark_placeholders
                    ),
                )
            )

            if (
                index_doc.page_count
                != index_page_count
            ):
                raise CommandError(
                    "La pagination de l'index a changé "
                    "entre les deux passes."
                )

            index_path = (
                STAGING_DIR
                / INDEX_FILENAME
            )

            index_doc.save(
                str(index_path),
                garbage=4,
                deflate=True,
            )

            # -----------------------------------------------------------
            # 6. Construire le cahier.
            # -----------------------------------------------------------

            cahier = fitz.open()

            add_cahier_cover(
                cahier,
                exhibit_count=len(
                    entries
                ),
                placeholder_count=(
                    placeholder_count
                ),
            )

            # Index après la couverture.
            cahier.insert_pdf(
                index_doc
            )

            # Pièces P-1 -> P-n.
            for entry in entries:
                source = fitz.open(
                    str(
                        entry.pdf_path
                    )
                )

                try:
                    cahier.insert_pdf(
                        source
                    )
                finally:
                    source.close()

            # -----------------------------------------------------------
            # 7. Index cliquable.
            #
            # Dans le cahier final :
            # page 0 = couverture
            # page 1 = première page d'index
            # -----------------------------------------------------------

            for (
                index_local_page,
                rect,
                target_page,
            ) in index_links:

                cahier_page_index = (
                    1
                    + index_local_page
                )

                page = cahier[
                    cahier_page_index
                ]

                page.insert_link(
                    {
                        "kind": (
                            fitz.LINK_GOTO
                        ),
                        "from": rect,
                        # LINK_GOTO utilise
                        # une page 0-based.
                        "page": (
                            target_page
                            - 1
                        ),
                    }
                )

            # -----------------------------------------------------------
            # 8. Signets PDF.
            # -----------------------------------------------------------

            toc = build_toc(
                entries,
                index_page_count=(
                    index_page_count
                ),
            )

            cahier.set_toc(
                toc
            )

            # -----------------------------------------------------------
            # 9. Pagination continue.
            # -----------------------------------------------------------

            if not no_page_numbers:
                stamp_page_numbers(
                    cahier
                )

            cahier_path = (
                STAGING_DIR
                / CAHIER_FILENAME
            )

            cahier.save(
                str(cahier_path),
                garbage=4,
                deflate=True,
            )

            cahier.close()
            index_doc.close()

            # -----------------------------------------------------------
            # 10. Manifest du cahier.
            # -----------------------------------------------------------

            cahier_manifest = (
                build_cahier_manifest(
                    entries,
                    index_page_count=(
                        index_page_count
                    ),
                    total_pages=(
                        expected_total_pages
                    ),
                )
            )

            manifest_path = (
                STAGING_DIR
                / MANIFEST_FILENAME
            )

            manifest_path.write_text(
                json.dumps(
                    cahier_manifest,
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )

            # -----------------------------------------------------------
            # 11. Validation du PDF final.
            # -----------------------------------------------------------

            validate_final_cahier(
                cahier_path,
                expected_pages=(
                    expected_total_pages
                ),
                expected_exhibits=(
                    len(entries)
                ),
            )

            # -----------------------------------------------------------
            # 12. Swap atomique.
            #
            # L'ancien cahier n'est remplacé qu'après validation complète.
            # -----------------------------------------------------------

            if BACKUP_DIR.exists():
                shutil.rmtree(
                    BACKUP_DIR
                )

            if OUTPUT_DIR.exists():
                OUTPUT_DIR.rename(
                    BACKUP_DIR
                )

            try:
                STAGING_DIR.rename(
                    OUTPUT_DIR
                )

            except Exception:
                if (
                    BACKUP_DIR.exists()
                    and not OUTPUT_DIR.exists()
                ):
                    BACKUP_DIR.rename(
                        OUTPUT_DIR
                    )

                raise

            if BACKUP_DIR.exists():
                shutil.rmtree(
                    BACKUP_DIR
                )

        except Exception as exc:
            # On conserve le staging pour diagnostic.
            if isinstance(
                exc,
                CommandError,
            ):
                raise

            raise CommandError(
                "Échec de construction du cahier. "
                f"Le diagnostic demeure dans "
                f"{STAGING_DIR.name}/. "
                f"Erreur : {exc}"
            ) from exc

        self.stdout.write(
            self.style.SUCCESS(
                "Cahier construit avec succès : "
                f"{OUTPUT_DIR / CAHIER_FILENAME}"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                "Index : "
                f"{OUTPUT_DIR / INDEX_FILENAME}"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                "Manifest : "
                f"{OUTPUT_DIR / MANIFEST_FILENAME}"
            )
        )
