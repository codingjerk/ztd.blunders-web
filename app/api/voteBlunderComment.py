
from flask import request, jsonify

from app import app, db
from app.db import mongo, postgre
from app.utils import session

from app.api.getBlunderInfo import getBlunderInfoById

@app.route('/voteBlunderComment', methods = ['POST'])
def voteBlunderComment():
    if session.isAnonymous(): return jsonify({
        'status': 'error',
        'message': 'Voting allowed only for authorized user'
    })

    try:
        blunder_id = request.json['blunder_id']
        comment_id = request.json['comment_id']
        vote = request.json['vote']
    except:
        return jsonify({
            'status': 'error',
            'message': 'Blunder id, comment id and vote required'
        })

    if vote not in [-1, 1]: 
        return jsonify({
            'status': 'error',
            'message': 'Vote must be +1 or -1'
        })

    if postgre.blunderCommentAuthor(comment_id) == session.username(): 
        return jsonify({
            'status': 'error', 
            'message': "Can't vote for own comments"
        })

    if not postgre.voteBlunderComment(session.username(), comment_id, vote): 
        return jsonify({
            'status': 'error', 
            'message': "Can't vote comment"
        })

    return getBlunderInfoById(blunder_id)
