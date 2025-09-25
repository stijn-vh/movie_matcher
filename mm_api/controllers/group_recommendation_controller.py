
class GroupRecommendationController():
    def __init__(self, dbc, mc, gc):
        self.dbc = dbc
        self.mc = mc
        self.gc = gc
        self.random_sample_size = 6
        
    def add_batch_to_stack(self, gip):
        group_object, group_ref = self.dc.get_group(gip)
        all_movies = self.dbc.get_movies_df()

        ghistory = group_object['history']
        user_count = len(group_object['users'])
        
        history_count = {}
        for movie in ghistory:
            weight = sum(rating == 1 for rating in movie.values()) / user_count

            if weight == 0 and len(movie.values()) >= user_count:
                del all_movies[movie]
            else:
                history_count[movie] = weight

        idxs = self.urc.determine_cosine_sim_all_movies(history_count.keys(), all_movies)
        random_ids = all_movies['ID'].sample(self.random_sample_size).tolist()

        rec_movies = all_movies[all_movies['ID'].isin(idxs + random_ids)]
        rec_movies = all_movies[~all_movies['ID'].isin(ghistory.keys())]
        rec_movies = all_movies[~all_movies['ID'].isin(group_object['stack'])] # ! Should be on keys

        group_object['stack'].append(rec_movies['ID'])
        group_ref.set(group_object)

        return {'movies': rec_movies.to_dict(orient='records')}, 200