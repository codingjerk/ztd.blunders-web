
engine_path = '/opt/stockfish/src/stockfish'
engine_time = 5000

class tasks(object):
    RATED = 'rated'
    EXPLORE = 'explore'
    PACK = 'pack'

class roles(object):
    ADMIN = 0
    USER = 3

class pack_type(object):
    RANDOM = "Random"
    MATEINN = "Mate in N"
    OPENING = "Opening"
    ENDGAME = "Endgame"
    PROMOTION = "Promotion"
    CLOSEDGAME = "Closed game"
