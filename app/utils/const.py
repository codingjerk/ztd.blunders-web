
# Yes, this is real hostname and password, but it's guarded by firewall
class database(object):
    host="blunders-master.clotqfqonef0.eu-west-1.rds.amazonaws.com"
    dbname="chessdb"
    user="postgres"
    password="chessdb"

class engine(object):
    path = '/opt/stockfish/src/stockfish'
    time = 1000

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
