from django import forms
from .models import PDFDocument

class PDFDocumentForm(forms.ModelForm):
    """
    A form for uploading and editing a PDF document.
    """
    class Meta:
        model = PDFDocument
        fields = ['title', 'file', 'document_date', 'document_type']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf'}),
            'document_date': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
            ),
            'document_type': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        """
        Override to make the file field not required when editing an existing instance.
        """
        super().__init__(*args, **kwargs)
        # If the form is for an existing instance (self.instance.pk is not None),
        # make the 'file' field not required.
        if self.instance and self.instance.pk:
            self.fields['file'].required = False
