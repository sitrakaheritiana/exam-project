from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.db import models
from django.shortcuts import get_object_or_404, redirect, render

from courses.models import Course
from formations.models import Formation
from students.forms import StudentAdminForm
from students.models import Student
from students.utils import get_or_create_student
from teachers.forms import TeacherAdminForm
from teachers.models import Teacher
from teachers.utils import get_or_create_teacher


def is_student(user):
    if user.role == "STUDENT":
        return True
    raise PermissionDenied


def is_teacher(user):
    if user.role == "TEACHER":
        return True
    raise PermissionDenied


def is_admin(user):
    if user.role == "ADMIN":
        return True
    raise PermissionDenied


@login_required
def dashboard_router(request):
    if request.user.role == "STUDENT":
        return redirect("dashboard:student")
    if request.user.role == "TEACHER":
        return redirect("dashboard:teacher")
    if request.user.role == "ADMIN":
        return redirect("dashboard:admin")
    return render(request, "403.html", status=403)


@login_required
@user_passes_test(is_student)
def student_dashboard(request):
    student = get_or_create_student(request.user)
    grades = student.grades.select_related("course").all()

    moyenne = grades.aggregate(models.Avg("valeur"))["valeur__avg"]
    stats = {
        "total_cours": grades.count(),
        "moyenne": round(moyenne, 2) if moyenne else 0,
        "max": grades.aggregate(models.Max("valeur"))["valeur__max"] or 0,
        "min": grades.aggregate(models.Min("valeur"))["valeur__min"] or 0,
    }

    return render(
        request,
        "dashboard/student_dashboard.html",
        {
            "student": student,
            "stats": stats,
            "grades": grades,
        },
    )


@login_required
@user_passes_test(is_teacher)
def teacher_dashboard(request):
    teacher = get_or_create_teacher(request.user)
    courses = teacher.courses.select_related("formation").all()
    return render(
        request,
        "dashboard/teacher_dashboard.html",
        {
            "teacher": teacher,
            "courses": courses,
        },
    )


@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    stats = {
        "students": Student.objects.count(),
        "teachers": Teacher.objects.count(),
        "courses": Formation.objects.count(),
    }
    return render(request, "dashboard/admin_dashboard.html", {"stats": stats})


@login_required
@user_passes_test(is_admin)
def student_list(request):
    students = Student.objects.select_related("user", "formation")
    return render(request, "dashboard/student_list.html", {"students": students})


@login_required
@user_passes_test(is_admin)
def teacher_list(request):
    teachers = Teacher.objects.select_related("user")
    return render(request, "dashboard/teacher_list.html", {"teachers": teachers})


@login_required
@user_passes_test(is_admin)
def student_create(request):
    if request.method == "POST":
        form = StudentAdminForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("dashboard:students")
    else:
        form = StudentAdminForm()

    return render(request, "dashboard/student_create.html", {"form": form})


@login_required
@user_passes_test(is_admin)
def teacher_create(request):
    if request.method == "POST":
        form = TeacherAdminForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("dashboard:teachers")
    else:
        form = TeacherAdminForm()

    return render(request, "dashboard/teacher_create.html", {"form": form})


@login_required
@user_passes_test(is_admin)
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)

    if request.method == "POST":
        form = StudentAdminForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect("dashboard:students")
    else:
        form = StudentAdminForm(instance=student)

    return render(request, "dashboard/student_update.html", {"form": form, "student": student})


@login_required
@user_passes_test(is_admin)
def student_detail(request, pk):
    student = get_object_or_404(Student.objects.select_related("user", "formation"), pk=pk)
    return render(request, "dashboard/student_detail.html", {"student": student})


@login_required
@user_passes_test(is_admin)
def teacher_update(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)

    if request.method == "POST":
        form = TeacherAdminForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            return redirect("dashboard:teachers")
    else:
        form = TeacherAdminForm(instance=teacher)

    return render(request, "dashboard/teacher_update.html", {"form": form, "teacher": teacher})
