from django.contrib import admin

from employees.models import Employee, MasterProcedure


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'position', 'coefficient')
    list_display_links = ('id', 'first_name', 'last_name', 'position', 'coefficient')


@admin.register(MasterProcedure)
class MasterProcedureAdmin(admin.ModelAdmin):
    list_display = ('id', 'procedure', 'employee', 'price', 'coefficient', 'archived')
    list_display_links = ('id', 'procedure', 'employee', 'price', 'coefficient', 'archived')
