import re

def init(func):
    """Decorator, that calls function on module import"""

    func()
    return func

def jsonifyBlunder(data):
    return {
        'id': str(data['id']),
        'game_id': str(data['game_id']),
        'move_index': data['move_index'],

        'forcedLine': data['forced_line'],

        'fenBefore': data['fen_before'],
        'blunderMove': data['blunder_move'],

        'elo': data['elo']
    }

def validateUsername(username):
    if username is None:
        return "Username is empty"

    if len(username) < 3:
        return "Username must contains at least 3 letter"

    # TODO: Use precompiled regexes
    usernameRegex = "^[-a-zA-Z0-9!#$%&'*+/=?^_`{|}~]+(\\.[-a-zA-Z0-9!#$%&'*+/=?^_`{|}~]+)*$"

    if not re.match(usernameRegex, username):
        return "Your name is too strange"

    return None

def validatePassword(password):
    if password is None:
        return "Password is empty"

    if len(password) < 5:
        return "Your password must be at least 5 characters long"

    return None

def validateEmail(email):
    if email is None:
        return "Email is empty"

    if email.strip() != email or email.lower() != email:
        return "Invalid email"

    from app.utils.email import MXDomainValidation
    if not MXDomainValidation(email):
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

def validateCode(email, validation_code):
    if validation_code is None:
        return {
            'status': 'error',
            'field': 'validation_code',
            'message': 'Validation Code is empty'
        }

    from app.db import postgre
    validation = postgre.user.validateUserGet(email=email)
    if validation is None:
        return {
            'status': 'error',
            'field': 'validation_code',
            'message': 'Incorrect validation code'
        }

    (count_tries, stored_code, date_create, date_update) = validation
    print(stored_code, validation_code, stored_code != validation_code)
    if stored_code != validation_code:
        return {
            'status': 'error',
            'field': 'validation_code',
            'message': 'Incorrect validation code'
        }

    return None
