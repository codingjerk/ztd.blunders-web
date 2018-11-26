from flask import request

from app import app
from app.db import postgre
from app.utils import wrappers, session, crossdomain, logger

logger = logger.Logger(__name__)

def getBlundersFavorites():
    logger.info("API Handler user/favorite-blunders")

    try:
        username = request.json['username']
        offset = request.json['offset']
        limit = request.json['limit']
    except Exception:
        return {
            'status': 'error',
            'message': 'Username, offset and limit required'
        }

    return postgre.statistic.getBlundersFavorites(username, offset, limit)

@app.route('/api/user/favorite-blunders', methods = ['POST'])
@wrappers.nullable()
def getBlundersFavoritesWeb():
    return getBlundersFavorites()

@app.route('/api/mobile/user/favorite-blunders', methods = ['POST', 'OPTIONS'])
@crossdomain.crossdomain()
@wrappers.tokenize()
def getBlundersFavoritesMobile():
    # If 'username' not set, use default username associated with token.
    if not 'username' in request.json:
        request.json['username'] = session.username()

    return getBlundersFavorites()
