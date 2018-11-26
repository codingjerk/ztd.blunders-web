from flask import request

from app import app
from app.db import postgre
from app.utils import wrappers, session, crossdomain, logger

logger = logger.Logger(__name__)

def getRatingByDate():
    logger.info("API Handler user/rating-by-date")

    try:
        username = request.json['username']
        interval = request.json['interval']
    except Exception:
        return {
            'status': 'error',
            'message': 'Username and interval required'
        }

    return postgre.user.getRatingByDate(username, interval)

@app.route('/api/user/rating-by-date', methods=['POST'])
@wrappers.nullable()
def getRatingByDateWeb():
    return getRatingByDate()

@app.route('/api/mobile/user/rating-by-date', methods = ['POST', 'OPTIONS'])
@crossdomain.crossdomain()
@wrappers.tokenize()
def getRatingByDateMobile():
    # If 'username' not set, use default username associated with token.
    if not 'username' in request.json:
        request.json['username'] = session.username()

    return getRatingByDate()
