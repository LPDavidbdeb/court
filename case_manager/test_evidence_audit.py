from django.test import SimpleTestCase

from case_manager.evidence_audit import _media_path_candidates, extract_references_from_text


class EvidenceReferenceExtractionTests(SimpleTestCase):
    def extract(self, text):
        return extract_references_from_text(
            text,
            source_file="test.md",
            source_format="markdown",
            source_location="line:1",
            context=text,
        )

    def test_piece_filename_resolves_to_canonical_tuple(self):
        occurrence = self.extract("`piece_pdf-35.md`")[0]
        self.assertEqual((occurrence.model, occurrence.pk), ("PDFDocument", 35))
        self.assertEqual(occurrence.reference_form, "piece_markdown")

    def test_thread_email_preserves_thread_context(self):
        occurrence = self.extract("piece_thread-119_email-484.md")[0]
        self.assertEqual((occurrence.model, occurrence.pk), ("Email", 484))
        self.assertEqual((occurrence.context_model, occurrence.context_pk), ("EmailThread", 119))

    def test_direct_tuple_resolves(self):
        occurrence = self.extract("PDFDocument id=63")[0]
        self.assertEqual((occurrence.model, occurrence.pk), ("PDFDocument", 63))
        self.assertEqual(occurrence.reference_form, "direct_tuple")

    def test_comma_list_creates_individual_tuples(self):
        occurrences = self.extract("Events id=244, 246, 255 et 267")
        self.assertEqual(
            [(item.model, item.pk) for item in occurrences],
            [("Event", 244), ("Event", 246), ("Event", 255), ("Event", 267)],
        )

    def test_range_remains_unresolved_collective(self):
        occurrence = self.extract("Events id=316–320")[0]
        self.assertIsNone(occurrence.model)
        self.assertIsNone(occurrence.pk)
        self.assertEqual(occurrence.reference_form, "collective_or_ambiguous")

    def test_unstructured_piece_name_is_not_guessed(self):
        occurrence = self.extract("piece_tableau_recap_evenements.md")[0]
        self.assertIsNone(occurrence.model)
        self.assertEqual(occurrence.reference_form, "unparsed_piece_reference")

    def test_standalone_procedural_alias_is_unresolved(self):
        occurrence = self.extract("P-355")[0]
        self.assertIsNone(occurrence.model)
        self.assertEqual(occurrence.reference_form, "procedural_alias_only")

    def test_media_path_is_normalized_without_media_prefix(self):
        paths = _media_path_candidates(
            "Source: `media/photos/IMG_3095.jpg` et pdf_documents/report.pdf."
        )
        self.assertEqual(paths, {"photos/IMG_3095.jpg", "pdf_documents/report.pdf"})
