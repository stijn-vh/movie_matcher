
from controllers.movie_controller import MovieController
from controllers.user_recommendation_controller import UserRecommendationController


class GroupRecommendationController():
    def __init__(self, dbc, gc):
        self.dbc = dbc
        self.mc = MovieController(dbc)
        self.gc = gc
        self.random_sample_size = 6
        self.urc = UserRecommendationController()

    def add_movies_to_stack(self, movie_ids, stack):
        for mid in movie_ids:
            if mid not in stack.keys():
                stack[mid] = {}
        return stack
    
    # Check stack for user rating updates
    # Remove from stack if all users interacted with movie
    def refresh_stack(self, group_object):
        user_count = len(group_object['users'])

        ids_to_rem = []
        for id, movie in group_object['stack'].items():
            ratings = [rating for key, rating in movie.items() if key != 'weight']
            weight = sum(rating == 1 for rating in ratings) / user_count

            if len(ratings) >= user_count:
                # Movie is rated by all users, move to history
                group_object['history'][id] = movie
                ids_to_rem.append(id)
            else:
                group_object['stack'][id]['weight'] = weight

        for id in ids_to_rem:
            del group_object['stack'][id]

    def retrieve_positive_interacted_movies(self, group_object):
        positive_movie_ids = []

        positive_movie_ids.extend(mid for mid, movie_data in group_object['stack'].items() 
            if movie_data.get('weight', 0) > 0)
        
        positive_movie_ids.extend(mid for mid, movie_data in group_object['history'].items() 
            if movie_data.get('weight', 0) > 0)
        return positive_movie_ids


    def generate_movies_for_stack(self, group_object):
        all_movies = self.dbc.get_movies_df()  
        idxs = list()

        random_ids = all_movies['ID'].sample(self.random_sample_size).tolist()

        if group_object['stack'] != {}:
            positive_movie_ids = self.retrieve_positive_interacted_movies(group_object)

            if len(positive_movie_ids) > 0:
                idxs = self.urc.determine_cosine_sim_all_movies(positive_movie_ids, all_movies)
        
        rec_movies = all_movies[all_movies['ID'].isin(idxs + random_ids)]
        #rec_movies = rec_movies[~rec_movies['ID'].isin(group_object['stack'])] # ! Should be on keys

        return rec_movies

    def add_batch_to_stack(self, gid):
        group_object, group_ref = self.dbc.get_group(gid)
        
        self.refresh_stack(group_object)

        rec_movies = self.generate_movies_for_stack(group_object)

        group_object['stack'] = self.add_movies_to_stack(rec_movies['ID'].to_list(), group_object['stack'])
        group_ref.set(group_object)

        return rec_movies
    
    def get_movies_from_stack(self, gid, uid):
        group_object, group_ref = self.dbc.get_group(gid)

        personal_stack = {}
        for id, movie in group_object['stack'].items():
            if uid not in movie.keys():
                personal_stack[id] = movie

        movies = self.dbc.get_movies_df(idxs = list(personal_stack.keys()))

        # Could check if personal_stack is large enough, else fill with random
        return movies