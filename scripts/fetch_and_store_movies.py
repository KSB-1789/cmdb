import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import json
import time
import requests
from bs4 import BeautifulSoup
from models import db, Movie
from app import app



def get_safe_filename(filename):
    return filename.replace(":", "_")

def fetch_top_50_movies():
    url = "https://www.imdb.com/chart/top/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    movies = []
    movie_list = soup.find('ul', {'class': 'ipc-metadata-list'})
    items = movie_list.find_all('li', {'class': 'ipc-metadata-list-summary-item'})[:50]

    for item in items:
        # Extract basic info from chart
        title_element = item.find('h3', {'class': 'ipc-title__text'})
        title = title_element.text.split('. ')[1]
        year = item.find('span', {'class': 'cli-title-metadata-item'}).text
        rating = item.find('span', {'class': 'ipc-rating-star'}).text.split()[0]
        
        # Get movie page URL
        movie_path = title_element.find_parent('a')['href']
        movie_url = f'https://www.imdb.com{movie_path}'
        
        # Fetch movie page
        time.sleep(1)  # Be polite to IMDb's servers
        movie_response = requests.get(movie_url, headers=headers)
        movie_soup = BeautifulSoup(movie_response.text, 'html.parser')
        
        # Extract JSON-LD data
        scripts = movie_soup.find_all('script', {'type': 'application/ld+json'})
        json_data = None
        for script in scripts:
            try:
                data = json.loads(script.string.strip())
                if data.get('@type') == 'Movie':
                    json_data = data
                    break
            except:
                continue
        
        # Get genre, release date, and description
        genres = json_data.get('genre', []) if json_data else []
        if isinstance(genres, str):
            genres = [genres]
        genre_str = ', '.join(genres) if genres else 'N/A'
        release_date = json_data.get('datePublished', 'N/A') if json_data else 'N/A'
        description = json_data.get('description', 'N/A') if json_data else 'N/A'

        # Generate poster URL
        poster_filename = f'{title.replace(" ", "_").lower()}_poster.jpg'
        safe_poster_filename = get_safe_filename(poster_filename)
        
        print(f"Fetched: {title} | Genre: {genre_str} | Release Date: {release_date} | Description: {description[:50]}...")
        
        movies.append({
            'title': title,
            'year': int(year),
            'rating': float(rating),
            'poster_url': f'images/{safe_poster_filename}',
            'genre': genre_str,
            'release_date': release_date,
            'description': description  # Add description to the movie data
        })

    return movies

def store_movies_in_db(movies):
    with app.app_context():
        try:
            db.drop_all()
            db.create_all()
            print(f"Adding {len(movies)} movies...")
            for movie in movies:
                new_movie = Movie(
                    title=movie['title'],
                    release_year=movie['year'],
                    imdb_rating=movie['rating'],
                    poster_url=movie['poster_url'],
                    genre=movie['genre'],
                    release_date=movie['release_date'],
                    description=movie['description']  # Add description to the database
                )
                db.session.add(new_movie)
            db.session.commit()
            print("Movies successfully added!")
        except Exception as e:
            print(f"Error: {e}")
            db.session.rollback()

if __name__ == "__main__":
    print("Starting scraper...")
    movies = fetch_top_50_movies()
    store_movies_in_db(movies)