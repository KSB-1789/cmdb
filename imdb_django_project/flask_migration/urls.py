from django.urls import path
from . import views

app_name = 'flask_migration'

urlpatterns = [
    path('search/', views.search_movies, name='search_movies'),
] 