from django.shortcuts import render, redirect
from profiles.forms import LoginForm, RegisterForm

def index(request):
    return render(request, 'index.html')
