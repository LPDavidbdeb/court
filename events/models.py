from django.db import models
from django.urls import reverse
from photos.models import Photo
from document_manager.models import DocumentNode
from email_manager.models import Email

class Event(models.Model):
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
        related_name='events',
        help_text="The specific allegation this event supports or refutes."
    )
    date = models.DateField(help_text="The date of the event.")
    explanation = models.TextField(
        blank=True,
        help_text="A detailed explanation of the event, auto-filled for photo clusters."
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
        related_name='events',
        help_text="The specific email this quote is from."
    )
    linked_photos = models.ManyToManyField(
        Photo,
        blank=True,
        related_name='events',
        help_text="A collection of photos related to this event.",
        # This explicitly tells Django how to handle the existing M2M table.
        through='SupportingEvidenceLinkedPhotos',
    )

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"
        db_table = 'SupportingEvidence_supportingevidence' 
        ordering = ['date']

    def get_absolute_url(self):
        """Returns the canonical URL for an event."""
        return reverse('events:detail', kwargs={'pk': self.pk})

    def get_display_id(self):
        return f"E-{self.pk}"

    def __str__(self):
        date_str = self.date.strftime('%Y-%m-%d') if self.date else "[No Date]"
        display_id_str = self.get_display_id() if self.pk else "New Event"
        description = self.explanation[:50] + '...' if self.explanation else "No explanation"

        linked_summary = []
        if self.pk:
            if self.linked_photos.exists():
                linked_summary.append(f"{self.linked_photos.count()} photo(s)")
            if self.linked_email:
                 linked_summary.append("1 email")

        linked_str = f" ({', '.join(linked_summary)})" if linked_summary else ""

        return f"{display_id_str} - {description} ({date_str}){linked_str}"

# This is the explicit definition of the intermediate table.
class SupportingEvidenceLinkedPhotos(models.Model):
    # This field points to our newly renamed Event model.
    # Crucially, `db_column` tells it to use the OLD column name in the database.
    supportingevidence = models.ForeignKey(Event, models.DO_NOTHING, db_column='supportingevidence_id')
    photo = models.ForeignKey(Photo, models.DO_NOTHING)

    class Meta:
        # Tell Django to use the existing table and not to manage its schema.
        db_table = 'SupportingEvidence_supportingevidence_linked_photos'
        managed = False
        unique_together = (('supportingevidence', 'photo'),)
