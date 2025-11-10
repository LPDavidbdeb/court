from django import forms
from ..models import Document, Statement, LibraryNode, DocumentSource

class ProducedDocumentForm(forms.ModelForm):
    """Form to create the top-level 'Produced' Document."""
    class Meta:
        model = Document
        fields = ['title', 'author']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.Select(attrs={'class': 'form-select'}),
        }

    def save(self, commit=True):
        # Force the source_type to 'PRODUCED' on save
        instance = super().save(commit=False)
        instance.source_type = DocumentSource.PRODUCED
        if commit:
            instance.save()
        return instance

class NodeForm(forms.Form):
    """A form for adding or editing a node (item + statement) in the tree."""
    item = forms.CharField(
        label="Title / Item", 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    text = forms.CharField(
        label="Content / Statement Text", 
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        required=False
    )
