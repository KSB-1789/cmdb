from django.core.management.base import BaseCommand
from movies.models import Movie

class Command(BaseCommand):
    help = 'Load initial movies into the database'

    def handle(self, *args, **kwargs):
        initial_movies = [
            {
                'title': 'The Godfather',
                'year': 1972,
                'genre': 'Crime, Drama',
                'rating': 9.2,
            },
            {
                'title': 'The Godfather Part II',
                'year': 1974,
                'genre': 'Crime, Drama',
                'rating': 9.0,
            },
            {
                'title': '12 Angry Men',
                'year': 1957,
                'genre': 'Crime, Drama',
                'rating': 9.0,
            },
            {
                'title': 'Pulp Fiction',
                'year': 1994,
                'genre': 'Crime, Drama',
                'rating': 8.9,
            },
            {
                'title': 'City of God',
                'year': 2002,
                'genre': 'Crime, Drama',
                'rating': 8.6,
            },
        ]

        for movie_data in initial_movies:
            Movie.objects.get_or_create(
                title=movie_data['title'],
                defaults={
                    'year': movie_data['year'],
                    'genre': movie_data['genre'],
                    'rating': movie_data['rating'],
                }
            )
            self.stdout.write(f"Added movie: {movie_data['title']}") 