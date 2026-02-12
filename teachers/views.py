from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render

from .forms import TeacherProfileForm
from .utils import get_or_create_teacher


def is_teacher(user):
    if user.role == "TEACHER":
        return True
    raise PermissionDenied


@login_required
@user_passes_test(is_teacher)
def teacher_profile(request):
    teacher = get_or_create_teacher(request.user)

    if request.method == "POST":
        form = TeacherProfileForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            return redirect("teachers:profile")
    else:
        form = TeacherProfileForm(instance=teacher)

    return render(request, "teachers/profile.html", {"form": form})
