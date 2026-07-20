# case_manager/exhibit_renderers/common.py

from __future__ import annotations

import re
from io import BytesIO
from pathlib import Path

import fitz
from PIL import Image, ImageOps


PAGE_WIDTH = 612
PAGE_HEIGHT = 792

MARGIN_LEFT = 54
MARGIN_RIGHT = 54
MARGIN_TOP = 54
MARGIN_BOTTOM = 54

FONT_NORMAL = "helv"
FONT_BOLD = "hebo"

TITLE_SIZE = 18
SUBTITLE_SIZE = 12
BODY_SIZE = 10
SMALL_SIZE = 8


def new_document() -> fitz.Document:
    return fitz.open()


def add_page(doc: fitz.Document) -> fitz.Page:
    return doc.new_page(width=PAGE_WIDTH, height=PAGE_HEIGHT)


def add_exhibit_cover(
    doc: fitz.Document,
    *,
    cote: str,
    description: str,
    date: str = "",
    source_type: str = "",
) -> fitz.Page:
    """
    Page de garde commune à toutes les pièces.
    Modifier cette fonction modifie la présentation globale.
    """
    page = add_page(doc)

    y = MARGIN_TOP

    page.insert_text(
        (MARGIN_LEFT, y),
        "COUR SUPÉRIEURE",
        fontsize=12,
        fontname=FONT_BOLD,
    )

    y += 30

    page.insert_text(
        (MARGIN_LEFT, y),
        f"PIÈCE {cote}",
        fontsize=TITLE_SIZE,
        fontname=FONT_BOLD,
    )

    y += 30

    if date:
        page.insert_text(
            (MARGIN_LEFT, y),
            str(date),
            fontsize=SUBTITLE_SIZE,
            fontname=FONT_NORMAL,
        )
        y += 28

    description_rect = fitz.Rect(
        MARGIN_LEFT,
        y,
        PAGE_WIDTH - MARGIN_RIGHT,
        PAGE_HEIGHT - 120,
    )

    page.insert_textbox(
        description_rect,
        description or "",
        fontsize=SUBTITLE_SIZE,
        fontname=FONT_NORMAL,
    )

    if source_type:
        page.insert_text(
            (MARGIN_LEFT, PAGE_HEIGHT - 45),
            f"Type de source : {source_type}",
            fontsize=SMALL_SIZE,
            fontname=FONT_NORMAL,
        )

    return page


def add_section_page(
    doc: fitz.Document,
    *,
    label: str,
    title: str = "",
    date: str = "",
    description: str = "",
) -> fitz.Page:
    """
    Séparateur pour les sous-cotes P-x.1, P-x.2, etc.
    """
    page = add_page(doc)

    y = MARGIN_TOP

    page.insert_text(
        (MARGIN_LEFT, y),
        label,
        fontsize=16,
        fontname=FONT_BOLD,
    )

    y += 30

    if title:
        page.insert_textbox(
            fitz.Rect(
                MARGIN_LEFT,
                y,
                PAGE_WIDTH - MARGIN_RIGHT,
                y + 80,
            ),
            title,
            fontsize=12,
            fontname=FONT_BOLD,
        )
        y += 70

    if date:
        page.insert_text(
            (MARGIN_LEFT, y),
            str(date),
            fontsize=10,
        )
        y += 25

    if description:
        page.insert_textbox(
            fitz.Rect(
                MARGIN_LEFT,
                y,
                PAGE_WIDTH - MARGIN_RIGHT,
                PAGE_HEIGHT - MARGIN_BOTTOM,
            ),
            description,
            fontsize=10,
        )

    return page


# ---------------------------------------------------------------------------
# Images
# ---------------------------------------------------------------------------

def normalize_image_bytes(
    raw: bytes,
    *,
    image_format: str = "jpeg",
    quality: int = 92,
) -> bytes:
    """
    Corrige l'orientation EXIF et réécrit l'image dans le format demandé.

    image_format="png"  -> **sans perte** : pour les captures et documents
                           (fidélité du texte — P-8, P-101, documents scannés).
    image_format="jpeg" -> qualité `quality` : pour les photographies
                           (liasses d'événements — taille maîtrisée).
    """
    with Image.open(BytesIO(raw)) as image:
        image = ImageOps.exif_transpose(image)

        output = BytesIO()

        if image_format == "png":
            if image.mode not in ("RGB", "RGBA", "L"):
                image = image.convert("RGB")
            image.save(output, format="PNG")
        else:
            if image.mode not in ("RGB", "L"):
                image = image.convert("RGB")
            image.save(output, format="JPEG", quality=quality)

        return output.getvalue()


