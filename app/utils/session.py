from flask import session

from app.db import postgre
from app.utils import hash

def isAnonymous():
    return 'user_id' not in session

def isAuthorized():
    return not isAnonymous()

def username():
    if isAnonymous():
        return None

    return session['username']

def userID():
    if isAnonymous():
        return None

    return session['user_id']

def authorize(username, password): #pylint: disable=redefined-outer-name
    try:
        if postgre.autentithicateUser(username, hash.get(username, password)):
            session['username'] = username
            session['user_id'] = postgre.getUserId(username)

            return {
                'status': 'ok'
            }
    except Exception:
        return {
            'status': 'error',
            'field': 'username',
            'message': 'Invalid username'
        }

    return {
        'status': 'error',
        'field': 'password',
        'message': 'Invalid password'
    }

def deauthorize():
    if isAnonymous():
        return

    del session['username']
    del session['user_id']
