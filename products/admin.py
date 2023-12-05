from django.contrib import admin
from . import models


class InformationAdmin(admin.StackedInline):
    model = models.Information


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price')
    inlines = (InformationAdmin,)


@admin.register(models.Category)
class CategroyAdmin(admin.ModelAdmin):
    list_display = ('parent', 'title', 'image', 'slug')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('products', 'user', 'active', 'body', 'created_at')


admin.site.register(models.Size)
admin.site.register(models.Color)
admin.site.register(models.Brand)
