import flask

from app import app
from app.db import postgre
from app.utils import wrappers, session, crossdomain, logger

logger = logger.Logger(__name__)

def getRating():
    logger.info("API Handler session/rating")

    return {
        'status': 'ok',
        'rating': postgre.user.getRating(session.userID())
    }

@app.route('/api/session/rating')
@wrappers.nullable()
def getRatingWeb():
    return getRating()

@app.route('/api/mobile/session/rating', methods = ['POST', 'OPTIONS'])
@crossdomain.crossdomain()
@wrappers.tokenize()
def getRatingMobile():
    return getRating()
