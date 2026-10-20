"""
Le régime des citations, étape 1 : l'isolation (invariant B).

Une citation du régime PHRASE, créée ici dans la base de test, ne doit être
observable par aucun consommateur de l'ancien système, ni rattachable par lui.

L'oracle est l'identité de la citation, jamais son texte : sur la fiche d'un
courriel, la phrase apparaît parce que le corps du courriel est affiché, que la
citation soit visible ou non. On cherche donc la PK — parmi les citations
instanciées pendant la requête (signal post_init), dans le contexte de rendu,
dans les liens et attributs HTML, dans le corps de la réponse. Les PK du
régime PHRASE sont choisies hors de portée des séquences (880001…) pour
qu'aucune autre valeur ne puisse les imiter.

Chaque surface porte un témoin : une citation de l'ancien régime qui, elle,
doit être vue. Sans témoin, une surface qui n'affiche aucune citation
réussirait le test sans rien prouver.

Plan : docs/modele_preuve/PLAN_REGIME_CITATIONS.md, § 3 (T1.2 à T1.7, T1.10).
"""
import json
import re
from collections.abc import ItemsView, KeysView, ValuesView
from contextlib import contextmanager
from datetime import date, datetime
from io import StringIO

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.management import call_command
from django.db.models import Model, QuerySet
from django.db.models.signals import post_init
from django.test import RequestFactory, TestCase
from django.utils import timezone

from argument_manager.models import TrameNarrative
from case_manager.models import ExhibitRegistry, LegalCase, PerjuryContestation, ProducedExhibit
from core.quote_regime import QuoteRegime, sha256_text
from document_manager.models import Document, DocumentSource, LibraryNode
from email_manager.models import Email, EmailThread
from email_manager.models import Quote as EmailQuote
from pdf_manager.models import PDFDocument
from pdf_manager.models import Quote as PDFQuote
from protagonist_manager.models import Protagonist

PHRASE = QuoteRegime.PHRASE
HERITE = QuoteRegime.HERITE

CORPS_1 = ("Bonjour. Phrase un de l'ancien régime. "
           "Phrase deux du nouveau régime, entière. Fin.")
CORPS_2 = "Une seule phrase, du nouveau régime."
TRANSCRIPTION_1 = "--- PAGE 1 ---\nLigne un de l'ancien régime.\nLigne deux du nouveau régime.\n"
TRANSCRIPTION_2 = "--- PAGE 1 ---\nUne ligne du nouveau régime.\n"


def _phrase(modele, pk, texte_reference, extrait, **source):
    """Une citation PHRASE ancrée et certifiée, posée par le gestionnaire de base,
    avec une PK hors de portée des séquences."""
    debut = texte_reference.index(extrait)
    return modele._base_manager.create(
        pk=pk, regime=PHRASE, quote_text=extrait, start=debut, end=debut + len(extrait),
        source_text_sha256=sha256_text(texte_reference), anchored_text_sha256=sha256_text(extrait),
        certified=True, certified_text_sha256=sha256_text(extrait), **source)


def _lien(trame, champ, citation):
    """Écrit le lien trame → citation dans la table de liaison, sans passer par
    le gestionnaire : c'est l'état qu'aucun chemin de l'ancien système ne doit
    produire, posé ici pour vérifier qu'il resterait invisible."""
    relation = getattr(TrameNarrative, champ)
    relation.through.objects.create(**{
        relation.field.m2m_field_name(): trame,
        relation.field.m2m_reverse_field_name(): citation,
    })


def _liens(trame, champ):
    """Les PK liées à la trame, lues dans la table de liaison elle-même."""
    relation = getattr(TrameNarrative, champ)
    colonne = relation.field.m2m_reverse_field_name() + "_id"
    return set(relation.through.objects.filter(
        **{relation.field.m2m_field_name(): trame}).values_list(colonne, flat=True))


@contextmanager
def instanciees():
    """Les citations (modèle, PK) instanciées pendant le bloc, quel que soit le
    chemin : gestionnaire, relation, gabarit, service."""
    vues = []

    def recepteur(sender, instance, **kwargs):
        if instance.pk is not None:
            vues.append((sender, instance.pk))

    for modele in (EmailQuote, PDFQuote):
        post_init.connect(recepteur, sender=modele, weak=False,
                          dispatch_uid=f"test-regime-{modele._meta.label}")
    try:
        yield vues
    finally:
        for modele in (EmailQuote, PDFQuote):
            post_init.disconnect(sender=modele, dispatch_uid=f"test-regime-{modele._meta.label}")


