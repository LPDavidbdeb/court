# case_manager/exhibit_renderers/email.py

from email import policy
from email.parser import BytesParser
from pathlib import Path

import fitz

from .base import BaseExhibitRenderer
from .common import (
    BODY_SIZE,
    MARGIN_LEFT,
    MARGIN_RIGHT,
    MARGIN_TOP,
    PAGE_HEIGHT,
    PAGE_WIDTH,
    add_exhibit_cover,
    add_image_page,
    add_page,
    add_paginated_text,
    add_section_page,
    append_pdf_bytes,
    new_document,
    save_document,
)


# Seuil sous lequel une image sans nom est considérée comme une
# signature / un pixel de suivi et ignorée.
SIGNATURE_IMAGE_MAX_BYTES = 10_240


def _read_eml_bytes(email_obj):
    """
    Lit le .eml associé (FileField ou chemin local). Retourne None si aucun
    n'est accessible — le fichier peut être absent du disque alors que le
    corps texte reste en base.
    """
    eml_file = getattr(email_obj, "eml_file", None)
    if eml_file and getattr(eml_file, "name", None):
        try:
            with eml_file.open("rb") as handle:
                return handle.read()
        except (FileNotFoundError, OSError):
            pass

    eml_path = getattr(email_obj, "eml_file_path", None)
    if eml_path:
        path = Path(eml_path)
        try:
            if path.exists():
                return path.read_bytes()
        except OSError:
            pass

    return None


def extract_eml_attachments(email_obj):
    """
    Retourne les pièces jointes réelles d'un courriel : (nom, content_type,
    octets). Parcourt **walk()** (et non iter_attachments()), car certaines
    PJ — notamment les PDF de P-31 — sont attachées en `inline` et seraient
    autrement ignorées. Ignore le corps texte et les petites images de
    signature. Robuste : .eml absent/illisible -> liste vide.
    """
    raw = _read_eml_bytes(email_obj)
    if not raw:
        return []

    try:
        message = BytesParser(policy=policy.default).parsebytes(raw)
    except Exception:
        return []

    attachments = []
    for part in message.walk():
        if part.is_multipart():
            continue

        maintype = part.get_content_maintype()
        ctype = part.get_content_type()
        disposition = (part.get_content_disposition() or "").lower()
        filename = part.get_filename()

        # Le corps du courriel (text/plain, text/html) n'est pas une PJ,
        # sauf s'il est explicitement marqué « attachment ».
        if maintype == "text" and disposition != "attachment":
            continue

        try:
            payload = part.get_payload(decode=True)
        except Exception:
            continue

        if not payload:
            continue

        # Petites images sans nom = signatures / pixels de suivi.
        if (
            maintype == "image"
            and not filename
            and len(payload) < SIGNATURE_IMAGE_MAX_BYTES
        ):
            continue

        if not filename:
            extension = ctype.split("/")[-1].split("+")[0]
            filename = f"piece_jointe.{extension}"

        attachments.append((filename, ctype, payload))

    return attachments


IMAGE_SUFFIXES = (
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".gif",
    ".tif",
    ".tiff",
    ".bmp",
)


def render_attachments_into_document(doc, *, email, label):
    """
    Rend chaque pièce jointe après le corps du courriel :
      - PDF    -> pages fusionnées
      - image  -> une page image (PNG, fidélité — souvent un document scanné)
      - autre  -> page de note (ex. .docx : conversion à définir)
    Toute pièce jointe illisible produit une note, jamais un crash.
    """
    for filename, ctype, payload in extract_eml_attachments(email):
        low = filename.lower()
        pj_label = f"{label} — pièce jointe"

        is_pdf = ctype == "application/pdf" or low.endswith(".pdf")
        is_image = ctype.startswith("image/") or low.endswith(IMAGE_SUFFIXES)

        try:
            if is_pdf:
                add_section_page(doc, label=pj_label, title=filename)
                append_pdf_bytes(doc, payload)

            elif is_image:
                add_section_page(doc, label=pj_label, title=filename)
                add_image_page(doc, payload, image_format="png")

            else:
                add_section_page(
                    doc,
                    label=pj_label,
                    title=filename,
                    description=(
                        f"Type : {ctype}\n\n"
                        "Le rendu automatique de ce format (p. ex. .docx) "
                        "n'est pas encore pris en charge. La pièce jointe "
                        "existe et doit être convertie ou incluse "
                        "manuellement."
                    ),
                )
        except Exception as exc:  # PJ corrompue / illisible
            add_section_page(
                doc,
                label=pj_label,
                title=filename,
                description=(
                    f"Type : {ctype}\n\n"
                    f"Pièce jointe illisible automatiquement : {exc}. "
                    "À inclure manuellement."
                ),
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

    body = (
        email.body_plain_text
        or "[Corps du courriel non disponible]"
    )

    body_first_rect = fitz.Rect(
        MARGIN_LEFT,
        y + 145,
        PAGE_WIDTH - MARGIN_RIGHT,
        PAGE_HEIGHT - MARGIN_TOP,
    )

    # Pagination fiable : le corps s'étend sur autant de pages que
    # nécessaire, la première commençant sous l'en-tête.
    add_paginated_text(
        doc,
        body,
        fontsize=BODY_SIZE,
        fontname="helv",
        first_page=page,
        first_rect=body_first_rect,
    )

    # Pièces jointes (talons de paie de P-31, DOCX de P-87, etc.).
    render_attachments_into_document(
        doc,
        email=email,
        label=label,
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
