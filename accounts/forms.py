from django import forms
from django.contrib.auth.password_validation import password_validators_help_text_html
from django.forms.models import ModelForm
from .models import User
from django.core.exceptions import ValidationError


class LoginUserForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))

class RegisterUserForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data['password']
        p2 = cleaned_data['confirm_password']
        if p1 and p2:
            if p1 != p2:
                raise ValidationError("password and confirm password not math")
        return cleaned_data