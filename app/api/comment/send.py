from flask import request, jsonify

from app import app
from app.db import postgre
from app.utils import session, const, crossdomain

@app.route('/api/comment/send', methods = ['POST'])
def commentBlunder():
    if session.isAnonymous():
        return jsonify({
            'status': 'error',
            'message': 'Commenting allowed only for authorized user'
        })

    try:
        blunder_id = request.json['blunder_id']
        comment_id = request.json['comment_id']
        user_input = request.json['user_input']
    except Exception:
        return jsonify({
            'status': 'error',
            'message': 'Blunder id, input and comment_id required'
        })

    # Frontend uses 0 to say comment is the root comment,
    # but backend uses None for that
    if comment_id == 0:
        comment_id = None

    if len(user_input) > const.comment.MAX_SIZE:
        return jsonify({
            'status': 'error',
            'message': 'Input length can\'t be greater than %d' % MAX_MESSAGE_SIZE
        })

    if not postgre.blunder.commentBlunder(session.userID(), blunder_id, comment_id, user_input):
        return jsonify({
            'status': 'error',
            'message': "Can't comment blunder"
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

@app.route('/api/mobile/comment/send', methods = ['POST', 'OPTIONS'])
@crossdomain.crossdomain()
@session.tokenize()
def commentBlunderMobile():
    return commentBlunder()
