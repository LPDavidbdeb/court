from django import forms
from ..models import DocumentNode


# from treebeard.forms import get_tree_fields # REMOVED: This import is not publicly exposed/needed

class DocumentNodeForm(forms.ModelForm):
    """
    Formulaire générique pour la création et la modification des instances de DocumentNode.
    Utilise django-treebeard's tree fields.
    """
    # Explicitly define the parent field as a ModelChoiceField
    # treebeard will use this to manage the parent relationship via its internal path
    parent = forms.ModelChoiceField(
        queryset=DocumentNode.objects.all(),  # Initial queryset, will be filtered in __init__
        required=False,  # Parent can be null for root nodes
        empty_label="-- Aucun (Nœud Racine) --",
        label="Parent",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = DocumentNode
        # 'parent' is now explicitly defined above, so remove it from Meta.fields
        # treebeard automatically provides 'path', 'depth', 'numchild', etc.
        fields = ['node_type', 'item', 'text']  # 'parent' removed from here

        widgets = {
            'node_type': forms.Select(attrs={'class': 'form-select'}),
            'item': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }
        labels = {
            'node_type': 'Type de Nœud',
            'item': 'Élément',
            'text': 'Texte du Nœud',
        }
        help_texts = {
            'node_type': 'Définissez le rôle de ce nœud dans la structure du document.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically set the queryset for the parent field to exclude the current node itself
        # This prevents a node from being its own parent or a descendant of itself.
        if self.instance.pk:
            # Exclude self and descendants from parent choices
            self.fields['parent'].queryset = DocumentNode.objects.exclude(
                pk=self.instance.pk
            ).exclude(
                path__startswith=self.instance.path
            ).order_by('path')
            # Set initial parent if instance has one
            if self.instance.get_parent():
                self.fields['parent'].initial = self.instance.get_parent().pk
        else:
            # For new nodes, allow any existing node as parent
            self.fields['parent'].queryset = DocumentNode.objects.all().order_by('path')

    def save(self, commit=True):
        """
        Overrides the default save method to only handle non-treebeard fields.
        Treebeard's tree manipulation (add_root, add_child, move) is handled in the views.
        """
        instance = super().save(commit=False)  # Get the instance without saving to DB yet

        # If commit is True, save the instance (non-treebeard fields)
        if commit:
            instance.save()

        return instance


class LibraryCreateForm(forms.ModelForm):
    """
    Formulaire spécialisé pour créer le nœud racine 'Bibliothèque'.
    Les champs parent, lft, rgt, depth, node_type sont prédéfinis dans la vue.
    """

    class Meta:
        model = DocumentNode
        fields = ['item', 'text']
        widgets = {
            'item': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de la Bibliothèque'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3,
                                          'placeholder': 'Description de la Bibliothèque (optionnel)'}),
        }
        labels = {
            'item': 'Nom de la Bibliothèque',
            'text': 'Description',
        }
        help_texts = {
            'item': 'Le nom de votre bibliothèque de documents.',
        }


class DocumentCreateForm(forms.ModelForm):
    """
    Formulaire spécialisé pour créer un nouveau 'Document Principal'.
    Le parent sera la 'Bibliothèque' racine, la profondeur sera 1.
    """

    class Meta:
        model = DocumentNode
        fields = ['item', 'text']
        widgets = {
            'item': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre du Document'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5,
                                          'placeholder': 'Contenu introductif du document (optionnel)'}),
        }
        labels = {
            'item': 'Titre du Document',
            'text': 'Contenu',
        }
        help_texts = {
            'item': 'Le titre principal de votre nouveau document.',
        }

