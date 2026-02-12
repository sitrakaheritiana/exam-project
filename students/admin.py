from django.contrib import admin

from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("matricule", "nom", "prenom", "formation", "user")
    search_fields = ("matricule", "nom", "prenom", "user__username", "user__email")
    list_filter = ("formation",)
