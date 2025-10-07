from django import forms
from tinymce.widgets import TinyMCE
from .models import TrameNarrative
from document_manager.models import DocumentNode

class DocumentNodeChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.text.replace('[PARAGRAPH]', '').strip()

class TrameNarrativeForm(forms.ModelForm):
    allegations_ciblees = DocumentNodeChoiceField(
        queryset=DocumentNode.objects.filter(is_true=False, is_falsifiable=True),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Targeted Allegations"
    )

    class Meta:
        model = TrameNarrative
        fields = [
            'titre',
            'resume',
            'type_argument',
            'allegations_ciblees',
        ]
        widgets = {
            'resume': TinyMCE(attrs={'cols': 80, 'rows': 30}),
        }
