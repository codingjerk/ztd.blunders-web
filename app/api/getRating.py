import flask

from app import app
from app.db import postgre
from app.utils import session

@app.route('/getRating')
def getRating():
    return flask.jsonify({
        'status': 'ok',
        'rating': postgre.getRating(session.username())
    })