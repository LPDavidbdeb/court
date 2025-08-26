from django.db import models
from django.core.validators import FileExtensionValidator
from django.urls import reverse

class PDFDocument(models.Model):
    """
    Represents a single uploaded PDF document.
    """
    title = models.CharField(
        max_length=255,
        help_text="The title of the PDF document."
    )
    file = models.FileField(
        upload_to='pdf_documents/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        help_text="The uploaded PDF file."
    )
    # NEW: Optional date field for the document itself
    document_date = models.DateField(
        null=True,
        blank=True,
        help_text="The date of the document, if applicable."
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        help_text="The date and time the document was uploaded."
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Returns the URL to access a detail page for this pdf document."""
        return reverse('pdf_manager:pdf_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "PDF Document"
        verbose_name_plural = "PDF Documents"
        ordering = ['-uploaded_at']
