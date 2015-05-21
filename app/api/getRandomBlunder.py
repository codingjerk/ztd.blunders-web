import random
import flask

from app import app
from app.db import mongo

@app.route('/getRandomBlunder')
def getRandomBlunder():
    randomIndex = random.randint(0, mongo.db['blunders'].count())

    data = mongo.db['blunders'].find().skip(randomIndex).limit(1)[0]
    data['_id'] = str(data['_id'])
    data['pgn_id'] = str(data['pgn_id'])

    return flask.jsonify(data)