def add_image_page(
    doc: fitz.Document,
    image_bytes: bytes,
    *,
    image_format: str = "jpeg",
) -> fitz.Page:
    """
    Une image par page, centrée et redimensionnée sans déformation.
    `image_format` : "png" (captures/documents) ou "jpeg" (photographies).
    """
    normalized = normalize_image_bytes(
        image_bytes,
        image_format=image_format,
    )

    image_doc = fitz.open(
        stream=normalized,
        filetype=image_format,
    )

    pix = image_doc[0].get_pixmap()

    page = add_page(doc)

    available_width = PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT
    available_height = PAGE_HEIGHT - MARGIN_TOP - MARGIN_BOTTOM

    ratio = min(
        available_width / pix.width,
        available_height / pix.height,
    )

    width = pix.width * ratio
    height = pix.height * ratio

    x0 = (PAGE_WIDTH - width) / 2
    y0 = (PAGE_HEIGHT - height) / 2

    target = fitz.Rect(
        x0,
        y0,
        x0 + width,
        y0 + height,
    )

    page.insert_image(
        target,
        stream=normalized,
        keep_proportion=True,
    )

    image_doc.close()

    return page


def append_pdf_bytes(
    target: fitz.Document,
    pdf_bytes: bytes,
) -> None:
    source = fitz.open(
        stream=pdf_bytes,
        filetype="pdf",
    )

    target.insert_pdf(source)
    source.close()


def save_document(
    doc: fitz.Document,
    destination: Path,
) -> Path:
    destination.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    doc.save(
        str(destination),
        garbage=4,
        deflate=True,
    )

    doc.close()

    return destination


# ---------------------------------------------------------------------------
# Pagination fiable du texte long (courriels)
# ---------------------------------------------------------------------------

def _text_fits(
    text: str,
    rect: fitz.Rect,
    fontsize: float,
    fontname: str,
) -> bool:
    """
    Teste, sur une page jetable, si `text` tient ENTIÈREMENT dans `rect`.
    insert_textbox retourne la hauteur inutilisée (>= 0) ou un débordement
    (< 0).
    """
    tmp = fitz.open()
    page = tmp.new_page(width=PAGE_WIDTH, height=PAGE_HEIGHT)
    rc = page.insert_textbox(
        rect,
        text,
        fontsize=fontsize,
        fontname=fontname,
        align=fitz.TEXT_ALIGN_LEFT,
    )
    tmp.close()
    return rc >= 0


def _largest_prefix(
    tokens: list[str],
    rect: fitz.Rect,
    fontsize: float,
    fontname: str,
) -> int:
    """
    Nombre de tokens de tête dont la concaténation tient dans `rect`
    (recherche par dichotomie ; monotone).
    """
    lo, hi, best = 0, len(tokens), 0
    while lo <= hi:
        mid = (lo + hi) // 2
        candidate = "".join(tokens[:mid])
        if mid == 0 or _text_fits(candidate, rect, fontsize, fontname):
            best, lo = mid, mid + 1
        else:
            hi = mid - 1
    return best


def add_paginated_text(
    doc: fitz.Document,
    text: str,
    *,
    fontsize: float = BODY_SIZE,
    fontname: str = FONT_NORMAL,
    first_page: fitz.Page | None = None,
    first_rect: fitz.Rect | None = None,
) -> None:
    """
    Insère `text` en le paginant sur autant de pages que nécessaire, sans
    jamais perdre de contenu : pour chaque page, on cherche par dichotomie
    le plus grand fragment (en tokens, espaces et sauts de ligne conservés)
    qui tient réellement.

    `first_page` / `first_rect` permettent de commencer sous un en-tête
    (courriel) ; les pages suivantes utilisent toute la surface utile.
    """
    full_rect = fitz.Rect(
        MARGIN_LEFT,
        MARGIN_TOP,
        PAGE_WIDTH - MARGIN_RIGHT,
        PAGE_HEIGHT - MARGIN_BOTTOM,
    )

    text = text or ""
    tokens = re.split(r"(\s+)", text)  # conserve espaces et sauts de ligne

    if not "".join(tokens).strip():
        return

    if first_page is not None:
        page, rect = first_page, (first_rect or full_rect)
    else:
        page, rect = add_page(doc), full_rect

    i = 0
    while i < len(tokens):
        n = _largest_prefix(tokens[i:], rect, fontsize, fontname)

        if n == 0:
            # Un token seul déborde même une page vide : on le force pour
            # garantir la progression (cas extrême d'un « mot » gigantesque).
            n = 1

        page.insert_textbox(
            rect,
            "".join(tokens[i:i + n]),
            fontsize=fontsize,
            fontname=fontname,
            align=fitz.TEXT_ALIGN_LEFT,
        )

        i += n

        if i < len(tokens):
            page, rect = add_page(doc), full_rect
