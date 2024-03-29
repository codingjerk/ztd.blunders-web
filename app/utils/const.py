
import os

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

class fluentd(object):
    label='app'
    host=os.environ.get('FLUENTD_HOST')
    port=int(os.environ.get('FLUENTD_PORT'))

class engine(object):
    path = '/opt/stockfish-8-linux/Linux/stockfish_8_x64'
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
    DIFFICULTYLEVELS = "Difficulty levels"
    REPLAYFAILED = "Replay failed"

class pack(object):
    DEFAULT_SIZE = 25

class time(object):
    MINUTE = 60
    HOUR = 60 * 60
    DAY = 60 * 60 * 24

class comment(object):
    MAX_SIZE = 500

class email_validation(object):
    limit = 3
    sender_email = "ztd.team.dev@gmail.com"
    credential_path = "/home/blunders/ztd.blunders-web/gmail_api_token.key" # For Gmail
