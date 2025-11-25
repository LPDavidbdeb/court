from django.db import models
from document_manager.models import Statement
from events.models import Event
from email_manager.models import Quote as EmailQuote
from pdf_manager.models import Quote as PDFQuote
from photos.models import PhotoDocument

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

    def __str__(self):
        return self.titre

    class Meta:
        verbose_name = "Trame Narrative"
        verbose_name_plural = "Trames Narratives"

class PerjuryArgument(models.Model):
    """
    An optional 'Sidecar' extension to TrameNarrative.
    If this exists, it imposes the strict 4-step perjury structure on the narrative.
    """
    trame = models.OneToOneField(
        TrameNarrative, 
        on_delete=models.CASCADE, 
        related_name='perjury_argument',
        null=True
    )

    # The 4 Strict Sections
    text_declaration = models.TextField(
        verbose_name="1. Déclaration faite sous serment",
        help_text="Contextualise the lie. (Use the plugin to link the Targeted Statement here)",
        blank=True
    )
    
    text_proof = models.TextField(
        verbose_name="2. Preuve de la fausseté",
        help_text="Demonstrate why it is false. (Use the plugin to inject Events, Emails, and Source Statements here)",
        blank=True
    )

    text_mens_rea = models.TextField(
        verbose_name="3. Connaissance de la fausseté (Mens Rea)",
        help_text="Demonstrate that they KNEW it was false.",
        blank=True
    )

    text_legal_consequence = models.TextField(
        verbose_name="4. Intention de tromper le tribunal",
        help_text="What did they hope to gain?",
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Argument: {self.trame.titre}"
