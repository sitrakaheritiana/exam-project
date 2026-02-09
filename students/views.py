from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import StudentProfileForm
from .models import Student

def get_or_create_student(user):
    student, created = Student.objects.get_or_create(
        user=user,
        defaults={
            'matricule': f"STD-{user.id}",
            'nom': user.username,
            'prenom': ''
        }
    )
    return student

@login_required
def student_profile(request):
    student = get_or_create_student(request.user)

    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect('students:profile')
    else:
        form = StudentProfileForm(instance=student)

    return render(request, 'students/profile.html', {'form': form})
