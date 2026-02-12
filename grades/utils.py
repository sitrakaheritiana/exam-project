import os

from django.conf import settings
from django.db.models import Avg
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def generate_transcript(student, grades):
    file_name = f"releve_{student.matricule}.pdf"
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)

    os.makedirs(settings.MEDIA_ROOT, exist_ok=True)

    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, height - 50, "RELEVE DE NOTES")

    c.setFont("Helvetica", 11)
    c.drawString(50, height - 100, f"Etudiant : {student.nom} {student.prenom}")
    c.drawString(50, height - 120, f"Matricule : {student.matricule}")

    y = height - 170
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, "Cours")
    c.drawString(350, y, "Note")
    y -= 20

    c.setFont("Helvetica", 11)
    for grade in grades:
        c.drawString(50, y, grade.course.titre[:45])
        c.drawString(350, y, str(grade.valeur))
        y -= 20

        if y < 70:
            c.showPage()
            y = height - 50
            c.setFont("Helvetica", 11)

    moyenne = grades.aggregate(Avg("valeur"))["valeur__avg"] or 0
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, max(y - 20, 40), f"Moyenne generale : {round(moyenne, 2)}")

    c.save()
    return file_path
