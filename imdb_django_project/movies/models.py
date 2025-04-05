from django.db import models
from django.utils import timezone

class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=80, unique=True, null=False)
    email = models.EmailField(max_length=120, unique=True, null=False)
    password = models.CharField(max_length=120, null=False)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, null=False)
    description = models.TextField(null=True)
    release_year = models.IntegerField(null=False)
    imdb_rating = models.FloatField(null=False)
    poster_url = models.CharField(max_length=200, null=True)
    genre = models.CharField(max_length=100, null=True)
    release_date = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.title

class Review(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField(null=False)
    rating = models.IntegerField(null=False)
    created_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')

    def __str__(self):
        return f"Review by {self.user.username} for {self.movie.title}"

class Watchlist(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlist')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='watchlist_entries')
    added_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"