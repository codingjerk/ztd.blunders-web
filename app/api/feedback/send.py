from flask import request

from app import app
from app.db import postgre

from app.utils import wrappers

def sendFeedback():
    try:
        message = request.json['message']
    except Exception:
        return {
            'status': 'error',
            'message': 'Message required'
        }

    return postgre.feedback.saveFeedback(message)

@app.route('/api/feedback/send', methods = ['POST'])
@wrappers.nullable()
def sendFeedbackWeb():
    return sendFeedback()
