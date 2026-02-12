from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render

from .forms import StudentProfileForm
from .utils import get_or_create_student


def is_student(user):
    if user.role == "STUDENT":
        return True
    raise PermissionDenied


@login_required
@user_passes_test(is_student)
def student_profile(request):
    student = get_or_create_student(request.user)

    if request.method == "POST":
        form = StudentProfileForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect("students:profile")
    else:
        form = StudentProfileForm(instance=student)

    return render(request, "students/profile.html", {"form": form})
