from django import forms

from accounts.models import CustomUser
from .models import Student


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["nom", "prenom", "photo"]


class StudentAdminForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["user", "matricule", "nom", "prenom", "photo", "formation"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        assigned_users = Student.objects.exclude(pk=getattr(self.instance, "pk", None)).values_list(
            "user_id",
            flat=True,
        )
        self.fields["user"].queryset = CustomUser.objects.filter(role="STUDENT").exclude(
            id__in=assigned_users
        )
