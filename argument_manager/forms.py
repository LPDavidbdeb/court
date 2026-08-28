from django import forms
from tinymce.widgets import TinyMCE
from .models import TrameNarrative, PerjuryArgument
from document_manager.models import Statement
from django.contrib.contenttypes.models import ContentType

class TrameNarrativeForm(forms.ModelForm):
    """
    This form remains unchanged and manages the 'Evidence Collector'.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['resume'].widget = TinyMCE(attrs={'cols': 80, 'rows': 30})
        # Filter targeted_statements to only show False and Falsifiable statements
        self.fields['targeted_statements'].queryset = Statement.objects.filter(is_true=False, is_falsifiable=True)

    class Meta:
        model = TrameNarrative
        fields = [
            'titre',
            'resume',
            'type_argument',
            'targeted_statements',
        ]
        widgets = {
            'targeted_statements': forms.CheckboxSelectMultiple,
            'type_argument': forms.Select(choices=TrameNarrative.TypeArgument.choices),
        }

class PerjuryArgumentForm(forms.ModelForm):
    """
    This is the new, correct form for the 'Sidecar' model.
    It only handles the 4 structured text fields.
    """
    class Meta:
        model = PerjuryArgument
        fields = ['text_declaration', 'text_proof', 'text_mens_rea', 'text_legal_consequence']

        # L'éditeur de cette page est monté par le gabarit
        # (`perjury_argument_form.html`), sur la classe `tinymce-editor` —
        # comme sur la page de contestation. C'est là que vivent les plugins et
        # la barre d'outils ; il n'y a rien à configurer ici.
        #
        # Un widget `TinyMCE` à cette place ne fonctionnait pas : il rend la
        # classe `tinymce`, que cet init ne vise pas, et sa configuration ne
        # part qu'avec `{{ form.media }}`, que le gabarit n'émet pas. Les
        # quatre champs restaient donc de simples zones de texte affichant leur
        # HTML en clair.
        widgets = {
            'text_declaration': forms.Textarea(attrs={'class': 'tinymce-editor', 'rows': 15}),
            'text_proof': forms.Textarea(attrs={'class': 'tinymce-editor', 'rows': 15}),
            'text_mens_rea': forms.Textarea(attrs={'class': 'tinymce-editor', 'rows': 15}),
            'text_legal_consequence': forms.Textarea(attrs={'class': 'tinymce-editor', 'rows': 15}),
        }
