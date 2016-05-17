
# Yes, this is real hostname and password, but it's guarded by firewall
class database(object):
    host=None
    dbname="chessdb"
    user="postgres"
    password=None

    connectionString = "%s %s %s %s" % (
        ("host=%s" % host) if host is not None else "",
        "dbname=%s" % dbname,
        "user=%s" % user,
        ("password=%s" % password) if password is not None else ""
    )

class redis(object):
    host='127.0.0.1'
    port=6379
    db=0

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

class time(object):
    MINUTE = 60
    HOUR = 60 * 60
    DAY = 60 * 60 * 24
