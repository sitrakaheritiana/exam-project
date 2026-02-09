from django.db import models
from teachers.models import Teacher

class Formation(models.Model):
    code = models.CharField(max_length=20, unique=True)
    libelle = models.CharField(max_length=200)
    active = models.BooleanField(default=True)
    enseignants = models.ManyToManyField(Teacher, blank=True, related_name='formations')

    def __str__(self):
        return f"{self.code} - {self.libelle}"
