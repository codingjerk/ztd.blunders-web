from flask import jsonify

from app import app
from app.db import postgre

@app.route('/statistic/getUsersStatistic', methods=['GET'])
def getUsersStatistic():
    return jsonify(postgre.getUsersStatistic())
