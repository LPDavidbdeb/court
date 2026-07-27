from __future__ import annotations

import json
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from case_manager.piece_file_audit import (
    audit_piece_chain,
    write_piece_audit_reports,
)


class Command(BaseCommand):
    help = (
        "Audite en lecture seule legal/piece*.md, le bordereau, les objets "
        "PostgreSQL, les originaux et l'assemblage pieces_pdf."
    )

    def add_arguments(self, parser):
        base_dir = Path(settings.BASE_DIR)
        parser.add_argument(
            "--legal-dir",
            type=Path,
            default=base_dir / "legal",
            help="Répertoire contenant les fiches piece*.md.",
        )
        parser.add_argument(
            "--bordereau",
            type=Path,
            default=base_dir / "legal" / "bordereau_pieces.md",
            help="Bordereau technique servant de source procédurale.",
        )
        parser.add_argument(
            "--assembly-dir",
            type=Path,
            default=base_dir / "pieces_pdf",
            help="Répertoire des PDF normalisés et de leur manifest.",
        )
        parser.add_argument(
            "--depot-bordereau",
            type=Path,
            default=base_dir / "legal" / "bordereau_bloc_depot.md",
            help="Bordereau procédural déposé ou destiné à la communication.",
        )
        parser.add_argument(
            "--output-dir",
            type=Path,
            default=None,
            help="Écrit les rapports JSON/CSV dans ce répertoire.",
        )
        parser.add_argument(
            "--strict",
            "--check",
            action="store_true",
            dest="strict",
            help="Retourne une erreur si au moins une anomalie de niveau error existe.",
        )

    def handle(self, *args, **options):
        legal_dir: Path = options["legal_dir"]
        bordereau: Path = options["bordereau"]
        assembly_dir: Path = options["assembly_dir"]
        depot_bordereau: Path = options["depot_bordereau"]
        output_dir: Path | None = options["output_dir"]

        if not legal_dir.is_dir():
            raise CommandError(f"Répertoire legal introuvable : {legal_dir}")
        if not bordereau.is_file():
            raise CommandError(f"Bordereau introuvable : {bordereau}")

        audit = audit_piece_chain(
            legal_dir=legal_dir,
            bordereau_path=bordereau,
            depot_bordereau_path=depot_bordereau,
            assembly_dir=assembly_dir,
        )
        if output_dir:
            paths = write_piece_audit_reports(output_dir, audit)
            self.stdout.write(
                self.style.SUCCESS(
                    f"{len(paths)} rapports écrits dans {output_dir.resolve()}"
                )
            )

        self.stdout.write(
            json.dumps(
                audit["summary"],
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
        )
        errors = audit["summary"]["error_count"]
        if options["strict"] and errors:
            raise CommandError(
                f"Audit non conforme : {errors} anomalie(s) de niveau error."
            )

        if errors:
            self.stdout.write(
                self.style.WARNING(
                    "Audit terminé avec des erreurs; les pièces ne sont pas "
                    "toutes prêtes à communiquer."
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    "Audit conforme : chaîne prête pour l'assemblage et la communication."
                )
            )
