class Roles:
    ADMIN = 0
    USER = 3

class TaskTypes:
    RATED = 'rated'
    EXPLORE = 'explore'

"""Decorator, that calls function on module import"""
def init(func):
    func();
    return func

def jsonifyBlunder(data):
    return {
        'status': 'ok',
        'data': {
            'id': str(data['_id']),
            'pgn_id': str(data['pgn_id']),
            'move_index': data['move_index'],

            'forcedLine': data['forcedLine'],
            'pv': data['pv'],

            'fenBefore': data['fenBefore'],
            'blunderMove': data['blunderMove'],

            'elo': data['elo']
        }

    }
    