from django import forms

from .models import Cause, EtatCause, LienCause


class CauseForm(forms.ModelForm):
    class Meta:
        model = Cause
        fields = ['numero_dossier', 'titre', 'tribunal', 'district_judiciaire', 'notes']


class EtatCauseForm(forms.ModelForm):
    class Meta:
        model = EtatCause
        fields = ['statut', 'date_effet', 'motif']
        widgets = {'date_effet': forms.DateInput(attrs={'type': 'date'})}


class LienCauseForm(forms.ModelForm):
    class Meta:
        model = LienCause
        fields = ['cause_liee', 'description']

    def __init__(self, *args, cause, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.cause = cause
        self.fields['cause_liee'].queryset = Cause.objects.exclude(pk=cause.pk)

    def clean_cause_liee(self):
        cible = self.cleaned_data['cause_liee']
        if LienCause.objects.filter(cause=self.instance.cause, cause_liee=cible).exists():
            raise forms.ValidationError('Ce lien existe déjà.')
        return cible
