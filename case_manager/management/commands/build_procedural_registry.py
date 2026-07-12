from __future__ import annotations

import json
import tempfile
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from case_manager.procedural_registry import (
    build_proposed_registry,
    build_registry_report,
    collect_historic_alias_mappings,
    expand_collective_references,
    extract_pleading_placeholders,
    parse_bordereau,
    reports_digest,
    write_registry_reports,
)


class Command(BaseCommand):
    help = "Construit un registre procédural proposé sans modifier la demande ni la base."

    def add_arguments(self, parser):
        base = Path(settings.BASE_DIR)
        parser.add_argument("--audit-json", type=Path, default=base / "legal/organisation_preuve/audit_canonique/audit_preuve.json")
        parser.add_argument("--bordereau", type=Path, default=base / "legal/bordereau_pieces.md")
        parser.add_argument("--pleading", type=Path, default=base / "legal/requete_secton_faits_lp.md")
        parser.add_argument("--input-dir", type=Path, default=base / "legal/organisation_preuve")
        parser.add_argument("--output-dir", type=Path, default=base / "legal/organisation_preuve/registre_procedural")
        parser.add_argument("--check", action="store_true")

    def handle(self, *args, **options):
        required = ["audit_json", "bordereau", "pleading", "input_dir"]
        for name in required:
            path = options[name]
            if not path.exists():
                raise CommandError(f"Entrée introuvable : {path}")

        audit = json.loads(options["audit_json"].read_text(encoding="utf-8"))
        legal_dir = options["bordereau"].parent
        bordereau_rows = parse_bordereau(options["bordereau"])
        registry, components, conflicts = build_proposed_registry(bordereau_rows, audit, legal_dir)
        aliases = collect_historic_alias_mappings(options["input_dir"], legal_dir)
        ranges = expand_collective_references(audit["unresolved"], audit)
        placeholders = extract_pleading_placeholders(options["pleading"])
        report = build_registry_report(
            audit=audit,
            bordereau_rows=bordereau_rows,
            registry_rows=registry,
            component_rows=components,
            conflict_rows=conflicts,
            alias_rows=aliases,
            range_rows=ranges,
            placeholder_rows=placeholders,
        )

        output_dir = options["output_dir"].resolve()
        if options["check"]:
            if not output_dir.is_dir():
                raise CommandError(f"Rapports absents : {output_dir}")
            with tempfile.TemporaryDirectory(prefix="registre-procedural-") as temp_dir:
                generated = write_registry_reports(Path(temp_dir), report)
                expected = [output_dir / path.name for path in generated]
                missing = [path.name for path in expected if not path.exists()]
                if missing:
                    raise CommandError(f"Rapports manquants : {', '.join(missing)}")
                if reports_digest(generated) != reports_digest(expected):
                    raise CommandError("Le registre procédural proposé n’est pas à jour.")
            self.stdout.write(self.style.SUCCESS("Le registre procédural proposé est reproductible et à jour."))
        else:
            paths = write_registry_reports(output_dir, report)
            self.stdout.write(self.style.SUCCESS(f"Registre proposé écrit dans {output_dir}"))
            self.stdout.write(f"Empreinte : {reports_digest(paths)}")
        self.stdout.write(json.dumps(report["summary"], ensure_ascii=False, indent=2, sort_keys=True))
