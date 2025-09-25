
from mm_api.yard.movie_controller import MovieController


if '__main__' == __name__:
    mc = MovieController()
    mc.refill_movie_db()