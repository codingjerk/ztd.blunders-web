from flask import request, jsonify

from app import app
from app.db import postgre

@app.route('/api/feedback/send', methods = ['POST'])
def sendFeedback():
    try:
        message = request.json['message']
    except Exception:
        return jsonify({
            'status': 'error',
            'message': 'Message required'
        })

    return jsonify(
        postgre.feedback.saveFeedback(message)
    )

