from flask import jsonify

from app import app
from app.db import postgre

@app.route('/api/global/users-online', methods=['POST'])
def getUsersOnline():
    return jsonify({
        'status': 'ok',
        'data': {
            "users-online-list" : postgre.statistic.getActiveUsers('1 HOUR')
        }
    })
