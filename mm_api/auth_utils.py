from flask import request
import firebase_admin
from firebase_admin import credentials, auth

def get_auth_uid():
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise Exception("Missing Authorization header")
    
    token = auth_header.split("Bearer ")[1]
    decoded = auth.verify_id_token(token)
    return decoded["uid"]
