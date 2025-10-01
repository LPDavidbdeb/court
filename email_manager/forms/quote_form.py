from django import forms
from ..models import Quote
from document_manager.models import DocumentNode

class QuoteForm(forms.ModelForm):
    perjury_elements = forms.ModelMultipleChoiceField(
        queryset=DocumentNode.objects.filter(is_true=False, is_falsifiable=True),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        label="Éléments de Parjure Associés",
        help_text="Sélectionnez un ou plusieurs éléments de parjure liés à cette citation."
    )

    class Meta:
        model = Quote
        fields = ['quote_text', 'perjury_elements']
        widgets = {
            'quote_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }
        labels = {
            'quote_text': "Citation Extraite de l'Email",
        }
