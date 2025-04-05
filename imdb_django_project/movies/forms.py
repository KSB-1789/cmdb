from django import forms
from django.core.exceptions import ValidationError

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=120, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', max_length=120, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class RegisterForm(forms.Form):
    username = forms.CharField(label='Username', max_length=80, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', max_length=120, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', max_length=120, widget=forms.PasswordInput(attrs={'class': 'form-control'}))