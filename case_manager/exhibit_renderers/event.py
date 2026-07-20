# case_manager/exhibit_renderers/event.py

from pathlib import Path

from .base import BaseExhibitRenderer
from .common import (
    add_exhibit_cover,
    add_image_page,
    add_section_page,
    new_document,
    save_document,
)


class EventRenderer(BaseExhibitRenderer):

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
            source_type="Événement photographique",
        )

        multiple_events = len(sources) > 1

        for index, event in enumerate(
            sources,
            start=1,
        ):
            label = (
                f"{row.cote}.{index}"
                if multiple_events
                else row.cote
            )

            explanation = (
                event.explanation or ""
            )

            # Pour une liasse, chaque Event est clairement
            # identifié comme sous-cote.
            #
            # Pour un Event unique, cette page constitue
            # également la fiche descriptive de l'événement.
            add_section_page(
                doc,
                label=label,
                title=row.description,
                date=str(event.date),
                description=explanation,
            )

            photos = list(
                event.linked_photos
                .all()
                .order_by(
                    "datetime_original",
                    "pk",
                )
            )

            if not photos:
                raise FileNotFoundError(
                    f"Event(pk={event.pk}) "
                    "ne contient aucune photo."
                )

            for photo in photos:
                if not photo.file:
                    raise FileNotFoundError(
                        f"Photo(pk={photo.pk}) "
                        f"liée à Event(pk={event.pk}) "
                        "sans fichier."
                    )

                with photo.file.open(
                    "rb"
                ) as handle:
                    # Cote `event` = photographies (liasses P-45→P-57) :
                    # JPEG q92 pour maîtriser la taille (PNG exploserait à
                    # des dizaines de Mo par pièce).
                    add_image_page(
                        doc,
                        handle.read(),
                        image_format="jpeg",
                    )

        return save_document(
            doc,
            destination,
        )
