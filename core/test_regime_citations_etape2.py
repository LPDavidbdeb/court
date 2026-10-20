"""
Le régime des citations, étape 2 : une citation PHRASE ancrée et certifiée.

Tests T2.1, T2.3, T2.4, T2.5 (clés génériques), T2.6, T2.7, T2.8a, T2.8b et T2.9
du plan, sur des données de test seulement. T2.2 (empreinte canonique) et la
partie « sauvegarde » de T2.5 se mesurent sur le clone de la base réelle. Le
refus du rendu par le nouveau pont (T-pont) attend ce pont.

L'invariant B en général — aucun consommateur de l'ancien système n'observe une
citation PHRASE — est éprouvé par core/test_regime_citations.py, dont les
citations PHRASE sont désormais ancrées et certifiées comme celles-ci.

Plan : docs/modele_preuve/PLAN_REGIME_CITATIONS.md, § 4.
"""
from datetime import date, datetime
from io import StringIO

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.core.management.base import CommandError
from django.db import IntegrityError, transaction
from django.db.models import F, ProtectedError
from django.test import TestCase
from django.utils import timezone

from case_manager.models import ProducedExhibit
from core.quote_regime import QuoteRegime, certify_phrase_quote, create_phrase_quote, sha256_text
from document_manager.models import LibraryNode
from email_manager.models import Email, EmailThread
from email_manager.models import Quote as EmailQuote
from pdf_manager.models import PDFDocument
from pdf_manager.models import Quote as PDFQuote
from protagonist_manager.models import Protagonist

PHRASE = QuoteRegime.PHRASE
HERITE = QuoteRegime.HERITE

CORPS = "mais je t'ai deja dit que les mardi et mercredi elise dansait.\n\n\nProfites en.\n"
LA_PHRASE = "je t'ai deja dit que les mardi et mercredi elise dansait"
AUTRE_CORPS = "Un autre courriel, une autre phrase."
TRANSCRIPTION = "--- PAGE 1 ---\nUne ligne native.\n--- PAGE 2 ---\nIl faut savotr lire.\n"
LIGNE_OCR = "Il faut savotr lire."
LECTURE_DU_SCAN = "Il faut savoir lire."


class EtapeDeuxBase(TestCase):
    """Un courriel dont la première phrase a déjà une citation de l'ancien régime,
    un second courriel, et un PDF dont la transcription OCR porte une erreur."""

    @classmethod
    def setUpTestData(cls):
        pere = Protagonist.objects.create(first_name="Père", last_name="Témoin", role="Père")
        fil = EmailThread.objects.create(thread_id="fil-etape2", subject="Fil", protagonist=pere)
        quand = timezone.make_aware(datetime(2013, 6, 11, 9, 0))
        cls.email = Email.objects.create(
            thread=fil, message_id="etape2-m1", subject="Sujet", sender="x@example.com",
            sender_protagonist=pere, date_sent=quand, dao_source="gmail",
            eml_file_path="etape2-m1.eml", body_plain_text=CORPS)
        cls.autre_email = Email.objects.create(
            thread=fil, message_id="etape2-m2", subject="Re", sender="x@example.com",
            sender_protagonist=pere, date_sent=quand.replace(day=12), dao_source="gmail",
            eml_file_path="etape2-m2.eml", body_plain_text=AUTRE_CORPS)
        cls.pdf = PDFDocument.objects.create(
            title="Document scanné", author=pere, file="pdf_documents/etape2.pdf",
            document_date=date(2013, 1, 1), ai_analysis=TRANSCRIPTION)
        # L'ancienne citation équivalente, telle que l'ancien système la produisait.
        cls.ancienne = EmailQuote.objects.create(
            email=cls.email, quote_text=" mais je t'ai deja dit que les mardi et mercredi elise dansait.")
        cls.ancienne_autre = EmailQuote.objects.create(email=cls.autre_email, quote_text=AUTRE_CORPS)
        cls.debut = CORPS.index(LA_PHRASE)
        cls.fin = cls.debut + len(LA_PHRASE)
        cls.ocr_debut = TRANSCRIPTION.index(LIGNE_OCR)
        cls.ocr_fin = cls.ocr_debut + len(LIGNE_OCR)

    def nouvelle(self, **extra):
        return create_phrase_quote(self.email, self.debut, self.fin, derived_from=self.ancienne, **extra)

    def scan(self):
        """Une citation PHRASE sur la ligne OCR, puis certifiée sur la lecture du scan."""
        q = create_phrase_quote(self.pdf, self.ocr_debut, self.ocr_fin)
        return certify_phrase_quote(q, certified_text=LECTURE_DU_SCAN)

    def relue(self, q):
        return type(q).all_objects.select_related().get(pk=q.pk)

    def audit(self):
        sortie = StringIO()
        try:
            call_command("audit_phrase_quotes", stdout=sortie)
            return None, sortie.getvalue()
        except CommandError as e:
            return e, sortie.getvalue()


