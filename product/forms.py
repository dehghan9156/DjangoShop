from django.forms.models import ModelForm
from django import forms
from .models import Product

class ProductCreateUpdateForm(forms.ModelForm):
    class Meta:
        model= Product
        fields = ["category","name","description","price","stock","image"]
