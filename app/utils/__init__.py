import re

class Roles:
    ADMIN = 0
    USER = 3

class TaskTypes:
    RATED = 'rated'
    EXPLORE = 'explore'

"""Decorator, that calls function on module import"""
def init(func):
    func();
    return func

def jsonifyBlunder(data):
    return {
        'status': 'ok',
        'data': {
            'id': str(data['_id']),
            'pgn_id': str(data['pgn_id']),
            'move_index': data['move_index'],

            'forcedLine': data['forcedLine'],
            'pv': data['pv'],

            'fenBefore': data['fenBefore'],
            'blunderMove': data['blunderMove'],

            'elo': data['elo']
        }

    }

def validateUsername(username):
    if len(username) < 3:
        return "Username must contains at least 3 letter" 

    if not re.match("^[-a-zA-Z0-9!#$%&'*+/=?^_`{|}~]+(\.[-a-zA-Z0-9!#$%&'*+/=?^_`{|}~]+)*$", username):
        return "Your name is too strange"

    return None

def validatePassword(password):
    if len(password) < 5:
        return "Your password must be at least 5 characters long"

    return None

def validateEmail(email):
    if len(email.strip()) == 0: return

    if not re.match('^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$', email):
        return "Invalid email"

    return None

def validateUser(username, password, email):
    usernameValidation = validateUsername(username)
    if usernameValidation is not None: return {
        'status': 'error',
        'field': 'username', 
        'message': usernameValidation
    }

    passwordValidation = validatePassword(password)
    if passwordValidation is not None: return {
        'status': 'error',
        'field': 'password', 
        'message': passwordValidation
    }

    emailValidation = validateEmail(email)
    if emailValidation is not None: return {
        'status': 'error',
        'field': 'email', 
        'message': emailValidation
    }

    return None