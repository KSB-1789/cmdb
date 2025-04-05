from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.index, name='index'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('register/', views.register, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('add_movie/', views.add_movie, name='add_movie'),
    path('logout/', views.logout_view, name='logout'),
    path('my_ratings/', views.my_ratings, name='my_ratings'),
    path('watchlist/', views.watchlist, name='watchlist'),
]