from django.db import models
from protagonist_manager.models import Protagonist
from document_manager.models import DocumentNode
import locale

class EmailThread(models.Model):
    """
    Represents a single conversation thread, grouping multiple emails.
    """
    thread_id = models.CharField(max_length=255, unique=True, db_index=True,
                                 help_text="The unique ID for the email thread (e.g., from Gmail).")
    protagonist = models.ForeignKey(Protagonist, on_delete=models.SET_NULL,
                                    null=True, blank=True, related_name='email_threads',
                                    help_text="The protagonist associated with this email thread.")
    subject = models.CharField(max_length=500, blank=True, null=True,
                               help_text="The subject of the conversation, typically from the first email.")
    saved_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Thread for '{self.subject}'"

    class Meta:
        verbose_name = "Email Thread"
        verbose_name_plural = "Email Threads"
        ordering = ['-updated_at']

class Email(models.Model):
    """
    Represents a single email message within a thread.
    """
    thread = models.ForeignKey(EmailThread, on_delete=models.CASCADE, related_name='emails')
    message_id = models.CharField(max_length=255, unique=True, db_index=True)
    dao_source = models.CharField(max_length=50, blank=True, null=True,
                                  help_text="The source used to acquire this email (e.g., Gmail).")
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
        return f"Email: '{self.subject}' from {self.sender}"

    class Meta:
        verbose_name = "Email"
        verbose_name_plural = "Emails"
        ordering = ['date_sent']

class Quote(models.Model):
    """
    Links a specific quote from an email to one or more perjury elements.
    """
    email = models.ForeignKey(Email, on_delete=models.CASCADE, related_name='quotes')
    perjury_elements = models.ManyToManyField(
        DocumentNode,
        related_name='quotes',
        limit_choices_to={'is_true': False, 'is_falsifiable': True}
    )
    quote_text = models.TextField()
    full_sentence = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.email and self.quote_text:
            # Set locale for French month names
            try:
                locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
            except locale.Error:
                locale.setlocale(locale.LC_TIME, '') # Fallback to system default

            date_str = self.email.date_sent.strftime("%d %B %Y à %Hh%M") if self.email.date_sent else "date inconnue"
            
            # Prioritize protagonist's full name, fallback to sender email
            sender_name = self.email.sender
            if self.email.thread and self.email.thread.protagonist:
                sender_name = self.email.thread.protagonist.get_full_name()

            email_subject = self.email.subject or "(Sans objet)"

            self.full_sentence = (
                f'Dans le courriel intitulé "{email_subject}", '
                f'{sender_name} a écrit, le {date_str} : '
                f'"{self.quote_text}"'
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Quote from {self.email.subject} on {self.email.date_sent.strftime("%Y-%m-%d")}'

    class Meta:
        verbose_name = "Quote"
        verbose_name_plural = "Quotes"
        ordering = ['-created_at']
