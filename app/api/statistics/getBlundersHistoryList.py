from flask import jsonify, request

import random

from app import app, db
from app.db import mongo, postgre
from app import utils

@app.route('/statistics/getBlundersHistoryList', methods=['POST'])
def getBlundersHistoryList():
    try:
        username = request.json['username']
        page = request.json['page']
        limit = request.json['limit']
    except:
        return jsonify({
            'status': 'error',
            'message': 'Username, page and limit required'
        })

    return jsonify(postgre.getBlundersHistoryList(username, page, limit))
    