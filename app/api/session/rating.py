import flask

from app import app
from app.db import postgre
from app.utils import session

@app.route('/api/session/rating')
def getRating():
    return flask.jsonify({
        'status': 'ok',
        'rating': postgre.getRating(session.userID())
    })