def _parcourir(valeur, trouvees, deja, profondeur=0):
    if profondeur > 7 or valeur is None or isinstance(valeur, (str, bytes, int, float, bool)):
        return
    if id(valeur) in deja:
        return
    deja.add(id(valeur))
    if isinstance(valeur, (EmailQuote, PDFQuote)):
        trouvees.add((type(valeur), valeur.pk))
        return
    if isinstance(valeur, Model):
        cache = getattr(valeur, "_prefetched_objects_cache", None) or {}
        for v in cache.values():
            _parcourir(v, trouvees, deja, profondeur + 1)
        return
    if isinstance(valeur, QuerySet):
        if valeur.model in (EmailQuote, PDFQuote) or valeur._result_cache is not None:
            for v in list(valeur):
                _parcourir(v, trouvees, deja, profondeur + 1)
        return
    if isinstance(valeur, dict):
        for v in valeur.values():
            _parcourir(v, trouvees, deja, profondeur + 1)
        return
    if isinstance(valeur, (list, tuple, set, frozenset, ItemsView, KeysView, ValuesView)):
        for v in valeur:
            _parcourir(v, trouvees, deja, profondeur + 1)
        return
    champs = getattr(valeur, "fields", None)
    if isinstance(champs, dict):
        for champ in champs.values():
            qs = getattr(champ, "queryset", None)
            if isinstance(qs, QuerySet):
                _parcourir(qs, trouvees, deja, profondeur + 1)
    attributs = getattr(valeur, "__dict__", None)
    if isinstance(attributs, dict) and type(valeur).__module__.split(".")[0] in {
        "argument_manager", "case_manager", "core", "document_manager",
        "email_manager", "pdf_manager", "protagonist_manager",
    }:
        _parcourir(attributs, trouvees, deja, profondeur + 1)


def contexte(response):
    """Les citations (modèle, PK) présentes dans le contexte de rendu."""
    trouvees, deja = set(), set()
    ctx = getattr(response, "context", None)
    if ctx is None:
        return trouvees
    for c in (ctx if isinstance(ctx, list) else [ctx]):
        try:
            _parcourir(c.flatten(), trouvees, deja)
        except AttributeError:
            _parcourir(dict(c), trouvees, deja)
    return trouvees


