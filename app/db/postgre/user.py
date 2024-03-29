from uuid import uuid4

from app.utils import chess, const, cache
from app.db.postgre import core

from psycopg2 import IntegrityError

def authorize(username, hash):
    if username is None:
        return False

    with core.PostgreConnection('r') as connection:
        connection.cursor.execute("""
            SELECT COUNT(1)
            FROM users AS u
            WHERE u.username = %s AND u.password = %s;
            """, (username, hash)
        )

        (count,) = connection.cursor.fetchone()

        success = (count == 1)

    if success:
        with core.PostgreConnection('w') as connection:
            connection.cursor.execute("""
                UPDATE users
                SET last_login = NOW()
                WHERE username = %s;
                """, (username,)
            )

    return success

def getUserIdByToken(token):
    with core.PostgreConnection('r') as connection:
        connection.cursor.execute(
            'SELECT user_id from api_tokens WHERE token = %s;'
            , (token,)
        )

        result = connection.cursor.fetchone()
        if result is None:
            return None

        (userId,) = result
        return userId

def getTokenForUser(username):
    user_id = getUserId(username)
    if user_id is None:
        raise Exception('Getting token for anonymous')

    with core.PostgreConnection('r') as connection:
        connection.cursor.execute(
            'SELECT token from api_tokens WHERE user_id = %s;'
            , (user_id,)
        )

        token = connection.cursor.fetchone()

    if token:
        return token[0]

    token = uuid4().hex

    with core.PostgreConnection('w') as connection:
        connection.cursor.execute("""
            INSERT INTO api_tokens (user_id, token)
            VALUES (
                %s,
                %s
            );
            """, (user_id, token)
        )

        if connection.cursor.rowcount != 1:
            raise Exception('Failed to save token')

    return token


def getUserField(user_id, field):
    with core.PostgreConnection('r') as connection:
        connection.cursor.execute(
            'SELECT ' + field + ' from users WHERE id = %s;'
            , (user_id,)
        )

        return connection.cursor.fetchone()[0]

def getRating(user_id):
    if user_id is None:
        return 0

    return getUserField(user_id, 'elo')

def getSalt(username):
    if username is None:
        raise Exception('Getting salt for None user!')

    user_id = getUserId(username)

    return getUserField(user_id, 'salt')

def getUserId(username):
    if username is None:
        raise Exception('postre.getUserId for anonim')

    with core.PostgreConnection('r') as connection:
        connection.cursor.execute(
            'SELECT id from users WHERE username = %s;'
            , (username,)
        )

        return connection.cursor.fetchone()[0]

def getUsernameById(user_id):
    with core.PostgreConnection('r') as connection:
        connection.cursor.execute("""
            SELECT username
            FROM users
            WHERE id = %s;
            """, (user_id,)
        )

        result = connection.cursor.fetchone()
        if result is None:
            raise Exception('User with id %d is not exist' % user_id)

        return result[0]

def setRatingUser(user_id, elo):
    if user_id is None:
        raise Exception('postre.setRatingUser for anonim')

    with core.PostgreConnection('w') as connection:
        connection.cursor.execute("""
            UPDATE users
            SET elo = %s
            WHERE id = %s;
            """, (elo, user_id)
        )

        if connection.cursor.rowcount != 1:
            raise Exception('Failed to change rating for user')

def signupUser(username, salt, hash, email):
    with core.PostgreConnection('w') as connection:
        try:
            connection.cursor.execute("""
                INSERT INTO users (username, salt, password, role, email, registration, last_login)
                VALUES (%s, %s, %s, %s, %s, NOW(), NOW());
                """, (username, salt, hash, const.roles.USER, email)
            )
        except IntegrityError:
            return {
                'status': 'error',
                'field': 'username',
                'message': 'Already registered'
            }

        success = (connection.cursor.rowcount == 1)

        if not success:
            return {
                'status': 'error',
                'message': "Unable to register user"
            }

    return {'status': 'ok'}

def getBlunderFavoritesCount(user_id):
    with core.PostgreConnection('r') as connection:
        connection.cursor.execute("""
            SELECT COUNT(id)
            FROM blunder_favorites AS f
            WHERE f.user_id = %s"""
            , (user_id,)
        )

        if connection.cursor.rowcount != 1:
            return {
                'status': 'error',
                'message': 'Error when counting favorites for user'
            }

        (total,) = connection.cursor.fetchone()

    return total

def lastUserActivity(username, format):
    with core.PostgreConnection('r') as connection:
        connection.cursor.execute("""
            SELECT u.username,
                   TO_CHAR(act.last_activity, %s)
            FROM vw_activities AS act
            INNER JOIN users as u
                ON act.user_id = u.id
            WHERE u.username = %s;"""
            , (format, username)
        )

        (_, last_activity) = connection.cursor.fetchone()

        return last_activity

