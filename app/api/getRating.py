import flask
from app import app

@app.route('/getRating')
def getRating():
    return flask.jsonify({'rating': 3200})