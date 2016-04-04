import flask

from app import app
from app.db import postgre
from app.utils import session, crossdomain

@app.route('/api/session/rating')
def getRating():
    return flask.jsonify({
        'status': 'ok',
        'rating': postgre.user.getRating(session.userID())
    })

@app.route('/api/mobile/session/rating', methods = ['POST', 'OPTIONS'])
@crossdomain.crossdomain()
@session.tokenize()
def getRatingMobile():
    return getRating()
