from django.db import models
from pgvector.django import VectorField
from django.core.validators import FileExtensionValidator
from django.urls import reverse
from core.mixins import ExhibitableMixin
from core.text_matching import fold_for_matching, locate
from datetime import datetime
import re

class PDFDocumentType(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="The name of the document type (e.g., 'Mémoire de Marie-Josée')."
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "PDF Document Type"
        verbose_name_plural = "PDF Document Types"
        ordering = ['name']

class PDFDocument(models.Model, ExhibitableMixin):
    title = models.CharField(
        max_length=255,
        help_text="The title of the PDF document."
    )
    author = models.ForeignKey(
        'protagonist_manager.Protagonist',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='authored_pdfs',
        help_text="The author of the document, if applicable."
    )
    file = models.FileField(
        upload_to='pdf_documents/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        help_text="The uploaded PDF file."
    )
    document_date = models.DateField(
        null=True,
        blank=True,
        help_text="The date of the document, if applicable."
    )
    document_type = models.ForeignKey(
        PDFDocumentType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="The type or category of this PDF document."
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        help_text="The date and time the document was uploaded."
    )
    ai_analysis = models.TextField(
        blank=True, null=True,
        help_text="Analyse forensique et résumé généré par l'IA pour économiser les tokens multimodaux."
    )
    embedding = VectorField(dimensions=768, null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('pdf_manager:pdf_detail', kwargs={'pk': self.pk})

    def get_public_url(self):
        return reverse('core:pdf_document_public', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "PDF Document"
        verbose_name_plural = "PDF Documents"
        ordering = ['-document_date']

    # --- Exhibitable Interface ---
    def get_exhibit_date(self):
        if self.document_date:
            return datetime.combine(self.document_date, datetime.min.time())
        return self.uploaded_at

    def get_exhibit_title(self):
        return self.title

    def get_exhibit_type(self):
        return "Document PDF"

    def get_exhibit_parties(self):
        return f"Auteur: {self.author.get_full_name_with_role()}" if self.author else ""

    def get_exhibit_description(self):
        return self.ai_analysis or self.title

class Quote(models.Model):
    embedding = VectorField(dimensions=768, null=True, blank=True)
    pdf_document = models.ForeignKey(PDFDocument, on_delete=models.CASCADE, related_name='quotes')
    quote_text = models.TextField()
    page_number = models.PositiveIntegerField(
        help_text="The page number where the quote can be found."
    )
    quote_location_details = models.CharField(
        max_length=255,
        blank=True,
        help_text="Optional details to locate the quote, e.g., 'Paragraph 3' or 'Header'."
    )
    position_anchor = models.TextField(
        blank=True,
        default="",
        help_text=(
            "A verbatim fragment of the document, used only to place this quote in "
            "the text. Fill it in when quote_text is a reading of the document — a "
            "summary of table rows, say — rather than a passage copied out of it, "
            "and so cannot be found by searching for it. Never displayed."
        )
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('pdf_manager:quote_detail', kwargs={'pk': self.pk})

    @property
    def source_text(self):
        """
        The transcribed text of the document this quote was taken from.

        ai_analysis holds the transcription itself, not a summary of it — the
        structured ones open with a provenance header and mark page boundaries
        with '--- PAGE n ---'. The header describes the transcription rather
        than the document, so it is dropped before matching; the page markers
        are left in place, since removing them would only shift every offset by
        the same amount.
        """
        text = (self.pdf_document.ai_analysis or "") if self.pdf_document else ""
        return re.sub(r'^\s*<!--.*?-->', '', text, count=1, flags=re.S)

    @property
    def position_in_source(self):
        """
        Sort key placing this quote where it actually sits in the document.

        Same reasoning as email_manager.Quote.position_in_source: created_at only
        describes the document while the reader never goes back up the text.

        The page is the dominant term and is always meaningful — page_number is
        populated on every quote. Position WITHIN a page used to be uncomputable,
        on the belief that ai_analysis was only a summary; it is in fact the
        transcription, so the offset of the quote in that text now ranks quotes
        sharing a page. The offset is measured document-wide rather than
        per-page, which orders a page's quotes identically and costs nothing to
        compute for the documents transcribed without page markers.

        A quote that reads the document rather than copying it — one that
        summarises a table's rows — is nowhere in the text to be found, however
        faithfully it renders what the table says. position_anchor exists for
        those: a verbatim fragment that says where the reading belongs, searched
        in place of quote_text whenever it is set. A wrong anchor simply fails
        to locate, exactly as an unfindable quote does.

        Returns (page, found, rank, pk). Quotes located in the transcription
        rank by offset; those that cannot be located trail them in creation
        order, which is the old behaviour kept where the new key has nothing to
        say. quote_location_details ('Paragraph 3', 'Header') is still not used:
        it is free text, filled on a small minority of quotes, and ordering on
        it would be guesswork dressed as precision.
        """
        page = self.page_number if self.page_number is not None else 10 ** 9
        offset = locate(fold_for_matching(self.source_text),
                        fold_for_matching(self.position_anchor or self.quote_text))
        if offset >= 0:
            return (page, 0, offset, self.pk)
        return (page, 1, self.created_at.timestamp() if self.created_at else 0.0, self.pk)

    @property
    def full_sentence(self):
        """
        Dynamically generates a full descriptive sentence for the quote,
        pulling metadata from the parent PDFDocument object.
        """
        if not self.pdf_document:
            return self.quote_text

        doc_title = self.pdf_document.title or "(Untitled Document)"
        return f'In the document "{doc_title}", on page {self.page_number}, it says: "{self.quote_text}"'

    def __str__(self):
        return f'Quote from "{self.pdf_document.title}" on page {self.page_number}'

    class Meta:
        verbose_name = "PDF Quote"
        verbose_name_plural = "PDF Quotes"
        ordering = ['-created_at']
