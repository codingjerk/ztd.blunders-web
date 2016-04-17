from flask import request, jsonify

from app import app
from app.db import postgre
from app.utils import session, crossdomain, const
from app.utils.analyze import Engine

@app.route('/api/blunder/analyze', methods = ['POST'])
def analyzeBlunder():
    print(request.json)
    try:
        blunder_id = request.json['blunder_id']
        line = request.json['line']
    except Exception:
        return jsonify({
            'status': 'error',
            'message': 'blunder_id and line is required'
        })

    if(session.isAnonymous()):
        return jsonify({
            'status': 'error',
            'message': 'Analyzing in anonymous mode is not supported'
        })

    blunder = postgre.blunder.getBlunderById(blunder_id)
    if blunder is None:
        return {
            'status': 'error',
            'message': "Invalid blunder id"
        }

    blunder_fen = blunder['fen_before']
    blunder_move = blunder['blunder_move']
    forced_line = blunder['forced_line']

    with Engine(const.engine_path) as engine:
        engine.new(blunder_fen)
        engine.moveLine(line)
        result = engine.think(const.engine_time)
        print(result)

    return jsonify({
        'status': 'ok',
        'data': {
            'variations': [
                result
            ]
        }
    })

@app.route('/api/mobile/blunder/analyze', methods = ['POST', 'OPTIONS'])
@crossdomain.crossdomain()
@session.tokenize()
def analyzeBlunderMobile():
    return analyzeBlunder()
