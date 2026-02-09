from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import TeacherProfileForm
from .models import Teacher

def get_or_create_teacher(user):
    teacher, created = Teacher.objects.get_or_create(
        user=user,
        defaults={
            'nom': user.username,
            'prenom': '',
            'specialite': ''
        }
    )
    return teacher

@login_required
def teacher_profile(request):
    teacher = get_or_create_teacher(request.user)

    if request.method == 'POST':
        form = TeacherProfileForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            return redirect('teachers:profile')
    else:
        form = TeacherProfileForm(instance=teacher)

    return render(request, 'teachers/profile.html', {'form': form})
