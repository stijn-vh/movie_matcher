from datetime import datetime
from flask import request

from controllers.utils import Utils
from controllers.user_recommendation_controller import UserRecommendationController

class MovieController:
    def __init__(self, dbc):
        self.dbc = dbc
        self.urc = UserRecommendationController()
        self.utils = Utils()
        pass
    
    def get_user_liked_movies(self, uid):
        liked_movies = []
        user_data, user_ref = self.dbc.get_user_profile(uid)
        user_movies = user_data.get('movies', {})

        for id, rating in user_movies.items():
            if rating['opinion'] == 1:
                liked_movies.append(id)

        all_movies = self.dbc.get_movies_df()

        if len(liked_movies) > 0:
            idxs = self.urc.determine_cosine_sim_all_movies(liked_movies, all_movies)
            random_sample_size = int(len(idxs) * 0.5)
        else:
            idxs = []
            random_sample_size = 10

        random_ids = all_movies['ID'].sample(random_sample_size).tolist()

        df = self.dbc.get_movies_df(idxs + random_ids)

        return {'movies': df.to_dict(orient='records')}, 200

    def rate_movie(self, uid):      
        data = request.get_json()
        movie_id = data.get('movie')
        opinion = data.get('opinion')

        if not uid or not movie_id or opinion is None:
            return {'error': 'Missing attribute'}, 400
        
        user_data, user_ref = self.dbc.get_user_profile(uid)

        if not user_data:
            return {'error': 'User not found'}, 404
        
        user_movies = user_data.get('movies', {})
        user_movies[str(movie_id)] = {
            'timestamp': datetime.now().isoformat(),
            'opinion': opinion
        }

        user_ref.update({'movies': user_movies})

        return {'message': 'Movie rated successfully'}, 200