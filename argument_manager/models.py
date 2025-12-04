from django.db import models
from document_manager.models import Statement
from events.models import Event
from email_manager.models import Quote as EmailQuote
from pdf_manager.models import Quote as PDFQuote
from photos.models import PhotoDocument
from googlechat_manager.models import ChatSequence
from datetime import datetime, date
from django.utils import timezone

class TrameNarrative(models.Model):
    """
    Construit un dossier d'argumentation qui lie un ensemble de preuves 
    à un ensemble d'allégations cibles, dans le but de les supporter ou 
    de les contredire. This is the 'Evidence Collector'.
    """
    
    class TypeArgument(models.TextChoices):
        CONTRADICTION = 'CONTRADICTION', 'Vise à contredire les allégations'
        SUPPORT = 'SUPPORT', 'Vise à supporter les allégations'

    titre = models.CharField(
        max_length=255, 
        help_text="Un titre descriptif pour ce dossier d'argumentation (ex: 'Preuve de l'implication parentale')."
    )
    resume = models.TextField(
        help_text="Le résumé expliquant comment les preuves assemblées forment un argument cohérent contre (ou pour) les allégations ciblées."
    )
    type_argument = models.CharField(
        max_length=20,
        choices=TypeArgument.choices
    )

    targeted_statements = models.ManyToManyField(
        Statement,
        related_name='narratives_targeting_this_statement',
        blank=True,
        help_text="The specific statements targeted by this narrative."
    )

    # --- L'ensemble des preuves documentaires ---
    source_statements = models.ManyToManyField(
        Statement,
        related_name='narratives_using_this_statement_as_evidence',
        blank=True,
        help_text="Statements from other documents used as evidence."
    )
    evenements = models.ManyToManyField(
        Event,
        blank=True,
        related_name='trames_narratives'
    )
    citations_courriel = models.ManyToManyField(
        EmailQuote,
        blank=True,
        related_name='trames_narratives'
    )
    citations_pdf = models.ManyToManyField(
        PDFQuote,
        blank=True,
        related_name='trames_narratives'
    )
    photo_documents = models.ManyToManyField(
        PhotoDocument,
        blank=True,
        related_name='trames_narratives'
    )
    citations_chat = models.ManyToManyField(
        ChatSequence,
        blank=True,
        related_name='trames_narratives',
        help_text="Sequences of chat messages used as evidence."
    )

    # === NOUVEAUX CHAMPS POUR L'AUDITEUR IA ===
    ai_analysis_json = models.JSONField(
        default=dict,
        blank=True,
        help_text="Analyse objective générée par l'IA confrontant preuves vs allégations."
    )
    analysis_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.titre

    def get_chronological_evidence(self):
        """
        Aggregates all evidence types and sorts them strictly by date.
        Converts all date-like objects to full datetime objects for safe comparison.
        """
        timeline = []

        def to_datetime(d):
            """Converts date or datetime objects to a timezone-aware datetime."""
            if d is None:
                return None
            if isinstance(d, datetime):
                return timezone.make_aware(d) if timezone.is_naive(d) else d
            if isinstance(d, date):
                return timezone.make_aware(datetime.combine(d, datetime.min.time()))
            return None

        for quote in self.citations_courriel.select_related('email'):
            timeline.append({
                'type': 'email',
                'date': to_datetime(quote.email.date_sent if quote.email else None),
                'object': quote
            })

        for quote in self.citations_pdf.select_related('pdf_document'):
            timeline.append({
                'type': 'pdf',
                'date': to_datetime(quote.pdf_document.document_date if quote.pdf_document else None),
                'object': quote
            })

        for seq in self.citations_chat.all():
            timeline.append({
                'type': 'chat',
                'date': to_datetime(seq.start_date),
                'object': seq
            })

        for event in self.evenements.all():
            timeline.append({
                'type': 'event',
                'date': to_datetime(event.date),
                'object': event
            })
            
        for photo in self.photo_documents.all():
             timeline.append({
                'type': 'photo',
                'date': to_datetime(photo.created_at),
                'object': photo
            })

        # Filter out items with no date and sort
        return sorted([item for item in timeline if item['date']], key=lambda x: x['date'])

    def get_structured_analysis(self):
        """
        Retourne l'analyse IA si elle existe, sinon retourne le résumé manuel (fallback).
        Sert d'interface unifiée pour l'étape suivante (le Procureur).
        """
        if self.ai_analysis_json and 'constats_objectifs' in self.ai_analysis_json:
            return self.ai_analysis_json
        
        # Fallback : Si pas d'analyse IA, on emballe le résumé manuel pour qu'il ressemble à du JSON
        return {
            "analyse_id": f"MANUAL-{self.pk}",
            "constats_objectifs": [{
                "fait_identifie": "Résumé narratif (Manuel)",
                "description_factuelle": self.resume,
                "contradiction_directe": "Non spécifié (Mode manuel)"
            }]
        }

    class Meta:
        verbose_name = "Trame Narrative"
        verbose_name_plural = "Trames Narratives"

class PerjuryArgument(models.Model):
    trame = models.OneToOneField(
        TrameNarrative, 
        on_delete=models.CASCADE, 
        related_name='perjury_argument',
        null=True
    )
    text_declaration = models.TextField(verbose_name="1. Déclaration faite sous serment", help_text="Contextualise the lie.", blank=True)
    text_proof = models.TextField(verbose_name="2. Preuve de la fausseté", help_text="Demonstrate why it is false.", blank=True)
    text_mens_rea = models.TextField(verbose_name="3. Connaissance de la fausseté (Mens Rea)", help_text="Demonstrate that they KNEW it was false.", blank=True)
    text_legal_consequence = models.TextField(verbose_name="4. Intention de tromper le tribunal", help_text="What did they hope to gain?", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Argument: {self.trame.titre}"