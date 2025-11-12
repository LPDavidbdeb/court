from django import forms
from ..models import Document, Statement, LibraryNode, DocumentSource
from django.contrib.contenttypes.models import ContentType

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

class LibraryNodeCreateForm(forms.ModelForm):
    """
    Form for creating a new LibraryNode, optionally with a new Statement.
    """
    # Add a text field for creating a new Statement directly
    statement_text = forms.CharField(
        label="New Statement Text (optional)",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=False,
        help_text="Enter text here to create a new Statement and link it to this node."
    )

    class Meta:
        model = LibraryNode
        fields = ['item'] # Only 'item' is directly from LibraryNode for now
        widgets = {
            'item': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Node Title/Short Name'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        statement_text = cleaned_data.get('statement_text')

        # If statement_text is provided, ensure it's not empty after stripping whitespace
        if statement_text and not statement_text.strip():
            self.add_error('statement_text', "Statement text cannot be empty if provided.")

        return cleaned_data

    def save(self, commit=True, document=None):
        library_node = super().save(commit=False)

        if document:
            library_node.document = document
        else:
            # This form is intended for nodes within a document, so 'document' should be provided.
            # If not, it's an error or needs to be handled by the view.
            raise ValueError("Document must be provided to create a LibraryNode.")

        statement_text = self.cleaned_data.get('statement_text')
        if statement_text:
            # Create a new Statement and mark it as user-created
            statement = Statement.objects.create(text=statement_text.strip(), is_user_created=True) # NEW: Set is_user_created
            library_node.content_object = statement

        if commit:
            library_node.save()
        return library_node
