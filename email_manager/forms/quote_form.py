from django import forms
from ..models import Quote
from document_manager.models import DocumentNode


class PerjuryElementSelectWidget(forms.SelectMultiple):
    """
    Custom widget to add a 'title' attribute to each option,
    which will be displayed as a tooltip by the browser.
    """
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex, attrs)
        if value:
            try:
                node = self.choices.queryset.get(pk=value)
                # Set the full text of the allegation as the tooltip.
                option['attrs']['title'] = node.text
            except (TypeError, ValueError, self.choices.queryset.model.DoesNotExist):
                pass  # Handle cases where the value isn't a valid pk
        return option


class PerjuryElementChoiceField(forms.ModelMultipleChoiceField):
    """
    Custom choice field to format the label for each perjury element.
    """
    def label_from_instance(self, obj):
        # Get the parent document to provide context.
        parent_doc = obj.get_ancestors().filter(node_type='document').first()
        parent_name = parent_doc.item if parent_doc else "Unknown Document"
        # Format as: "Parent Document -> Allegation Title"
        return f"{parent_name} -> {obj.item}"


class QuoteForm(forms.ModelForm):
    perjury_elements = PerjuryElementChoiceField(
        # FIXED: Removed the invalid .select_related('parent')
        queryset=DocumentNode.objects.filter(is_true=False, is_falsifiable=True),
        widget=PerjuryElementSelectWidget(attrs={'class': 'form-control'}),
        label="Éléments de Parjure Associés",
        help_text="Survolez une option pour voir l'allégation complète.",
        required=True
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
