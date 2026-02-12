import os

from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.db.models import Avg, Max, Min
from django.http import FileResponse, Http404
from django.shortcuts import redirect, render

from students.utils import get_or_create_student
from .forms import GradeForm
from .models import Grade
from .utils import generate_transcript


def is_teacher_or_admin(user):
    if user.role in ["TEACHER", "ADMIN"]:
        return True
    raise PermissionDenied


def is_student(user):
    if user.role == "STUDENT":
        return True
    raise PermissionDenied


@login_required
@user_passes_test(is_teacher_or_admin)
def grade_list(request):
    if request.user.role == "TEACHER":
        grades = Grade.objects.filter(course__enseignant=request.user.teacher)
    else:
        grades = Grade.objects.all()

    grades = grades.select_related("etudiant", "course", "course__formation")
    return render(request, "grades/list.html", {"grades": grades})


@login_required
@user_passes_test(is_teacher_or_admin)
def grade_create(request):
    if request.method == "POST":
        form = GradeForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect("grades:list")
    else:
        form = GradeForm(user=request.user)

    return render(request, "grades/form.html", {"form": form, "title": "Ajouter Note"})


@login_required
@user_passes_test(is_student)
def student_grades(request):
    student = get_or_create_student(request.user)
    grades = student.grades.select_related("course")
    moyenne = grades.aggregate(Avg("valeur"))["valeur__avg"] or 0
    stats = {
        "total_cours": grades.count(),
        "moyenne": round(moyenne, 2),
        "max": grades.aggregate(Max("valeur"))["valeur__max"] or 0,
        "min": grades.aggregate(Min("valeur"))["valeur__min"] or 0,
    }
    return render(request, "grades/student_grades.html", {"grades": grades, "stats": stats})


@login_required
@user_passes_test(is_student)
def download_transcript(request):
    student = get_or_create_student(request.user)
    grades = student.grades.select_related("course")

    if not grades.exists():
        raise Http404("Aucune note disponible")

    pdf_path = generate_transcript(student, grades)

    return FileResponse(
        open(pdf_path, "rb"),
        as_attachment=True,
        filename=os.path.basename(pdf_path),
    )


@login_required
@user_passes_test(is_student)
def download_transcript_view(request):
    return download_transcript(request)
