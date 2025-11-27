import itertools
from flask import Blueprint, Flask, g, request
from flask_cors import CORS

from controllers.movie_controller import MovieController
from controllers.database_controller import DatabaseController
from controllers.group_controller import GroupController
from auth_utils import get_auth_uid

app = Flask(__name__)
CORS(app, resources={
    r"/users/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS"], "allow_headers": ["Content-Type", "Authorization"]},
    r"/groups/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS"], "allow_headers": ["Content-Type", "Authorization"]}
})

dbc = DatabaseController()
mc = MovieController(dbc)

user_bp = Blueprint('users', __name__, url_prefix='/users')

@user_bp.route('/get', methods=['GET'])
def get_user():
    uid = get_auth_uid()

    if uid is None:
        return { 'error': 'User not authenticated' }, 404
    
    user_dict, user_ref = dbc.get_user_profile(uid)

    if user_dict is None:
        return {'error': 'User not found'}, 404

    return { 'user': user_dict }, 200

@user_bp.route('/init', methods=['POST'])
def init_user():
    # !! TODO do authentication
    uid = get_auth_uid()

    if uid is None:
        return { 'error': 'User not authenticated' }, 404
    
    user_ref, user_doc = dbc.create_user(uid)

    return { 'user': user_doc }, 200

@user_bp.route('/movies', methods=['GET'])
def get_movies():
    uid = get_auth_uid()

    if uid is None:
        return { 'error': 'User not authenticated' }, 404
    
    return mc.get_user_liked_movies(uid)

app.register_blueprint(user_bp)

gc = GroupController(dbc)

@gc.group.route('/create/', methods=['POST'])
def add_user_to_group():
    uid = get_auth_uid()

    if uid is None:
        return { 'error': 'User not authenticated' }, 404
    
    return gc.create_group(uid)

@gc.group.route('/all', methods=['GET'])
def get_groups():
    return gc.get_groups()

@gc.group.route('/<gid>/join', methods=['POST'])
def join_group(gid):
    return gc.join_group(gid)

@gc.group.route('/<gid>/movies/', methods=['GET'])
def get_group_movies(gid):
    uid = get_auth_uid()

    if uid is None:
        return { 'error': 'User not authenticated' }, 404
    
    return gc.get_group_movies(gid, uid)

@gc.group.route('/<gid>/rate', methods=['POST', 'OPTIONS'])
def rate_movie(gid):
    if request.method == "OPTIONS":
        return "", 200
    
    uid = get_auth_uid()

    if uid is None:
        return { 'error': 'User not authenticated' }, 404
    
    
    return mc.rate_movie(gid, uid)

app.register_blueprint(gc.group)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader = False)