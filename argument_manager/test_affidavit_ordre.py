"""
L'ordre des citations PDF dans le générateur d'affidavit (`/arguments/<pk>/affidavit/`).

Sous une même pièce, les citations se suivent comme on lit le document : page,
position dans la transcription, puis PK (`Quote.position_in_source`). Avant, la
requête ne triait que sur (document, page) : l'ordre des citations d'une même
page revenait au plan d'exécution de PostgreSQL, et leur sous-cote P-n-k avec
lui. C'est un défaut de déterminisme préexistant, révélé par l'empreinte du
régime des citations (docs/modele_preuve/PLAN_REGIME_CITATIONS.md, § 10).
"""
from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from argument_manager.models import TrameNarrative
from pdf_manager.models import PDFDocument
from pdf_manager.models import Quote as PDFQuote

TRANSCRIPTION = ("--- PAGE 1 ---\nAlpha ouvre la page. Bêta la poursuit. Gamma la ferme.\n"
                 "--- PAGE 2 ---\nDelta est seule sur la sienne.\n")


class OrdreDesCitationsPDF(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.admin = get_user_model().objects.create_superuser("admin-affidavit", "a@example.com", "x")
        cls.pdf = PDFDocument.objects.create(title="Document", file="pdf_documents/ordre.pdf",
                                             document_date=date(2013, 1, 1), ai_analysis=TRANSCRIPTION)
        cree = lambda texte, page: PDFQuote.objects.create(pdf_document=cls.pdf, quote_text=texte, page_number=page)
        # créées dans un autre ordre que celui de la lecture
        cls.delta = cree("Delta est seule sur la sienne.", 2)
        cls.gamma = cree("Gamma la ferme.", 1)
        cls.alpha = cree("Alpha ouvre la page.", 1)
        cls.beta = cree("Bêta la poursuit.", 1)
        cls.trame = TrameNarrative.objects.create(titre="Trame", resume="Résumé",
                                                  type_argument=TrameNarrative.TypeArgument.SUPPORT)
        cls.trame.citations_pdf.add(cls.gamma, cls.delta, cls.beta, cls.alpha)

    def setUp(self):
        self.client.force_login(self.admin)

    def ordre(self, trame=None):
        r = self.client.get(f"/arguments/{(trame or self.trame).pk}/affidavit/")
        self.assertEqual(r.status_code, 200)
        piece = next(ex for ex in r.context["exhibits"] if ex["type"] == "PDFDocument")
        return [(item["id"], item["obj"].pk) for item in piece["items"]]

    def test_tc1_rendus_repetes_identiques(self):
        premier = self.ordre()
        for _ in range(4):
            self.assertEqual(self.ordre(), premier)

    def test_tc2_la_position_dans_la_source_decide(self):
        self.assertEqual(self.ordre(), [("P-1-1", self.alpha.pk), ("P-1-2", self.beta.pk),
                                        ("P-1-3", self.gamma.pk), ("P-1-4", self.delta.pk)])

    def test_tc2_independant_de_l_ordre_des_liens(self):
        autre = TrameNarrative.objects.create(titre="Autre", resume="Résumé",
                                              type_argument=TrameNarrative.TypeArgument.SUPPORT)
        autre.citations_pdf.add(self.alpha, self.beta, self.delta, self.gamma)
        self.assertEqual([pk for _, pk in self.ordre(autre)], [pk for _, pk in self.ordre()])

    def test_tc3_meme_position_departage_par_pk(self):
        # deux citations du même passage : page et position égales
        jumelle_1 = PDFQuote.objects.create(pdf_document=self.pdf, quote_text="Bêta la poursuit.", page_number=1)
        jumelle_2 = PDFQuote.objects.create(pdf_document=self.pdf, quote_text="Bêta la poursuit.", page_number=1)
        self.trame.citations_pdf.add(jumelle_2, jumelle_1)
        pks = [pk for _, pk in self.ordre()]
        beta = [pk for pk in pks if pk in (self.beta.pk, jumelle_1.pk, jumelle_2.pk)]
        self.assertEqual(beta, sorted(beta))

    def test_tc3_introuvables_meme_creation_departage_par_pk(self):
        # introuvables dans la transcription : elles suivent les citations situées,
        # par date de création, puis par PK quand la date est la même
        x = PDFQuote.objects.create(pdf_document=self.pdf, quote_text="Absente du texte, un.", page_number=1)
        y = PDFQuote.objects.create(pdf_document=self.pdf, quote_text="Absente du texte, deux.", page_number=1)
        meme = timezone.now()
        PDFQuote.objects.filter(pk__in=[x.pk, y.pk]).update(created_at=meme)
        self.trame.citations_pdf.add(y, x)
        pks = [pk for _, pk in self.ordre()]
        self.assertEqual(pks, [self.alpha.pk, self.beta.pk, self.gamma.pk, min(x.pk, y.pk), max(x.pk, y.pk),
                               self.delta.pk])
