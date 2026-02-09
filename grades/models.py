from django.db import models
from students.models import Student
from courses.models import Course

class Grade(models.Model):
    etudiant = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='grades')
    valeur = models.FloatField()

    class Meta:
        unique_together = ('etudiant', 'course')  # une note par étudiant par cours

    def __str__(self):
        return f"{self.etudiant.nom} - {self.course.titre}: {self.valeur}"
