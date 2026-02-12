from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from students.utils import get_or_create_student
from teachers.utils import get_or_create_teacher
from .forms import CustomUserCreationForm


def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            if user.role == "STUDENT":
                get_or_create_student(user)
            elif user.role == "TEACHER":
                get_or_create_teacher(user)

            login(request, user)
            return redirect("dashboard:dashboard")
    else:
        form = CustomUserCreationForm()

    return render(request, "accounts/register.html", {"form": form})


@require_POST
def logout_view(request):
    logout(request)
    return redirect("accounts:login")
