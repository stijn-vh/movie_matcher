from flask_cors import CORS
import random
from flask import Blueprint, request
from controllers.database_controller import DatabaseController
from controllers.group_recommendation_controller import GroupRecommendationController

class GroupController:
    def __init__(self, database_controller):
        self.group = Blueprint('group', __name__, url_prefix='/group')
        self.dc = database_controller

        self.grc = GroupRecommendationController(database_controller, self)

    def create_group(self, uid):
        group_dict = {
            'users': [uid],
            'stack': [],
            'history': []
        }

        self.dc.create_group(group_dict)

        return { 'group': group_dict }, 200
    
    def get_groups(self):
        groups_dict, groups_ref = self.dc.get_groups()

        return { 'groups': groups_dict }
    
    def get_group_movies(self, gid, uid):
        personal_movies = self.grc.get_movies_from_stack(gid, uid)

        print('pppp', personal_movies)
        if not personal_movies.empty:
            movies = personal_movies
        else:
            movies = self.grc.add_batch_to_stack(gid)

        return { 'movies': movies.to_dict(orient='records') }, 200


    def join_group(self, gid):
        group_dict, group_ref = self.dc.get_group(gid)

        if group_dict is None:
            return {'Error': 'Group not found'}, 400
        
        data = request.get_json()
        uid = data.get('uid')
        
        group_dict['users'].append(uid)
        group_ref.set(group_dict)

        user_dict, user_ref = self.dc.get_user_profile(uid)
        user_dict['active_group'] = gid
        user_ref.set(user_dict)

        return { 'group': group_dict }, 200

    # TODO: remove movies rated by player in group
    def leave_group(self, gid, uid):
        group_dict, group_ref = self.dc.get_group(gid)

        if group_dict is None:
            return {'Error': 'Group not found'}, 400
        
        group_dict['users'].remove(uid)
        group_ref.set(group_dict)

        user_dict, user_ref = self.dc.get_user_profile(uid)
        user_dict['active_group'] = None
        user_ref.set(user_dict)

        return { 'group': group_dict }, 200
    
    def archive_group(self, gid):
        group_dict, group_ref = self.dc.get_group(gid)

        if group_dict is None:
            return {'Error': 'Group not found'}, 400        
        
        for uid in group_dict['users']:
            user_dict, user_ref = self.dc.get_user_profile(uid)
            user_dict['active_group'] = None
            user_ref.set(user_dict)
        
        return { 'message': 'Group succesfully archived' }, 200
