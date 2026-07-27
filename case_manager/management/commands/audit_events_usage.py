# case_manager/management/commands/audit_events_usage.py

from __future__ import annotations

import csv
import json
import re
from collections import defaultdict
from pathlib import Path

from django.conf import settings
from django.core.management.base import (
    BaseCommand,
    CommandError,
)

from events.models import Event

from case_manager.management.commands.sync_pieces import (
    BORDEREAU_PATH,
    parse_bordereau,
    resolve_source,
)


BASE_DIR = Path(settings.BASE_DIR)

# Votre demande actuelle.
DEFAULT_DEMANDE_PATH = (
    BASE_DIR
    / "legal"
    / "demande_DEPOT_2026-07-21.md"
)

# Dossier de sortie des rapports.
OUTPUT_DIR = (
    BASE_DIR
    / "audit_events"
)


def cote_sort_key(cote: str) -> tuple[int, str]:
    """
    Trie P-1, P-2, ..., P-10 correctement.
    """
    match = re.fullmatch(
        r"P-(\d+)",
        cote.strip(),
        re.IGNORECASE,
    )

    if not match:
        return (10**9, cote)

    return (
        int(match.group(1)),
        cote,
    )


def extract_cotes_from_demande(
    path: Path,
) -> set[str]:
    """
    Relève les références explicites P-n présentes
    dans le texte de la demande.

    Note :
        "P-1 à P-105" produit seulement P-1 et P-105.
        La plage n'est volontairement pas développée,
        puisqu'on cherche ici les pièces effectivement
        citées individuellement dans le corps du texte.
    """

    if not path.exists():
        raise CommandError(
            f"Demande introuvable : {path}"
        )

    text = path.read_text(
        encoding="utf-8"
    )

    numbers = re.findall(
        r"\bP-(\d+)\b",
        text,
        flags=re.IGNORECASE,
    )

    return {
        f"P-{int(number)}"
        for number in numbers
    }


def truncate(
    value: str,
    length: int = 120,
) -> str:
    """
    Version compacte d'un texte pour affichage console.
    """
    value = " ".join(
        (value or "").split()
    )

    if len(value) <= length:
        return value

    return (
        value[: length - 3]
        + "..."
    )


def event_to_dict(
    event: Event,
    *,
    used: bool,
    cotes: list[str],
) -> dict:
    """
    Représentation normalisée d'un Event pour JSON/CSV.
    """

    return {
        "event_id": event.pk,
        "display_id": (
            event.get_display_id()
            if hasattr(
                event,
                "get_display_id",
            )
            else f"E-{event.pk}"
        ),
        "date": (
            event.date.isoformat()
            if event.date
            else None
        ),
        "used": used,
        "cotes": cotes,
        "explanation": (
            event.explanation
            or ""
        ),
        "photo_count": (
            event.linked_photos.count()
        ),
        "linked_email_id": (
            event.linked_email_id
        ),
        "parent_id": (
            event.parent_id
        ),
    }


