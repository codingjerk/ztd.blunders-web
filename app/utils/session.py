from flask import session, request, jsonify

from app.db import postgre
from app.utils import hash

from functools import update_wrapper

#pylint: disable=too-few-public-methods
class State:
    token = None
    username = None
    userID = None

    def __init__(self):
        raise Exception("State is static class, can't call State.__init__")

    def authorize(token): #pylint: disable=no-self-argument
        State.token = token
        State.userID = postgre.user.getUserIdByToken(token)
        State.username = postgre.user.getUsernameById(State.userID)

    #pylint: disable=no-method-argument
    def clean():
        State.token = None
        State.userID = None
        State.username = None

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

                result = f()
            except Exception as e:
                print(e) # Useful debug printing
                return jsonify({
                    'status': 'error',
                    'message': 'Invalid API token'
                })

            State.clean()

            return result

        return update_wrapper(wrapped, f)

    return decorator

#pylint: disable=redefined-outer-name
def authorizeWithToken(username, password):
    try:
        if postgre.user.authorize(username, hash.get(username, password)):
            token = postgre.user.getTokenForUser(username)

            return {
                'status': 'ok',
                'token': token
            }
    except (Exception, KeyError) as e:
        print(e)
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
    if State.token:
        return False

    return 'user_id' not in session

def isAuthorized():
    return not isAnonymous()

def username():
    if State.token:
        return State.username

    if isAnonymous():
        return None

    return session['username']

def userID():
    if State.token:
        return State.userID

    if isAnonymous():
        return None

    return session['user_id']

def authorize(username, password): #pylint: disable=redefined-outer-name
    try:
        if postgre.user.authorize(username, hash.get(username, password)):
            session['username'] = username
            session['user_id'] = postgre.user.getUserId(username)

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
