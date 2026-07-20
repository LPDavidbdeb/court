# case_manager/exhibit_renderers/email.py

from pathlib import Path

import fitz

from .base import BaseExhibitRenderer
from .common import (
    BODY_SIZE,
    MARGIN_BOTTOM,
    MARGIN_LEFT,
    MARGIN_RIGHT,
    MARGIN_TOP,
    PAGE_HEIGHT,
    PAGE_WIDTH,
    add_exhibit_cover,
    add_page,
    new_document,
    save_document,
)


def render_email_into_document(
    doc,
    *,
    email,
    label: str,
):
    page = add_page(doc)

    y = MARGIN_TOP

    metadata = [
        f"{label}",
        f"Date : {email.date_sent or ''}",
        f"De : {email.sender or ''}",
        f"À : {email.recipients_to or ''}",
    ]

    if email.recipients_cc:
        metadata.append(
            f"Cc : {email.recipients_cc}"
        )

    metadata.append(
        f"Objet : {email.subject or ''}"
    )

    header = "\n".join(metadata)

    header_rect = fitz.Rect(
        MARGIN_LEFT,
        y,
        PAGE_WIDTH - MARGIN_RIGHT,
        y + 130,
    )

    page.insert_textbox(
        header_rect,
        header,
        fontsize=10,
        fontname="hebo",
    )

    body_y = y + 145

    body = (
        email.body_plain_text
        or "[Corps du courriel non disponible]"
    )

    body_rect = fitz.Rect(
        MARGIN_LEFT,
        body_y,
        PAGE_WIDTH - MARGIN_RIGHT,
        PAGE_HEIGHT - MARGIN_BOTTOM,
    )

    remaining = page.insert_textbox(
        body_rect,
        body,
        fontsize=BODY_SIZE,
        fontname="helv",
    )

    # Version initiale :
    # si le texte est trop long, PyMuPDF retourne une valeur négative.
    #
    # On pourra ensuite améliorer ceci avec une vraie pagination
    # paragraphe par paragraphe.
    if remaining < 0:
        overflow_page = add_page(doc)

        overflow_page.insert_textbox(
            fitz.Rect(
                MARGIN_LEFT,
                MARGIN_TOP,
                PAGE_WIDTH - MARGIN_RIGHT,
                PAGE_HEIGHT - MARGIN_BOTTOM,
            ),
            body,
            fontsize=BODY_SIZE,
            fontname="helv",
        )


class EmailRenderer(
    BaseExhibitRenderer
):

    def render(
        self,
        *,
        row,
        sources,
        destination: Path,
    ) -> Path:

        doc = new_document()

        add_exhibit_cover(
            doc,
            cote=row.cote,
            description=row.description,
            date=row.date,
            source_type="Courriel",
        )

        multiple = len(sources) > 1

        for index, email in enumerate(
            sources,
            start=1,
        ):
            label = (
                f"{row.cote}.{index}"
                if multiple
                else row.cote
            )

            render_email_into_document(
                doc,
                email=email,
                label=label,
            )

        return save_document(
            doc,
            destination,
        )
