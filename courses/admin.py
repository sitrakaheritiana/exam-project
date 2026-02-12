from django.contrib import admin

from .models import Course


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("titre", "formation", "enseignant")
    search_fields = ("titre", "formation__code", "formation__libelle", "enseignant__nom")
    list_filter = ("formation", "enseignant")
