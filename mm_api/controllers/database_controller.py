import sqlite3
from flask import Flask, app, g, json


import firebase_admin
from firebase_admin import credentials, firestore
from pandas import DataFrame

class DatabaseController:
    def __init__(self):
        cred = credentials.Certificate("./env/firebase.json")
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()

        self.path_to_movie_json = 'movies.json'

    def get_db(self):
        return self.db
    
    def get_movies_json(self):
        with open(self.path_to_movie_json, 'r', encoding='utf-8') as f:
            movies = json.load(f)
        return movies
    
    def get_movies_df(self, idxs = None):
        json_movies = self.get_movies_json()

        if idxs == None:
            return DataFrame(json_movies)
        else:
            df = DataFrame(json_movies)

            return df[df['ID'].isin(idxs)]
        
    def get_user_profile(self, user_id):
        user_ref = self.db.collection('users').document(str(user_id))
        user_dict = user_ref.get().to_dict()

        if not user_dict:
            user_dict = {'Name': 'test', 'movies': {}}
            user_ref.set(user_dict)

        return user_dict, user_ref

    def create_group(self, group):
        # TODO: Do some validation
        return self.db.collection('groups').add(group)
    
    def get_group(self, gid):
        group_ref = self.db.collection('groups').document(str(gid))
        group_dict = group_ref.get().to_dict()

        return group_dict, group_ref
    
    def get_groups(self):
        groups_ref = self.db.collection('groups')
        groups_docs = groups_ref.get()

        groups_dict = [
            {**doc.to_dict(), 'id': doc.id} 
            for doc in groups_docs
        ]

        return groups_dict, groups_ref

    def store_movies_in_json(self):
        movies_ref = self.db.collection('movies')

        movies = [movie.to_dict() for movie in movies_ref.get()]

        with open(self.path_to_movie_json, 'w', encoding='utf-8') as f:
            json.dump(movies, f)

        print('Exported FireBase movies to movies.json')

