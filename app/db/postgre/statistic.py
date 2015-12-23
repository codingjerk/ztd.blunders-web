
from app.utils import cache
from app.db.postgre import core,blunder

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

def getRatingByDate(username):
    user_id = getUserId(username)

    with core.PostgreConnection('r') as connection:
        connection.cursor.execute("""
            SELECT TO_CHAR(b.date_finish, 'YYYY/MM/DD HH:00') AS date,
                   AVG(b.user_elo)
            FROM blunder_history AS b
            GROUP BY date, b.user_id HAVING b.user_id = %s;"""
            , (user_id,)
        )

        data = connection.cursor.fetchall()
        rating = [[date, int(elo)] for (date, elo) in data]

    return {
        'status': 'ok',
        'username': username,
        'data' : {
            'rating-statistic': rating
        }
    }

def getBlundersByDate(username):
    user_id = getUserId(username)

    with core.PostgreConnection('r') as connection:
        connection.cursor.execute("""
            SELECT TO_CHAR(b.date_finish, 'YYYY/MM/DD 00:00') AS date,
                   COUNT(b.id) as total,
                   COUNT(b.id) FILTER (WHERE b.result = 1) as solved,
                   COUNT(b.id) FILTER (WHERE b.result = 0) as failed
            FROM blunder_history AS b
            GROUP BY date, b.user_id HAVING b.user_id = %s"""
            , (user_id,)
        )

        data = connection.cursor.fetchall()

        total = [[date, total] for (date, total, _1, _2) in data]     #pylint: disable=unused-variable
        solved = [[date, solved] for (date, _1, solved, _2) in data]  #pylint: disable=unused-variable
        failed = [[date, failed] for (date, _1, _2, failed) in data]  #pylint: disable=unused-variable

    return {
        'status': 'ok',
        'username': username,
        'data': {
            'blunder-count-statistic': {
                'total' : total,
                'solved': solved,
                'failed': failed
            }
        }
    }

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

def getBlundersHistory(user_id, offset, limit):
    with core.PostgreConnection('r') as connection:
        connection.cursor.execute("""
            SELECT h.blunder_id,
                   h.result,
                   h.date_start,
                   h.spent_time
            FROM blunder_history AS h
            WHERE h.user_id = %s
            ORDER BY h.date_start DESC
            LIMIT %s OFFSET %s"""
            , (user_id, limit, offset, )
        )

        data = connection.cursor.fetchall()

        blunders = [
            {
                "blunder_id": blunder_id,
                "result": True if result == 1 else False,
                "date_start": date_start,
                "spent_time": spent_time
            }
            for (blunder_id, result, date_start, spent_time) in data
        ]

    return blunders

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

def getBlundersFavorites(user_id, offset, limit):
    with core.PostgreConnection('r') as connection:
        connection.cursor.execute("""
            SELECT f.blunder_id,
                   f.assign_date
            FROM blunder_favorites AS f
            WHERE f.user_id = %s
            ORDER BY f.assign_date DESC
            LIMIT %s OFFSET %s"""
            , (user_id, limit, offset, )
        )

        data = connection.cursor.fetchall()

        blunders = [
            {
                "blunder_id": blunder_id,
                "assign_date": assign_date
            }
            for (blunder_id, assign_date) in data
        ]

    return blunders

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

def getActiveUsers(interval):
    with core.PostgreConnection('r') as connection:
        connection.cursor.execute("""
            SELECT u.username,
                   act.last_activity
            FROM vw_activities AS act
            INNER JOIN users as u
                ON act.user_id = u.id
            WHERE act.last_activity > NOW() - INTERVAL %s;"""
            , (interval,)
        )

        data = connection.cursor.fetchall()

        users = [username for (username, _1) in data] #pylint: disable=unused-variable

        return users

def getUsersTop(number):
    with core.PostgreConnection('r') as connection:
        connection.cursor.execute("""
            SELECT u.username,
                   u.elo
            FROM users AS u
            ORDER BY u.elo DESC
            LIMIT %s"""
            , (number,)
        )

        data = connection.cursor.fetchall()

        top = [{'username':username, 'elo':elo} for (username, elo) in data]

    return top

def getUsersCount():
    with core.PostgreConnection('r') as connection:
        connection.cursor.execute("""
                SELECT COUNT(id)
                FROM users AS u"""
            )
        (users_registered_value, ) = connection.cursor.fetchone()

    users_day = getActiveUsers('1 HOUR')
    users_week = getActiveUsers('1 WEEK')

    return {
        'status': 'ok',
        'data': {
            "users-registered-value": users_registered_value,
            "users-online-value": len(users_day),
            "users-active-value": len(users_week)
        }
    }

