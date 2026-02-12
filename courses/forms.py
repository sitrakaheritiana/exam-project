from django import forms

from teachers.models import Teacher
from .models import Course


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["titre", "fichier_pdf", "formation", "enseignant"]

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

        if user and user.role == "TEACHER":
            teacher = getattr(user, "teacher", None)
            self.fields["enseignant"].queryset = Teacher.objects.filter(pk=getattr(teacher, "pk", None))
            self.fields["enseignant"].initial = teacher
            self.fields["enseignant"].disabled = True
            if teacher:
                self.fields["formation"].queryset = teacher.formations.filter(active=True)
            else:
                self.fields["formation"].queryset = self.fields["formation"].queryset.none()

    def clean_fichier_pdf(self):
        fichier = self.cleaned_data.get("fichier_pdf")
        if fichier:
            if not fichier.name.lower().endswith(".pdf"):
                raise forms.ValidationError("Seuls les fichiers PDF sont autorises.")
            if fichier.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Le fichier est trop volumineux (max 5MB).")
        return fichier

    def clean(self):
        cleaned_data = super().clean()
        formation = cleaned_data.get("formation")
        enseignant = cleaned_data.get("enseignant")

        if formation and enseignant and not formation.enseignants.filter(pk=enseignant.pk).exists():
            self.add_error(
                "enseignant",
                "Cet enseignant doit etre assigne a la formation selectionnee.",
            )

        return cleaned_data
