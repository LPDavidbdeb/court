from django import forms
from .models import LegalCase, PerjuryContestation

class LegalCaseForm(forms.ModelForm):
    class Meta:
        model = LegalCase
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Divorce Proceedings 2025'}),
        }

class PerjuryContestationForm(forms.ModelForm):
    class Meta:
        model = PerjuryContestation
        fields = ['title', 'targeted_statements', 'supporting_narratives']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'targeted_statements': forms.CheckboxSelectMultiple,
            'supporting_narratives': forms.CheckboxSelectMultiple,
        }
