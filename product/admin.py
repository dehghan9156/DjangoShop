from django.contrib import admin
from .models import Product,Category
from django.contrib.admin import ModelAdmin


class CustomProductAdmin(ModelAdmin):
    search_fields = ("id","name",)

admin.site.register(Product,CustomProductAdmin)
admin.site.register(Category)
# Register your models here.
