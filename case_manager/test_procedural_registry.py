from pathlib import Path
from tempfile import TemporaryDirectory

from django.test import SimpleTestCase

from case_manager.procedural_registry import (
    expand_collective_references,
    extract_pleading_placeholders,
    parse_bordereau,
    resolve_reference_text,
)


class ProceduralRegistryTests(SimpleTestCase):
    def test_parse_bordereau_provisional_cote(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "bordereau.md"
            path.write_text(
                "| Cote prov. | Date | Pièce | Fichier d'appui | Source (base) |\n"
                "|---|---|---|---|---|\n"
                "| P-2 | 11 juin 2013 | Courriel | piece_pdf-1 | pdf-1 |\n",
                encoding="utf-8",
            )
            rows = parse_bordereau(path)
        self.assertEqual(rows[0]["proposed_cote"], "P-2")
        self.assertEqual(rows[0]["support_reference"], "piece_pdf-1")

    def test_extract_strong_and_context_placeholders(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "pleading.md"
            path.write_text(
                "1. Requête, pièce P-[REQUÊTE-2015].\n"
                "2. Autre fait, pièce P-[●].\n"
                "3. Départ, pièce P-[preuve du départ du 23 février 2015].\n"
                "4. Déclaration, pièce P-[DA-2019].\n",
                encoding="utf-8",
            )
            rows = extract_pleading_placeholders(path)
        self.assertEqual(rows[0]["proposed_cote"], "P-19")
        self.assertEqual(rows[0]["mapping_status"], "proposed_strong")
        self.assertEqual(rows[1]["mapping_status"], "context_required")
        self.assertEqual(rows[2]["proposed_cote"], "P-9")
        self.assertEqual(rows[2]["mapping_basis"], "piece_pdf-3_explicit_depart_date")
        self.assertEqual(rows[3]["proposed_cote"], "P-42")
        self.assertEqual(rows[3]["mapping_basis"], "document_3_sworn_declaration")

    def test_expand_small_range_but_not_large_chat_range(self):
        unresolved = [
            {"raw_reference": "Events id=257 à 260", "reference_form": "collective_or_ambiguous", "source_files": "x"},
            {"raw_reference": "ChatMessages id=111 à 311", "reference_form": "collective_or_ambiguous", "source_files": "y"},
        ]
        audit = {"canonical": []}
        rows = expand_collective_references(unresolved, audit)
        self.assertEqual([row["candidate_pk"] for row in rows[:4]], [257, 258, 259, 260])
        self.assertEqual(rows[-1]["expansion_status"], "range_too_large_or_invalid")

    def test_slash_email_components_are_expanded(self):
        with TemporaryDirectory() as directory:
            occurrences = resolve_reference_text(
                "piece_thread-6_reconstruction (email-6/8/295/306)",
                Path(directory),
                "bordereau.md",
            )
        keys = {item.canonical_key for item in occurrences if item.canonical_key}
        self.assertTrue({"EmailThread:6", "Email:6", "Email:8", "Email:295", "Email:306"}.issubset(keys))
