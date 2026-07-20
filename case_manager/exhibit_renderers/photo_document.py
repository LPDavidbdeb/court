# case_manager/exhibit_renderers/photo_document.py

from pathlib import Path

from .base import BaseExhibitRenderer
from .common import (
    add_exhibit_cover,
    add_image_page,
    add_section_page,
    new_document,
    save_document,
)


class PhotoDocumentRenderer(
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
            source_type="Document photographié",
        )

        multiple_documents = (
            len(sources) > 1
        )

        for index, photodoc in enumerate(
            sources,
            start=1,
        ):
            label = (
                f"{row.cote}.{index}"
                if multiple_documents
                else row.cote
            )

            add_section_page(
                doc,
                label=label,
                title=photodoc.title or "",
                description=(
                    photodoc.description or ""
                ),
            )

            photos = list(
                photodoc.photos
                .all()
                .order_by(
                    "datetime_original",
                    "pk",
                )
            )

            if not photos:
                raise FileNotFoundError(
                    f"PhotoDocument("
                    f"pk={photodoc.pk}) vide."
                )

            for photo in photos:
                if not photo.file:
                    raise FileNotFoundError(
                        f"Photo(pk={photo.pk}) "
                        "sans fichier."
                    )

                with photo.file.open(
                    "rb"
                ) as handle:
                    add_image_page(
                        doc,
                        handle.read(),
                    )

        return save_document(
            doc,
            destination,
        )
