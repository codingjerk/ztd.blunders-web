from flask import request, jsonify

from app import app
from app.db import postgre
from app.utils import session, crossdomain, analyze

@app.route('/api/blunder/analyze', methods = ['POST'])
def analyzeBlunder():
    try:
        blunder_id = request.json['blunder_id']
        line = request.json['line']
    except Exception:
        return jsonify({
            'status': 'error',
            'message': 'blunder_id and line is required'
        })

    print(request.json)
    #analyze.analyzePosition()
    return jsonify({
        'status': 'ok',
        'data': {
            'calculations': [
                {
                    'score': 1.78,
                    'line': ['e2-e4', 'h7-h8']
                }
            ]
        }
    })

@app.route('/api/mobile/blunder/analyze', methods = ['POST', 'OPTIONS'])
@crossdomain.crossdomain()
@session.tokenize()
def analyzeBlunderMobile():
    return analyzeBlunder()
