from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

app_name = 'profiles'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', LoginView.as_view(template_name='profiles/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='movies:index'), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
]