'''
Created on Jul 11, 2013

@author: Pheonix
'''
from functools import wraps
from flask import request, Response


def check_username_password():
    # Connect to database and check the combo
    return False

def do_authentication():
    return Response('Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def needs_authentication(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth and not check_username_password():
            return do_authentication()
        return f(*args, **kwargs)
    return decorated