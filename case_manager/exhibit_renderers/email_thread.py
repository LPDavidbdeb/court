# case_manager/exhibit_renderers/email_thread.py

from pathlib import Path

from .base import BaseExhibitRenderer
from .common import (
    add_exhibit_cover,
    new_document,
    save_document,
)

from .email import (
    render_email_into_document,
)


class EmailThreadRenderer(
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
                "EmailThreadRenderer attend "
                "un seul EmailThread."
            )

        thread = sources[0]

        doc = new_document()

        add_exhibit_cover(
            doc,
            cote=row.cote,
            description=row.description,
            date=row.date,
            source_type="Fil de courriels",
        )

        emails = list(
            thread.emails
            .all()
            .order_by(
                "date_sent",
                "pk",
            )
        )

        if not emails:
            raise FileNotFoundError(
                f"EmailThread(pk={thread.pk}) "
                "ne contient aucun courriel."
            )

        for index, email in enumerate(
            emails,
            start=1,
        ):
            render_email_into_document(
                doc,
                email=email,
                label=(
                    f"{row.cote} — "
                    f"courriel {index}/{len(emails)}"
                ),
            )

        return save_document(
            doc,
            destination,
        )
