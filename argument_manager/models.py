from django.db import models
from document_manager.models import DocumentNode
from events.models import Event
from email_manager.models import Quote as EmailQuote
from pdf_manager.models import Quote as PDFQuote

class TrameNarrative(models.Model):
    """
    Construit un dossier d'argumentation qui lie un ensemble de preuves 
    à un ensemble d'allégations cibles, dans le but de les supporter ou 
    de les contredire.
    """
    
    class TypeArgument(models.TextChoices):
        CONTRADICTION = 'CONTRADICTION', 'Vise à contredire les allégations'
        SUPPORT = 'SUPPORT', 'Vise à supporter les allégations'

    # Le nom de votre dossier d'argumentation
    titre = models.CharField(
        max_length=255, 
        help_text="Un titre descriptif pour ce dossier d'argumentation (ex: 'Preuve de l'implication parentale')."
    )

    # L'argumentaire que vous rédigez
    resume = models.TextField(
        help_text="Le résumé expliquant comment les preuves assemblées forment un argument cohérent contre (ou pour) les allégations ciblées."
    )
    
    type_argument = models.CharField(
        max_length=20,
        choices=TypeArgument.choices
    )

    # LA MODIFICATION CLÉ : Lier à PLUSIEURS allégations
    allegations_ciblees = models.ManyToManyField(
        DocumentNode,
        related_name='trames_narratives',
        help_text="Les allégations spécifiques ciblées par cet argumentaire."
    )

    # --- L'ensemble des preuves documentaires ---
    
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

    def __str__(self):
        return self.titre

    class Meta:
        verbose_name = "Trame Narrative"
        verbose_name_plural = "Trames Narratives"
