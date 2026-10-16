from django import forms

from ..models import Email


class EmailCauseForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = ['cause_origine']
        widgets = {'cause_origine': forms.Select(attrs={'class': 'form-select'})}

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            # Ne pas réécrire le message ou ses annotations depuis cette fiche.
            instance.save(update_fields=['cause_origine'])
        return instance
