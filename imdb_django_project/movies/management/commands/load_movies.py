from django.core.management.base import BaseCommand
from django.core.files import File
from movies.models import Movie
import os

class Command(BaseCommand):
    help = 'Load movies with their posters'

    def handle(self, *args, **kwargs):
        movies_data = [
            {
                'title': 'The Godfather',
                'year': 1972,
                'genre': 'Crime, Drama',
                'rating': 9.2,
                'poster': 'the_godfather_poster.jpg'
            },
            {
                'title': 'The Godfather Part II',
                'year': 1974,
                'genre': 'Crime, Drama',
                'rating': 9.0,
                'poster': 'the_godfather_part_ii_poster.jpg'
            },
            {
                'title': 'The Dark Knight',
                'year': 2008,
                'genre': 'Action, Crime, Drama',
                'rating': 9.0,
                'poster': 'the_dark_knight_poster.jpg'
            },
            {
                'title': '12 Angry Men',
                'year': 1957,
                'genre': 'Crime, Drama',
                'rating': 9.0,
                'poster': '12_angry_men_poster.jpg'
            },
            {
                'title': 'Schindler\'s List',
                'year': 1993,
                'genre': 'Biography, Drama, History',
                'rating': 8.9,
                'poster': 'schindler\'s_list_poster.jpg'
            },
            {
                'title': 'The Lord of the Rings: The Return of the King',
                'year': 2003,
                'genre': 'Adventure, Drama, Fantasy',
                'rating': 8.9,
                'poster': 'the_lord_of_the_rings__the_return_of_the_king_poster.jpg'
            },
            {
                'title': 'Pulp Fiction',
                'year': 1994,
                'genre': 'Crime, Drama',
                'rating': 8.9,
                'poster': 'pulp_fiction_poster.jpg'
            },
            {
                'title': 'The Good, the Bad and the Ugly',
                'year': 1966,
                'genre': 'Western',
                'rating': 8.8,
                'poster': 'the_good,_the_bad_and_the_ugly_poster.jpg'
            },
            {
                'title': 'Fight Club',
                'year': 1999,
                'genre': 'Drama',
                'rating': 8.8,
                'poster': 'fight_club_poster.jpg'
            },
            {
                'title': 'Forrest Gump',
                'year': 1994,
                'genre': 'Drama, Romance',
                'rating': 8.8,
                'poster': 'forrest_gump_poster.jpg'
            },
            {
                'title': 'Inception',
                'year': 2010,
                'genre': 'Action, Adventure, Sci-Fi',
                'rating': 8.8,
                'poster': 'inception_poster.jpg'
            },
            {
                'title': 'The Matrix',
                'year': 1999,
                'genre': 'Action, Sci-Fi',
                'rating': 8.7,
                'poster': 'the_matrix_poster.jpg'
            },
            {
                'title': 'Goodfellas',
                'year': 1990,
                'genre': 'Biography, Crime, Drama',
                'rating': 8.7,
                'poster': 'goodfellas_poster.jpg'
            },
            {
                'title': 'One Flew Over the Cuckoo\'s Nest',
                'year': 1975,
                'genre': 'Drama',
                'rating': 8.7,
                'poster': 'one_flew_over_the_cuckoo\'s_nest_poster.jpg'
            },
            {
                'title': 'Seven Samurai',
                'year': 1954,
                'genre': 'Action, Drama',
                'rating': 8.6,
                'poster': 'seven_samurai_poster.jpg'
            },
            {
                'title': 'City of God',
                'year': 2002,
                'genre': 'Crime, Drama',
                'rating': 8.6,
                'poster': 'city_of_god_poster.jpg'
            },
            {
                'title': 'Se7en',
                'year': 1995,
                'genre': 'Crime, Drama, Mystery',
                'rating': 8.6,
                'poster': 'se7en_poster.jpg'
            },
            {
                'title': 'The Silence of the Lambs',
                'year': 1991,
                'genre': 'Crime, Drama, Thriller',
                'rating': 8.6,
                'poster': 'the_silence_of_the_lambs_poster.jpg'
            },
            {
                'title': 'It\'s a Wonderful Life',
                'year': 1946,
                'genre': 'Drama, Family, Fantasy',
                'rating': 8.6,
                'poster': 'it\'s_a_wonderful_life_poster.jpg'
            },
            {
                'title': 'Saving Private Ryan',
                'year': 1998,
                'genre': 'Drama, War',
                'rating': 8.6,
                'poster': 'saving_private_ryan_poster.jpg'
            },
            {
                'title': 'Interstellar',
                'year': 2014,
                'genre': 'Adventure, Drama, Sci-Fi',
                'rating': 8.6,
                'poster': 'interstellar_poster.jpg'
            },
            {
                'title': 'The Lord of the Rings: The Fellowship of the Ring',
                'year': 2001,
                'genre': 'Adventure, Drama, Fantasy',
                'rating': 8.8,
                'poster': 'the_lord_of_the_rings__the_fellowship_of_the_ring_poster.jpg'
            },
            {
                'title': 'The Lord of the Rings: The Two Towers',
                'year': 2002,
                'genre': 'Adventure, Drama, Fantasy',
                'rating': 8.7,
                'poster': 'the_lord_of_the_rings__the_two_towers_poster.jpg'
            },
            {
                'title': 'Star Wars: Episode V - The Empire Strikes Back',
                'year': 1980,
                'genre': 'Action, Adventure, Fantasy',
                'rating': 8.7,
                'poster': 'star_wars__episode_v_-_the_empire_strikes_back_poster.jpg'
            },
            {
                'title': 'The Shawshank Redemption',
                'year': 1994,
                'genre': 'Drama',
                'rating': 9.3,
                'poster': 'the_shawshank_redemption_poster.jpg'
            }
        ]

        for movie_data in movies_data:
            movie, created = Movie.objects.get_or_create(
                title=movie_data['title'],
                defaults={
                    'year': movie_data['year'],
                    'genre': movie_data['genre'],
                    'rating': movie_data['rating']
                }
            )

            if created and movie_data['poster']:
                poster_path = os.path.join('static', 'images', movie_data['poster'])
                if os.path.exists(poster_path):
                    with open(poster_path, 'rb') as f:
                        movie.poster.save(movie_data['poster'], File(f), save=True)
                    self.stdout.write(self.style.SUCCESS(f'Added movie: {movie.title} with poster'))
                else:
                    self.stdout.write(self.style.WARNING(f'Poster not found for {movie.title}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Movie already exists: {movie.title}')) 