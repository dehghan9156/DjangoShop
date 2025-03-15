from django import forms
from .models import Basket

class EdithBasketForm(forms.ModelForm):
    class Meta:
        model = Basket
        fields = ["quantity"]
        widgets = {
            'quantity': forms.NumberInput(attrs={'min': 1, 'class': 'form-control', 'style': 'max-width: 80px;'}),        }