@cache.cached('usersByRating','hour')
def getUsersByRating(interval):
    with core.PostgreConnection('r') as connection:
        connection.cursor.execute("""
            SELECT u.elo - MOD(u.elo, %s) AS elo_category,
                   COUNT(u.id)
            FROM users AS u
            GROUP BY elo_category;"""
            , (interval,)
        )

        data = connection.cursor.fetchall()

        distribution = [[elo_category, count] for (elo_category, count) in data]

    return {
        'status': 'ok',
        'data': {
            'users-rating-distribution': distribution
        }
    }

def saveFeedback(message):
    if len(message.strip()) == 0:
        return {
            'status': 'error',
            'message': "Can't store empty feedback"
        }

    if len(message) >= 100 * 50:
        return {
            'status': 'error',
            'message': "Message too long"
        }

    with core.PostgreConnection('w') as connection:
        connection.cursor.execute("""
            INSERT INTO feedback (message)
            VALUES (%s);
            """, (message,)
        )

        if connection.cursor.rowcount != 1:
            return {
                'status': 'error',
                'message': "Can't store feedback"
            }

    return {
        'status': 'ok'
    }

@cache.cached('blundersByRating','day')
def getBlundersByRating(interval):
    with core.PostgreConnection('r') as connection:
        connection.cursor.execute("""
            SELECT (b.elo - b.elo %% %s) AS elo_category,
                   COUNT(b.id) as count FROM blunders AS b
            GROUP BY elo_category
            ORDER BY elo_category;"""
            , (interval,)
        )

        data = connection.cursor.fetchall()

        distribution = [[elo_category, count] for (elo_category, count) in data]

    return {
        'status': 'ok',
        'data': {
            'blunders-rating-distribution' : distribution
        }
    }

def getCommentsByUser(username, offset, limit):
    try:
        user_id = postgre.user.getUserId(username)
    except Exception:
        return {
            'status': 'error',
            'message': 'Trying to get not exist user with name %s' % username
        }

    total = postgre.statistic.getCommentsByUserCount(user_id)
    comments = postgre.statistic.getCommentsByUser(user_id, offset, limit)

    result = {}
    for comment in comments:
        blunder_id = comment['blunder_id']

        # TODO: Don't send many requests for every blunder
        blunder_info = postgre.blunder.getBlunderById(blunder_id)
        fen = chess.blunderStartPosition(blunder_info['fen_before'], blunder_info['blunder_move'])

        if blunder_id not in result:
            result[blunder_id] = {
                "blunder_id": blunder_id,
                "fen": fen,
                "comments": []
            }

        result[blunder_id]['comments'].append(
            {
                "date": comment['date'],
                "text": comment['text']
            }
        )

    return {
        'status': 'ok',
        'username': username,
        'data': {
            "total": total,
            "blunders": result
        }
    }

def getBlundersStatistic():
    return {
        'status': 'ok',
        'data': {
            'total-blunders-value' : blunder.countBlunders()
        }
    }

def getBlundersHistory(username, offset, limit):
    try:
        user_id = postgre.user.getUserId(username)
    except Exception:
        return {
            'status': 'error',
            'message': 'Trying to get not exist user with name %s' % username
        }

    total = postgre.statistic.getBlunderHistoryCount(user_id)
    blunders = postgre.statistic.getBlundersHistory(user_id, offset, limit)

    result = []
    for blunder in blunders:
        blunder_info = postgre.blunder.getBlunderById(blunder['blunder_id'])
        fen = chess.blunderStartPosition(blunder_info['fen_before'], blunder_info['blunder_move'])

        result.append({
            "blunder_id": blunder['blunder_id'],
            "fen": fen,
            "result": blunder['result'],
            "date_start": blunder['date_start'],
            "spent_time": blunder['spent_time']
        })

    return {
        'status': 'ok',
        'username': username,
        'data': {
            "total": total,
            "blunders": result
        }
    }

def getBlundersFavorites(username, offset, limit):
    try:
        user_id = postgre.user.getUserId(username)
    except Exception:
        return {
            'status': 'error',
            'message': 'Trying to get not exist user with name %s' % username
        }

    total = postgre.statistic.getBlunderFavoritesCount(user_id)
    blunders = postgre.statistic.getBlundersFavorites(user_id, offset, limit)

    result = []
    for blunder in blunders:
        blunder_info = postgre.blunder.getBlunderById(blunder['blunder_id'])
        fen = chess.blunderStartPosition(blunder_info['fen_before'], blunder_info['blunder_move'])

        result.append({
            "blunder_id": blunder['blunder_id'],
            "fen": fen,
            "assign_date": blunder['assign_date']
        })

    return {
        'status': 'ok',
        'username': username,
        'data': {
            "total": total,
            "blunders": result
        }
    }