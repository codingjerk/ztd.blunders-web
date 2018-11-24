from flask import request

from app import app
from app.db import postgre
from app.utils import wrappers, session, const, crossdomain

def voteBlunderComment():
    if session.isAnonymous():
        return {
            'status': 'error',
            'message': 'Voting allowed only for authorized user'
        }

    try:
        blunder_id = request.json['blunder_id']
        comment_id = request.json['comment_id']
        vote = request.json['vote']
    except Exception:
        return {
            'status': 'error',
            'message': 'Blunder id, comment id and vote required'
        }

    if postgre.blunder.blunderCommentAuthor(comment_id) == session.userID():
        return {
            'status': 'error',
            'message': "Can't vote for own comments"
        }

    if not postgre.blunder.voteBlunderComment(session.userID(), comment_id, vote):
        return {
            'status': 'error',
            'message': "Can't vote comment"
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

@app.route('/api/comment/vote', methods = ['POST'])
@wrappers.nullable()
def voteBlunderCommentWeb():
    return voteBlunderComment()

@app.route('/api/mobile/comment/vote', methods = ['POST', 'OPTIONS'])
@crossdomain.crossdomain()
@wrappers.tokenize()
def voteBlunderCommentMobile():
    return voteBlunderComment()
