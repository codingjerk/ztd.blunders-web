from flask import jsonify

from app import app
from app.db import postgre

@app.route('/api/global/users-top', methods=['POST'])
def getUsersTop():
    return jsonify({
        'status': 'ok',
        'data': {
            "users-top-by-rating": postgre.statistic.getUsersTopByRating(10),
            "users-top-by-activity": postgre.statistic.getUsersTopByActivity('1 WEEK', 10),
        }
    })
