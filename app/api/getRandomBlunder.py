import random
import flask

from app import app
from app.api import blunderCollection

@app.route('/getRandomBlunder')
def getRandomBlunder():
    randomIndex = random.randint(0, blunderCollection.count())

    data = blunderCollection.find().skip(randomIndex).limit(1)[0]
    data['_id'] = str(data['_id'])
    data['pgn_id'] = str(data['pgn_id'])

    return flask.jsonify(data)