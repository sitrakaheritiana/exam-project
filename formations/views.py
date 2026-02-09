from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Formation
from .forms import FormationForm

def is_admin(user):
    return user.role == 'ADMIN'

@login_required
@user_passes_test(is_admin)
def formation_list(request):
    formations = Formation.objects.all()
    return render(request, 'formations/list.html', {'formations': formations})

@login_required
@user_passes_test(is_admin)
def formation_create(request):
    if request.method == 'POST':
        form = FormationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('formations:list')
    else:
        form = FormationForm()
    return render(request, 'formations/form.html', {'form': form, 'title': 'Ajouter Formation'})

@login_required
@user_passes_test(is_admin)
def formation_update(request, pk):
    formation = get_object_or_404(Formation, pk=pk)
    if request.method == 'POST':
        form = FormationForm(request.POST, instance=formation)
        if form.is_valid():
            form.save()
            return redirect('formations:list')
    else:
        form = FormationForm(instance=formation)
    return render(request, 'formations/form.html', {'form': form, 'title': 'Modifier Formation'})

@login_required
@user_passes_test(is_admin)
def formation_delete(request, pk):
    formation = get_object_or_404(Formation, pk=pk)
    if request.method == 'POST':
        formation.delete()
        return redirect('formations:list')
    return render(request, 'formations/confirm_delete.html', {'formation': formation})
