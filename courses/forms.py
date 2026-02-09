from django import forms
from .models import Course

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['titre', 'fichier_pdf', 'formation', 'enseignant']

    def clean_fichier_pdf(self):
        fichier = self.cleaned_data.get('fichier_pdf')
        if fichier:
            if not fichier.name.endswith('.pdf'):
                raise forms.ValidationError("Seuls les fichiers PDF sont autorisés.")
            if fichier.size > 5*1024*1024:  # 5 MB max
                raise forms.ValidationError("Le fichier est trop volumineux (max 5MB).")
        return fichier