class RegimeCitationsBase(TestCase):
    """Un fil de deux courriels, deux PDF, une trame liée à une cause.

    Ancien régime (témoins) : q_old sur email1, p_old sur pdf1, liés à la trame.
    Nouveau régime : q_new sur email1, q_new2 sur email2 (qui n'a rien
    d'autre), p_new sur pdf1, p_new2 sur pdf2 (qui n'a rien d'autre) — tous
    liés à la trame directement dans la table de liaison, pour éprouver le
    filtre des relations.
    """

    @classmethod
    def setUpTestData(cls):
        cls.admin = get_user_model().objects.create_superuser("admin-regime", "a@example.com", "x")
        cls.pere = Protagonist.objects.create(first_name="Père", last_name="Témoin", role="Père")
        cls.fil = EmailThread.objects.create(thread_id="fil-regime", subject="Fil de test",
                                         protagonist=cls.pere)
        quand = timezone.make_aware(datetime(2010, 10, 5, 20, 0))
        cls.email1 = Email.objects.create(
            thread=cls.fil, message_id="regime-m1", subject="Sujet", sender="pere@example.com",
            sender_protagonist=cls.pere, date_sent=quand, dao_source="gmail",
            eml_file_path="regime-m1.eml", body_plain_text=CORPS_1)
        cls.email2 = Email.objects.create(
            thread=cls.fil, message_id="regime-m2", subject="Re: Sujet", sender="pere@example.com",
            sender_protagonist=cls.pere, date_sent=quand.replace(day=6), dao_source="gmail",
            eml_file_path="regime-m2.eml", body_plain_text=CORPS_2)
        cls.pdf1 = PDFDocument.objects.create(
            title="Document un", author=cls.pere, file="pdf_documents/regime-1.pdf",
            document_date=date(2013, 1, 1), ai_analysis=TRANSCRIPTION_1)
        cls.pdf2 = PDFDocument.objects.create(
            title="Document deux", author=cls.pere, file="pdf_documents/regime-2.pdf",
            document_date=date(2013, 9, 1), ai_analysis=TRANSCRIPTION_2)

        # Ancien régime : par le chemin ordinaire.
        cls.q_old = EmailQuote.objects.create(email=cls.email1, quote_text="Phrase un de l'ancien régime.")
        cls.p_old = PDFQuote.objects.create(pdf_document=cls.pdf1, quote_text="Ligne un de l'ancien régime.",
                                            page_number=1)
        # Nouveau régime : par le gestionnaire de base, qui ne filtre pas. Depuis
        # l'étape 2, une citation PHRASE est ancrée et certifiée, sinon la garde
        # de save() la refuse : mêmes PK et mêmes textes qu'à l'étape 1.
        cls.q_new = _phrase(EmailQuote, 880001, CORPS_1, "Phrase deux du nouveau régime, entière.",
                            email=cls.email1)
        cls.q_new2 = _phrase(EmailQuote, 880002, CORPS_2, CORPS_2, email=cls.email2)
        cls.p_new = _phrase(PDFQuote, 880101, TRANSCRIPTION_1, "Ligne deux du nouveau régime.",
                            pdf_document=cls.pdf1, page_number=1)
        cls.p_new2 = _phrase(PDFQuote, 880102, TRANSCRIPTION_2, "Une ligne du nouveau régime.",
                             pdf_document=cls.pdf2, page_number=1)

        cls.trame = TrameNarrative.objects.create(
            titre="Trame témoin", resume="Résumé", type_argument=TrameNarrative.TypeArgument.SUPPORT)
        cls.trame.citations_courriel.add(cls.q_old)
        cls.trame.citations_pdf.add(cls.p_old)
        for q in (cls.q_new, cls.q_new2):
            _lien(cls.trame, "citations_courriel", q)
        for q in (cls.p_new, cls.p_new2):
            _lien(cls.trame, "citations_pdf", q)
        cls.trame_vide = TrameNarrative.objects.create(
            titre="Trame vide", resume="Résumé", type_argument=TrameNarrative.TypeArgument.SUPPORT)

        cls.cause = LegalCase.objects.create(title="Cause témoin")
        cls.contestation = PerjuryContestation.objects.create(case=cls.cause, title="Contestation témoin")
        cls.contestation.supporting_narratives.add(cls.trame)
        cls.archive = LegalCase.objects.create(title="MASTER ARCHIVE - ALL EVIDENCE")

        cls.nouvelles = {(EmailQuote, 880001), (EmailQuote, 880002), (PDFQuote, 880101), (PDFQuote, 880102)}
        cls.pk_nouvelles = {880001, 880002, 880101, 880102}

    def setUp(self):
        self.client.force_login(self.admin)

    def assertAucuneNouvelle(self, paires, ou):
        self.assertFalse(set(paires) & self.nouvelles, f"citation PHRASE observée : {ou}")


# --------------------------------------------------------------------------
# T1.2 — les gestionnaires
# --------------------------------------------------------------------------
class T12Gestionnaires(RegimeCitationsBase):

    def test_objects_exclut_le_nouveau_regime(self):
        self.assertEqual(set(EmailQuote.objects.values_list("pk", flat=True)), {self.q_old.pk})
        self.assertEqual(set(PDFQuote.objects.values_list("pk", flat=True)), {self.p_old.pk})
        with self.assertRaises(EmailQuote.DoesNotExist):
            EmailQuote.objects.get(pk=880001)
        with self.assertRaises(PDFQuote.DoesNotExist):
            PDFQuote.objects.get(pk=880101)

    def test_all_objects_rend_tout(self):
        self.assertEqual(set(EmailQuote.all_objects.values_list("pk", flat=True)),
                         {self.q_old.pk, 880001, 880002})
        self.assertEqual(set(PDFQuote.all_objects.values_list("pk", flat=True)),
                         {self.p_old.pk, 880101, 880102})

    def test_phrase_objects_ne_rend_que_le_nouveau_regime(self):
        self.assertEqual(set(EmailQuote.phrase_objects.values_list("pk", flat=True)), {880001, 880002})
        self.assertEqual(set(PDFQuote.phrase_objects.values_list("pk", flat=True)), {880101, 880102})

    def test_gestionnaires_declares(self):
        for modele in (EmailQuote, PDFQuote):
            self.assertIs(modele._default_manager, modele.objects)
            self.assertIs(modele._base_manager, modele.all_objects)


