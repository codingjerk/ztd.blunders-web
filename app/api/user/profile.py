from flask import request

from app import app
from app.db import postgre
from app.utils import wrappers, session, crossdomain, logger

logger = logger.Logger(__name__)

def getUserProfile():
    logger.info("API Handler user/profile")

    try:
        username = request.json['username']
    except Exception:
        return {
            'status': 'error',
            'message': 'Username required'
        }

    return postgre.user.getUserProfile(username)

@app.route('/api/user/profile', methods=['POST'])
@wrappers.nullable()
def getUserProfileWeb():
    return getUserProfile()

@app.route('/api/mobile/user/profile', methods = ['POST', 'OPTIONS'])
@crossdomain.crossdomain()
@wrappers.tokenize()
def getUserProfileMobile():
    # If 'username' not set, use default username associated with token.
    if not 'username' in request.json:
        request.json['username'] = session.username()

    return getUserProfile()
