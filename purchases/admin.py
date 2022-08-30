from django.contrib import admin

from purchases.models import Purchase, PurchaseProcedure, UsedMaterial


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'time', 'is_paid_by_card')
    list_display_links = ('id', 'time', 'is_paid_by_card')


@admin.register(PurchaseProcedure)
class PurchaseProcedureAdmin(admin.ModelAdmin):
    list_display = ('id', 'purchase', 'procedure')
    list_display_links = ('id', 'purchase', 'procedure')


@admin.register(UsedMaterial)
class UsedMaterialAdmin(admin.ModelAdmin):
    list_display = ('id', 'procedure', 'material', 'amount')
    list_display_links = ('id', 'procedure', 'material', 'amount')
