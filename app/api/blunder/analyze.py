from flask import request, jsonify

from app import app
from app.db import postgre
from app.utils import session, crossdomain, const, chess
from app.utils.analyze import Engine

#def getAnalyzeFromCache(blunder_fen, data):
#    for element in data:
#        stored = postgre.blunders.getAnalyze(data['fen'], data['line'])


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

    if chess.mismatchCheck(blunder_move, forced_line, line):
        return {
            'status': 'error',
            'message': "Remote database has been changed"
        }

    data = chess.boardsToAnalyze(blunder_fen, blunder_move, forced_line, line)

    with Engine(const.engine.path) as engine:
        engine.new()
        for element in data:
            user_fen = chess.fenAfterVariation(blunder_fen, element['user_line'])
            engine.set(user_fen)
            element['engine'] = engine.think(const.engine.time, move = element['user_move'])
            postgre.blunder.saveAnalyze(session.userID(), blunder_id, element, const.engine.time)

    return jsonify({
        'status': 'ok',
        'data': {
            'variations': [element['engine'] for element in data ]
        }
    })

@app.route('/api/mobile/blunder/analyze', methods = ['POST', 'OPTIONS'])
@crossdomain.crossdomain()
@session.tokenize()
def analyzeBlunderMobile():
    return analyzeBlunder()