# --------------------------------------------------------------------------
# T2.1 — contraintes en base, point d'entrée et garde de save()
# --------------------------------------------------------------------------
class T21Contraintes(EtapeDeuxBase):

    def test_seconde_citation_sur_la_meme_phrase(self):
        q = self.nouvelle()
        with self.assertRaises(ValidationError):           # le point d'entrée (full_clean)
            self.nouvelle()
        with self.assertRaises(IntegrityError), transaction.atomic():   # la base elle-même
            EmailQuote.all_objects.create(
                email=self.email, regime=PHRASE, start=q.start, end=q.end, quote_text=q.quote_text,
                source_text_sha256=q.source_text_sha256, anchored_text_sha256=q.anchored_text_sha256)

    def test_citation_phrase_sans_bornes(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            EmailQuote.all_objects.bulk_create([EmailQuote(email=self.email, regime=PHRASE, quote_text=LA_PHRASE)])

    def test_debut_superieur_ou_egal_a_la_fin(self):
        q = self.nouvelle()
        with self.assertRaises(IntegrityError), transaction.atomic():
            EmailQuote.all_objects.filter(pk=q.pk).update(start=F("end"))
        with self.assertRaises(IntegrityError), transaction.atomic():
            EmailQuote.all_objects.filter(pk=q.pk).update(start=F("end") + 1)

    def test_fin_au_dela_du_texte_refusee_par_le_point_d_entree(self):
        with self.assertRaises(ValidationError):
            create_phrase_quote(self.email, self.debut, len(CORPS) + 1)
        self.assertFalse(EmailQuote.phrase_objects.exists())

    def test_fin_au_dela_du_texte_refusee_par_la_garde_de_save(self):
        texte = CORPS[self.debut:]
        with self.assertRaises(ValidationError):
            EmailQuote.all_objects.create(
                email=self.email, regime=PHRASE, start=self.debut, end=len(CORPS) + 1, quote_text=texte,
                source_text_sha256=sha256_text(CORPS), anchored_text_sha256=sha256_text(texte))
        self.assertFalse(EmailQuote.phrase_objects.exists())

    def test_tranche_differente_du_texte_refusee_par_la_garde(self):
        with self.assertRaises(ValidationError):
            EmailQuote.all_objects.create(
                email=self.email, regime=PHRASE, start=self.debut, end=self.fin, quote_text="autre chose",
                source_text_sha256=sha256_text(CORPS), anchored_text_sha256=sha256_text(LA_PHRASE))

    def test_antecedent_d_une_autre_source_refuse(self):
        with self.assertRaises(ValidationError):
            create_phrase_quote(self.email, self.debut, self.fin, derived_from=self.ancienne_autre)

    def test_l_ancien_regime_n_est_pas_concerne(self):
        q = EmailQuote.objects.create(email=self.email, quote_text="n'importe quel texte")
        self.assertEqual(q.regime, HERITE)
        self.assertIsNone(q.start)


# --------------------------------------------------------------------------
# T2.3 — la citation, son ancrage et sa certification ; isolation (B)
# --------------------------------------------------------------------------
class T23Ancrage(EtapeDeuxBase):

    def test_phrase_objects_la_rend_et_l_ancrage_concorde(self):
        q = self.nouvelle()
        self.assertEqual(list(EmailQuote.phrase_objects.values_list("pk", flat=True)), [q.pk])
        q = self.relue(q)
        self.assertEqual(CORPS[q.start:q.end], q.quote_text)
        self.assertEqual(q.quote_text, LA_PHRASE)
        self.assertEqual(sha256_text(self.email.body_plain_text), q.source_text_sha256)
        self.assertEqual(sha256_text(q.quote_text), q.anchored_text_sha256)
        self.assertEqual(sha256_text(q.quote_text), q.certified_text_sha256)
        self.assertTrue(q.certified)
        self.assertFalse(q.corrected_on_scan)
        self.assertTrue(q.valid_anchor)
        self.assertTrue(q.effective_certification)
        self.assertEqual(q.derived_from_id, self.ancienne.pk)

    def test_l_ancien_systeme_ne_la_voit_pas(self):
        q = self.nouvelle()
        self.assertFalse(EmailQuote.objects.filter(pk=q.pk).exists())
        self.assertNotIn(q.pk, self.email.quotes.values_list("pk", flat=True))
        self.assertIn(self.ancienne.pk, self.email.quotes.values_list("pk", flat=True))
        # la relation inverse de l'antécédent prend le gestionnaire par défaut : filtrée aussi
        self.assertFalse(self.ancienne.derived_phrases.exists())
        self.assertEqual(list(EmailQuote.phrase_objects.filter(derived_from=self.ancienne)), [q])

    def test_l_audit_ne_signale_rien(self):
        self.nouvelle()
        erreur, sortie = self.audit()
        self.assertIsNone(erreur, sortie)
        self.assertIn("1 citation(s) PHRASE auditée(s), 0 en défaut", sortie)


# --------------------------------------------------------------------------
# T2.4 — l'antécédence est protégée
# --------------------------------------------------------------------------
class T24Antecedence(EtapeDeuxBase):

    def test_supprimer_l_ancienne_citation_est_refuse(self):
        self.nouvelle()
        with self.assertRaises(ProtectedError):
            self.ancienne.delete()
        self.assertTrue(EmailQuote.objects.filter(pk=self.ancienne.pk).exists())


# --------------------------------------------------------------------------
# T2.5 — aucune clé générique de l'ancien pont ne la désigne
# --------------------------------------------------------------------------
class T25ClesGeneriques(EtapeDeuxBase):

    def test_aucune_cle_generique(self):
        q = self.nouvelle()
        ct = ContentType.objects.get_for_model(EmailQuote)
        self.assertFalse(LibraryNode.objects.filter(content_type=ct, object_id=q.pk).exists())
        self.assertFalse(ProducedExhibit.objects.filter(content_type=ct, object_id=q.pk).exists())


# --------------------------------------------------------------------------
# T2.6 à T2.9 — la certification effective tombe dès qu'une composante change
# --------------------------------------------------------------------------
class T26Source(EtapeDeuxBase):

    def test_source_modifiee(self):
        q = self.nouvelle()
        Email.objects.filter(pk=self.email.pk).update(body_plain_text=CORPS + " ")
        q = self.relue(q)
        self.assertFalse(q.effective_certification)
        erreur, sortie = self.audit()
        self.assertIsNotNone(erreur)
        self.assertIn(f"DÉFAUT  email_manager.Quote {q.pk}", sortie)
        self.assertIn("source_text_sha256", sortie)


class T27Bornes(EtapeDeuxBase):

    def test_fin_hors_du_texte(self):
        q = self.nouvelle()
        EmailQuote.all_objects.filter(pk=q.pk).update(end=len(CORPS) + 5)
        self.assertFalse(self.relue(q).effective_certification)
        erreur, sortie = self.audit()
        self.assertIsNotNone(erreur)
        self.assertIn("hors du texte", sortie)

    def test_tranche_decalee(self):
        q = self.nouvelle()
        EmailQuote.all_objects.filter(pk=q.pk).update(start=F("start") + 1, end=F("end") + 1)
        self.assertFalse(self.relue(q).effective_certification)
        erreur, sortie = self.audit()
        self.assertIsNotNone(erreur)
        self.assertIn("anchored_text_sha256", sortie)


class T28Scan(EtapeDeuxBase):

    def test_certification_d_un_scan_est_un_acte_distinct(self):
        q = create_phrase_quote(self.pdf, self.ocr_debut, self.ocr_fin)
        self.assertEqual(q.page_number, 2)
        self.assertFalse(q.certified)
        self.assertFalse(q.effective_certification)
        erreur, sortie = self.audit()
        self.assertIsNone(erreur, sortie)
        self.assertIn("en attente de certification", sortie)
        q = certify_phrase_quote(q, certified_text=LECTURE_DU_SCAN)
        q = self.relue(q)
        self.assertTrue(q.corrected_on_scan)
        self.assertEqual(q.quote_text, LECTURE_DU_SCAN)
        self.assertNotEqual(q.anchored_text_sha256, q.certified_text_sha256)
        self.assertTrue(q.effective_certification)

    def test_t28a_bornes_modifiees(self):
        q = self.scan()
        PDFQuote.all_objects.filter(pk=q.pk).update(start=F("start") + 1, end=F("end") + 1)
        self.assertFalse(self.relue(q).effective_certification)

    def test_t28b_texte_certifie_modifie(self):
        q = self.scan()
        PDFQuote.all_objects.filter(pk=q.pk).update(quote_text="Il faut savoir écrire.")
        q = self.relue(q)
        self.assertFalse(q.effective_certification)
        self.assertIn("certified_text_sha256", " ".join(q.audit_problems()))


class T29CertificationSansEmpreinte(EtapeDeuxBase):

    def test_certifiee_sans_empreinte_du_texte_certifie(self):
        q = self.nouvelle()
        EmailQuote.all_objects.filter(pk=q.pk).update(certified_text_sha256="")
        q = self.relue(q)
        self.assertTrue(q.certified)
        self.assertFalse(q.effective_certification)
        erreur, sortie = self.audit()
        self.assertIsNotNone(erreur)
        self.assertIn("certified_text_sha256", sortie)
