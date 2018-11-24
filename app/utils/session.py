from flask import session

from app.db import postgre
from app.utils import hash

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

#pylint: disable=too-few-public-methods
class State(metaclass = Singleton):
    __token = None
    __username = None
    __userID = None

    @property
    def token(self):
        return self.__token

    @property
    def username(self):
        return self.__username

    @property
    def userID(self):
        return self.__userID

    def __init__(self):
        pass

    def authorize(self, token): #pylint: disable=no-self-argument
        userId = postgre.user.getUserIdByToken(token)
        if userId is None:
            return False

        self.__token = token
        self.__userID = userId
        self.__username = postgre.user.getUsernameById(self.userID)

        return True

    #pylint: disable=no-method-argument
    def clean(self):
        State.__token = None
        State.__userID = None
        State.__username = None

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
    if State().token:
        return False

    return 'user_id' not in session

def isAuthorized():
    return not isAnonymous()

def username():
    if State().token:
        return State().username

    if isAnonymous():
        return None

    return session['username']

def userID():
    if State().token:
        return State().userID

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
