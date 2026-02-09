from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db import models
from students.views import get_or_create_student
from grades.models import Grade
from teachers.utils import get_or_create_teacher

@login_required
def dashboard_router(request):
    user = request.user

    if user.role == 'STUDENT':
        return redirect('dashboard:student')
    elif user.role == 'TEACHER':
        return redirect('dashboard:teacher')
    elif user.role == 'ADMIN':
        return redirect('dashboard:admin')
    else:
        return render(request, '403.html', status=403)

@login_required
def student_dashboard(request):
    student = get_or_create_student(request.user)

    grades = student.grades.all()

    moyenne = grades.aggregate(
        models.Avg('valeur')
    )['valeur__avg']

    stats = {
        'total_cours': grades.count(),
        'moyenne': round(moyenne, 2) if moyenne else 0,
        'max': grades.aggregate(models.Max('valeur'))['valeur__max'],
        'min': grades.aggregate(models.Min('valeur'))['valeur__min'],
    }

    return render(request, 'dashboard/student_dashboard.html', {
        'student': student,
        'stats': stats,
        'grades': grades
    })

@login_required
def teacher_dashboard(request):
    teacher = request.user.teacher
    courses = teacher.courses.all()

    return render(request, 'dashboard/teacher_dashboard.html', {
        'teacher': teacher,
        'courses': courses
    })

from students.models import Student
from teachers.models import Teacher
from courses.models import Course

@login_required
def admin_dashboard(request):
    stats = {
        'students': Student.objects.count(),
        'teachers': Teacher.objects.count(),
        'courses': Course.objects.count(),
    }

    return render(request, 'dashboard/admin_dashboard.html', {
        'stats': stats
    })

@login_required
def teacher_dashboard(request):
    teacher = get_or_create_teacher(request.user)

    courses = teacher.courses.all()  # ou related_name si défini

    return render(request, 'dashboard/teacher_dashboard.html', {
        'teacher': teacher,
        'courses': courses
    })