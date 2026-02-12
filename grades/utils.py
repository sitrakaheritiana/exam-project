from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.conf import settings
import os

def generate_transcript(student, grades):
    file_name = f"releve_{student.matricule}.pdf"
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)

    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    # Titre
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, height - 50, "RELEVÉ DE NOTES")

    # Infos étudiant
    c.setFont("Helvetica", 11)
    c.drawString(50, height - 100, f"Étudiant : {student.nom} {student.prenom}")
    c.drawString(50, height - 120, f"Matricule : {student.matricule}")

    # Tableau notes
    y = height - 170
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, "Cours")
    c.drawString(350, y, "Note")

    c.setFont("Helvetica", 11)
    y -= 20

    for grade in grades:
        c.drawString(50, y, grade.course.titre)
        c.drawString(350, y, str(grade.valeur))
        y -= 20

        if y < 50:
            c.showPage()
            y = height - 50

    c.save()
    return file_path
