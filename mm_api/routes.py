import itertools
from flask import Blueprint, Flask, g, request
from flask_cors import CORS

from controllers.movie_controller import MovieController
from controllers.database_controller import DatabaseController
from controllers.group_controller import GroupController

app = Flask(__name__)
CORS(app)

dbc = DatabaseController()
mc = MovieController(dbc)

user_bp = Blueprint('users', __name__, url_prefix='/users')

@user_bp.route('/<uid>/movies', methods=['GET'])
def get_movies(uid):
    return mc.get_user_liked_movies(uid)

@user_bp.route('/<uid>/rate', methods=['POST', 'OPTIONS'])
def rate_movie(uid):
    return mc.rate_movie(uid)

app.register_blueprint(user_bp)



gc = GroupController(dbc)

@gc.group.route('/create/<uid>', methods=['POST'])
def add_user_to_group(uid):
    return gc.create_group(uid)

@gc.group.route('/all', methods=['GET'])
def get_groups():
    return gc.get_groups()

@gc.group.route('/<gid>/join', methods=['POST'])
def join_group(gid):
    return gc.join_group(gid)

@gc.group.route('/<gid>/movies/<uid>', methods=['GET'])
def get_group_movies(gid, uid):
    return gc.get_group_movies(gid, uid)

app.register_blueprint(gc.group)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)