def getCommentsByUserCount(user_id):
    with core.PostgreConnection('r') as connection:
        connection.cursor.execute("""
            SELECT COUNT(id)
            FROM blunder_comments AS c
            WHERE c.user_id = %s"""
            , (user_id,)
        )

        if connection.cursor.rowcount != 1:
            return {
                'status': 'error',
                'message': 'Error when counting comments for user'
            }

        (total,) = connection.cursor.fetchone()

    return total

def getCommentsByUser(user_id, offset, limit):
    with core.PostgreConnection('r') as connection:
        connection.cursor.execute("""
            SELECT c.blunder_id,
                   c.date,
                   c.comment
            FROM blunder_comments AS c
            WHERE c.user_id = %s
            ORDER BY c.date DESC
            LIMIT %s OFFSET %s"""
            , (user_id, limit, offset,)
        )

        data = connection.cursor.fetchall()

        comments = [
            {
                "blunder_id": blunder_id,
                "date": date,
                "text": text
            }
            for (blunder_id, date, text) in data
        ]

    return comments

def getBlunderHistoryCount(user_id):
    with core.PostgreConnection('r') as connection:
        connection.cursor.execute("""
            SELECT COUNT(id)
            FROM blunder_history AS h
            WHERE h.user_id = %s"""
            , (user_id,)
        )

        if connection.cursor.rowcount != 1:
            return {
                'status': 'error',
                'message': 'Error when counting blunders for user'
            }

        (total,) = connection.cursor.fetchone()

    return total

def getUserProfile(username):
    with core.PostgreConnection('r') as connection:
        connection.cursor.execute("""
            SELECT u.id,
                   u.username,
                   u.elo
            FROM users AS u
            WHERE u.username = %s;"""
            , (username,)
        )

        if connection.cursor.rowcount != 1:
            return {
                'status': 'error',
                'message': 'Trying to get not exist user with name %s' % username
            }

        (user_id, username, user_elo) = connection.cursor.fetchone()

    with core.PostgreConnection('r') as connection:
        connection.cursor.execute("""
            SELECT SUM(bcv.vote)
            FROM blunder_comments as bc INNER JOIN blunder_comments_votes as bcv
                ON bc.id = bcv.comment_id WHERE bc.user_id = %s;"""
            , (user_id,)
        )

        (commentLikeSum,) = connection.cursor.fetchone()
        if commentLikeSum is None:
            commentLikeSum = 0

    with core.PostgreConnection('r') as connection:
        connection.cursor.execute("""
             SELECT COUNT(id)
             FROM blunder_comments_votes AS bvc
                WHERE bvc.user_id = %s;"""
            , (user_id,)
        )

        (commentVoteSum,) = connection.cursor.fetchone()
        if commentVoteSum is None:
            commentVoteSum = 0

    with core.PostgreConnection('r') as connection:
        connection.cursor.execute("""
             SELECT COUNT(id)
             FROM blunder_votes AS bv
                WHERE bv.user_id = %s;"""
            , (user_id,)
        )

        (voteSum,) = connection.cursor.fetchone()
        if voteSum is None:
            voteSum = 0

    favoriteCount = getBlunderFavoritesCount(user_id)
    commentCount = getCommentsByUserCount(user_id)

    karma = 10 + commentLikeSum * 5 + commentCount * 2 + voteSum + favoriteCount + commentVoteSum

    userJoinDate = getUserField(user_id, "to_char(registration, 'Month DD, YYYY')")

    userLastActivity = lastUserActivity(username, 'Month DD, YYYY')

    return {
        'status': 'ok',
        'data': {
            'user-rating-value':     user_elo,
            'user-karma-value':      karma,
            'username-value':        username,
            'user-join-value':       userJoinDate,
            'user-last-activity-value': userLastActivity
        }
    }

def getBlundersStatistic(username):
    with core.PostgreConnection('r') as connection:
        connection.cursor.execute("""
            SELECT u.id,
                   COUNT(b.id) as total,
                   COUNT(b.id) FILTER (WHERE b.result = 1) as solved,
                   COUNT(b.id) FILTER (WHERE b.result = 0) as failed
            FROM users AS u INNER JOIN blunder_history AS b ON u.id = b.user_id
            GROUP BY u.id, u.elo HAVING u.username = %s;"""
            , (username,)
        )

        if connection.cursor.rowcount != 1: # New user, no records in blunder_history
            total, solved, failed = 0, 0, 0
        else:
            (_1, total, solved, failed) = connection.cursor.fetchone() #pylint: disable=unused-variable

    return {
        'status': 'ok',
        'data': {
            'username': username,
            'failed-blunders-value': failed,
            'total-blunders-value':  total,
            'solved-blunders-value': solved
        }
    }

