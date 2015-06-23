from flask import jsonify

from app import app
from app.db import postgre

@app.route('/statistics/getUsersStatistics', methods=['GET'])
def getUsersStatistics():
    return jsonify(postgre.getUsersStatistics())
