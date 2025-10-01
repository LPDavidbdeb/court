from django.db import models
from photos.models import Photo
# Corrected imports for the final model structure
from document_manager.models import DocumentNode
from email_manager.models import Email

class SupportingEvidence(models.Model):
    # Kept the advanced hierarchical and linking fields from the main branch
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        help_text="The parent event for this piece of evidence."
    )
    allegation = models.ForeignKey(
        DocumentNode, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='evidence',
        help_text="The specific allegation this evidence supports or refutes."
    )
    date = models.DateField(help_text="The date of the evidence.")
    explanation = models.TextField(
        blank=True,
        help_text="A detailed explanation of the supporting evidence, auto-filled for photo clusters."
    )
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
    linked_photos = models.ManyToManyField(
        Photo,
        blank=True,
        related_name='evidence',
        help_text="A collection of photos related to this evidence."
    )

    class Meta:
        verbose_name = "Supporting Evidence"
        verbose_name_plural = "Supporting Evidences"
        # Using the more logical ordering from the main branch
        ordering = ['date']

    # Kept the useful helper method from the other branch
    def get_display_id(self):
        """
        Returns the P-PK formatted ID using the instance's primary key.
        """
        return f"P-{self.pk}"

    # Created a new, robust __str__ method that works with the final fields
    def __str__(self):
        date_str = self.date.strftime('%Y-%m-%d') if self.date else "[No Date]"
        display_id_str = self.get_display_id() if self.pk else "New Evidence"
        description = self.explanation[:50] + '...' if self.explanation else "No explanation"

        linked_summary = []
        if self.pk:
            if self.linked_photos.exists():
                linked_summary.append(f"{self.linked_photos.count()} photo(s)")
            if self.linked_email:
                 linked_summary.append("1 email")

        linked_str = f" ({', '.join(linked_summary)})" if linked_summary else ""

        return f"{display_id_str} - {description} ({date_str}){linked_str}"
