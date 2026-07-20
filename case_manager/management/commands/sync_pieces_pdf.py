# case_manager/management/commands/sync_pieces_pdf.py

from __future__ import annotations

import json
import shutil
from pathlib import Path

from django.conf import settings
from django.core.management.base import (
    BaseCommand,
    CommandError,
)

from document_manager.models import Document
from email_manager.models import (
    Email,
    EmailThread,
)
from events.models import Event
from googlechat_manager.models import (
    ChatSequence,
)
from pdf_manager.models import PDFDocument
from photos.models import (
    Photo,
    PhotoDocument,
)

from case_manager.exhibit_renderers.registry import (
    RENDERERS,
)

# Réutilisation du moteur déjà validé.
from case_manager.management.commands.sync_pieces import (
    BORDEREAU_PATH,
    parse_bordereau,
    resolve_source,
)


OUTPUT_DIR = (
    Path(settings.BASE_DIR)
    / "pieces_pdf"
)

STAGING_DIR = (
    Path(settings.BASE_DIR)
    / ".pieces_pdf_build"
)

BACKUP_DIR = (
    Path(settings.BASE_DIR)
    / ".pieces_pdf_backup"
)


def resolve_objects(ref):
    """
    Transforme SourceRef en objets Django.
    """

    if ref.kind == "pdf":
        return [
            PDFDocument.objects.get(
                pk=int(pk)
            )
            for pk in ref.ids
        ]

    if ref.kind == "photo":
        return [
            Photo.objects.get(
                pk=int(pk)
            )
            for pk in ref.ids
        ]

    if ref.kind == "photodoc":
        return [
            PhotoDocument.objects.get(
                pk=int(pk)
            )
            for pk in ref.ids
        ]

    if ref.kind == "event":
        return [
            Event.objects.get(
                pk=int(pk)
            )
            for pk in ref.ids
        ]

    if ref.kind == "email":
        return [
            Email.objects.get(
                pk=int(pk)
            )
            for pk in ref.ids
        ]

    if ref.kind == "thread":
        if len(ref.ids) != 1:
            raise ValueError(
                "Une cote thread doit "
                "référencer un seul thread."
            )

        raw_id = ref.ids[0]

        if raw_id.isdigit():
            thread = (
                EmailThread.objects.get(
                    pk=int(raw_id)
                )
            )
        else:
            thread = (
                EmailThread.objects.get(
                    thread_id=raw_id
                )
            )

        return [thread]

    if ref.kind == "document":
        return [
            Document.objects.get(
                pk=int(ref.ids[0])
            )
        ]

    if ref.kind == "chatsequence":
        return [
            ChatSequence.objects.get(
                pk=int(ref.ids[0])
            )
        ]

    raise ValueError(
        f"Type non supporté : "
        f"{ref.kind}"
    )


class Command(BaseCommand):

    help = (
        "Génère une représentation PDF "
        "normalisée de chaque pièce."
    )

    def add_arguments(
        self,
        parser,
    ):
        parser.add_argument(
            "--dry-run",
            action="store_true",
        )
        parser.add_argument(
            "--only",
            nargs="+",
            default=None,
            help=(
                "Limite le traitement à une "
                "liste de cotes, ex. --only P-2 P-43"
            ),
        )

    def handle(
        self,
        *args,
        **options,
    ):
        dry_run = options["dry_run"]
        only = options.get("only")

        # --only en génération RÉELLE : sortie dans un dossier séparé
        # (pieces_pdf_test/), afin de ne JAMAIS écraser le jeu complet
        # pieces_pdf/. Un filtrage partiel ne doit pas détruire les 105.
        if only and not dry_run:
            output_dir = Path(settings.BASE_DIR) / "pieces_pdf_test"
            staging_dir = Path(settings.BASE_DIR) / ".pieces_pdf_test_build"
            backup_dir = Path(settings.BASE_DIR) / ".pieces_pdf_test_backup"
            self.stdout.write(
                self.style.WARNING(
                    "Mode --only : génération partielle dans "
                    "pieces_pdf_test/ (pieces_pdf/ n'est pas modifié)."
                )
            )
        else:
            output_dir, staging_dir, backup_dir = (
                OUTPUT_DIR,
                STAGING_DIR,
                BACKUP_DIR,
            )

        rows = parse_bordereau(
            BORDEREAU_PATH
        )

        if only:
            wanted = set(only)
            rows = [r for r in rows if r.cote in wanted]

        self.stdout.write(
            f"{len(rows)} cotes trouvées."
        )

        manifest = {}

        if dry_run:
            for row in rows:
                ref = resolve_source(row)

                if ref is None:
                    raise CommandError(
                        f"{row.cote} non résolue."
                    )

                if ref.kind not in RENDERERS:
                    raise CommandError(
                        f"Aucun renderer pour "
                        f"{ref.kind}."
                    )

                sources = resolve_objects(
                    ref
                )

                self.stdout.write(
                    f"{row.cote:<6} "
                    f"-> {ref.kind}:"
                    f"{','.join(ref.ids)} "
                    f"-> {row.cote}.pdf"
                )

            self.stdout.write(
                self.style.SUCCESS(
                    "Dry-run terminé."
                )
            )

            return

        if staging_dir.exists():
            shutil.rmtree(
                staging_dir
            )

        staging_dir.mkdir(
            parents=True
        )

        try:
            for row in rows:

                ref = resolve_source(row)

                if ref is None:
                    raise CommandError(
                        f"{row.cote} "
                        "non résolue."
                    )

                renderer = (
                    RENDERERS.get(
                        ref.kind
                    )
                )

                if renderer is None:
                    raise CommandError(
                        f"Aucun renderer "
                        f"pour {ref.kind}."
                    )

                sources = (
                    resolve_objects(ref)
                )

                destination = (
                    staging_dir
                    / f"{row.cote}.pdf"
                )

                self.stdout.write(
                    f"{row.cote:<6} "
                    f"-> {ref.kind}:"
                    f"{','.join(ref.ids)}"
                )

                output = renderer.render(
                    row=row,
                    sources=sources,
                    destination=destination,
                )

                manifest[row.cote] = {
                    "status": "ok",
                    "source_type": (
                        ref.kind
                    ),
                    "source_ids": (
                        list(ref.ids)
                    ),
                    "description": (
                        row.description
                    ),
                    "output": (
                        output.name
                    ),
                }

            manifest_path = (
                staging_dir
                / "manifest.json"
            )

            manifest_path.write_text(
                json.dumps(
                    manifest,
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )

            if backup_dir.exists():
                shutil.rmtree(
                    backup_dir
                )

            if output_dir.exists():
                output_dir.rename(
                    backup_dir
                )

            try:
                staging_dir.rename(
                    output_dir
                )

            except Exception:
                if (
                    backup_dir.exists()
                    and not output_dir.exists()
                ):
                    backup_dir.rename(
                        output_dir
                    )

                raise

            if backup_dir.exists():
                shutil.rmtree(
                    backup_dir
                )

        except Exception:
            if staging_dir.exists():
                shutil.rmtree(
                    staging_dir
                )

            raise

        self.stdout.write(
            self.style.SUCCESS(
                "PDF générés dans : "
                f"{output_dir}"
            )
        )
