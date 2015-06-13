from flask import jsonify, request

import random

from app import app, db
from app.db import mongo, postgre
from app import utils

@app.route('/statistics/getRatingByDate', methods=['POST'])
def getRatingByDate():
    try:
        username = request.json['username']
    except:
        return jsonify({
            'status': 'error',
            'message': 'Username required'
        })

    return jsonify(postgre.getRatingByDate(username))
    