from django.contrib import admin

from users.models import User


@admin.register(User)
class PurchaseAdmin(admin.ModelAdmin):
    pass
