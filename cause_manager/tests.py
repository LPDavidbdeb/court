from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.db.models.deletion import ProtectedError
from django.test import TestCase
from django.urls import reverse

from document_manager.forms import DocumentForm
from document_manager.forms.manual_forms import ProducedDocumentForm
from document_manager.models import Document, LibraryNode, ReferentHistorique, Statement
from email_manager.forms import EmailCauseForm
from email_manager.models import Email, EmailThread, Quote

from .models import Cause, LienCause, StatutCause


class CausesTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.cause = Cause.objects.create(numero_dossier='DOSSIER-A', titre='Cause actuelle')
        cls.origine = Cause.objects.create(numero_dossier='DOSSIER-B', titre='Cause source')
        cls.document = Document.objects.create(title='Acte adverse', cause_origine=cls.origine)
        cls.thread = EmailThread.objects.create(thread_id='fil-test')
        cls.email = Email.objects.create(
            thread=cls.thread, message_id='message-test', dao_source='test',
            subject='Courriel original', body_plain_text='Texte reçu à conserver.',
        )
        cls.quote = Quote.objects.create(email=cls.email, quote_text='Texte reçu')
        cls.user = get_user_model().objects.create_superuser(
            username='causes-test', email='causes@example.test', password='test-only',
        )

    def test_origine_facultative_et_distincte_de_la_cause_qui_utilise_la_preuve(self):
        self.assertIsNone(self.email.cause_origine)
        LienCause.objects.create(cause=self.cause, cause_liee=self.origine,
                                 description='Les actes de cette cause servent de preuve.')
        self.assertEqual(list(self.origine.documents_origine.all()), [self.document])
        self.assertFalse(self.cause.documents_origine.exists())
        self.assertFalse(self.cause.courriels_origine.exists())

    def test_rattacher_un_message_ne_classe_pas_les_autres_messages_du_fil(self):
        autre = Email.objects.create(thread=self.thread, message_id='autre', dao_source='test')
        self.email.cause_origine = self.origine
        self.email.save(update_fields=['cause_origine'])
        autre.refresh_from_db()
        self.assertIsNone(autre.cause_origine)
        self.quote.refresh_from_db()
        self.assertEqual(self.quote.email.cause_origine, self.origine)

    def test_une_cause_referencee_ne_se_supprime_pas_en_cascade(self):
        with self.assertRaises(ProtectedError), transaction.atomic():
            self.origine.delete()
        self.email.cause_origine = self.cause
        self.email.save(update_fields=['cause_origine'])
        with self.assertRaises(ProtectedError), transaction.atomic():
            self.cause.delete()
        self.assertTrue(Email.objects.filter(pk=self.email.pk).exists())

    def test_numero_unique_et_liens_distincts_au_niveau_sql(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            Cause.objects.create(numero_dossier=self.cause.numero_dossier, titre='Doublon')
        with self.assertRaises(IntegrityError), transaction.atomic():
            LienCause.objects.create(cause=self.cause, cause_liee=self.cause, description='X')
        LienCause.objects.create(cause=self.cause, cause_liee=self.origine, description='X')
        with self.assertRaises(IntegrityError), transaction.atomic():
            LienCause.objects.create(cause=self.cause, cause_liee=self.origine, description='Y')

    def test_etats_conservent_historique_et_dates_inconnues(self):
        self.assertEqual(self.cause.statut, StatutCause.A_PRECISER)
        premier = self.cause.consigner_etat(StatutCause.EN_COURS, motif='État observé')
        # Même après préchargement, l'objet expose sa nouvelle observation.
        cause = Cause.objects.prefetch_related('etats').get(pk=self.cause.pk)
        dernier = cause.consigner_etat(StatutCause.CLOSE, date_effet=date(2026, 10, 1))
        self.assertEqual(cause.statut, StatutCause.CLOSE)
        self.assertEqual(list(cause.etats.all()), [dernier, premier])
        premier.refresh_from_db()
        self.assertIsNone(premier.date_effet)
        self.assertEqual(premier.statut, StatutCause.EN_COURS)
        self.assertIsNotNone(premier.consigne_le)
        with self.assertRaises(ValidationError):
            cause.consigner_etat('INVENTE')
        self.assertEqual(cause.etats.count(), 2)

    def test_rattachement_document_historique_preserve_texte_et_numeros(self):
        document = Document.objects.create(title='Demande déposée', source_type='PRODUCED',
                                           numbering_mode='STORED')
        statement = Statement.objects.create(text='Texte déposé.')
        node = LibraryNode.add_root(document=document, item='Paragraphe', paragraph_number='41',
                                    content_type=ContentType.objects.get_for_model(Statement),
                                    object_id=statement.pk)
        ReferentHistorique.objects.create(document=document, libelle='Dépôt de test')
        form = DocumentForm({
            'title': document.title, 'source_type': 'PRODUCED',
            'document_original_date': '2026-07-24', 'cause_origine': self.cause.pk,
        }, instance=document)
        self.assertTrue(form.is_valid(), form.errors)
        form.save()
        node.refresh_from_db()
        statement.refresh_from_db()
        self.assertEqual(document.cause_origine, self.cause)
        self.assertEqual(node.paragraph_number, '41')
        self.assertEqual(statement.text, 'Texte déposé.')
        self.assertEqual(document.numbering_mode, 'STORED')

    def test_creation_document_avec_cause(self):
        form = ProducedDocumentForm({'title': 'Nouvelle version', 'cause_origine': self.cause.pk})
        self.assertTrue(form.is_valid(), form.errors)
        document = form.save()
        self.assertEqual(document.source_type, 'PRODUCED')
        self.assertEqual(document.cause_origine, self.cause)

    def test_formulaire_courriel_ne_reecrit_pas_le_message(self):
        # Simule une annotation mise à jour après le chargement de la fiche.
        Email.objects.filter(pk=self.email.pk).update(note='Annotation récente')
        form = EmailCauseForm({'cause_origine': self.origine.pk, 'body_plain_text': 'Altération'},
                              instance=self.email)
        self.assertTrue(form.is_valid(), form.errors)
        form.save()
        self.email.refresh_from_db()
        self.assertEqual(self.email.body_plain_text, 'Texte reçu à conserver.')
        self.assertEqual(self.email.note, 'Annotation récente')
        self.assertEqual(self.email.cause_origine, self.origine)
        form = EmailCauseForm({'cause_origine': ''}, instance=self.email)
        self.assertTrue(form.is_valid(), form.errors)
        form.save()
        self.assertIsNone(self.email.cause_origine)

    def test_parcours_creation_et_consultation(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('cause_manager:create'), {
            'numero_dossier': 'DOSSIER-C', 'titre': 'Cause créée', 'tribunal': 'Tribunal de test',
        })
        nouvelle = Cause.objects.get(numero_dossier='DOSSIER-C')
        self.assertRedirects(response, nouvelle.get_absolute_url())
        self.assertContains(self.client.get(reverse('cause_manager:list')), 'DOSSIER-C')
        response = self.client.get(self.origine.get_absolute_url())
        self.assertContains(response, self.document.get_absolute_url())
        self.assertContains(response, 'Acte adverse')
        for url in [reverse('cause_manager:update', args=[nouvelle.pk]),
                    reverse('document_manager:document_update', args=[self.document.pk]),
                    reverse('email_manager:email_cause', args=[self.email.pk])]:
            self.assertEqual(self.client.get(url).status_code, 200)

    def test_parcours_consigne_etat_et_lien(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('cause_manager:etat', args=[self.cause.pk]), {
            'statut': 'EN_COURS', 'date_effet': '', 'motif': 'Vérifié',
        })
        self.assertRedirects(response, self.cause.get_absolute_url())
        self.assertEqual(self.cause.statut, StatutCause.EN_COURS)
        url = reverse('cause_manager:lier', args=[self.cause.pk])
        data = {'cause_liee': self.origine.pk, 'description': 'Source des actes contestés'}
        self.assertRedirects(self.client.post(url, data), self.cause.get_absolute_url())
        self.assertContains(self.client.get(self.origine.get_absolute_url()), 'Source des actes contestés')
        self.assertEqual(self.client.post(url, data).status_code, 400)
        self.assertEqual(self.client.post(url, {**data, 'cause_liee': self.cause.pk}).status_code, 400)

    def test_parcours_courriel_et_provenance_visible(self):
        self.client.force_login(self.user)
        url = reverse('email_manager:email_cause', args=[self.email.pk])
        self.assertRedirects(self.client.post(url, {'cause_origine': self.origine.pk}),
                             self.email.get_absolute_url())
        self.assertContains(self.client.get(self.email.get_absolute_url()), 'DOSSIER-B')
        self.assertContains(self.client.get(self.origine.get_absolute_url()), 'Courriel original')
        self.assertContains(self.client.get(self.document.get_absolute_url()), 'DOSSIER-B')
        self.assertEqual(self.client.post(url, {'cause_origine': 999999}).status_code, 200)
        self.email.refresh_from_db()
        self.assertEqual(self.email.cause_origine, self.origine)

    def test_acces_protege_et_get_sans_ecriture(self):
        url = reverse('cause_manager:etat', args=[self.cause.pk])
        self.assertEqual(self.client.post(url, {'statut': 'CLOSE'}).status_code, 302)
        self.client.force_login(self.user)
        self.assertEqual(self.client.get(url).status_code, 405)
        self.assertFalse(self.cause.etats.exists())
