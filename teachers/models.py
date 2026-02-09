from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Teacher(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'TEACHER'}
    )
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    specialite = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.nom} {self.prenom} ({self.specialite})"
