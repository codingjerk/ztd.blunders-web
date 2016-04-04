from flask import request, jsonify

from app import app
from app.db import postgre
from app.utils import session, crossdomain

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

    if not postgre.blunder.voteBlunder(session.userID(), blunder_id, vote):
        return jsonify({
            'status': 'error',
            'message': "Can't vote blunder"
        })

    result = postgre.blunder.getBlunderInfoById(session.userID(), blunder_id)
    if result is None:
        return {
            'status': 'error',
            'message': 'Invalid blunder id',
        }

    return jsonify({
        'status': 'ok',
        'data': result
    })

@app.route('/api/mobile/blunder/vote', methods = ['POST', 'OPTIONS'])
@crossdomain.crossdomain()
@session.tokenize()
def voteBlunderMobile():
    return voteBlunder()