# --------------------------------------------------------------------------
# T1.3 — relations inverses, M2M, prefetch
# --------------------------------------------------------------------------
class T13Relations(RegimeCitationsBase):

    def test_relations_inverses(self):
        self.assertEqual(set(self.email1.quotes.values_list("pk", flat=True)), {self.q_old.pk})
        self.assertEqual(list(self.email2.quotes.all()), [])
        self.assertEqual(self.email1.quotes.count(), 1)
        self.assertEqual(set(self.pdf1.quotes.values_list("pk", flat=True)), {self.p_old.pk})
        self.assertEqual(list(self.pdf2.quotes.all()), [])

    def test_m2m_des_trames(self):
        trame = TrameNarrative.objects.get(pk=self.trame.pk)
        self.assertEqual(set(trame.citations_courriel.values_list("pk", flat=True)), {self.q_old.pk})
        self.assertEqual(set(trame.citations_pdf.values_list("pk", flat=True)), {self.p_old.pk})
        self.assertEqual(set(EmailQuote.objects.filter(trames_narratives=trame).values_list("pk", flat=True)),
                         {self.q_old.pk})

    def test_prefetch(self):
        with instanciees() as vues:
            courriels = list(Email.objects.filter(pk__in=[self.email1.pk, self.email2.pk])
                             .prefetch_related("quotes"))
            prefetches = {e.pk: {q.pk for q in e.quotes.all()} for e in courriels}
            trames = list(TrameNarrative.objects.filter(pk=self.trame.pk)
                          .prefetch_related("citations_courriel", "citations_pdf"))
            liees = {q.pk for t in trames for q in list(t.citations_courriel.all()) + list(t.citations_pdf.all())}
        self.assertEqual(prefetches, {self.email1.pk: {self.q_old.pk}, self.email2.pk: set()})
        self.assertEqual(liees, {self.q_old.pk, self.p_old.pk})
        self.assertAucuneNouvelle(vues, "prefetch_related")


