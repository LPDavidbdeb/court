# case_manager/exhibit_renderers/common.py

from __future__ import annotations

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


def draw_wrapped_text(
    page: fitz.Page,
    text: str,
    rect: fitz.Rect,
    *,
    fontsize: float = BODY_SIZE,
    fontname: str = FONT_NORMAL,
) -> float:
    """
    Insère du texte dans un rectangle.
    Retourne approximativement la position verticale suivante.
    """
    text = text or ""

    page.insert_textbox(
        rect,
        text,
        fontsize=fontsize,
        fontname=fontname,
        align=fitz.TEXT_ALIGN_LEFT,
    )

    line_height = fontsize * 1.35
    estimated_lines = max(
        1,
        len(text) // max(1, int(rect.width / (fontsize * 0.55))) + 1,
    )

    return rect.y0 + estimated_lines * line_height


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


def normalize_image_bytes(raw: bytes) -> bytes:
    """
    Corrige notamment l'orientation EXIF avant insertion dans le PDF.
    """
    with Image.open(BytesIO(raw)) as image:
        image = ImageOps.exif_transpose(image)

        if image.mode not in ("RGB", "L"):
            image = image.convert("RGB")

        output = BytesIO()
        image.save(output, format="JPEG", quality=92)
        return output.getvalue()


def add_image_page(
    doc: fitz.Document,
    image_bytes: bytes,
) -> fitz.Page:
    """
    Une image par page, centrée et redimensionnée sans déformation.
    """
    normalized = normalize_image_bytes(image_bytes)

    image_doc = fitz.open(
        stream=normalized,
        filetype="jpeg",
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
