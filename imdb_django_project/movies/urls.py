from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.index, name='index'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('register/', views.register, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('add/', views.add_movie, name='add_movie'),
    path('watchlist/', views.watchlist, name='watchlist'),
    path('my_ratings/', views.my_ratings, name='my_ratings'),
    path('logout/', views.logout_view, name='logout'),
    path('movie/<int:movie_id>/add_to_watchlist/', views.add_to_watchlist, name='add_to_watchlist'),
    path('review/<int:review_id>/edit/', views.edit_review, name='edit_review'),
    path('review/<int:review_id>/delete/', views.delete_review, name='delete_review'),
    path('movie/<int:movie_id>/delete/', views.delete_movie, name='delete_movie'),
]