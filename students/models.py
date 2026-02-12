from django.conf import settings
from django.db import models

from formations.models import Formation

User = settings.AUTH_USER_MODEL


class Student(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={"role": "STUDENT"},
    )
    matricule = models.CharField(max_length=50, unique=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    photo = models.ImageField(upload_to="students/photos/", null=True, blank=True)
    formation = models.ForeignKey(
        Formation,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="students",
    )

    def __str__(self):
        return f"{self.matricule} - {self.nom} {self.prenom}"
