#!/usr/bin/env python3
"""Regenerate the consolidated 2015 bridges while preserving authored legal means."""

from __future__ import annotations

import argparse
from pathlib import Path


LEGAL_DIR = Path(__file__).resolve().parent
OUTPUT_PATH = LEGAL_DIR / "ponts_requete_2015_consolides.md"
AUTHORED_MARKER = (
    "<!-- ========================= SECTION RÉDIGÉE (NON CONCATÉNÉE) "
    "========================= -->"
)

SOURCES = (
    ("§4-5-6", "pont/pont_par4-5-6_2015.md"),
    ("§7", "pont/pont_par7_2015.md"),
    ("§9", "pont/pont_par9_2015.md"),
    ("§10", "pont/pont_par10_2015.md"),
    ("§14-17", "pont/pont_par14-17_2015.md"),
    ("§18", "pont/pont_par18_2015.md"),
    ("§20-21", "pont/pont_par20-21_2015.md"),
    ("§23-24", "pont/pont_par23-24_2015.md"),
    ("§28-29", "pont/pont_par28-29_2015.md"),
    ("§30-31", "pont/pont_par30-31_2015.md"),
    ("§56-57", "pont/pont_par56-57_2015.md"),
    ("§59", "pont/pont_par59_2015.md"),
)


def read_authored_section() -> str:
    current = OUTPUT_PATH.read_text(encoding="utf-8")
    marker_index = current.find(AUTHORED_MARKER)
    if marker_index < 0:
        raise RuntimeError(
            f"Authored section marker not found in {OUTPUT_PATH}; refusing to overwrite."
        )
    return current[marker_index:].strip()


def build_document() -> str:
    order = " · ".join(label for label, _ in SOURCES)
    parts = [
        "# PONTS CONSOLIDÉS — Requête du 19 novembre 2015",
        "",
        (
            f"> **Fichier généré par concaténation.** Regroupe, en ordre de "
            f"paragraphe, les {len(SOURCES)} ponts relatifs à la Requête assermentée "
            "du 19 novembre 2015. **Ne pas éditer les sections de ponts ici** — "
            "chaque section est une copie de son fichier source dans `legal/pont/`; "
            "modifier le source, puis régénérer."
        ),
        ">",
        (
            "> ⚠️ **Exception :** une section auteure — `MOYENS DE DROIT` — est "
            "ajoutée **à la fin** du fichier (balises `SECTION RÉDIGÉE "
            "(NON CONCATÉNÉE)`). Elle n'est copiée d'aucun source; **la "
            "préserver** en cas de régénération, ou l'extraire vers un fichier "
            "source dédié."
        ),
        "",
        f"**Ordre :** {order}",
    ]

    for _, relative_path in SOURCES:
        source_path = LEGAL_DIR / relative_path
        source_text = source_path.read_text(encoding="utf-8").strip()
        parts.extend(
            (
                "",
                "---",
                "",
                (
                    "<!-- ========================= SOURCE : legal/"
                    f"{relative_path} ========================= -->"
                ),
                "",
                source_text,
            )
        )

    parts.extend(("", "", "---", "", read_authored_section()))
    return "\n".join(parts).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="Return a non-zero status when the consolidated file is stale.",
    )
    args = parser.parse_args()

    generated = build_document()
    current = OUTPUT_PATH.read_text(encoding="utf-8")

    if args.check:
        if current == generated:
            print("Consolidated bridges are up to date.")
            return 0
        print("Consolidated bridges are stale; regenerate them.")
        return 1

    OUTPUT_PATH.write_text(generated, encoding="utf-8")
    print(f"Regenerated {OUTPUT_PATH} from {len(SOURCES)} source bridges.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
