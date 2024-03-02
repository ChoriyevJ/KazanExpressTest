from django.contrib import admin
# from django.apps import apps

from store import models


class PhotoInline(admin.TabularInline):
    model = models.Photo
    extra = 0


@admin.register(models.Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('title', 'image')
    search_fields = ('title', 'uuid')


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title', 'uuid')


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'amount', 'price', 'main_photo', 'active', 'shop')
    list_filter = ('active', 'shop', 'categories')
    list_editable = ('amount', 'price', 'active')
    raw_id_fields = ('shop', 'categories')
    autocomplete_fields = ('shop',)
    search_fields = ('title', 'uuid')
    inlines = (PhotoInline,)
