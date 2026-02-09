from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Grade
from .forms import GradeForm
from students.utils import generate_transcript
from django.db.models import Avg, Max, Min

def is_teacher(user):
    return user.role == 'TEACHER'

def is_student(user):
    return user.role == 'STUDENT'

@login_required
@user_passes_test(is_teacher)
def grade_list(request):
    grades = Grade.objects.filter(course__enseignant=request.user.teacher)
    return render(request, 'grades/list.html', {'grades': grades})

@login_required
@user_passes_test(is_teacher)
def grade_create(request):
    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('grades:list')
    else:
        form = GradeForm()
    return render(request, 'grades/form.html', {'form': form, 'title': 'Ajouter Note'})

@login_required
@user_passes_test(is_student)
def student_grades(request):
    student = request.user.student
    grades = student.grades.all()
    moyenne = grades.aggregate(Avg('valeur'))['valeur__avg'] or 0
    stats = {
        'total_cours': grades.count(),
        'moyenne': round(moyenne, 2),
        'max': grades.aggregate(Max('valeur'))['valeur__max'] or 0,
        'min': grades.aggregate(Min('valeur'))['valeur__min'] or 0,
    }
    return render(request, 'grades/student_grades.html', {'grades': grades, 'stats': stats})

@login_required
@user_passes_test(is_student)
def download_transcript_view(request):
    student = request.user.student
    grades = student.grades.all()
    pdf_file = generate_transcript(student, grades)
    from django.http import FileResponse
    return FileResponse(open(pdf_file, 'rb'), as_attachment=True)
