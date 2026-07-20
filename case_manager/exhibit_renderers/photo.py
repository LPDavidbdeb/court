# case_manager/exhibit_renderers/photo.py

from pathlib import Path

from .base import BaseExhibitRenderer
from .common import (
    add_exhibit_cover,
    add_image_page,
    add_section_page,
    new_document,
    save_document,
)


class PhotoRenderer(BaseExhibitRenderer):

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
            source_type="Photo",
        )

        multiple = len(sources) > 1

        for index, photo in enumerate(
            sources,
            start=1,
        ):
            if multiple:
                add_section_page(
                    doc,
                    label=f"{row.cote}.{index}",
                )

            if not photo.file:
                raise FileNotFoundError(
                    f"Photo(pk={photo.pk}) sans fichier."
                )

            with photo.file.open("rb") as handle:
                add_image_page(
                    doc,
                    handle.read(),
                )

        return save_document(
            doc,
            destination,
        )
