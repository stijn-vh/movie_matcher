import itertools
from flask import Blueprint, Flask, g, request
from flask_cors import CORS

from controllers.movie_controller import MovieController
from controllers.database_controller import DatabaseController
from controllers.group_controller import GroupController

app = Flask(__name__)
CORS(app)

dbc = DatabaseController()
user_bp = Blueprint('users', __name__, url_prefix='/users')
mc = MovieController(dbc)

@user_bp.route('/<uid>/movies', methods=['GET'])
def get_movies(uid):
    return mc.get_user_liked_movies(uid)

@user_bp.route('/<uid>/rate', methods=['POST', 'OPTIONS'])
def rate_movie(uid):
    return mc.rate_movie(uid)

app.register_blueprint(user_bp)



group_bp = Blueprint('groups', __name__, url_prefix='/groups')
gc = GroupController(dbc)

@group_bp.route('/create/<uid>', methods=['POST'])
def add_user_to_group(uid):
    return gc.create_group(uid)

@group_bp.route('<gid>/join/<uid>', methods=['POST'])
def join_group(gid, uid):
    return gc.join_group(gid, uid)