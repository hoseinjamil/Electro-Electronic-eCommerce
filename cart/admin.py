from django.contrib import admin
from . import models


class orderadmin(admin.TabularInline):
    model = models.Orderitem


@admin.register(models.Order)
class orderadmin(admin.ModelAdmin):
    list_display = ('user', 'is_paid')
    inlines = (orderadmin,)
    list_filter = ('is_paid',)


@admin.register(models.DiscountCode)
class DiscountCodeadmin(admin.ModelAdmin):
    list_display = ('name', 'discount', 'quantity')