# --------------------------------------------------------------------------
# T1.4 — listes de choix et POST forgés
# --------------------------------------------------------------------------
class T14Formulaires(RegimeCitationsBase):

    def _json(self, url, donnees):
        return self.client.post(url, data=json.dumps(donnees), content_type="application/json")

    def test_listes_de_choix_ajax(self):
        for url, temoin in (("/arguments/ajax/get-email-quotes-list/", (EmailQuote, self.q_old.pk)),
                            ("/arguments/ajax/get-pdf-quotes-list/", (PDFQuote, self.p_old.pk))):
            with self.subTest(url=url):
                with instanciees() as instances:
                    r = self.client.get(url)
                self.assertEqual(r.status_code, 200)
                vues = contexte(r)
                self.assertIn(temoin, vues)
                self.assertAucuneNouvelle(vues | set(instances), url)

    def test_choix_de_l_administration_des_trames(self):
        modele_admin = admin.site._registry[TrameNarrative]
        requete = RequestFactory().get("/")
        requete.user = self.admin
        formulaire = modele_admin.get_form(requete)()
        choix_courriel = set(formulaire.fields["citations_courriel"].queryset.values_list("pk", flat=True))
        choix_pdf = set(formulaire.fields["citations_pdf"].queryset.values_list("pk", flat=True))
        self.assertIn(self.q_old.pk, choix_courriel)
        self.assertIn(self.p_old.pk, choix_pdf)
        self.assertFalse((choix_courriel | choix_pdf) & self.pk_nouvelles)

    def test_post_administration_des_trames_rejete(self):
        modele_admin = admin.site._registry[TrameNarrative]
        requete = RequestFactory().get("/")
        requete.user = self.admin
        Formulaire = modele_admin.get_form(requete, obj=self.trame_vide)
        f = Formulaire(instance=self.trame_vide, data={
            "titre": "Trame vide", "resume": "Résumé", "type_argument": "SUPPORT",
            "citations_courriel": [self.q_old.pk, 880001], "citations_pdf": [880101],
        })
        self.assertFalse(f.is_valid())
        self.assertIn("citations_courriel", f.errors)
        self.assertIn("citations_pdf", f.errors)

    def test_post_ajax_citations_courriel_rejete(self):
        url = f"/arguments/{self.trame_vide.pk}/ajax_update_email_quotes/"
        r = self._json(url, {"quote_ids": [self.q_old.pk, 880001]})
        self.assertEqual(r.status_code, 400)
        self.assertEqual(_liens(self.trame_vide, "citations_courriel"), set())
        # témoin : la même requête sans la citation nouvelle passe
        r = self._json(url, {"quote_ids": [self.q_old.pk]})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(_liens(self.trame_vide, "citations_courriel"), {self.q_old.pk})

    def test_post_ajax_citations_pdf_rejete(self):
        url = f"/arguments/{self.trame_vide.pk}/ajax_update_pdf_quotes/"
        r = self._json(url, {"quote_ids": [self.p_old.pk, 880101]})
        self.assertEqual(r.status_code, 400)
        self.assertEqual(_liens(self.trame_vide, "citations_pdf"), set())
        r = self._json(url, {"quote_ids": [self.p_old.pk]})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(_liens(self.trame_vide, "citations_pdf"), {self.p_old.pk})

    def _edition_de_trame(self, courriel, pdf):
        url = f"/arguments/{self.trame_vide.pk}/update/"
        self.client.post(url, {"titre": "Titre modifié", "resume": "Résumé", "type_argument": "SUPPORT",
                               "selected_email_quotes": courriel, "selected_pdf_quotes": pdf})

    def _rien_n_a_change(self):
        self.assertEqual(_liens(self.trame_vide, "citations_courriel"), set())
        self.assertEqual(_liens(self.trame_vide, "citations_pdf"), set())
        self.assertEqual(TrameNarrative.objects.get(pk=self.trame_vide.pk).titre, "Trame vide")

    def test_post_edition_de_trame_courriel_rejete(self):
        # seule la citation de courriel est du nouveau régime ; la citation PDF est valide
        self._edition_de_trame(f"{self.q_old.pk},880001", f"{self.p_old.pk}")
        self._rien_n_a_change()

    def test_post_edition_de_trame_pdf_rejete(self):
        # seule la citation PDF est du nouveau régime ; la citation de courriel est valide
        self._edition_de_trame(f"{self.q_old.pk}", f"{self.p_old.pk},880101")
        self._rien_n_a_change()

    def test_post_edition_de_trame_temoin_accepte(self):
        self._edition_de_trame(f"{self.q_old.pk}", f"{self.p_old.pk}")
        self.assertEqual(_liens(self.trame_vide, "citations_courriel"), {self.q_old.pk})
        self.assertEqual(_liens(self.trame_vide, "citations_pdf"), {self.p_old.pk})
        self.assertEqual(TrameNarrative.objects.get(pk=self.trame_vide.pk).titre, "Titre modifié")

    def test_post_noeud_de_document_lie_a_une_citation_nouvelle_rejete(self):
        doc = Document.objects.create(title="Acte témoin", source_type=DocumentSource.PRODUCED)
        ct = ContentType.objects.get_for_model(EmailQuote)
        r = self.client.post(f"/documents/ajax/library-node/add/{doc.pk}/", {
            "item": "Noeud", "content_type_id": ct.pk, "object_id": 880001, "action_type": "add_root"})
        self.assertIn(r.status_code, (400, 404))
        self.assertFalse(LibraryNode.objects.filter(content_type=ct, object_id=880001).exists())
        # témoin
        r = self.client.post(f"/documents/ajax/library-node/add/{doc.pk}/", {
            "item": "Noeud", "content_type_id": ct.pk, "object_id": self.q_old.pk, "action_type": "add_root"})
        self.assertTrue(LibraryNode.objects.filter(content_type=ct, object_id=self.q_old.pk).exists())

    def test_post_edition_en_place_rejete(self):
        for app, pk, modele in (("email_manager", 880001, EmailQuote), ("pdf_manager", 880101, PDFQuote)):
            with self.subTest(app=app):
                avant = modele.all_objects.get(pk=pk).quote_text
                r = self._json(f"/texte/{app}/quote/{pk}/quote_text/", {"contenu": "écrasé"})
                self.assertEqual(r.status_code, 404)
                self.assertEqual(modele.all_objects.get(pk=pk).quote_text, avant)

    def test_post_modification_et_suppression_rejetes(self):
        r = self.client.post("/emails/quote/880001/update/", {"quote_text": "écrasé"})
        self.assertEqual(r.status_code, 404)
        r = self.client.post("/emails/quote/880001/delete/")
        self.assertEqual(r.status_code, 404)
        r = self.client.post("/pdfs/quote/880101/delete/")
        self.assertEqual(r.status_code, 404)
        self.assertEqual(EmailQuote.all_objects.get(pk=880001).quote_text,
                         "Phrase deux du nouveau régime, entière.")
        self.assertTrue(PDFQuote.all_objects.filter(pk=880101).exists())

    def test_post_retrait_de_preuve_rejete(self):
        # La vue enveloppe son 404 dans un `except Exception` : le refus sort en 500.
        r = self._json(f"/arguments/{self.trame.pk}/ajax_remove_evidence/",
                       {"evidence_type": "EmailQuote", "evidence_id": 880001})
        self.assertNotEqual(r.status_code, 200)
        self.assertFalse(r.json()["success"])
        self.assertIn(880001, _liens(self.trame, "citations_courriel"))


