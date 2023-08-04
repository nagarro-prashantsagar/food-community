# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

# class CustomUserLoginForm(forms.Form):
#     email = forms.EmailField()
#     password = forms.CharField(widget=forms.PasswordInput)
#

class AdminLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = '__all__'


class AdminLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
