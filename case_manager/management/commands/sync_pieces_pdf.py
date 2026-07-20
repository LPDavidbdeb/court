# case_manager/management/commands/sync_pieces_pdf.py

from __future__ import annotations

import json
import shutil
from pathlib import Path

import fitz

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
from case_manager.exhibit_renderers.email import (
    extract_eml_attachments,
)
from case_manager.exhibit_renderers.manual import (
    MANUAL_DIR,
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


def _page_count(path) -> int:
    doc = fitz.open(str(path))
    count = doc.page_count
    doc.close()
    return count


def compute_stats(ref, sources, output_path) -> dict:
    """
    Compteurs d'intégrité par cote : compare les OBJETS SOURCES attendus au
    nombre de pages réellement rendues, pour détecter toute perte avant même
    d'ouvrir les PDF. Les compteurs varient selon le type.
    """
    stats = {
        "source_count": len(ref.ids),
        "page_count": _page_count(output_path),
        "placeholder": False,
    }

    kind = ref.kind

    if kind == "email":
        stats["email_count"] = len(sources)
        stats["attachment_count"] = sum(
            len(extract_eml_attachments(e)) for e in sources
        )

    elif kind == "thread":
        emails = list(sources[0].emails.all())
        stats["email_count"] = len(emails)
        stats["attachment_count"] = sum(
            len(extract_eml_attachments(e)) for e in emails
        )

    elif kind == "event":
        stats["event_count"] = len(sources)
        stats["photo_count"] = sum(
            e.linked_photos.count() for e in sources
        )

    elif kind == "photodoc":
        stats["photodoc_count"] = len(sources)
        stats["photo_count"] = sum(
            pd.photos.count() for pd in sources
        )

    elif kind == "photo":
        stats["photo_count"] = len(sources)

    elif kind == "pdf":
        stats["pdf_count"] = len(sources)

    elif kind in ("document", "chatsequence"):
        src = sources[0]
        key = f"{src.__class__.__name__.lower()}-{src.pk}"
        directory = MANUAL_DIR / key
        supported_exts = {".pdf", ".jpg", ".jpeg", ".png", ".webp"}
        has_manual = directory.exists() and any(
            p.is_file() and p.suffix.lower() in supported_exts
            for p in directory.iterdir()
        )
        stats["placeholder"] = not has_manual

    return stats


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
            error_count = 0

            for row in rows:
                ref = None

                try:
                    ref = resolve_source(row)

                    if ref is None:
                        raise ValueError(
                            f"{row.cote} non résolue."
                        )

                    renderer = RENDERERS.get(ref.kind)

                    if renderer is None:
                        raise ValueError(
                            f"Aucun renderer pour {ref.kind}."
                        )

                    base = {
                        "status": "ok",
                        "source_type": ref.kind,
                        "source_ids": list(ref.ids),
                        "description": row.description,
                    }

                    # Erreur de rendu d'UNE cote : enregistrée, n'interrompt
                    # pas les 104 autres (le run reste un test d'intégrité).
                    sources = resolve_objects(ref)

                    destination = (
                        staging_dir / f"{row.cote}.pdf"
                    )

                    output = renderer.render(
                        row=row,
                        sources=sources,
                        destination=destination,
                    )

                    stats = compute_stats(
                        ref, sources, output
                    )

                    manifest[row.cote] = {
                        **base,
                        "output": output.name,
                        **stats,
                    }

                    self.stdout.write(
                        f"{row.cote:<6} "
                        f"-> {ref.kind}:"
                        f"{','.join(ref.ids):<14} "
                        f"{stats['page_count']:>3} p."
                        + (
                            "  [placeholder]"
                            if stats.get("placeholder")
                            else ""
                        )
                    )

                except Exception as exc:
                    error_count += 1
                    base = {
                        "status": "error",
                        "source_type": ref.kind if ref else "unknown",
                        "source_ids": list(ref.ids) if ref else [],
                        "description": row.description,
                        "error": str(exc),
                    }
                    manifest[row.cote] = base
                    self.stdout.write(
                        self.style.ERROR(
                            f"{row.cote:<6} ERREUR : {exc}"
                        )
                    )

            # Résumé global d'intégrité.
            cote_entries = [
                v for k, v in manifest.items() if k != "_summary"
            ]
            manifest["_summary"] = {
                "exhibit_count": len(rows),
                "success_count": sum(
                    1 for v in cote_entries
                    if v.get("status") == "ok"
                ),
                "placeholder_count": sum(
                    1 for v in cote_entries
                    if v.get("placeholder")
                ),
                "error_count": error_count,
                "total_pages": sum(
                    v.get("page_count", 0) for v in cote_entries
                ),
            }

            manifest_path = (
                staging_dir / "manifest.json"
            )

            manifest_path.write_text(
                json.dumps(
                    manifest,
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )

            if error_count > 0:
                raise CommandError(
                    f"{error_count} pièce(s) en erreur. "
                    "Le dossier pieces_pdf existant est conservé."
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

        except Exception as exc:
            if staging_dir.exists() and not isinstance(exc, CommandError):
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
