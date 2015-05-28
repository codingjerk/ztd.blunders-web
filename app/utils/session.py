from flask import session

from app.db import postgre
from app.utils import hash

def isAnonymous():
    return 'username' not in session

def isAuthorized():
    return not isAnonymous()

def username():
    if isAnonymous(): return None
    return session['username']

def authorize(username, password):
    if postgre.autentithicateUser(username, hash.get(username, password)):
        session['username'] = username

def deauthorize():
    if isAnonymous(): return
    del session['username']