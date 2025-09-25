from flask_cors import CORS
import random
from flask import Blueprint, request, group
from controllers.database_controller import DatabaseController
class GroupController:
    def __init__(self, app):
        self.group = Blueprint('group', __name__, url_prefix='/group')
        app.register_blueprint(self.group)

        self.dc = DatabaseController()

    def create_group(self, uid):
        group_dict = {
            'users': [uid],
            'movie_stack': []
        }

        self.dc.create_group(group_dict)

        return { 'group': group_dict }, 200

    def join_group(self, gid, uid):
        group_dict, group_ref = self.dc.get_group(gid)

        if group_dict is None:
            return {'Error': 'Group not found'}, 400
        
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
