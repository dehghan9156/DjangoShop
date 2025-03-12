from django.contrib import admin
from .models import Order,OrderDetail,Basket
from django.contrib.admin import ModelAdmin


class CustomOrder(ModelAdmin):
    search_fields = ("id","profile",)

class CustomOrderDetail(ModelAdmin):
    search_fields = ("id",)

class CustomBasket(ModelAdmin):
    search_fields = ("id","profile","product")



admin.site.register(Order,CustomOrder)
admin.site.register(OrderDetail,CustomOrderDetail)
admin.site.register(Basket,CustomBasket)