# --------------------------------------------------------------------------
# T1.5 — les vues
# --------------------------------------------------------------------------
LIENS = [re.compile(r"/emails/quote/(\d+)/"), re.compile(r"/pdfs/quote/(\d+)/"),
         re.compile(r"data-quote-id=\\?[\"'](\d+)")]


class T15Vues(RegimeCitationsBase):

    def surfaces(self):
        e1, e2, p1, p2, t = self.email1.pk, self.email2.pk, self.pdf1.pk, self.pdf2.pk, self.trame.pk
        qo, po = (EmailQuote, self.q_old.pk), (PDFQuote, self.p_old.pk)
        return [
            (f"/emails/email/{e1}/", {qo}),
            (f"/emails/email/{e2}/", set()),
            (f"/emails/email/{e1}/print/", set()),  # la page imprimable n'affiche pas les citations
            (f"/email/{e1}/", {qo}),
            (f"/emails/thread/{self.fil.pk}/", {qo}),
            ("/emails/quotes/", {qo}),
            (f"/emails/quote/add/{e1}/", set()),
            (f"/emails/quote/{self.q_old.pk}/", {qo}),
            (f"/emails/quote/{self.q_old.pk}/update/", {qo}),
            (f"/pdfs/pdf/{p1}/", {po}),
            (f"/pdfs/pdf/{p2}/", set()),
            (f"/pdfs/quote/{self.p_old.pk}/", {po}),
            (f"/arguments/{t}/", {qo, po}),
            (f"/arguments/{t}/update/", {qo, po}),
            (f"/arguments/{t}/affidavit/", {qo, po}),
            (f"/story/{t}/", set()),
            (f"/histoire/cinematique/{t}/", set()),
            ("/arguments/ajax/all-quotes-for-tinymce/", {qo, po}),
            (f"/arguments/ajax/all-quotes-for-tinymce/?app=email_manager&modele=email&pk={e1}", {qo}),
            (f"/arguments/ajax/all-quotes-for-tinymce/?app=email_manager&modele=emailthread&pk={self.fil.pk}",
             {qo}),
            (f"/arguments/ajax/all-quotes-for-tinymce/?app=pdf_manager&modele=pdfdocument&pk={p1}", {po}),
            ("/arguments/ajax/pdf-quotes-for-tinymce/", {po}),
            ("/arguments/ajax/get-email-quotes-list/", {qo}),
            ("/arguments/ajax/get-pdf-quotes-list/", {po}),
            (f"/arguments/ajax/get-thread-emails/{self.fil.pk}/", set()),
            (f"/arguments/ajax/get-pdf-viewer/{p1}/", set()),
            ("/documents/ajax/search-evidence/?query=nouveau", set()),
            ("/documents/ajax/search-evidence/?query=ancien", {qo, po}),
            (f"/cases/{self.cause.pk}/", set()),
            (f"/cases/contestations/{self.contestation.pk}/", set()),
            (f"/cases/contestations/{self.contestation.pk}/preview/", set()),
            (f"/cases/{self.cause.pk}/export-llm/", {qo, po}),
            (f"/admin/argument_manager/tramenarrative/{t}/change/", {qo, po}),
        ]

    def test_les_surfaces_ne_voient_pas_le_nouveau_regime(self):
        for url, temoins in self.surfaces():
            with self.subTest(url=url):
                with instanciees() as vues:
                    r = self.client.get(url)
                self.assertIn(r.status_code, (200, 302), f"{url} → {r.status_code}")
                observees = set(vues) | contexte(r)
                for temoin in temoins:
                    self.assertIn(temoin, observees, f"témoin absent de {url}")
                self.assertAucuneNouvelle(observees, url)
                corps = r.content.decode("utf-8", "replace")
                for rx in LIENS:
                    self.assertFalse({int(x) for x in rx.findall(corps)} & self.pk_nouvelles,
                                     f"lien vers une citation PHRASE : {url}")
                for pk in self.pk_nouvelles:
                    self.assertNotIn(str(pk), corps, f"PK {pk} dans le corps de {url}")

    def test_la_fiche_d_une_citation_nouvelle_rend_404(self):
        for url in ("/emails/quote/880001/", "/emails/quote/880001/update/", "/pdfs/quote/880101/"):
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 404)


