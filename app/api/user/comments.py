from flask import jsonify, request

from app import app
from app.db import postgre
from app.utils import session, crossdomain

@app.route('/api/user/comments', methods = ['POST'])
def getCommentsByUser():
    try:
        username = request.json['username']
        offset = request.json['offset']
        limit = request.json['limit']
    except Exception:
        return jsonify({
            'status': 'error',
            'message': 'Username, offset and limit required'
        })

    return jsonify(postgre.statistic.getCommentsByUser(username, offset, limit))

@app.route('/api/mobile/user/comments', methods = ['POST', 'OPTIONS'])
@crossdomain.crossdomain()
@session.tokenize()
def getCommentsByUserMobile():
    # If 'username' not set, use username associated with token.
    if not 'username' in request.json:
        request.json['username'] = session.username()
        
    return getCommentsByUser()
