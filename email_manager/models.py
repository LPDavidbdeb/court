from django.db import models
from pgvector.django import VectorField
from django.urls import reverse
from protagonist_manager.models import Protagonist
from core.mixins import ExhibitableMixin
from core.text_matching import fold_for_matching, locate
import locale
import os

class EmailThread(models.Model, ExhibitableMixin):
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

    # --- Exhibitable Interface ---
    def get_exhibit_date(self):
        """
        Un fil est un ensemble de courriels : il se situe dans le temps là où il
        commence, donc à l'envoi du premier. Sans ça, le mixin retombe sur
        `created_at` — que ce modèle n'a pas — puis sur `timezone.now()`, ce qui
        daterait le fil du jour de sa consultation et le renverrait en fin de
        classement chronologique.

        `saved_at` n'est qu'un repli : c'est la date d'import, pas celle du fil.
        """
        premier = self.emails.exclude(date_sent=None).order_by('date_sent').first()
        if premier:
            return premier.date_sent
        return self.saved_at

    def get_exhibit_title(self):
        return self.subject or '[Sans sujet]'

    def get_exhibit_type(self):
        return "Fil de courriels"

    def get_exhibit_parties(self):
        expediteurs = []
        for e in self.emails.select_related('sender_protagonist').order_by('date_sent'):
            nom = (e.sender_protagonist.get_full_name_with_role()
                   if e.sender_protagonist else e.sender)
            if nom and nom not in expediteurs:
                expediteurs.append(nom)
        return "Entre : " + ", ".join(expediteurs) if expediteurs else ""

    def get_exhibit_description(self):
        n = self.emails.count()
        return f"{self.subject or '[Sans sujet]'} — {n} courriel(s)"

    # Un fil est une pièce à part entière : quatre d'entre eux figurent au
    # registre avec leur propre cote (P-4, P-14, P-24, P-27). Sans adresse de
    # consultation, ils étaient les seuls du tableau des cotes à ne pas être
    # ouvrables.
    def get_absolute_url(self):
        return reverse('email_manager:thread_detail', kwargs={'pk': self.pk})

    def get_public_url(self):
        return self.get_absolute_url()


class Email(models.Model, ExhibitableMixin):
    """
    Represents a single email message within a thread.
    """
    thread = models.ForeignKey(EmailThread, on_delete=models.CASCADE, related_name='emails')
    message_id = models.CharField(max_length=255, unique=True, db_index=True)
    dao_source = models.CharField(max_length=50,
                                  help_text="The source used to acquire this email (e.g., Gmail).")
    subject = models.CharField(max_length=500, blank=True, null=True)
    sender = models.CharField(max_length=255, blank=True, null=True)
    recipients_to = models.TextField(blank=True, null=True, help_text="Comma-separated 'To' recipients")
    recipients_cc = models.TextField(blank=True, null=True, help_text="Comma-separated 'Cc' recipients")
    recipients_bcc = models.TextField(blank=True, null=True, help_text="Comma-separated 'Bcc' recipients")
    date_sent = models.DateTimeField(blank=True, null=True)
    body_plain_text = models.TextField(blank=True, null=True)
    embedding = VectorField(dimensions=768, null=True, blank=True)
    eml_file_path = models.CharField(max_length=1024)
    saved_at = models.DateTimeField(auto_now_add=True)
    eml_file = models.FileField(upload_to='emails/', blank=True, null=True)

    sender_protagonist = models.ForeignKey(
        Protagonist, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='sent_emails',
        help_text="The protagonist who sent this email."
    )
    recipient_protagonists = models.ManyToManyField(
        Protagonist, 
        related_name='received_emails',
        blank=True,
        help_text="The protagonists who received this email."
    )

    def get_absolute_url(self):
        return reverse('email_manager:email_detail', kwargs={'pk': self.pk})

    def get_public_url(self):
        return reverse('core:email_public', kwargs={'pk': self.pk})

    @property
    def eml_filename(self):
        """Returns the base name of the EML file path."""
        if self.eml_file_path:
            return os.path.basename(self.eml_file_path)
        return None

    def __str__(self):
        return f"Email: '{self.subject}' from {self.sender}"

    class Meta:
        verbose_name = "Email"
        verbose_name_plural = "Emails"
        ordering = ['date_sent']

    # --- Exhibitable Interface ---
    def get_exhibit_date(self):
        return self.date_sent or self.saved_at

    def get_exhibit_title(self):
        return self.subject or '[Sans sujet]'

    def get_exhibit_type(self):
        return "Courriel"

    def get_exhibit_parties(self):
        sender = self.sender_protagonist.get_full_name_with_role() if self.sender_protagonist else self.sender
        recipients = ", ".join([p.get_full_name_with_role() for p in self.recipient_protagonists.all()])
        return f"De: {sender}\nÀ: {recipients}"

    def get_exhibit_description(self):
        return self.subject or '[Sans sujet]'

