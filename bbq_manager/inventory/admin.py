from django.contrib import admin

from inventory.models import Material, ProductMaterial, Stock


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'unit', 'archived')
    list_display_links = ('id', 'name', 'unit', 'archived')


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('id', 'price', 'material', 'amount')
    list_display_links = ('id', 'price', 'material', 'amount')


@admin.register(ProductMaterial)
class ProductMaterialAdmin(admin.ModelAdmin):
    list_display = ('id', 'material', 'price', 'archived')
    list_display_links = ('id', 'material', 'price', 'archived')
