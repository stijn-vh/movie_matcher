
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity, linear_kernel

class UserRecommendationController():
    def determine_cosine_sim_all_movies(self, liked_movies, movies):
        indices = pd.Series(movies.index, index=movies['ID']).drop_duplicates()

        desc_cos_sim = self.get_description_cosine_similarity(movies)
        meta_cos_sim = self.get_metadata_cosine_similarity(movies)

        cos_sim = self.mix_similarity_cosines([desc_cos_sim, meta_cos_sim])

        recommended_movie_idxs = self.get_sim_movie_recommendations(liked_movies, cos_sim, indices)

        idxs = list(movies['ID'].iloc[recommended_movie_idxs])

        return idxs
    
    def get_sim_movie_recommendations(self, movies, cos_sim, idxs):
        m_idxs = [idxs[movie] if movie in idxs else print(movie + ' not in database') for movie in movies]
        m_idxs = [idx for idx in m_idxs if idx is not None]

        sim_mean_vector = np.mean([cos_sim[idx] for idx in m_idxs], axis = 0)

        similarity_scores = sorted(list(enumerate(sim_mean_vector)), key=lambda x: x[1], reverse=True) #
        top_scores = [i for i in similarity_scores if i[0] not in m_idxs][:11]

        return [i[0] for i in top_scores]
    
    def get_description_cosine_similarity(self, movies):
        tdidf = TfidfVectorizer(stop_words='english')

        tdidf_matrix = tdidf.fit_transform(movies['Description'])

        return linear_kernel(tdidf_matrix, tdidf_matrix)
    
    def get_metadata_cosine_similarity(self, movies):
        features = ['Category20Cluster', 'Category40Cluster', 'genres', 'directors', 'actors']

        for f in features:
            movies[f] = movies[f].apply(self.utils.clean_data)

        movies['f_concat'] = movies.apply(lambda m: self.utils.concat_features(m, features), axis = 1)

        cv = CountVectorizer(stop_words='english')
        count_matrix = cv.fit_transform(movies['f_concat'])

        return cosine_similarity(count_matrix, count_matrix)
    
    def mix_similarity_cosines(self, cos_arrays):
        weight = 1.0 / len(cos_arrays)
        hybrid_sim = np.zeros_like(cos_arrays[0])

        for arr in cos_arrays:
            hybrid_sim += weight * arr

        return hybrid_sim