class Quote(models.Model):
    embedding = VectorField(dimensions=768, null=True, blank=True)
    """
    A specific quote extracted from an email.
    """
    email = models.ForeignKey(Email, on_delete=models.CASCADE, related_name='quotes')
    quote_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('email_manager:quote_detail', kwargs={'pk': self.pk})

    @property
    def source_text(self):
        """
        The text this quote was taken from.

        Normally the body. A message whose entire content is its subject line
        arrives with an empty body, and a quote of such a message would be
        unlocatable in a body that does not exist; for those the subject is the
        source. Only consulted when the body is genuinely empty, so a quote is
        never matched against a subject that merely happens to contain it.
        """
        if not self.email:
            return ""
        body = self.email.body_plain_text or ""
        return body if body.strip() else (self.email.subject or "")

    @property
    def position_in_source(self):
        """
        Sort key placing this quote where it actually sits in the email body.

        Quotes used to be ordered by created_at, on the premise that one reads a
        document front to back and extracts as one goes. That premise holds until
        the reader goes back up the text — from then on creation order no longer
        describes the document. Position does, and unlike created_at it does not
        move when a quote is deleted and re-extracted.

        Returns (found, rank, pk). Quotes located in the source sort by their
        offset; quotes that cannot be located trail behind them in creation
        order, which is the old behaviour preserved exactly where the new key
        has nothing to say. The offset is measured in folded coordinates (see
        core.text_matching), so it is only meaningful as a comparison between
        quotes of the same email — which is the only use it is put to.

        Matching is deliberately tolerant. Requiring the stored text to be
        character-for-character what the email says left 38 of 211 quotes
        unplaceable, almost all of them over differences that do not change
        which passage is meant: an apostrophe rendered as U+2019 in the body and
        as a space in the quote, accents present in one and not the other, a
        typo in the original tidied up on its way into the quote. Being strict
        here does not protect anything — the key only decides display order, and
        a quote that cannot be placed is simply shown out of order.
        """
        haystack = fold_for_matching(self.source_text)
        needle = fold_for_matching(self.quote_text)
        idx = locate(haystack, needle)
        if idx >= 0:
            return (0, idx, self.pk)
        return (1, self.created_at.timestamp() if self.created_at else 0.0, self.pk)

    @property
    def full_sentence(self):
        """
        Dynamically generates a full descriptive sentence for the quote,
        pulling metadata from the parent Email object.
        """
        if not self.email:
            return self.quote_text

        try:
            locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
        except locale.Error:
            locale.setlocale(locale.LC_TIME, '')  # Fallback to system default

        date_str = self.email.date_sent.strftime("%d %B %Y à %Hh%M") if self.email.date_sent else "date inconnue"
        
        if self.email.sender_protagonist:
            sender_name = self.email.sender_protagonist.get_full_name()
        else:
            sender_name = self.email.sender

        email_subject = self.email.subject or "(Sans objet)"

        return (
            f'Dans le courriel intitulé "{email_subject}", '
            f'{sender_name} a écrit, le {date_str} : '
            f'"{self.quote_text}"'
        )
    def __str__(self):
        if self.email and self.email.date_sent:
            return f'Quote from {self.email.subject} on {self.email.date_sent.strftime("%Y-%m-%d")}'
        return f'Quote from {self.email.subject} (date unknown)'

    class Meta:
        verbose_name = "Quote"
        verbose_name_plural = "Quotes"
        ordering = ['-created_at']
