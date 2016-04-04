from flask import jsonify

from app import app
from app.db import postgre

@app.route('/api/global/blunders-count', methods=['POST'])
def totalBlundersCount():
    return jsonify(postgre.statistic.getBlundersStatistic())
