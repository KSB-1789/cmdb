from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm

def index(request):
    return render(request, 'profiles/index.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('movies:index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'profiles/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'profiles/profile.html')
