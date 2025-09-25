import json
import requests
import sqlite3
import time
import re

conn = sqlite3.connect('mm_api/movies.db')
c = conn.cursor()

def extract_movie(movie_data):
    movie_id = movie_data.get('imdbID')
    title = movie_data.get('Title')
    plot = movie_data.get('Plot')
    genre = movie_data.get('Genre')
    release_year = movie_data.get('Year')
    runtime = movie_data.get('Runtime')
    pop = movie_data.get('imdbRating')
    awards = movie_data.get('Awards')
    box_office = movie_data.get('BoxOffice')
    directors = movie_data.get('Director')
    actors = movie_data.get('Actors')
    poster = movie_data.get('Poster')

    wins_match = re.search(r'(\d+) win', awards)
    if wins_match:
        wins = int(wins_match.group(1))

    nominations_match = re.search(r'(\d+) nomination', awards)
    if nominations_match:
        nominations = int(nominations_match.group(1))

    # Handle ratings - check if it's already a list or needs parsing
    ratings_data = movie_data.get('Ratings')
    if isinstance(ratings_data, str):
        ratings = json.loads(ratings_data.replace("'", "\""))
    elif isinstance(ratings_data, list):
        ratings = ratings_data
    else:
        ratings = []

    for rating in ratings:
        if rating['Source'] == 'Internet Movie Database':
            ratingIMD = int(float(rating['Value'][:-3]) * 10)
        elif rating['Source'] == 'Rotten Tomatoes':
            ratingRT = int(rating['Value'][:-1])
        elif rating['Source'] == 'Metacritic':
            ratingMC = int(rating['Value'][:-4])

    c.execute('INSERT INTO Movie (ID, Name, Description, ReleaseYear, RunTime, Popularity, Awards, BoxOffice, AwardWins, AwardNominations, RatingIMD, RatingRT, RatingMc, Poster) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
              (movie_id, title, plot, release_year, runtime, pop, awards, box_office, wins, nominations, ratingIMD, ratingRT, ratingMC, poster))
    
    movie_id = c.lastrowid
    
    genres = genre.split(', ')
    for genre in genres:
        c.execute('INSERT INTO MovieGenre (MovieID, Genre) VALUES (?, ?)', (movie_id, genre))

    directors = directors.split(', ')
    for director in directors:
        c.execute('INSERT INTO MovieDirector (MovieID, DirectorName) VALUES (?, ?)', (movie_id, director))

    actors = actors.split(', ')
    for actor in actors:
        c.execute('INSERT INTO MovieActor (MovieID, ActorName) VALUES (?, ?)', (movie_id, actor))

    conn.commit()

def get_movies(movie_names):
    for name in movie_names:
        try:
            response = requests.get(f'http://www.omdbapi.com/?apikey=c1c322d6&t={name}&plot=full')
            movie_data = response.json()
            
            if (movie_data.get('Response') == 'False'):
                print(f'Failed to get data for {name}')
                continue
            else:
                extract_movie(movie_data)
        except Exception as e:
            print(f'An error occurred: {e}')
        finally:
            print(f'Successfully added {name} to the database')

def replace_ids():
    # Fetch all movies from the Movie table
    c.execute('SELECT ID, name FROM Movie')
    movies = c.fetchall()

    for movie in movies:
        movie_id, name = movie
        try:
            # Make an API call to fetch the imdbID
            response = requests.get(f'http://www.omdbapi.com/?apikey=c1c322d6&t={name}&plot=full')
            movie_data = response.json()
            
            if movie_data.get('Response') == 'False':
                print(f'Failed to get data for {name}')
                continue

            # Update the ID field in the Movie table with the fetched imdbID
            pop = movie_data.get('imdbVotes')
            if pop is not None:
                c.execute('UPDATE Movie SET Popularity = ? WHERE Name = ?', (pop, name))
                conn.commit()
                print(f'Successfully updated {name} with imdb popularity {pop}')
            else:
                print(f'No imdb id found for {name}')

        except Exception as e:
            print(f'An error occurred: {e}')



def is_valid_integer(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def update_posters():
    # Ensure the Poster column exists in the Movie table
    c.execute("PRAGMA table_info(Movie)")
    columns = [col[1] for col in c.fetchall()]
    if 'Poster' not in columns:
        c.execute("ALTER TABLE Movie ADD COLUMN Poster TEXT")
        conn.commit()

    c.execute('SELECT ID, Name FROM Movie')
    movies = c.fetchall()
    for movie_id, name in movies:
        try:
            response = requests.get(f'http://www.omdbapi.com/?apikey=c1c322d6&t={name}&plot=full')
            movie_data = response.json()
            if movie_data.get('Response') == 'False':
                print(f'Failed to get data for {name}')
                continue
            poster_url = movie_data.get('Poster')
            if poster_url and poster_url != 'N/A':
                c.execute('UPDATE Movie SET Poster = ? WHERE ID = ?', (poster_url, movie_id))
                conn.commit()
            else:
                print(f'No poster found for {name}')
        except Exception as e:
            print(f'Error updating poster for {name}: {e}')

update_posters()