import sqlite3
import json
import re
import statistics


conn = sqlite3.connect('mm_api/movies.db')
c = conn.cursor()

c.execute('SELECT ID, Awards FROM Movie')

movies = c.fetchall()

for movie in movies:
    wins = 0
    nominations = 0

    awards = movie[1]

    if awards != 'N/A':
        wins_match = re.search(r'(\d+) win', awards)
        if wins_match:
            wins = int(wins_match.group(1))

        nominations_match = re.search(r'(\d+) nomination', awards)
        if nominations_match:
            nominations = int(nominations_match.group(1))

    c.execute('UPDATE Movie SET AwardWins = ?, AwardNominations = ? WHERE ID = ?', (wins, nominations, movie[0]))
    
conn.commit()


# c.execute('SELECT ID, RatingIMD, RatingRT, RatingMc FROM Movie')
# movies = c.fetchall()

# names = ['x', 'RatingIMD', 'RatingRT', 'RatingMc']

# for movie in movies:
#     none_indexes = [i for i, value in enumerate(movie) if value is None]

#     values = [value for value in movie[1:] if value is not None]

#     if len(values) == 0:
#         continue

#     average = int(statistics.mean(values))

#     for none_i in none_indexes:
#         c.execute('UPDATE Movie SET ' + names[none_i] + ' = ? WHERE ID = ?', (average, movie[0]))

# conn.commit()

# for movie in movies:
#     rating = movie[1]

#     if rating == '[]':
#         continue

#     ratings = json.loads(rating.replace("'", "\""))

#     for rating in ratings:
#         if rating['Source'] == 'Internet Movie Database':
#             number = int(float(rating['Value'][:-3]) * 10)
#             c.execute('UPDATE Movie SET RatingIMD = ? WHERE ID = ?', (number, movie[0]))

#         elif rating['Source'] == 'Rotten Tomatoes':
#             number = int(rating['Value'][:-1])
#             c.execute('UPDATE Movie SET RatingRT = ? WHERE ID = ?', (number, movie[0]))

#         elif rating['Source'] == 'Metacritic':
#             number = int(rating['Value'][:-4])
#             c.execute('UPDATE Movie SET RatingMc = ? WHERE ID = ?', (number, movie[0]))

# conn.commit()
