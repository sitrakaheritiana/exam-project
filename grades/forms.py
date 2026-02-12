from django import forms

from students.models import Student
from .models import Grade


class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ["etudiant", "course", "valeur"]

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

        if user and user.role == "TEACHER":
            teacher = getattr(user, "teacher", None)
            if teacher:
                formations = teacher.formations.all()
                self.fields["course"].queryset = teacher.courses.select_related("formation")
                self.fields["etudiant"].queryset = Student.objects.filter(
                    formation__in=formations
                ).select_related("formation", "user")
            else:
                self.fields["course"].queryset = self.fields["course"].queryset.none()
                self.fields["etudiant"].queryset = self.fields["etudiant"].queryset.none()

    def clean(self):
        cleaned_data = super().clean()
        etudiant = cleaned_data.get("etudiant")
        course = cleaned_data.get("course")

        if etudiant and not etudiant.formation_id:
            self.add_error(
                "etudiant",
                "L'etudiant doit etre assigne a une formation.",
            )

        if etudiant and course and etudiant.formation_id and etudiant.formation_id != course.formation_id:
            self.add_error(
                "course",
                "Le cours choisi ne correspond pas a la formation de l'etudiant.",
            )

        if self.user and self.user.role == "TEACHER" and course:
            teacher = getattr(self.user, "teacher", None)
            if teacher and course.enseignant_id != teacher.id:
                self.add_error("course", "Vous ne pouvez noter que vos propres cours.")

        return cleaned_data
