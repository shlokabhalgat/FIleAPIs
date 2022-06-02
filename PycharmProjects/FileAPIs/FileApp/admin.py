from django.contrib import admin
from FileApp.models import File


class FileAdmin(admin.ModelAdmin):
    list_display = ["id", "staff_name", "position", "age", "year_joined"]


admin.site.register(File, FileAdmin)
