from django.contrib import admin

from inventory.models import Material


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'unit', 'archived')
    list_display_links = ('id', 'name', 'unit', 'archived')
