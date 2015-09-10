from flask import session, request, jsonify

from app.db import postgre
from app.utils import hash

from functools import update_wrapper

class State:
    token = None
    username = None
    userID = None

    def authorize(token):
        State.token = token
        State.userID = postgre.getUserIdByToken(token)
        State.username = postgre.getUsernameById(State.userID)

def tokenize():
    def decorator(f):
        def wrapped():
            try:
                token = request.json['token']
            except Exception:
                return jsonify({
                    'status': 'error',
                    'message': 'API token is required'
                })

            try:
                State.authorize(token)
            except Exception:
                return jsonify({
                    'status': 'error',
                    'message': 'Invalid API token'
                })

            return f()

        return update_wrapper(wrapped, f)

    return decorator

def authorizeWithToken(username, password):
    try:
        if postgre.autentithicateUser(username, hash.get(username, password)):
            token = postgre.getTokenForUser(username)

            return {
                'status': 'ok',
                'token': token
            }
    except (Exception, KeyError):
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

def isAnonymous():
    if State.token: return False

    return 'user_id' not in session

def isAuthorized():
    return not isAnonymous()

def username():
    if State.token: return State.username

    if isAnonymous():
        return None

    return session['username']

def userID():
    if State.token: return State.userID

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

