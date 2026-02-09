from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.db.models import Avg

def generate_transcript(student, grades):
    file_name = f"media/releve_{student.user.username}.pdf"
    c = canvas.Canvas(file_name, pagesize=A4)

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 800, "RELEVÉ DE NOTES")
    c.setFont("Helvetica", 11)
    c.drawString(50, 770, f"Étudiant : {student.nom} {student.prenom}")

    y = 730
    for grade in grades:
        c.drawString(50, y, f"{grade.course.titre} : {grade.valeur}")
        y -= 20

    moyenne = grades.aggregate(Avg('valeur'))['valeur__avg'] or 0
    c.drawString(50, y-20, f"Moyenne générale : {round(moyenne,2)}")
    c.save()
    return file_name
