from django.contrib import admin

from .models import Procedure


@admin.register(Procedure)
class ProcedureAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
