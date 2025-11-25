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
    de les contredire.
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

    # This field is for the claims the narrative is ABOUT.
    targeted_statements = models.ManyToManyField(
        Statement,
        related_name='narratives_targeting_this_statement', # More descriptive related_name
        blank=True,
        help_text="The specific statements targeted by this narrative."
    )

    # --- L'ensemble des preuves documentaires ---
    
    # NEW: Add a M2M to Statement for evidence
    source_statements = models.ManyToManyField(
        Statement,
        related_name='narratives_using_this_statement_as_evidence', # New distinct related_name
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
    This model enforces the 4-step structure for every refutation.
    It links the 'Lies' (Targeted Statements) to the 'Truth' (Evidence).
    """
    
    # 1. The Container (Theme)
    trame_narrative = models.ForeignKey(
        'TrameNarrative', 
        on_delete=models.CASCADE, 
        related_name='arguments'
    )
    
    # 2. The Lies (Can be one or multiple, as per your requirement)
    # Filter this to only show Statements where is_true=False and is_falsifiable=True
    targeted_statements = models.ManyToManyField(
        Statement,
        related_name='refutations',
        help_text="The specific false allegations being refuted in this block."
    )

    title = models.CharField(max_length=255, help_text="e.g., 'Allégation N°1 : Fausse déclaration sur...'")
    order = models.PositiveIntegerField(default=0)

    # 3. The Enforced Structure (RichText fields for TinyMCE)
    # Section 1
    text_declaration = models.TextField(
        verbose_name="1. Déclaration faite sous serment",
        help_text="Describe the context of the lie (Action/Reference)."
    )
    
    # Section 2
    text_proof = models.TextField(
        verbose_name="2. Preuve de la fausseté",
        help_text="Insert evidence here using the custom plugin."
    )
    
    # Section 3
    text_mens_rea = models.TextField(
        verbose_name="3. Connaissance de la fausseté (Mens Rea)",
        help_text="Why did they know it was false?"
    )
    
    # Section 4
    text_intent = models.TextField(
        verbose_name="4. Intention de tromper le tribunal",
        help_text="What did they hope to gain?"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title