# --------------------------------------------------------------------------
# T1.6 — les services
# --------------------------------------------------------------------------
class T16Services(RegimeCitationsBase):

    def _pieces(self, cause):
        return {(p.content_type.model_class(), p.object_id)
                for p in ProducedExhibit.objects.filter(case=cause).select_related("content_type")}

    def test_registre_et_pieces_produites(self):
        from case_manager.exhibit_service import rebuild_produced_exhibits, refresh_case_exhibits
        with instanciees() as vues:
            refresh_case_exhibits(self.cause.pk)
            rebuild_produced_exhibits(self.cause.pk)
        registre = {(e.content_type.model_class(), e.object_id)
                    for e in ExhibitRegistry.objects.filter(case=self.cause).select_related("content_type")}
        self.assertIn((Email, self.email1.pk), registre)
        self.assertIn((PDFDocument, self.pdf1.pk), registre)
        # email2 et pdf2 ne portent que des citations PHRASE : rien ne doit les inscrire
        self.assertNotIn((Email, self.email2.pk), registre)
        self.assertNotIn((PDFDocument, self.pdf2.pk), registre)
        pieces = self._pieces(self.cause)
        self.assertIn((EmailQuote, self.q_old.pk), pieces)
        self.assertIn((PDFQuote, self.p_old.pk), pieces)
        self.assertAucuneNouvelle(pieces, "rebuild_produced_exhibits")
        self.assertAucuneNouvelle(vues, "refresh/rebuild_produced_exhibits")

    def test_archive_globale(self):
        from case_manager.archive_service import rebuild_global_exhibits
        with instanciees() as vues:
            rebuild_global_exhibits(self.archive.pk)
        pieces = self._pieces(self.archive)
        self.assertIn((EmailQuote, self.q_old.pk), pieces)
        self.assertIn((PDFQuote, self.p_old.pk), pieces)
        self.assertAucuneNouvelle(pieces, "rebuild_global_exhibits")
        self.assertAucuneNouvelle(vues, "rebuild_global_exhibits")

    def test_selection_du_rattrapage_des_plongements(self):
        from document_manager.management.commands import backfill_embeddings as be
        choisies = []

        def sans_appel(commande, cfg, lignes):
            choisies.extend((type(x), x.pk) for x in lignes)

        original = be.Command._embed_and_update
        be.Command._embed_and_update = sans_appel
        try:
            call_command("backfill_embeddings", stdout=StringIO(), stderr=StringIO())
        finally:
            be.Command._embed_and_update = original
        self.assertIn((EmailQuote, self.q_old.pk), choisies)
        self.assertIn((PDFQuote, self.p_old.pk), choisies)
        self.assertAucuneNouvelle(choisies, "backfill_embeddings")

    def test_methodes_de_preuve_des_trames(self):
        trame = TrameNarrative.objects.get(pk=self.trame.pk)
        with instanciees() as vues:
            chrono = trame.get_chronological_evidence()
            sources = trame.get_source_documents()
        trouvees, deja = set(), set()
        _parcourir([chrono, sources], trouvees, deja)
        self.assertIn((EmailQuote, self.q_old.pk), set(vues) | trouvees)
        self.assertAucuneNouvelle(set(vues) | trouvees, "TrameNarrative")

    def test_serialisation_pour_l_ia(self):
        from ai_services.utils import EvidenceFormatter
        trame = TrameNarrative.objects.get(pk=self.trame.pk)
        with instanciees() as vues:
            textes = [
                EvidenceFormatter.format_narrative_context_xml(trame),
                EvidenceFormatter.format_police_context_xml(TrameNarrative.objects.filter(pk=trame.pk)),
            ]
            collecte = EvidenceFormatter.collect_global_evidence(TrameNarrative.objects.filter(pk=trame.pk))
        trouvees, deja = set(), set()
        _parcourir(collecte, trouvees, deja)
        self.assertIn((EmailQuote, self.q_old.pk), vues)
        self.assertIn(f"P-EMAIL-{self.q_old.pk}", textes[0])
        self.assertAucuneNouvelle(set(vues) | trouvees, "ai_services.utils")
        for texte in textes:
            for pk in self.pk_nouvelles:
                self.assertNotIn(str(pk), texte)


