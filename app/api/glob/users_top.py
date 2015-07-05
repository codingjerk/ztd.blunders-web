from flask import jsonify

from app import app
from app.db import postgre

@app.route('/api/global/users-top', methods=['POST'])
def getUsersTop():
    return jsonify({
        'status': 'ok',
        'data': {
            "users-top-list": postgre.getUsersTop(10)
        }
    })