class Command(BaseCommand):

    help = (
        "Compare les Event utilisés dans les pièces "
        "de la demande avec tous les Event présents "
        "dans la base de données."
    )

    def add_arguments(
        self,
        parser,
    ):
        parser.add_argument(
            "--demand-only",
            action="store_true",
            help=(
                "Ne considère comme exploités que les Event "
                "rattachés à des cotes P-n explicitement "
                "citées dans le texte de la demande."
            ),
        )

        parser.add_argument(
            "--demande",
            type=str,
            default=str(
                DEFAULT_DEMANDE_PATH
            ),
            help=(
                "Chemin du fichier Markdown de la demande."
            ),
        )

        parser.add_argument(
            "--unused-only",
            action="store_true",
            help=(
                "Affiche uniquement les Event "
                "non exploités."
            ),
        )

        parser.add_argument(
            "--used-only",
            action="store_true",
            help=(
                "Affiche uniquement les Event exploités."
            ),
        )

        parser.add_argument(
            "--export",
            action="store_true",
            help=(
                "Produit également les fichiers JSON "
                "et CSV dans audit_events/."
            ),
        )

    def handle(
        self,
        *args,
        **options,
    ):
        demand_only = options[
            "demand_only"
        ]

        unused_only = options[
            "unused_only"
        ]

        used_only = options[
            "used_only"
        ]

        export = options[
            "export"
        ]

        if (
            unused_only
            and used_only
        ):
            raise CommandError(
                "--unused-only et --used-only "
                "sont mutuellement exclusifs."
            )

        # -------------------------------------------------------------
        # 1. Lire le bordereau canonique
        # -------------------------------------------------------------

        rows = parse_bordereau(
            BORDEREAU_PATH
        )

        # -------------------------------------------------------------
        # 2. Optionnel :
        #    limiter aux cotes explicitement citées dans la demande
        # -------------------------------------------------------------

        demand_cotes = None

        if demand_only:
            demande_path = Path(
                options["demande"]
            )

            demand_cotes = (
                extract_cotes_from_demande(
                    demande_path
                )
            )

            self.stdout.write(
                f"{len(demand_cotes)} cote(s) P-n "
                "explicitement détectée(s) "
                "dans la demande."
            )

        # -------------------------------------------------------------
        # 3. Construire :
        #
        #    Event ID -> [P-5, P-45, ...]
        #
        # On utilise resolve_source() :
        # même moteur que sync_pieces et sync_pieces_pdf.
        # -------------------------------------------------------------

        event_cotes: dict[
            int,
            list[str],
        ] = defaultdict(list)

        event_piece_rows = 0

        for row in rows:

            if (
                demand_cotes is not None
                and row.cote
                not in demand_cotes
            ):
                continue

            ref = resolve_source(
                row
            )

            if (
                ref is None
                or ref.kind != "event"
            ):
                continue

            event_piece_rows += 1

            for raw_id in ref.ids:
                try:
                    event_id = int(
                        raw_id
                    )
                except (
                    TypeError,
                    ValueError,
                ):
                    self.stdout.write(
                        self.style.WARNING(
                            f"{row.cote}: "
                            f"Event ID invalide "
                            f"{raw_id!r}"
                        )
                    )
                    continue

                event_cotes[
                    event_id
                ].append(
                    row.cote
                )

        # Dédupliquer et trier les cotes.
        event_cotes = {
            event_id: sorted(
                set(cotes),
                key=cote_sort_key,
            )
            for (
                event_id,
                cotes,
            ) in event_cotes.items()
        }

        used_ids = set(
            event_cotes
        )

        # -------------------------------------------------------------
        # 4. Charger tous les Event de la BD
        # -------------------------------------------------------------

        all_events = list(
            Event.objects
            .all()
            .select_related(
                "linked_email",
                "parent",
            )
            .prefetch_related(
                "linked_photos",
            )
            .order_by(
                "date",
                "pk",
            )
        )

        all_ids = {
            event.pk
            for event in all_events
        }

        # Event référencés dans le bordereau,
        # mais inexistants en BD.
        missing_ids = (
            used_ids
            - all_ids
        )

        # Event réellement présents et utilisés.
        existing_used_ids = (
            used_ids
            & all_ids
        )

        # Event présents mais inexploités.
        unused_ids = (
            all_ids
            - used_ids
        )

        used_events = [
            event
            for event in all_events
            if event.pk
            in existing_used_ids
        ]

        unused_events = [
            event
            for event in all_events
            if event.pk
            in unused_ids
        ]

        # -------------------------------------------------------------
        # 5. Résumé
        # -------------------------------------------------------------

        scope = (
            "demande uniquement"
            if demand_only
            else "bordereau complet"
        )

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                "AUDIT DES EVENTS"
            )
        )

        self.stdout.write(
            f"Portée : {scope}"
        )

        self.stdout.write(
            f"Event en base : "
            f"{len(all_events)}"
        )

        self.stdout.write(
            f"Cotes de type Event : "
            f"{event_piece_rows}"
        )

        self.stdout.write(
            f"Event distincts exploités : "
            f"{len(existing_used_ids)}"
        )

        self.stdout.write(
            f"Event non exploités : "
            f"{len(unused_events)}"
        )

        self.stdout.write(
            f"Event référencés mais absents "
            f"de la BD : "
            f"{len(missing_ids)}"
        )

        # -------------------------------------------------------------
        # 6. Event utilisés
        # -------------------------------------------------------------

        if not unused_only:

            self.stdout.write("")
            self.stdout.write(
                self.style.SUCCESS(
                    "EVENTS EXPLOITÉS"
                )
            )

            for event in used_events:
                cotes = ", ".join(
                    event_cotes.get(
                        event.pk,
                        [],
                    )
                )

                self.stdout.write(
                    (
                        f"E-{event.pk:<5} "
                        f"{event.date}  "
                        f"[{cotes}]  "
                        f"photos="
                        f"{event.linked_photos.count():<3} "
                        f"{truncate(event.explanation)}"
                    )
                )

        # -------------------------------------------------------------
        # 7. Event non utilisés
        # -------------------------------------------------------------

        if not used_only:

            self.stdout.write("")
            self.stdout.write(
                self.style.WARNING(
                    "EVENTS NON EXPLOITÉS"
                )
            )

            for event in unused_events:

                linked_email = (
                    f"email-{event.linked_email_id}"
                    if event.linked_email_id
                    else "-"
                )

                parent = (
                    f"E-{event.parent_id}"
                    if event.parent_id
                    else "-"
                )

                self.stdout.write(
                    (
                        f"E-{event.pk:<5} "
                        f"{event.date}  "
                        f"photos="
                        f"{event.linked_photos.count():<3} "
                        f"email={linked_email:<10} "
                        f"parent={parent:<8} "
                        f"{truncate(event.explanation)}"
                    )
                )

        # -------------------------------------------------------------
        # 8. Références cassées
        # -------------------------------------------------------------

        if missing_ids:

            self.stdout.write("")
            self.stdout.write(
                self.style.ERROR(
                    "EVENTS RÉFÉRENCÉS "
                    "MAIS ABSENTS DE LA BD"
                )
            )

            for event_id in sorted(
                missing_ids
            ):
                cotes = ", ".join(
                    event_cotes.get(
                        event_id,
                        [],
                    )
                )

                self.stdout.write(
                    self.style.ERROR(
                        f"E-{event_id} "
                        f"-> {cotes}"
                    )
                )

        # -------------------------------------------------------------
        # 9. Export JSON / CSV
        # -------------------------------------------------------------

        if export:

            OUTPUT_DIR.mkdir(
                parents=True,
                exist_ok=True,
            )

            records = []

            for event in all_events:
                records.append(
                    event_to_dict(
                        event,
                        used=(
                            event.pk
                            in existing_used_ids
                        ),
                        cotes=(
                            event_cotes.get(
                                event.pk,
                                [],
                            )
                        ),
                    )
                )

            report = {
                "_summary": {
                    "scope": scope,
                    "database_event_count": (
                        len(all_events)
                    ),
                    "used_event_count": (
                        len(existing_used_ids)
                    ),
                    "unused_event_count": (
                        len(unused_events)
                    ),
                    "missing_event_count": (
                        len(missing_ids)
                    ),
                    "missing_event_ids": (
                        sorted(
                            missing_ids
                        )
                    ),
                },
                "events": records,
            }

            json_path = (
                OUTPUT_DIR
                / "event_usage.json"
            )

            json_path.write_text(
                json.dumps(
                    report,
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )

            csv_path = (
                OUTPUT_DIR
                / "event_usage.csv"
            )

            with csv_path.open(
                "w",
                encoding="utf-8",
                newline="",
            ) as handle:

                writer = csv.DictWriter(
                    handle,
                    fieldnames=[
                        "event_id",
                        "display_id",
                        "date",
                        "used",
                        "cotes",
                        "photo_count",
                        "linked_email_id",
                        "parent_id",
                        "explanation",
                    ],
                )

                writer.writeheader()

                for record in records:

                    row = dict(
                        record
                    )

                    row["cotes"] = (
                        ", ".join(
                            record[
                                "cotes"
                            ]
                        )
                    )

                    writer.writerow(
                        row
                    )

            self.stdout.write("")
            self.stdout.write(
                self.style.SUCCESS(
                    f"JSON : {json_path}"
                )
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f"CSV  : {csv_path}"
                )
            )