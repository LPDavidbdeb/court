from django.db import models
from django.core.validators import FileExtensionValidator
from django.urls import reverse

# NEW: Model to represent the type of a PDF document
class PDFDocumentType(models.Model):
    """
    A model to categorize PDF documents, e.g., 'Memoir', 'Correspondence'.
    """
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
    document_date = models.DateField(
        null=True,
        blank=True,
        help_text="The date of the document, if applicable."
    )
    # NEW: ForeignKey to the PDFDocumentType model
    document_type = models.ForeignKey(
        PDFDocumentType,
        on_delete=models.SET_NULL, # If a type is deleted, don't delete the PDFs
        null=True,
        blank=True,
        help_text="The type or category of this PDF document."
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        help_text="The date and time the document was uploaded."
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('pdf_manager:pdf_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "PDF Document"
        verbose_name_plural = "PDF Documents"
        ordering = ['-document_date']
