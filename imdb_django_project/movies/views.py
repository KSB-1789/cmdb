from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.urls import reverse
from .forms import LoginForm, RegisterForm

def login_view(request):
    if request.user.is_authenticated:
        return redirect(reverse('movies:index'))

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            email = form.cleaned_data.get('email')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, 'Login successful!')
                return redirect(reverse('movies:index'))
            else:
                messages.error(request, 'Invalid email or password')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = LoginForm()

    return render(request, 'movies/login.html', {'form': form, 'next_page': request.GET.get('next')})

def register_view(request):
    if request.user.is_authenticated:
        return redirect(reverse('movies:index'))

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            User = get_user_model()
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists.")
                return render(request, 'movies/register.html', {'form': form})

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
            )

            auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, 'Registration successful!')
            return redirect(reverse('movies:index'))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = RegisterForm()

    return render(request, 'movies/register.html', {'form': form})

def logout_view(request):
    auth_logout(request)
    messages.success(request, 'Logged out successfully!')
    next_page = request.GET.get('next', reverse('movies:index'))
    return redirect(next_page)

def index_view(request):
    return render(request, 'movies/index.html')
