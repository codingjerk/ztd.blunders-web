from flask import request

from app import app
from app.db import postgre
from app import utils
from app.utils import hash, wrappers, session, crossdomain

def validate_user(username, password, email, validation_code):
    # Basic staqtic validations for username, email and email
    validateUserResult = utils.validateUser(
        username = username,
        password = password,
        email = email
    )
    if validateUserResult is not None:
        return validateUserResult

    # Check if user or email already in use
    duplicate_count = postgre.user.checkUserDuplicate(
        username = username,
        email = email
    )
    if duplicate_count > 0:
        return {
            'status': 'error',
            'message': 'username or email are already in use'
        }

    # Check if providen validation code correct
    validateCodeResult = utils.validateCode(
        email = email,
        validation_code = validation_code
    )
    if validateCodeResult is not None:
        return validateCodeResult

    return None

@app.route('/api/session/signup', methods=['POST'])
@wrappers.nullable()
def signupPostWeb():
    try:
        username = request.json['username']
        password = request.json['password']
        email = request.json['email']
        validation_code = request.json['validation_code']
    except Exception:
        return {
            'status': 'error',
            'message': 'Required: username, password, validation_code, email'
        }

    validation = validate_user(
        username,
        password,
        email,
        validation_code
    )
    if validation is not None:
        return validation

    salt, hashPass = hash.new(password)
    status = postgre.user.signupUser(username, salt, hashPass, email)

    if status['status'] == 'ok':
        session.authorize(username, password)

    return status

@app.route('/api/mobile/session/signup', methods=['POST', 'OPTIONS'])
@crossdomain.crossdomain()
@wrappers.nullable()
def signupPostMobile():
    if 'validation_code' not in request.json:
        return {
            'status': 'error',
            'message': 'Upgrade your application. Current client is deprecated.'
        }

    try:
        username = request.json['username']
        password = request.json['password']
        email = request.json['email']
        validation_code = request.json['validation_code']
    except Exception:
        return {
            'status': 'error',
            'message': 'Required: username, password, validation_code, email'
        }

    validation = validate_user(
        username,
        password,
        email,
        validation_code
    )
    if validation is not None:
        return validation

    salt, hashPass = hash.new(password)
    status = postgre.user.signupUser(username, salt, hashPass, email)

    if status['status'] != 'ok':
        return status

    return session.authorizeWithToken(username, password)
