from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from courses.models import Course
from students.models import Student


class Grade(models.Model):
    etudiant = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="grades")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="grades")
    valeur = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(20)])

    class Meta:
        unique_together = ("etudiant", "course")

    def clean(self):
        if self.etudiant_id and self.course_id:
            student_formation_id = self.etudiant.formation_id
            course_formation_id = self.course.formation_id
            if not student_formation_id:
                raise ValidationError(
                    {"etudiant": "L'etudiant doit etre assigne a une formation avant notation."}
                )
            if student_formation_id != course_formation_id:
                raise ValidationError(
                    {"course": "Le cours doit appartenir a la meme formation que l'etudiant."}
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.etudiant.nom} - {self.course.titre}: {self.valeur}"
