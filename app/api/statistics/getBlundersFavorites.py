from flask import jsonify, request

import random

from app import app, db
from app.db import mongo, postgre
from app import utils

@app.route('/statistics/getBlundersFavorites', methods = ['POST'])
def getBlundersFavorites():
    try:
        username = request.json['username']
        offset = request.json['offset']
        limit = request.json['limit']
    except:
        return jsonify({
            'status': 'error',
            'message': 'Username, offset and limit required'
        })

    return jsonify(db.getBlundersFavorites(username, offset, limit))
    