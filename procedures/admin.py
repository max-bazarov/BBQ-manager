from django.contrib import admin

from .models import Procedure


@admin.register(Procedure)
class ProcedureAdmin(admin.ModelAdmin):
    pass