# --------------------------------------------------------------------------
# T1.7 — les chemins de création produisent l'ancien régime
# --------------------------------------------------------------------------
class T17Creation(RegimeCitationsBase):

    def _derniere(self, modele):
        return modele.all_objects.exclude(pk__in=self.pk_nouvelles).order_by("-pk").first()

    def test_valeur_par_defaut_du_champ(self):
        q = EmailQuote(email=self.email1, quote_text="x")
        self.assertEqual(q.regime, HERITE)
        self.assertEqual(PDFQuote(pdf_document=self.pdf1, quote_text="x", page_number=1).regime, HERITE)

    def test_ajout_ajax_courriel(self):
        r = self.client.post(f"/arguments/{self.trame_vide.pk}/ajax/add-email-quote/",
                             data=json.dumps({"email_id": self.email1.pk, "quote_text": "Bonjour."}),
                             content_type="application/json")
        self.assertEqual(r.status_code, 200)
        q = EmailQuote.all_objects.get(pk=r.json()["quote"]["id"])
        self.assertEqual(q.regime, HERITE)

    def test_ajout_ajax_pdf(self):
        r = self.client.post(f"/arguments/{self.trame_vide.pk}/ajax/add-pdf-quote/",
                             data=json.dumps({"doc_id": self.pdf1.pk, "quote_text": "Ligne.", "page_number": 1}),
                             content_type="application/json")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(PDFQuote.all_objects.get(pk=r.json()["quote"]["pk"]).regime, HERITE)

    def test_formulaire_de_citation_de_courriel(self):
        avant = EmailQuote.all_objects.count()
        self.client.post(f"/emails/quote/add/{self.email1.pk}/", {"quote_text": "Fin."})
        self.assertEqual(EmailQuote.all_objects.count(), avant + 1)
        self.assertEqual(self._derniere(EmailQuote).regime, HERITE)

    def test_vue_de_creation_de_citation_pdf(self):
        avant = PDFQuote.all_objects.count()
        self.client.post(f"/pdfs/pdf/{self.pdf1.pk}/create_quote/", {"quote_text": "Ligne.", "page_number": 1})
        self.assertEqual(PDFQuote.all_objects.count(), avant + 1)
        self.assertEqual(self._derniere(PDFQuote).regime, HERITE)


# --------------------------------------------------------------------------
# T1.10 — l'administration des citations voit les deux régimes
# --------------------------------------------------------------------------
class T110Administration(RegimeCitationsBase):

    def _liste(self, url):
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200, url)
        return {o.pk for o in r.context["cl"].result_list}

    def test_liste_et_filtre(self):
        for app, ancienne, nouvelles in (("email_manager", self.q_old.pk, {880001, 880002}),
                                        ("pdf_manager", self.p_old.pk, {880101, 880102})):
            with self.subTest(app=app):
                base = f"/admin/{app}/quote/"
                self.assertEqual(self._liste(base), {ancienne} | nouvelles)
                self.assertEqual(self._liste(base + "?regime__exact=PHRASE"), nouvelles)
                self.assertEqual(self._liste(base + "?regime__exact=HERITE"), {ancienne})

    def test_fiche_d_une_citation_nouvelle(self):
        for url in ("/admin/email_manager/quote/880001/change/", "/admin/pdf_manager/quote/880101/change/"):
            with self.subTest(url=url):
                r = self.client.get(url)
                self.assertEqual(r.status_code, 200)
                self.assertEqual(r.context["original"].regime, PHRASE)
