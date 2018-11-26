from flask import request

from app import app
from app.utils import wrappers, session, crossdomain, logger

logger = logger.Logger(__name__)

@app.route('/api/session/login', methods=['POST'])
@wrappers.nullable()
def loginPostWeb():
    logger.info("API Handler session/login web version")

    try:
        username = request.json['username']
        password = request.json['password']
    except Exception:
        return {
            'status': 'error',
            'message': 'Username and password is required'
        }

    result = session.authorize(username, password)

    return result

@app.route('/api/mobile/session/login', methods=['POST', 'OPTIONS'])
@crossdomain.crossdomain()
@wrappers.nullable()
def loginPostMobile():
    logger.info("API Handler session/login mobile version")

    try:
        username = request.json['username']
        password = request.json['password']
    except Exception:
        return {
            'status': 'error',
            'message': 'Username and password is required'
        }

    result = session.authorizeWithToken(username, password)

    return result
