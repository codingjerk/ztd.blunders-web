import flask
from flask import session

from app import app
from app.db import postgre

@app.route('/getRating')
def getRating():
    rating = postgre.getRating(session['username']) if 'username' in session else 0

    return flask.jsonify({'rating': rating})