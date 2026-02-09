from django.db import models
from formations.models import Formation
from teachers.models import Teacher

def upload_to(instance, filename):
    return f"courses/{instance.formation.code}/{filename}"

class Course(models.Model):
    titre = models.CharField(max_length=200)
    fichier_pdf = models.FileField(upload_to=upload_to)
    formation = models.ForeignKey(Formation, on_delete=models.CASCADE, related_name='courses')
    enseignant = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='courses')

    def __str__(self):
        return f"{self.titre} ({self.formation.code})"
