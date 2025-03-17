from django.contrib import admin
from .models import HeaderFactor,Factor
from django.contrib.admin import ModelAdmin


class CustomHeaderFactor(ModelAdmin):
    search_fields = ("id","profile",)

class CustomFactor(ModelAdmin):
    search_fields = ("id",)

admin.site.register(HeaderFactor,CustomHeaderFactor)
admin.site.register(Factor,CustomFactor)
