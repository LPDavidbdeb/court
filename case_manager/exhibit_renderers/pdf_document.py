# case_manager/exhibit_renderers/pdf_document.py

from pathlib import Path

from .base import BaseExhibitRenderer
from .common import (
    add_exhibit_cover,
    add_section_page,
    append_pdf_bytes,
    new_document,
    save_document,
)


class PdfDocumentRenderer(
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
            source_type="Document PDF",
        )

        multiple = len(sources) > 1

        for index, pdf_obj in enumerate(
            sources,
            start=1,
        ):
            if multiple:
                add_section_page(
                    doc,
                    label=f"{row.cote}.{index}",
                    title=(
                        getattr(
                            pdf_obj,
                            "title",
                            "",
                        )
                        or ""
                    ),
                )

            if not pdf_obj.file:
                raise FileNotFoundError(
                    f"PDFDocument("
                    f"pk={pdf_obj.pk}) "
                    "sans fichier."
                )

            with pdf_obj.file.open(
                "rb"
            ) as handle:
                append_pdf_bytes(
                    doc,
                    handle.read(),
                )

        return save_document(
            doc,
            destination,
        )
