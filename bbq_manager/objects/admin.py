from django.contrib import admin

from .models import Company, Department, Object


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Company._meta.fields]


@admin.register(Object)
class ObjectAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Object._meta.fields]


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Department._meta.fields]