@cache.cached('ratingByDate', const.time.HOUR)
def getRatingByDate(username, interval):
    user_id = getUserId(username)

    if interval == 'all':
        query = """
            SELECT TO_CHAR(b.date_finish, 'YYYY/MM/DD 12:00') AS date,
                   AVG(b.user_elo)
            FROM blunder_history AS b
            GROUP BY date, b.user_id
            HAVING b.user_id = %s
            ORDER BY date ASC;"""
    elif interval == 'last-month':  # TODO: NOW() - INTERVAL 1 MONTH -> use date_trunct to set to midnight?
        query = """
            SELECT TO_CHAR(b.date_finish, 'YYYY/MM/DD 12:00') AS date,
                   AVG(b.user_elo)
            FROM blunder_history AS b
            WHERE b.date_finish > NOW() - INTERVAL '1 MONTH'
            GROUP BY date, b.user_id
            HAVING b.user_id = %s
            ORDER BY date ASC;"""
    else:
        return {
            'status': 'error',
            'message': 'Error value for interval parameter: %s' % interval
        }

    with core.PostgreConnection('r') as connection:
        connection.cursor.execute(query, (user_id,))

        data = connection.cursor.fetchall()
        rating = [[date, int(elo)] for (date, elo) in data]

    return {
        'status': 'ok',
        'username': username,
        'data' : {
            'rating-statistic': rating
        }
    }

@cache.cached('blundersByDate', const.time.HOUR)
def getBlundersByDate(username, interval):
    user_id = getUserId(username)

    if interval == 'all':
        query = """
            SELECT TO_CHAR(b.date_finish, 'YYYY/MM/DD 12:00') AS date,
                   COUNT(b.id) FILTER (WHERE b.result = 1) as solved,
                   COUNT(b.id) FILTER (WHERE b.result = 0) as failed
            FROM blunder_history AS b
            GROUP BY date, b.user_id
            HAVING b.user_id = %s
            ORDER BY date ASC"""
    elif interval == 'last-month': # TODO: NOW() - INTERVAL 1 MONTH -> use date_trunct to set to midnight?
        query = """
            SELECT TO_CHAR(b.date_finish, 'YYYY/MM/DD 12:00') AS date,
                   COUNT(b.id) FILTER (WHERE b.result = 1) as solved,
                   COUNT(b.id) FILTER (WHERE b.result = 0) as failed
            FROM blunder_history AS b
            WHERE b.date_finish > NOW() - INTERVAL '1 MONTH'
            GROUP BY date, b.user_id
            HAVING b.user_id = %s
            ORDER BY date ASC"""
    else:
        return {
            'status': 'error',
            'message': 'Error value for interval parameter: %s' % interval
        }

    with core.PostgreConnection('r') as connection:
        connection.cursor.execute(query, (user_id,))

        data = connection.cursor.fetchall()

        solved = [[date, solved] for (date, solved, _1) in data]  #pylint: disable=unused-variable
        failed = [[date, failed] for (date, _1, failed) in data]  #pylint: disable=unused-variable

    return {
        'status': 'ok',
        'username': username,
        'data': {
            'blunder-count-statistic': {
                'solved': solved,
                'failed': failed
            }
        }
    }

def validateUserGet(email):
    with core.PostgreConnection('r') as connection:
        connection.cursor.execute("""
            SELECT uv.count_tries,
                   uv.code,
                   uv.date_create,
                   uv.date_update
            FROM user_validations AS uv
            WHERE uv.email = %s;""", (email,)
        )

        if connection.cursor.rowcount == 0:
            return None

        if connection.cursor.rowcount > 1:
            raise Exception("Multiple records for one email")

        result = connection.cursor.fetchall()[0]

    return result

def validateUserCreate(email, code):
    with core.PostgreConnection('w') as connection:
        try:
            connection.cursor.execute("""
                INSERT INTO user_validations (email, code)
                VALUES (%s, %s);
                """, (email, code)
            )
        except IntegrityError:
            return False

        success = (connection.cursor.rowcount == 1)

        if not success:
            return False

    return True

def validateUserIncrement(email):
    with core.PostgreConnection('w') as connection:
        try:
            connection.cursor.execute("""
                UPDATE user_validations
                SET count_tries = count_tries + 1,
                date_update = NOW()
                WHERE email = %s;""", (email,)
            )
        except IntegrityError:
            return False

        success = (connection.cursor.rowcount == 1)

        if not success:
            return False

    return True

def checkUserDuplicate(username, email):
    with core.PostgreConnection('r') as connection:
        connection.cursor.execute("""
            SELECT COUNT(1)
            FROM users AS u
            WHERE u.username = %s OR
                  u.email = %s;"""
            , (username, email)
        )

        (count,) = connection.cursor.fetchone()

    return count
