from django import forms

from accounts.models import CustomUser
from .models import Teacher


class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ["nom", "prenom", "specialite"]


class TeacherAdminForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ["user", "nom", "prenom", "specialite"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        assigned_users = Teacher.objects.exclude(pk=getattr(self.instance, "pk", None)).values_list(
            "user_id",
            flat=True,
        )
        self.fields["user"].queryset = CustomUser.objects.filter(role="TEACHER").exclude(
            id__in=assigned_users
        )
