from django.forms.models import ModelForm
from django import forms
from .models import Product

class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model= Product
        fields = ["name","image","description","price","stock"]