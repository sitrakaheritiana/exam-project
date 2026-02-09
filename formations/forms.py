from django import forms
from .models import Formation

class FormationForm(forms.ModelForm):
    class Meta:
        model = Formation
        fields = ['code', 'libelle', 'active', 'enseignants']
        widgets = {
            'enseignants': forms.CheckboxSelectMultiple()
        }
