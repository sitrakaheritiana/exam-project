from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Student(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'STUDENT'}
    )
    matricule = models.CharField(max_length=50, unique=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='students/photos/', null=True, blank=True)

    def __str__(self):
        return f"{self.matricule} - {self.nom} {self.prenom}"
