from django.db import models
from django.utils import timezone

class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    release_year = models.IntegerField()
    imdb_rating = models.FloatField()
    poster_url = models.CharField(max_length=200, blank=True, null=True)
    genre = models.CharField(max_length=100, blank=True, null=True)
    release_date = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f'<Movie {self.title}>'

class Review(models.Model):
    content = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey('profiles.User', on_delete=models.CASCADE, related_name='reviews')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews_set')

class Watchlist(models.Model):    
    user = models.ForeignKey('profiles.User', on_delete=models.CASCADE, related_name='watchlist')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='watchlist_entries_set')
    added_at = models.DateTimeField(default=timezone.now)