"""
Formulaire de création et de modification d'un axe.

Un axe n'est pas un dossier libre : il vise des ALLÉGATIONS précises d'un acte
reproduit, et c'est ce qui lui donne sa fonction. Le formulaire impose donc que
les cibles se choisissent parmi les seuls `Statement` de documents REPRODUCED —
proposer les 772 statements du dossier, dont ceux de la demande elle-même,
laisserait construire un axe qui se conteste lui-même.
"""
from django import forms
from django.contrib.contenttypes.models import ContentType

from argument_manager.models import Axe
from document_manager.models import (Document, DocumentSource, LibraryNode,
                                     Statement)


def _cibles_possibles():
    """Les statements des actes REPRODUITS, étiquetés de façon lisible."""
    ct = ContentType.objects.get_for_model(Statement)
    noeuds = (LibraryNode.objects
              .filter(content_type=ct,
                      document__source_type=DocumentSource.REPRODUCED)
              .select_related('document')
              .order_by('document__pk', 'path'))
    par_stmt = {}
    for n in noeuds:
        # Un statement peut apparaître dans plusieurs nœuds ; le premier suffit
        # à l'étiqueter.
        par_stmt.setdefault(n.object_id, n)
    return par_stmt


class EtiquetteStatement(forms.ModelMultipleChoiceField):
    """« Requête 2015 · § 15 — le défendeur était rarement disponible… »"""

    def __init__(self, *args, **kwargs):
        self._index = _cibles_possibles()
        super().__init__(*args, **kwargs)

    # ⚠️ Dans les actes REPRODUITS, `LibraryNode.item` porte du TEXTE, pas un
    # numéro — c'est l'inverse du document produit, où il porte « 27 », « 22-A ».
    # Le préfixer d'un « § » donnait « § Les parties se sont fréquentées… »,
    # suivi du même texte : un libellé illisible répété 170 fois.
    RE_NUMERO = __import__('re').compile(r"^\d+(-[A-Z])?$")

    def label_from_instance(self, obj):
        n = self._index.get(obj.pk)
        texte = " ".join((obj.text or "").split())
        if n is None:
            return texte[:120] or f"Statement {obj.pk}"
        titre = " ".join((n.document.title or "").split())[:26]
        item = str(n.item or "").strip()
        if item and self.RE_NUMERO.match(item):
            return f"{titre} · § {item} — {texte[:96]}"
        return f"{titre} — {texte[:104]}"


class AxeForm(forms.ModelForm):
    cibles = EtiquetteStatement(
        queryset=Statement.objects.none(),
        required=False,
        widget=forms.SelectMultiple(attrs={'size': 14, 'class': 'form-select'}),
        label="Allégations contestées",
        help_text="Les énoncés d'un acte REPRODUIT que cet axe vient contredire. "
                  "Un axe peut n'en viser aucune — il documente alors une "
                  "dimension sans s'opposer à un paragraphe précis.",
    )

    class Meta:
        model = Axe
        fields = ['nom', 'description', 'fenetre_debut', 'fenetre_fin', 'cibles']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'fenetre_debut': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fenetre_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
        labels = {
            'nom': "Nom de l'axe",
            'description': "Ce que l'axe établit",
            'fenetre_debut': "Fenêtre — début",
            'fenetre_fin': "Fenêtre — fin",
        }
        help_texts = {
            'fenetre_debut': "Facultative. Elle amorce l'axe par une union "
                             "temporelle; l'appartenance d'une pièce n'en dépend "
                             "pas — un horaire non daté ou une vérification "
                             "postérieure de plusieurs années y ont leur place.",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cibles'].queryset = (
            Statement.objects
            .filter(pk__in=list(_cibles_possibles().keys()))
            .order_by('pk'))

    def clean(self):
        donnees = super().clean()
        d, f = donnees.get('fenetre_debut'), donnees.get('fenetre_fin')
        if d and f and f < d:
            self.add_error('fenetre_fin',
                           "La fin de la fenêtre précède son début.")
        return donnees
