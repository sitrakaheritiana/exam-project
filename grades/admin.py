from django.contrib import admin

from .models import Grade


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ("etudiant", "course", "valeur")
    search_fields = ("etudiant__nom", "etudiant__prenom", "course__titre")
    list_filter = ("course__formation", "course")
