from flask import request, jsonify

from app import app
from app.db import postgre
from app.utils import session

from app.api.getBlunderInfo import getBlunderInfoById

@app.route('/api/blunder/vote', methods = ['POST'])
def voteBlunder():
    if session.isAnonymous():
        return jsonify({
            'status': 'error',
            'message': 'Voting allowed only for authorized user'
        })

    try:
        blunder_id = request.json['blunder_id']
        vote = request.json['vote']
    except Exception:
        return jsonify({
            'status': 'error',
            'message': 'Blunder id and vote required'
        })

    if not postgre.voteBlunder(session.userID(), blunder_id, vote):
        return jsonify({
            'status': 'error',
            'message': "Can't vote blunder"
        })

    return getBlunderInfoById(blunder_id)
