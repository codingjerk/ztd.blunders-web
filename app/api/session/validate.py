from flask import request

from random import randint

from app import app
from app.db import postgre
from app import utils
from app.utils import crossdomain, wrappers, const, logger
from app.utils.email import GMailAPIValidation

logger = logger.Logger(__name__)

def validatePost():
    logger.info("API Handler session/validate")

    try:
        email = request.json['email']
        password = request.json['password']
        username = request.json['username']
    except Exception:
        return {
            'status': 'error',
            'message': 'username, password and email are required'
        }

    validateUserResult = utils.validateUser(
        username = username,
        password = password,
        email = email
    )
    if validateUserResult is not None:
        return validateUserResult

    duplicate_count = postgre.user.checkUserDuplicate(
        username = username,
        email = email
    )
    if duplicate_count > 0:
        return {
            'status': 'error',
            'message': 'username or email are already in use'
        }

    validation = postgre.user.validateUserGet(email=email)

    if validation is None:
        count_tries = 1
        code = str(randint(100000, 999999))
        status = postgre.user.validateUserCreate(email = email, code = code)
    else:
        (count_tries, code, date_create, date_update) = validation
        status = postgre.user.validateUserIncrement(email=email)

    if not status:
        return {
            'status': 'error',
            'message': 'Exception in email validation'
        }

    if count_tries < const.email_validation.limit:
        email_validation = GMailAPIValidation()

        email_validation.send(
            user_name = username,
            user_email=email,
            validation_code = code
        )

    return {
        'status': 'ok'
    }

@app.route('/api/session/validate', methods=['POST'])
@wrappers.nullable()
def validatePostWeb():
    return validatePost()

@app.route('/api/mobile/session/validate', methods=['POST', 'OPTIONS'])
@crossdomain.crossdomain()
@wrappers.nullable()
def validatePostMobile():
    return validatePost()
