from flask import request

from app import app
from app.db import postgre
from app.utils import wrappers, session, crossdomain, logger

logger = logger.Logger(__name__)

def getCommentsByUser():
    logger.info("API Handler user/comments")

    try:
        username = request.json['username']
        offset = request.json['offset']
        limit = request.json['limit']
    except Exception:
        return {
            'status': 'error',
            'message': 'Username, offset and limit required'
        }

    return postgre.statistic.getCommentsByUser(username, offset, limit)

@app.route('/api/user/comments', methods = ['POST'])
@wrappers.nullable()
def getCommentsByUserWeb():
    return getCommentsByUser()

@app.route('/api/mobile/user/comments', methods = ['POST', 'OPTIONS'])
@crossdomain.crossdomain()
@wrappers.tokenize()
def getCommentsByUserMobile():
    # If 'username' not set, use default username associated with token.
    if not 'username' in request.json:
        request.json['username'] = session.username()

    return getCommentsByUser()
