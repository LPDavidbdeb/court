from __future__ import annotations

import json
import tempfile
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from case_manager.evidence_audit import (
    audit_occurrences,
    collect_occurrences,
    reports_digest,
    resolve_descriptive_piece_occurrences,
    write_audit_reports,
)


class Command(BaseCommand):
    help = (
        "Audite en lecture seule les références de legal/organisation_preuve, "
        "les normalise vers (model, pk) et produit les rapports de couverture."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--input-dir",
            type=Path,
            default=Path(settings.BASE_DIR) / "legal" / "organisation_preuve",
        )
        parser.add_argument(
            "--output-dir",
            type=Path,
            default=Path(settings.BASE_DIR) / "legal" / "organisation_preuve" / "audit_canonique",
        )
        parser.add_argument(
            "--check",
            action="store_true",
            help="Vérifie que les rapports existants sont reproductibles sans les modifier.",
        )

    def handle(self, *args, **options):
        input_dir: Path = options["input_dir"].resolve()
        output_dir: Path = options["output_dir"].resolve()
        if not input_dir.is_dir():
            raise CommandError(f"Répertoire introuvable : {input_dir}")

        occurrences = collect_occurrences(input_dir)
        occurrences = resolve_descriptive_piece_occurrences(occurrences, input_dir.parent)
        audit = audit_occurrences(occurrences)
        supported_inputs = [
            path for path in input_dir.iterdir()
            if path.is_file() and path.suffix.casefold() in {".md", ".csv", ".xlsx"}
        ]
        audit["summary"]["input_file_count"] = len(supported_inputs)
        audit["summary"]["source_files_with_references"] = audit["summary"].pop("source_file_count")

        if options["check"]:
            if not output_dir.is_dir():
                raise CommandError(f"Rapports absents : {output_dir}")
            with tempfile.TemporaryDirectory(prefix="audit-preuve-") as temp_dir:
                generated = write_audit_reports(Path(temp_dir), audit)
                expected = [output_dir / path.name for path in generated]
                missing = [path.name for path in expected if not path.exists()]
                if missing:
                    raise CommandError(f"Rapports manquants : {', '.join(missing)}")
                if reports_digest(generated) != reports_digest(expected):
                    raise CommandError("Les rapports d’audit ne sont pas à jour.")
            self.stdout.write(self.style.SUCCESS("Les rapports d’audit sont reproductibles et à jour."))
        else:
            paths = write_audit_reports(output_dir, audit)
            self.stdout.write(self.style.SUCCESS(f"Audit écrit dans {output_dir}"))
            self.stdout.write(f"Empreinte des rapports : {reports_digest(paths)}")

        self.stdout.write(json.dumps(audit["summary"], ensure_ascii=False, indent=2, sort_keys=True))
