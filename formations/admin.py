from django.contrib import admin

from .models import Formation


@admin.register(Formation)
class FormationAdmin(admin.ModelAdmin):
    list_display = ("code", "libelle", "active")
    search_fields = ("code", "libelle")
    list_filter = ("active",)
    filter_horizontal = ("enseignants",)
