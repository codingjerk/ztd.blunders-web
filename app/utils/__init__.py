"""Decorator, that calls function on module import"""
def init(func):
    func();
    return func

def jsonifyBlunder(data):
    return {
        'id': str(data['_id']),
        'pgn_id': str(data['pgn_id']),
        'move_index': data['move_index'],

        'forcedLine': data['forcedLine'],
        'pv': data['pv'],

        'fenBefore': data['fenBefore'],
        'blunderMove': data['blunderMove'],

        'elo': data['elo'],
        
        'status': 'ok',
    }