from django.core.management.base import BaseCommand
from movies.models import Movie

class Command(BaseCommand):
    help = 'Update poster paths in the database'

    def handle(self, *args, **options):
        movies = Movie.objects.all()
        for movie in movies:
            if movie.poster and 'static/images' in movie.poster.name:
                movie.poster.name = movie.poster.name.replace('static/images/', 'images/')
                movie.save()
                self.stdout.write(self.style.SUCCESS(f'Updated poster path for {movie.title}')) 