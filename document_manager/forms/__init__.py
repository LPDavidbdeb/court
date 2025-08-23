from django import forms
from ..models import DocumentNode

# ==============================================================================
# FORMS FOR STRUCTURED DOCUMENT UPLOAD
# ==============================================================================

class StructuredDocumentUploadForm(forms.Form):
    """
    A form for uploading a structured document from a CSV file.
    """
    root_name = forms.CharField(
        label="Document Title",
        max_length=255,
        required=True,
        help_text="Enter a descriptive title for the main document.",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    csv_file = forms.FileField(
        label="Structured Document CSV File",
        required=True,
        help_text="Select the CSV file to import. It must contain 'id', 'parent_id', and 'claim_text' columns.",
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.csv'})
    )

    def clean_csv_file(self):
        file = self.cleaned_data.get('csv_file')
        if file and not file.name.endswith('.csv'):
            raise forms.ValidationError("The uploaded file must be a CSV.")
        return file

# ==============================================================================
# FORMS FROM YOUR ORIGINAL crud_views.py
# ==============================================================================

class DocumentNodeForm(forms.ModelForm):
    """
    Generic form for creating and modifying DocumentNode instances.
    """
    parent = forms.ModelChoiceField(
        queryset=DocumentNode.objects.all(),
        required=False,
        empty_label="-- Aucun (Nœud Racine) --",
        label="Parent",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = DocumentNode
        fields = ['node_type', 'item', 'text']
        widgets = {
            'node_type': forms.Select(attrs={'class': 'form-select'}),
            'item': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['parent'].queryset = DocumentNode.objects.exclude(
                pk=self.instance.pk
            ).exclude(
                path__startswith=self.instance.path
            ).order_by('path')
            if self.instance.get_parent():
                self.fields['parent'].initial = self.instance.get_parent().pk
        else:
            self.fields['parent'].queryset = DocumentNode.objects.all().order_by('path')

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance

class LibraryCreateForm(forms.ModelForm):
    """
    Specialized form for creating the root 'Library' node.
    """
    class Meta:
        model = DocumentNode
        fields = ['item', 'text']

class DocumentCreateForm(forms.ModelForm):
    """
    Specialized form for creating a new 'Main Document'.
    """
    class Meta:
        model = DocumentNode
        fields = ['item', 'text']
