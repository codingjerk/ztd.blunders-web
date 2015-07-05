from flask import jsonify

from app import app
from app.db import postgre

# TODO: Split to three requests
# /api/global/users-count
# /api/global/users-top
# /api/global/users-online
@app.route('/api/statistic/users', methods=['POST'])
def getUsersStatistic():
    return jsonify(postgre.getUsersStatistic())
