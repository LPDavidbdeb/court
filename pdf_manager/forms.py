from django import forms
from .models import PDFDocument

class PDFDocumentForm(forms.ModelForm):
    """
    A form for uploading and editing a PDF document.
    """
    class Meta:
        model = PDFDocument
        # Include the new document_date field
        fields = ['title', 'file', 'document_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf'}),
            # Add a date picker widget for the new field
            'document_date': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
            ),
        }
