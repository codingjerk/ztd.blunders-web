import random
import flask

from app import app
from app.db import mongo

@app.route('/getRandomBlunder')
def getRandomBlunder():
    randomIndex = random.randrange(0, mongo.db['filtered_blunders'].count())

    data = mongo.db['filtered_blunders'].find().skip(randomIndex).limit(1)[0]
    
    result = {
        'pgn_id': str(data['pgn_id']),
        'move_index': data['move_index'],

        'forcedLine': data['forcedLine'],
        'pv': data['pv'],

        'fenBefore': data['fenBefore'],
        'blunderMove': data['blunderMove'],

        'elo': data['elo'],
    }

    return flask.jsonify(result)