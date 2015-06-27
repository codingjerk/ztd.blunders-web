import re

def init(func):
    """Decorator, that calls function on module import"""

    func()
    return func

def jsonifyBlunder(data):
    return {
        'status': 'ok',
        'data': {
            'id': str(data['id']),
            'pgn_id': str(data['pgn_id']),
            'move_index': data['move_index'],

            'forcedLine': data['forced_line'],
            'pv': data['pv'],

            'fenBefore': data['fen_before'],
            'blunderMove': data['blunder_move'],

            'elo': data['elo']
        }
    }

def validateUsername(username):
    if len(username) < 3:
        return "Username must contains at least 3 letter"

    # TODO: Use precompiled regexes
    usernameRegex = "^[-a-zA-Z0-9!#$%&'*+/=?^_`{|}~]+(\\.[-a-zA-Z0-9!#$%&'*+/=?^_`{|}~]+)*$"

    if not re.match(usernameRegex, username):
        return "Your name is too strange"

    return None

def validatePassword(password):
    if len(password) < 5:
        return "Your password must be at least 5 characters long"

    return None

def validateEmail(email):
    if len(email.strip()) == 0:
        return None

    # TODO: Use precompiled regexes
    emailRegex = '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,6}$'

    if not re.match(emailRegex, email):
        return "Invalid email"

    return None

def validateUser(username, password, email):
    usernameValidation = validateUsername(username)
    if usernameValidation is not None:
        return {
            'status': 'error',
            'field': 'username',
            'message': usernameValidation
        }

    passwordValidation = validatePassword(password)
    if passwordValidation is not None:
        return {
            'status': 'error',
            'field': 'password',
            'message': passwordValidation
        }

    emailValidation = validateEmail(email)
    if emailValidation is not None:
        return {
            'status': 'error',
            'field': 'email',
            'message': emailValidation
        }

    return None
