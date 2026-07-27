from pathlib import Path
from tempfile import TemporaryDirectory

from django.test import SimpleTestCase

from case_manager.management.commands.sync_pieces import BordereauRow, SourceRef
from case_manager.piece_file_audit import (
    _validate_assembled_entry,
    compare_identity_sets,
    extract_piece_filenames,
    normalize_piece_filename,
    parse_depot_bordereau,
    validate_depot_bordereau,
)


class PieceFilenameTests(SimpleTestCase):
    def test_normalize_piece_filename_adds_markdown_suffix(self):
        self.assertEqual(
            normalize_piece_filename("`piece_event-135`"),
            "piece_event-135.md",
        )

    def test_extracts_multiple_piece_files_from_support_cell(self):
        names = extract_piece_filenames(
            "piece_thread-120_email-485 ; "
            "piece_thread-121_email-486"
        )
        self.assertEqual(
            names,
            [
                "piece_thread-120_email-485.md",
                "piece_thread-121_email-486.md",
            ],
        )

    def test_duplicate_piece_names_are_collapsed(self):
        names = extract_piece_filenames(
            "piece_pdf-35 (doublon : piece_pdf-35.md)"
        )
        self.assertEqual(names, ["piece_pdf-35.md"])


class IdentityComparisonTests(SimpleTestCase):
    def test_exact_identity_sets_match(self):
        self.assertIsNone(
            compare_identity_sets(
                {"Email:485", "Email:486"},
                {"Email:486", "Email:485"},
            )
        )

    def test_missing_piece_identity_is_error(self):
        result = compare_identity_sets(
            {"Email:485", "Email:486"},
            {"Email:485"},
        )
        self.assertEqual(result[0:2], ("error", "BORDEREAU_PIECE_SOURCE_MISMATCH"))

    def test_additional_context_identity_is_warning(self):
        result = compare_identity_sets(
            {"Email:485"},
            {"Email:485", "EmailThread:120"},
        )
        self.assertEqual(result[0:2], ("warning", "PIECE_HAS_ADDITIONAL_SOURCES"))


class AssemblyManifestTests(SimpleTestCase):
    def setUp(self):
        self.row = BordereauRow(
            cote="P-2",
            date="11 juin 2013",
            description="Courriel",
            fichier_appui="piece_pdf-1",
            source_base="pdf-1",
        )
        self.ref = SourceRef("pdf", ("1",))

    def test_valid_manifest_entry_and_pdf_are_accepted(self):
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            document = __import__("fitz").open()
            document.new_page()
            document.save(root / "P-2.pdf")
            document.close()
            manifest = {
                "P-2": {
                    "status": "ok",
                    "source_type": "pdf",
                    "source_ids": ["1"],
                    "output": "P-2.pdf",
                    "placeholder": False,
                    "page_count": 1,
                }
            }
            result, issues = _validate_assembled_entry(
                row=self.row,
                ref=self.ref,
                manifest=manifest,
                assembly_dir=root,
            )
            self.assertTrue(result["assembled_exists"])
            self.assertEqual(result["assembled_page_count"], 1)
            self.assertEqual(len(result["assembled_sha256"]), 64)
            self.assertEqual(issues, [])

    def test_placeholder_is_blocking(self):
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            document = __import__("fitz").open()
            document.new_page()
            document.save(root / "P-2.pdf")
            document.close()
            manifest = {
                "P-2": {
                    "status": "ok",
                    "source_type": "pdf",
                    "source_ids": ["1"],
                    "output": "P-2.pdf",
                    "placeholder": True,
                }
            }
            _, issues = _validate_assembled_entry(
                row=self.row,
                ref=self.ref,
                manifest=manifest,
                assembly_dir=root,
            )
            self.assertIn("ASSEMBLED_PLACEHOLDER", {issue.code for issue in issues})

    def test_manifest_source_mismatch_is_blocking(self):
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            document = __import__("fitz").open()
            document.new_page()
            document.save(root / "P-2.pdf")
            document.close()
            manifest = {
                "P-2": {
                    "status": "ok",
                    "source_type": "pdf",
                    "source_ids": ["35"],
                    "output": "P-2.pdf",
                    "placeholder": False,
                }
            }
            _, issues = _validate_assembled_entry(
                row=self.row,
                ref=self.ref,
                manifest=manifest,
                assembly_dir=root,
            )
            self.assertIn(
                "ASSEMBLY_SOURCE_IDS_MISMATCH",
                {issue.code for issue in issues},
            )

    def test_corrupt_pdf_is_blocking(self):
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "P-2.pdf").write_bytes(b"not a pdf")
            manifest = {
                "P-2": {
                    "status": "ok",
                    "source_type": "pdf",
                    "source_ids": ["1"],
                    "output": "P-2.pdf",
                    "placeholder": False,
                }
            }
            _, issues = _validate_assembled_entry(
                row=self.row,
                ref=self.ref,
                manifest=manifest,
                assembly_dir=root,
            )
            self.assertIn("ASSEMBLED_PDF_INVALID", {issue.code for issue in issues})


class DepotBordereauTests(SimpleTestCase):
    def test_parses_top_level_and_subcote_sources(self):
        with TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "bordereau.md"
            path.write_text(
                "- **P-1** — date — Première pièce ;\n"
                "- **P-2** — date — Deuxième pièce ;\n"
                "| P-2.1 | date | Email:10 | Courriel |\n"
                "| P-2.2 | date | Email:11 | Courriel |\n",
                encoding="utf-8",
            )
            parsed = parse_depot_bordereau(path)
            self.assertEqual(parsed["top_level"], ["P-1", "P-2"])
            self.assertEqual(
                parsed["subcotes"]["P-2"],
                [("P-2.1", "Email:10"), ("P-2.2", "Email:11")],
            )

    def test_detects_missing_top_level_cote(self):
        rows = [
            BordereauRow("P-1", "date", "Un", "email-1", "email-1"),
            BordereauRow("P-2", "date", "Deux", "email-2", "email-2"),
        ]
        with TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "bordereau.md"
            path.write_text(
                "- **P-1** — date — Première pièce ;\n",
                encoding="utf-8",
            )
            _, issues = validate_depot_bordereau(
                technical_rows=rows,
                depot_path=path,
            )
            self.assertIn("DEPOT_COTE_MISSING", {issue.code for issue in issues})

    def test_detects_subcote_source_order_mismatch(self):
        rows = [
            BordereauRow(
                "P-2",
                "date",
                "Deux",
                "Emails id=10, 11",
                "emails-10/11",
            )
        ]
        with TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "bordereau.md"
            path.write_text(
                "- **P-2** — date — Deuxième pièce ;\n"
                "| P-2.1 | date | Email:11 | Courriel |\n"
                "| P-2.2 | date | Email:10 | Courriel |\n",
                encoding="utf-8",
            )
            _, issues = validate_depot_bordereau(
                technical_rows=rows,
                depot_path=path,
            )
            self.assertIn(
                "DEPOT_SUBCOTE_SOURCE_MISMATCH",
                {issue.code for issue in issues},
            )
