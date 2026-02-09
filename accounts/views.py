from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            if user.role == 'STUDENT':
                from students.utils import get_or_create_student
                get_or_create_student(user)

            elif user.role == 'TEACHER':
                from teachers.utils import get_or_create_teacher
                get_or_create_teacher(user)

            login(request, user)
            return redirect('dashboard:dashboard')
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})


@require_POST
def logout_view(request):
    logout(request)
    return redirect('accounts:login')
