from flask import request, jsonify

from app import app
from app.db import postgre
from app.utils import session

from app.api.blunder.info import getBlunderInfoById

@app.route('/api/comment/vote', methods = ['POST'])
def voteBlunderComment():
    if session.isAnonymous():
        return jsonify({
            'status': 'error',
            'message': 'Voting allowed only for authorized user'
        })

    try:
        blunder_id = request.json['blunder_id']
        comment_id = request.json['comment_id']
        vote = request.json['vote']
    except Exception:
        return jsonify({
            'status': 'error',
            'message': 'Blunder id, comment id and vote required'
        })

    if postgre.blunderCommentAuthor(comment_id) == session.userID():
        return jsonify({
            'status': 'error',
            'message': "Can't vote for own comments"
        })

    if not postgre.voteBlunderComment(session.userID(), comment_id, vote):
        return jsonify({
            'status': 'error',
            'message': "Can't vote comment"
        })

    return getBlunderInfoById(blunder_id)
