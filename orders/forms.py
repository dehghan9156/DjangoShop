from django import forms
from .models import Factor

class EdithFactorForm(forms.ModelForm):
    class Meta:
        model = Factor
        fields = ["quantity"]
        widgets = {
            'quantity': forms.NumberInput(attrs={'min': 1, 'class': 'form-control', 'style': 'max-width: 80px;'}),        }