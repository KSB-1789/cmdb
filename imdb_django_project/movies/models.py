from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Movie(models.Model):
    title = models.CharField(max_length=200)
    year = models.IntegerField(default=2024)
    genre = models.CharField(max_length=100, default='Drama')
    rating = models.FloatField(default=0.0, validators=[MinValueValidator(0), MaxValueValidator(10)])
    poster = models.ImageField(upload_to='images/', null=True, blank=True)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='added_movies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0)
    watchlist_users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Watchlist', related_name='watchlist_movies')

    def __str__(self):
        return f"{self.title} ({self.year})"

    def save(self, *args, **kwargs):
        # Update the poster path if it contains 'static/images'
        if self.poster and 'static/images' in self.poster.name:
            self.poster.name = self.poster.name.replace('static/images/', 'images/')
        super().save(*args, **kwargs)

class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s review of {self.movie.title}"

class Watchlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='watchlist_entries')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='watchlist_entries')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'movie')

    def __str__(self):
        return f"{self.user.username}'s watchlist: {self.movie.title}"