# your_project_root/evidence/models.py

from django.db import models
# No longer need ContentType or GenericForeignKey as we're using specific ManyToManyFields
# from django.contrib.contenttypes.fields import GenericForeignKey
# from django.contrib.contenttypes.models import ContentType

# Assuming Photo model is in the 'photos' app, import it
from photos.models import Photo


class SupportingEvidence(models.Model):
    # Django automatically creates an 'id' (primary key) field for every model.
    # We will use this default 'id' and simply prefix it with 'P-' when needed for display.

    # Date or date range
    start_date = models.DateField(
        help_text="The start date of the evidence's relevance."
    )
    end_date = models.DateField(
        null=True,
        blank=True,
        help_text="The end date of the evidence's relevance (optional, for ranges)."
    )

    # Description (short text)
    description = models.CharField(
        max_length=255,
        help_text="A short description of the supporting evidence."
    )

    # Explanation (long text)
    explanation = models.TextField(
        help_text="A detailed explanation of the supporting evidence."
    )

    # --- NEW: Many-to-Many fields for linking to multiple objects of specific types ---
    # blank=True means it's not mandatory to link any items
    # related_name allows you to access SupportingEvidence from the linked model (e.g., photo.evidence_as_photo.all())
    linked_photos = models.ManyToManyField(
        Photo,
        blank=True,
        related_name='evidence_as_photo',
        help_text="A collection of photos related to this evidence."
    )
    # linked_emails = models.ManyToManyField(
    #     'Email', # Use string reference if Email model is defined later in this file or in another app
    #     blank=True,
    #     related_name='evidence_as_email',
    #     help_text="A collection of emails related to this evidence."
    # )
    # linked_pdfs = models.ManyToManyField(
    #     'PDF', # Use string reference if PDF model is defined later in this file or in another app
    #     blank=True,
    #     related_name='evidence_as_pdf',
    #     help_text="A collection of PDF documents related to this evidence."
    # )
    # --- END NEW FIELDS ---

    class Meta:
        verbose_name = "Supporting Evidence"
        verbose_name_plural = "Supporting Evidences"
        ordering = ['start_date', 'id'] # Order by start_date, then by the default primary key (id)

    def get_display_id(self):
        """
        Returns the P-PK formatted ID using the instance's primary key.
        """
        return f"P-{self.pk}"

    def __str__(self):
        date_range_str = self.start_date.strftime('%Y-%m-%d')
        if self.end_date:
            date_range_str += f" to {self.end_date.strftime('%Y-%m-%d')}"

        display_id_str = self.get_display_id() if self.pk else "New Evidence"

        # Dynamically build a summary of linked items for the string representation
        linked_summary = []
        if self.pk: # Only query if the object is saved and has an ID
            if self.linked_photos.exists():
                linked_summary.append(f"{self.linked_photos.count()} photo(s)")
            # if self.linked_emails.exists():
            #     linked_summary.append(f"{self.linked_emails.count()} email(s)")
            # if self.linked_pdfs.exists():
            #     linked_summary.append(f"{self.linked_pdfs.count()} PDF(s)")

        linked_str = f" ({', '.join(linked_summary)})" if linked_summary else ""

        return f"{display_id_str} - {self.description} ({date_range_str}){linked_str}"