from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from students.utils import get_or_create_student
from .forms import CourseForm
from .models import Course


def is_admin_or_teacher(user):
    if user.role in ["ADMIN", "TEACHER"]:
        return True
    raise PermissionDenied


def is_admin_teacher_or_student(user):
    if user.role in ["ADMIN", "TEACHER", "STUDENT"]:
        return True
    raise PermissionDenied


@login_required
@user_passes_test(is_admin_teacher_or_student)
def course_list(request):
    if request.user.role == "TEACHER":
        courses = Course.objects.filter(enseignant=request.user.teacher).select_related(
            "formation",
            "enseignant",
        )
    elif request.user.role == "STUDENT":
        student = get_or_create_student(request.user)
        if student.formation_id:
            courses = Course.objects.filter(formation=student.formation).select_related(
                "formation",
                "enseignant",
            )
        else:
            courses = Course.objects.none()
    else:
        courses = Course.objects.all().select_related("formation", "enseignant")

    return render(request, "courses/list.html", {"courses": courses})


@login_required
@user_passes_test(is_admin_or_teacher)
def course_create(request):
    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            course = form.save(commit=False)
            if request.user.role == "TEACHER":
                course.enseignant = request.user.teacher
            course.save()
            return redirect("courses:list")
    else:
        form = CourseForm(user=request.user)
    return render(request, "courses/form.html", {"form": form, "title": "Ajouter Cours"})


@login_required
@user_passes_test(is_admin_or_teacher)
def course_update(request, pk):
    course = get_object_or_404(Course, pk=pk)

    if request.user.role == "TEACHER" and course.enseignant_id != request.user.teacher.id:
        raise Http404()

    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES, instance=course, user=request.user)
        if form.is_valid():
            updated_course = form.save(commit=False)
            if request.user.role == "TEACHER":
                updated_course.enseignant = request.user.teacher
            updated_course.save()
            return redirect("courses:list")
    else:
        form = CourseForm(instance=course, user=request.user)
    return render(request, "courses/form.html", {"form": form, "title": "Modifier Cours"})


@login_required
@user_passes_test(is_admin_or_teacher)
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)

    if request.user.role == "TEACHER" and course.enseignant_id != request.user.teacher.id:
        raise Http404()

    if request.method == "POST":
        course.delete()
        return redirect("courses:list")
    return render(request, "courses/confirm_delete.html", {"course": course})
