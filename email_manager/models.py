from django.db import models
import os
from django.conf import settings
from protagonist_manager.models import Protagonist  # Import the Protagonist model


class SavedEmail(models.Model):
    """
    Django model to store metadata about saved emails.
    """
    message_id = models.CharField(max_length=255, unique=True, db_index=True)
    thread_id = models.CharField(max_length=255, db_index=True)

    # New ForeignKey to Protagonist
    # on_delete=models.SET_NULL means if a Protagonist is deleted,
    # this field will be set to NULL instead of deleting the SavedEmail.
    # null=True, blank=True allows emails to exist without a linked protagonist.
    protagonist = models.ForeignKey(Protagonist, on_delete=models.SET_NULL,
                                    null=True, blank=True, related_name='saved_emails')

    dao_source = models.CharField(max_length=50, blank=True, null=True,
                                  help_text="The source DAO used to acquire this email (e.g., Gmail, EML Upload).")

    subject = models.CharField(max_length=500, blank=True, null=True)
    sender = models.CharField(max_length=255, blank=True, null=True)

    recipients_to = models.TextField(blank=True, null=True, help_text="Comma-separated 'To' recipients")
    recipients_cc = models.TextField(blank=True, null=True, help_text="Comma-separated 'Cc' recipients")
    recipients_bcc = models.TextField(blank=True, null=True, help_text="Comma-separated 'Bcc' recipients")

    date_sent = models.DateTimeField(blank=True, null=True)

    body_plain_text = models.TextField(blank=True, null=True)

    eml_file_path = models.CharField(max_length=1024, blank=True, null=True)

    saved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Email: '{self.subject}' from {self.sender} on {self.date_sent.strftime('%Y-%m-%d') if self.date_sent else 'N/A'}"

    class Meta:
        verbose_name = "Saved Email"
        verbose_name_plural = "Saved Emails"
        ordering = ['-date_sent']
