import itertools
import sqlite3
from mm_api.database_controller import DatabaseController
import re 
import json
import requests

class MovieController:
    def __init__(self) -> None:
        self.dc = DatabaseController()

    def extract_awards(self, movie_data):
        awards = movie_data.get('Awards')

        wins_match = re.search(r'(\d+) win', awards)
        if wins_match:
            wins = int(wins_match.group(1))

        nominations_match = re.search(r'(\d+) nomination', awards)
        if nominations_match:
            nominations = int(nominations_match.group(1))

        return wins, nominations
    
    def extract_ratings(self, movie_data):
        ratings = json.loads(movie_data.get('Ratings').replace("'", "\""))
        ratingIMD, ratingRT, ratingMC = None, None, None

        for rating in ratings:
            if rating['Source'] == 'Internet Movie Database':
                ratingIMD = int(float(rating['Value'][:-3]) * 10)
            elif rating['Source'] == 'Rotten Tomatoes':
                ratingRT = int(rating['Value'][:-1])
            elif rating['Source'] == 'Metacritic':
                ratingMC = int(rating['Value'][:-4])
        
        return ratingIMD, ratingRT, ratingMC
    
    def add_new_movie(self, name):
        response = requests.get(f'http://www.omdbapi.com/?apikey=c1c322d6&t={name}&plot=full')
        movie_data = response.json()

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

        wins, nominations = self.extract_awards(movie_data)
        ratingIMD, ratingRT, ratingMC = self.extract_ratings(movie_data)

        self.dc.write(['INSERT INTO Movie (ID, Name, Description, ReleaseYear, RunTime, Popularity, Awards, BoxOffice, AwardWins, AwardNominations, RatingIMD, RatingRT, RatingMc)  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (movie_id, title, plot, release_year, runtime, pop, awards, box_office, wins, nominations, ratingIMD, ratingRT, ratingMC)], False)
    
        queries = []

        genres = genre.split(', ')
        for genre in genres:
            queries.append(['INSERT INTO MovieGenre (MovieID, Genre) VALUES (?, ?)', (movie_id, genre)])

        directors = directors.split(', ')
        for director in directors:
            queries.append(['INSERT INTO MovieDirector (MovieID, DirectorName) VALUES (?, ?)', (movie_id, director)])

        actors = actors.split(', ')
        for actor in actors:
            queries.append(['INSERT INTO MovieActor (MovieID, ActorName) VALUES (?, ?)', (movie_id, actor)])

        self.dc.write(queries)

    def get_relation_rows(cursor, table, column_to_select, rowid):
        cursor.execute(f'SELECT {column_to_select} FROM {table} WHERE MovieID = ?', (rowid,))

        return list(itertools.chain.from_iterable(cursor.fetchall()))


    def transfer_movies(self):
        conn = sqlite3.connect('movies.db')
        cursor = conn.cursor()
        cursor.execute('SELECT rowid, * FROM Movie')
        movies = cursor.fetchall()

        db = None # Replace

        mcolumns = ['rowid'] + [mc[1] for mc in cursor.execute('PRAGMA table_info(Movie)').fetchall()]

        BATCH_SIZE = 500
        batch = db.batch()
        count = 0

        for i, m in enumerate(movies):
            doc_id = str(m[1])
            movie_ref = db.collection('movies').document(doc_id)

            movie = {mcolumns[j]: m[j] for j in range(len(mcolumns))}

            movie['actors'] = self.get_relation_rows(cursor, 'MovieActor', 'ActorName', movie['rowid'])
            movie['directors'] = self.get_relation_rows(cursor, 'MovieDirector', 'DirectorName', movie['rowid'])
            movie['genres'] = self.get_relation_rows(cursor, 'MovieGenre', 'Genre', movie['rowid'])

            batch.set(movie_ref, movie)
            if count == 499:
                batch.commit()
                print(f'Batch {i // BATCH_SIZE + 1} committed.')
                batch = db.batch()
                count = 0

            count += 1

        batch.commit()
        conn.close()
        print('Final batch committed.')
        
        return {'status': 'Transfer complete'}

