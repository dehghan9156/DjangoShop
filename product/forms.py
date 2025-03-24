from django.forms.models import ModelForm
from django import forms
from .models import Product

class ProductCreateUpdateForm(forms.ModelForm):
    class Meta:
        model= Product
        fields = ["category","name","description","price","stock","image"]
        widgets = {
            'category': forms.Select(attrs={
                'class': 'form-control',
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            })
        }