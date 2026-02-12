from django.contrib import admin

from .models import Teacher


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("nom", "prenom", "specialite", "user")
    search_fields = ("nom", "prenom", "specialite", "user__username", "user__email")
