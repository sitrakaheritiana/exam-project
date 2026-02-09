from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Course
from .forms import CourseForm

def is_admin_or_teacher(user):
    return user.role in ['ADMIN', 'TEACHER']

@login_required
@user_passes_test(is_admin_or_teacher)
def course_list(request):
    if request.user.role == 'TEACHER':
        courses = Course.objects.filter(enseignant=request.user.teacher)
    else:
        courses = Course.objects.all()
    return render(request, 'courses/list.html', {'courses': courses})

@login_required
@user_passes_test(is_admin_or_teacher)
def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('courses:list')
    else:
        form = CourseForm()
    return render(request, 'courses/form.html', {'form': form, 'title': 'Ajouter Cours'})

@login_required
@user_passes_test(is_admin_or_teacher)
def course_update(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            return redirect('courses:list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'courses/form.html', {'form': form, 'title': 'Modifier Cours'})

@login_required
@user_passes_test(is_admin_or_teacher)
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.delete()
        return redirect('courses:list')
    return render(request, 'courses/confirm_delete.html', {'course': course})
