
from app.utils import cache,chess
from app.db.postgre import core,user,blunder

def getRatingByDate(username):
    user_id = user.getUserId(username)

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
    user_id = user.getUserId(username)

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
        user_id = user.getUserId(username)
    except Exception:
        return {
            'status': 'error',
            'message': 'Trying to get not exist user with name %s' % username
        }

    total = user.getCommentsByUserCount(user_id)
    comments = user.getCommentsByUser(user_id, offset, limit)

    result = {}
    for comment in comments:
        blunder_id = comment['blunder_id']

        # TODO: Don't send many requests for every blunder
        blunder_info = blunder.getBlunderById(blunder_id)
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
        user_id = user.getUserId(username)
    except Exception:
        return {
            'status': 'error',
            'message': 'Trying to get not exist user with name %s' % username
        }

    total = user.getBlunderHistoryCount(user_id)
    blunders = user.getBlundersHistory(user_id, offset, limit)

    result = []
    for theblunder in blunders:
        blunder_info = blunder.getBlunderById(theblunder['blunder_id'])
        fen = chess.blunderStartPosition(blunder_info['fen_before'], blunder_info['blunder_move'])

        result.append({
            "blunder_id": theblunder['blunder_id'],
            "fen": fen,
            "result": theblunder['result'],
            "date_start": theblunder['date_start'],
            "spent_time": theblunder['spent_time']
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
        user_id = user.getUserId(username)
    except Exception:
        return {
            'status': 'error',
            'message': 'Trying to get not exist user with name %s' % username
        }

    total = user.getBlunderFavoritesCount(user_id)
    blunders = user.getBlundersFavorites(user_id, offset, limit)

    result = []
    for theblunder in blunders:
        blunder_info = blunder.getBlunderById(theblunder['blunder_id'])
        fen = chess.blunderStartPosition(blunder_info['fen_before'], blunder_info['blunder_move'])

        result.append({
            "blunder_id": theblunder['blunder_id'],
            "fen": fen,
            "assign_date": theblunder['assign_date']
        })

    return {
        'status': 'ok',
        'username': username,
        'data': {
            "total": total,
            "blunders": result
        }
    }