from flask import jsonify, request

import random

from app import app, db
from app.db import mongo, postgre
from app import utils

@app.route('/statistics/getBlundersByDate', methods=['POST'])
def getBlundersByDate():
    try:
        username = request.json['username']
    except:
        return jsonify({
            'status': 'error',
            'message': 'Username required'
        })

    return jsonify(postgre.getBlundersByDate(username))
    