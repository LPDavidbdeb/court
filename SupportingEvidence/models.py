from django.db import models
from photos.models import Photo
# Assuming your email and document models are in these locations
# from email_manager.models import Email 
# from document_manager.models import DocumentNode

# Placeholder for DocumentNode if the app is not yet created
from django.contrib.auth.models import User as DocumentNode
from django.contrib.auth.models import User as Email # Placeholder

class SupportingEvidence(models.Model):
    # Self-referencing ForeignKey for parent-child hierarchy
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        help_text="The parent event for this piece of evidence."
    )

    # Link to the top-level allegation
    allegation = models.ForeignKey(
        DocumentNode, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='evidence',
        help_text="The specific allegation this evidence supports or refutes."
    )

    # A single date for the event, as clusters happen on the same day
    date = models.DateField(help_text="The date of the evidence.")
    
    # The single field for the description/explanation
    explanation = models.TextField(
        blank=True,
        help_text="A detailed explanation of the supporting evidence, auto-filled for photo clusters."
    )

    # --- Fields for specific evidence types ---
    email_quote = models.TextField(
        blank=True,
        null=True,
        help_text="A specific quote or excerpt from an email."
    )
    linked_email = models.ForeignKey(
        Email, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='evidence_quotes',
        help_text="The specific email this quote is from."
    )

    # M2M for photos
    linked_photos = models.ManyToManyField(
        Photo,
        blank=True,
        related_name='evidence',
        help_text="A collection of photos related to this evidence."
    )

    class Meta:
        verbose_name = "Supporting Evidence"
        verbose_name_plural = "Supporting Evidences"
        ordering = ['date']

    def __str__(self):
        return f"Evidence for {self.date}: {self.explanation[:50]}..."
