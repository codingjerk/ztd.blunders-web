
import os

# Yes, this is real hostname and password, but it's guarded by firewall
class database(object):
    host=os.environ.get('DB_HOST')
    dbname=os.environ.get('DB_NAME')
    user=os.environ.get('DB_USER')
    password=os.environ.get('DB_PASSWORD')

    connectionString = "%s %s %s %s" % (
        ("host=%s" % host) if host is not None else "",
        "dbname=%s" % dbname,
        "user=%s" % user,
        ("password=%s" % password) if password is not None else ""
    )

class redis(object):
    host='redis' # docker link
    port=6379
    db=0

class engine(object):
    path = '/opt/stockfish/src/stockfish'
    time = 1000

class app(object):
    name = 'Chess Blunders',
    title = '%s - endless database of chess puzzles' % name

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
    GRANDMASTERS = "Grandmasters"
    RATINGABOUTX = "Rating about X"
    USERLEVEL = "User level"

class time(object):
    MINUTE = 60
    HOUR = 60 * 60
    DAY = 60 * 60 * 24

class comment(object):
    MAX_SIZE = 500
