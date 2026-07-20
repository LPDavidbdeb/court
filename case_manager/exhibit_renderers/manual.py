# case_manager/exhibit_renderers/manual.py

from pathlib import Path

from django.conf import settings

from .base import BaseExhibitRenderer
from .common import (
    add_exhibit_cover,
    add_image_page,
    append_pdf_bytes,
    new_document,
    save_document,
)


MANUAL_DIR = (
    Path(settings.BASE_DIR)
    / "manual_pieces"
)


class ManualRenderer(
    BaseExhibitRenderer
):

    def render(
        self,
        *,
        row,
        sources,
        destination: Path,
    ) -> Path:

        if len(sources) != 1:
            raise ValueError(
                "ManualRenderer attend "
                "une seule source."
            )

        source = sources[0]

        model_name = (
            source.__class__
            .__name__
            .lower()
        )

        source_key = (
            f"{model_name}-{source.pk}"
        )

        directory = (
            MANUAL_DIR
            / source_key
        )

        doc = new_document()

        add_exhibit_cover(
            doc,
            cote=row.cote,
            description=row.description,
            date=row.date,
            source_type=model_name,
        )

        if not directory.exists():
            page = doc.new_page()

            page.insert_textbox(
                page.rect,
                (
                    "REPRÉSENTATION PHYSIQUE "
                    "NON ENCORE DISPONIBLE\n\n"
                    f"Source : {source_key}\n"
                    f"Cote : {row.cote}"
                ),
                fontsize=14,
            )

            return save_document(
                doc,
                destination,
            )

        files = sorted(
            p
            for p in directory.iterdir()
            if p.is_file()
        )

        for file_path in files:
            suffix = (
                file_path.suffix.lower()
            )

            if suffix == ".pdf":
                append_pdf_bytes(
                    doc,
                    file_path.read_bytes(),
                )

            elif suffix in {
                ".jpg",
                ".jpeg",
                ".png",
                ".webp",
            }:
                add_image_page(
                    doc,
                    file_path.read_bytes(),
                )

        return save_document(
            doc,
            destination,
        )
