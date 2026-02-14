from django.shortcuts import render
from django.db.utils import OperationalError, ProgrammingError

from courses.models import Course
from formations.models import Formation
from students.models import Student
from teachers.models import Teacher


def public_home(request):
    stats = {
        "students": 0,
        "teachers": 0,
        "formations": 0,
        "courses": 0,
    }

    try:
        stats["students"] = Student.objects.count()
        stats["teachers"] = Teacher.objects.count()
        stats["formations"] = Formation.objects.filter(active=True).count()
        stats["courses"] = Course.objects.count()
    except (OperationalError, ProgrammingError):
        # Keep fallback values if tables are not ready.
        pass

    return render(request, "home_public.html", {"stats": stats})


def custom_403(request, exception=None):
    return render(request, "403.html", status=403)


def custom_404(request, exception=None):
    return render(request, "404.html", status=404)


def preview_403(request):
    return render(request, "403.html", status=403)


def preview_404(request):
    return render(request, "404.html", status=404)
