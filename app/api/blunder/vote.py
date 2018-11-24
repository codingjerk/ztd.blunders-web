from flask import request

from app import app
from app.db import postgre
from app.utils import wrappers, session, crossdomain

def voteBlunder():
    if session.isAnonymous():
        return {
            'status': 'error',
            'message': 'Voting allowed only for authorized user'
        }

    try:
        blunder_id = request.json['blunder_id']
        vote = request.json['vote']
    except Exception:
        return {
            'status': 'error',
            'message': 'Blunder id and vote required'
        }

    if not postgre.blunder.voteBlunder(session.userID(), blunder_id, vote):
        return {
            'status': 'error',
            'message': "Can't vote blunder"
        }

    result = postgre.blunder.getBlunderInfoById(session.userID(), blunder_id)
    if result is None:
        return {
            'status': 'error',
            'message': 'Invalid blunder id',
        }

    return {
        'status': 'ok',
        'data': result
    }

@app.route('/api/blunder/vote', methods = ['POST'])
@wrappers.nullable()
def voteBlunderWeb():
    return voteBlunder()

@app.route('/api/mobile/blunder/vote', methods = ['POST', 'OPTIONS'])
@crossdomain.crossdomain()
@wrappers.tokenize()
def voteBlunderMobile():
    return voteBlunder()
