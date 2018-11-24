from flask import request

from app import app
from app.db import postgre
from app.utils import wrappers, session, crossdomain, const, chess
from app.utils.analyze import Engine

def searchForPreanalyzed(blunder_id, data):
    # TODO: if engine calculation time is longer,
    # than stored time, don't take stored result, recalulate
    for element in data:
        if 'engine' in element:
            continue;

        user_line = element['user']['line']
        user_move = element['user']['move']

        result = postgre.blunder.getAnalyze(blunder_id, user_line, user_move)

        if result is not None:
            engine_line, engine_score, time_ms = result

            element['engine'] = {
                'line' : engine_line,
                'score': engine_score
            }

    return data

def calcualteWithEngine(blunder_id, blunder_fen, data):
    with Engine(const.engine.path) as engine:
        for element in data:
            if 'engine' in element:
                continue;

            user_line = element['user']['line']
            user_move = element['user']['move']

            # Mathematical equality: element['user_line'] + element['user_move'] = user_line
            user_fen = chess.fenAfterVariation(blunder_fen, user_line)

            engine.new()
            engine.set(user_fen)
            element['engine'] = engine.think(const.engine.time, move = user_move)

            engine_line = element['engine']['line']
            engine_score = element['engine']['score']
            # TODO: calculating is long procedure. In order to avoid error, checking once more
            # In the future, after upgrade to 9.5 please use ON CONFLICT DO NOTHING
            if postgre.blunder.getAnalyze(blunder_id, user_line, user_move) is None:
                postgre.blunder.saveAnalyze(session.userID(), blunder_id, user_line, user_move,
                                            engine_line, engine_score, const.engine.time)

        return data

def isAllCalculated(data):
    return sum('engine' in element for element in data) == len(data)

def analyzeBlunder():
    try:
        blunder_id = request.json['blunder_id']
        line = request.json['line']
    except Exception:
        return {
            'status': 'error',
            'message': 'blunder_id and line is required'
        }

    if(session.isAnonymous()):
        return {
            'status': 'error',
            'message': 'Analyzing in anonymous mode is not supported'
        }

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

    data = searchForPreanalyzed(blunder_id, data)

    # No need to start engine process if all needed data known
    if not isAllCalculated(data):
        data = calcualteWithEngine(blunder_id, blunder_fen, data)

    return {
        'status': 'ok',
        'data': {
            'variations': [{
                    'line': element['engine']['line'],
                    'score': element['engine']['score'],
                    'status': element['status']
                } for element in data ]
        }
    }

@app.route('/api/blunder/analyze', methods = ['POST'])
@wrappers.nullable()
def analyzeBlunderWeb():
    return analyzeBlunder()

@app.route('/api/mobile/blunder/analyze', methods = ['POST', 'OPTIONS'])
@crossdomain.crossdomain()
@wrappers.tokenize()
def analyzeBlunderMobile():
    return analyzeBlunder()
