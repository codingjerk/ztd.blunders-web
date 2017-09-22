from json import dumps

from app.db.postgre import core,user,game
from app.utils import const,chess

# Get random blunder from database
def getRandomBlunder():
    with core.PostgreConnection('r') as connection:
        connection.cursor.execute("""
            SELECT * FROM GET_RANDOM_BLUNDER();
            """
        )

        if connection.cursor.rowcount != 1:
            raise Exception('Fail to get random blunder')

        (
            id,
            forced_line,
            elo,
            fen_before,
            blunder_move,
            move_index,
            game_id
        ) = connection.cursor.fetchone()

    return {
        'id': id,
        'forced_line': forced_line,
        'elo': elo,
        'fen_before': fen_before,
        'blunder_move': blunder_move,
        'move_index': move_index,
        'game_id': game_id
    }


# Assign blunder to user
def assignBlunderTask(user_id, blunder_id, type):
    if user_id is None:
        return #TODO: value or exception?

    with core.PostgreConnection('w') as connection:
        connection.cursor.execute("""
            INSERT INTO blunder_tasks (user_id, blunder_id, type_id)
            VALUES (
                %s,
                %s,
                (SELECT id FROM blunder_task_type WHERE name = %s)
            );
            """, (user_id, blunder_id, type)
        )

        if connection.cursor.rowcount != 1:
            raise Exception('Failed to assign new blunder')

def isBlunderTaskExist(user_id, blunder_id, type):
    with core.PostgreConnection('r') as connection:
        connection.cursor.execute("""
            SELECT bt.id
            FROM blunder_tasks as bt
            WHERE bt.user_id = %s AND
                  bt.blunder_id = %s AND
                  bt.type_id =
                      (
                       SELECT btt.id
                       FROM blunder_task_type AS btt
                       WHERE btt.name = %s
                      )
            """, (user_id, blunder_id, type)
        )

        if connection.cursor.rowcount != 0:
            return True

        return False

# Get time, when blunder was assigned to user
def getTaskStartDate(user_id, blunder_id, type):
    if user_id is None:
        return #TODO: value or exception?

    with core.PostgreConnection('r') as connection:
        connection.cursor.execute(
            """SELECT assign_date
               FROM blunder_tasks AS bt
               INNER JOIN blunder_task_type AS btt
                   ON bt.type_id = btt.id
               WHERE bt.user_id = %s
                 AND bt.blunder_id = %s
                 AND btt.name = %s;"""
            , (user_id, blunder_id, type)
        )

        if connection.cursor.rowcount != 1:
            return None

        (assign_date,) = connection.cursor.fetchone()

        return assign_date

#pylint: disable=too-many-arguments
def saveBlunderHistory(user_id, user_elo, blunder_id, blunder_elo, success, userLine, date_start, spent_time):
    if user_id is None:
        raise Exception('postre.saveBlunderHistory for anonim')
    if date_start is None:
        raise Exception('postre.saveBlunderHistory date start is not defined')

    result = 1 if success else 0
    if success:
        userLine = []

    with core.PostgreConnection('w') as connection:
        connection.cursor.execute("""
            INSERT INTO blunder_history
            (user_id, blunder_id, result, user_elo, blunder_elo, user_line, date_start, spent_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            """,
            (user_id, blunder_id, result, user_elo, blunder_elo, userLine, date_start, spent_time)
        )

        if connection.cursor.rowcount != 1:
            raise Exception('Failed to write into blunder history table')

def closeBlunderTask(user_id, blunder_id, type):
    if user_id is None:
        return #TODO: value or exception?

    with core.PostgreConnection('w') as connection:
        connection.cursor.execute("""
            DELETE FROM blunder_tasks
            WHERE user_id = %s
                AND blunder_id = %s
                AND type_id = (SELECT id FROM blunder_task_type WHERE name = %s);
            """, (user_id, blunder_id, type)
        )

        return connection.cursor.rowcount == 1


def setRatingBlunder(blunder_id, newBlunderElo):
    if blunder_id is None:
        raise Exception('postre.setRatingBlunder for anonim')

    with core.PostgreConnection('w') as connection:
        connection.cursor.execute("""
            UPDATE blunders
            SET elo = %s
            WHERE id = %s;
            """, (newBlunderElo, blunder_id)
        )

        if connection.cursor.rowcount != 1:
            raise Exception('Failed to change rating for blunder')

def getBlunderById(blunder_id):
    with core.PostgreConnection('r') as connection:
        connection.cursor.execute("""
            SELECT b.id, b.forced_line, b.elo, b.fen_before, b.blunder_move, b.move_index, b.game_id
            FROM blunders AS b
            WHERE b.id = %s
            """, (blunder_id,)
        )

        if connection.cursor.rowcount != 1:
            return None

        (
            id,
            forced_line,
            elo,
            fen_before,
            blunder_move,
            move_index,
            game_id
        ) = connection.cursor.fetchone()

        return {
            'id': id,
            'forced_line': forced_line,
            'elo': elo,
            'fen_before': fen_before,
            'blunder_move': blunder_move,
            'move_index': move_index,
            'game_id': game_id
        }

def gameShortInfo(data):
    whitePlayer = 'Unknown'
    whiteElo = '?'
    blackPlayer = 'Unknown'
    blackElo = '?'

    if data is not None:
        if 'white' in data and data['white'] is not None:
            whitePlayer = data['white']

        if 'white_elo' in data and data['white_elo'] is not None:
            whiteElo    = data['white_elo']

        if 'black' in data and data['black'] is not None:
            blackPlayer = data['black']

        if 'black_elo' in data and data['black_elo'] is not None:
            blackElo    = data['black_elo']

    return {
        'White': whitePlayer,
        'WhiteElo': whiteElo,
        'Black': blackPlayer,
        'BlackElo': blackElo,
    }

def getBlunderInfoById(user_id, blunder_id):
    blunder = getBlunderById(blunder_id)

    if blunder is None:
        return None

    elo = blunder['elo']
    comments = getBlunderComments(blunder_id)
    favorites = getBlunderPopularity(blunder_id)
    likes, dislikes = getBlunderVotes(blunder_id)
    gameInfo = gameShortInfo(game.getGameById(blunder['game_id']))

    result = {
        'elo': elo,
        'comments': comments,
        'likes': likes,
        'dislikes': dislikes,
        'favorites': favorites,
        'game-info': gameInfo,
        'history': getCommonHistory(blunder_id, blunder)
    }

    if user_id != None:
        result['my'] = {
            'favorite': isFavorite(user_id, blunder_id),
            'vote': getUserVote(user_id, blunder_id),
            'history': getUserHistory(user_id, blunder)
        }

    # Back compatibility, TODO: remove in the future
    result['totalTries'] = result['history']['total']
    result['successTries'] = result['history']['success']

    return result

def getAssignedBlunder(user_id, type):
    if user_id is None:
        return None

    with core.PostgreConnection('r') as connection:
        connection.cursor.execute("""
            SELECT bt.blunder_id
            FROM blunder_tasks AS bt
            INNER JOIN blunder_task_type AS btt
                ON bt.type_id = btt.id
            WHERE bt.user_id = %s
                AND btt.name = %s;
            """, (user_id, type)
        )

        if connection.cursor.rowcount != 1:
            return None

        (blunder_id,) = connection.cursor.fetchone()

        return getBlunderById(blunder_id)

# Some variations can be obsolete and not relevant due to solution line change
# We need to filter such variations to not confuse user with obsolete variations
def variationSanity(variations, blunder):
    result = [
        variation
        for variation in variations
        if (not chess.mismatchCheck(blunder['blunder_move'], blunder['forced_line'], variation['line'])) and
           (not chess.compareLines(blunder['blunder_move'], blunder['forced_line'], variation['line']))
    ]

    for variation in result: # Remove first move because it's blunder move
        variation['line'] = variation['line'][1:]

    return result

def getCommonHistory(blunder_id, blunder):
    with core.PostgreConnection('r') as connection:
        connection.cursor.execute("""
            SELECT bh.user_line,
                   COUNT(1) AS times
            FROM blunder_history as bh
            WHERE bh.blunder_id = %s
            GROUP BY bh.user_line
            """, (blunder_id,)
        )

        history = connection.cursor.fetchall()

        success = [
            {'line': 'correct_line', 'times': times }
            for (line, times) in history
            if len(line) == 0
        ]

        if len(success) > 1:
            raise Exception('Invalid data received from database')

        failures = variationSanity([
            {'line': line, 'times': times }
            for (line, times) in history
            if len(line) != 0
        ], blunder)

        success_times = success[0]['times'] if len(success) > 0 else 0
        failure_times = sum(variation['times'] for variation in failures)

        return {
            'total': success_times + failure_times,
            'success': success_times,
            'failures': failures
        }


def getBlunderComments(blunder_id):
    result = []

    with core.PostgreConnection('r') as connection:
        connection.cursor.execute("""
            SELECT id, date, parent_id, user_id, comment
            FROM blunder_comments
            WHERE blunder_id = %s
            """, (blunder_id,)
        )

        comments = connection.cursor.fetchall()

        for comment in comments:
            comment_id, date, parent_id, user_id, text = comment
            username = user.getUsernameById(user_id)
            likes, dislikes = getBlunderCommentVotes(comment_id)

            pythonComment = {
                'id': comment_id,
                'date': date,
                'parent_id': parent_id if parent_id is not None else 0,
                'username': username,
                'text': text,
                'likes': likes,
                'dislikes': dislikes,
            }

            result.append(pythonComment)

    return result

def isFavorite(user_id, blunder_id):
    if user_id is None:
        return False

    with core.PostgreConnection('r') as connection:
        connection.cursor.execute(
            """SELECT * from blunder_favorites
               WHERE blunder_id = %s
                 AND user_id = %s;"""
            , (blunder_id, user_id)
        )

        if connection.cursor.rowcount == 1:
            return True
        return False

def getUserVote(user_id, blunder_id):
    if user_id is None:
        return False

    with core.PostgreConnection('r') as connection:
        connection.cursor.execute(
            """SELECT vote from blunder_votes
               WHERE blunder_id = %s
                 AND user_id = %s;"""
            , (blunder_id, user_id)
        )

        if connection.cursor.rowcount == 1:
            return connection.cursor.fetchone()[0]

    return 0

# Returns all user's history for solving given blunder
def getUserHistory(user_id, blunder):
    if user_id is None:
        return False

    blunder_id = blunder['id']

    with core.PostgreConnection('r') as connection:
        connection.cursor.execute(
            """SELECT bh.result AS score,
                      bh.user_line AS user_line,
                      bh.date_finish AS date_finish
               FROM blunder_history AS bh
               WHERE bh.user_id = %s
                  AND bh.blunder_id=%s;
"""
            , (user_id, blunder_id)
        )

        history = connection.cursor.fetchall()
        result = [ {
                'score': score,
                'date': date,
                'line': line if line != '' else correct_line
            } for (score, line, date) in history
        ]

        result = variationSanity(result, blunder)

        return result

def getBlunderPopularity(blunder_id):
    with core.PostgreConnection('r') as connection:
        connection.cursor.execute(
            """SELECT *
               FROM blunder_favorites
               WHERE blunder_id = %s;"""
            , (blunder_id,)
        )

        return connection.cursor.rowcount

def getBlunderVotes(blunder_id):
    with core.PostgreConnection('r') as connection:
        connection.cursor.execute(
            """SELECT *
               FROM blunder_votes
               WHERE blunder_id = %s and vote = 1;"""
            , (blunder_id,)
        )

        likes = connection.cursor.rowcount

    with core.PostgreConnection('r') as connection:
        connection.cursor.execute(
            """SELECT *
               FROM blunder_votes
               WHERE blunder_id = %s AND vote = -1;"""
            , (blunder_id,)
        )

        dislikes = connection.cursor.rowcount

    return likes, dislikes

def getBlunderCommentVotes(comment_id):
    with core.PostgreConnection('r') as connection:
        connection.cursor.execute(
            """SELECT *
               FROM blunder_comments_votes
               WHERE comment_id = %s
                 AND vote = 1;"""
            , (comment_id,)
        )

        likes = connection.cursor.rowcount

    with core.PostgreConnection('r') as connection:
        connection.cursor.execute(
            """SELECT *
               FROM blunder_comments_votes
               WHERE comment_id = %s
                 AND vote = -1;"""
            , (comment_id,)
        )

        dislikes = connection.cursor.rowcount

    return likes, dislikes

def voteBlunder(user_id, blunder_id, vote):
    if user_id is None:
        return False

    with core.PostgreConnection('w') as connection:
        connection.cursor.execute(
            """UPDATE blunder_votes
               SET vote = %s, assign_date = NOW()
               WHERE blunder_id = %s
                 AND user_id = %s;"""
            , (vote, blunder_id, user_id)
        )

        count = connection.cursor.rowcount

        if count == 1:
            return True

    with core.PostgreConnection('w') as connection:
        connection.cursor.execute(
            """INSERT INTO blunder_votes(user_id, blunder_id, vote)
               VALUES (%s, %s, %s);"""
            , (user_id, blunder_id, vote)
        )

        if connection.cursor.rowcount != 1:
            raise Exception(
                'Can not add vote for user id %s with blunder id %s' %
                (user_id, blunder_id)
            )

    return True

def favoriteBlunder(user_id, blunder_id):
    if user_id is None:
        return False

    with core.PostgreConnection('w') as connection:
        connection.cursor.execute(
            """DELETE FROM blunder_favorites
               WHERE blunder_id = %s
                 AND user_id = %s;"""
            , (blunder_id, user_id)
        )

        count = connection.cursor.rowcount

        if count == 1:
            return True

    with core.PostgreConnection('w') as connection:
        connection.cursor.execute(
            """INSERT INTO blunder_favorites(user_id, blunder_id)
               VALUES (%s,%s);"""
            , (user_id, blunder_id)
        )

        if connection.cursor.rowcount != 1:
            raise Exception(
                'Error inserting favorite for user id %s with blunder id %s' %
                (user_id, blunder_id)
            )

    return True

def commentBlunder(user_id, blunder_id, parent_id, user_input):
    if user_id is None:
        return False

    with core.PostgreConnection('w') as connection:
        connection.cursor.execute(
            """INSERT INTO blunder_comments(user_id, blunder_id, parent_id, comment)
               VALUES (%s, %s, %s, %s);"""
            , (user_id, blunder_id, parent_id, user_input)
        )

        if connection.cursor.rowcount != 1:
            raise Exception('Failed to comment')

    return True

def voteBlunderComment(user_id, comment_id, vote):
    if user_id is None:
        return False

    with core.PostgreConnection('w') as connection:
        connection.cursor.execute(
            """UPDATE blunder_comments_votes
               SET vote = %s, assign_date = NOW()
               WHERE comment_id = %s
                 AND user_id = %s;"""
            , (vote, comment_id, user_id)
        )

        if connection.cursor.rowcount  == 1:
            return True

    with core.PostgreConnection('w') as connection:
        connection.cursor.execute(
            """INSERT INTO blunder_comments_votes(user_id, comment_id, vote)
               VALUES (%s, %s, %s);"""
            , (user_id, comment_id, vote)
        )

        if connection.cursor.rowcount != 1:
            raise Exception('Can not add comment vote for user id %s' % (user_id))

    return True

def blunderCommentAuthor(comment_id):
    with core.PostgreConnection('r') as connection:
        connection.cursor.execute(
            """SELECT user_id
               FROM blunder_comments
               WHERE id = %s;"""
            , (comment_id,)
        )

        if connection.cursor.rowcount != 1:
            raise Exception('Trying to get not exist comment with id %s' % (comment_id))

        (user_id,) = connection.cursor.fetchone()

        return user_id

def countBlunders():
    with core.PostgreConnection('r') as connection:
        connection.cursor.execute(
            """SELECT c.blunders_upper_limit - c.blunders_lower_limit + 1
               FROM configuration AS c;"""
        )

        if connection.cursor.rowcount != 1:
            raise Exception('Can not count blunders')

        (count,) = connection.cursor.fetchone()

        return count

def getBlunderByTag(tag_name, count):
    with core.PostgreConnection('r') as connection:
        connection.cursor.execute(
            """SELECT bt.blunder_id
               FROM blunder_tags AS bt
               INNER JOIN blunder_tag_type AS btt
                      ON bt.type_id = btt.id
               WHERE btt.name = %s
               ORDER BY RANDOM()
               LIMIT %s;""" , (tag_name, count)
        )

        result = connection.cursor.fetchall()

        return result

def getBlunderByRating(expected_elo, deviation_elo, count):
    with core.PostgreConnection('r') as connection:
        connection.cursor.execute(
            """SELECT b.id
               FROM blunders AS b
               LEFT JOIN (
                   SELECT pb.blunder_id
                   FROM pack_blunders AS pb
                   INNER JOIN packs AS p
                       ON p.id = pb.pack_id
                   WHERE p.type_id = (
                       SELECT pt.id
                       FROM pack_type AS pt
                       WHERE pt.name = %s
                   )
               ) AS ba
                   ON b.id = ba.blunder_id
               WHERE b.elo > %s
                 AND b.elo <= %s
                 AND b.enabled = 1
                 AND ba.blunder_id IS NULL
               LIMIT %s;""" , (const.pack_type.DIFFICULTYLEVELS, expected_elo - deviation_elo/2, expected_elo + deviation_elo/2, count)
        )

        result = connection.cursor.fetchall()

        return result

def getBlunderForReplayFailed(user_id, count):
    forgot_interval = '1 week'

    with core.PostgreConnection('r') as connection:
        connection.cursor.execute(
            """ SELECT grouped.blunder_id
                FROM
                  (SELECT f.blunder_id,
                          sum(f.result) AS success_tries,
                          count(1) AS total_tries,
                          max(f.date_finish) AS date_last
                   FROM
                     (SELECT *
                      FROM
                        (SELECT bh.blunder_id,
                                bh.result,
                                bh.date_finish
                         FROM blunder_history AS bh
                         WHERE bh.user_id = %s) AS history
                      LEFT JOIN
                        (SELECT pb.blunder_id
                         FROM pack_users AS pu
                         INNER JOIN pack_blunders AS pb ON pu.pack_id = pb.pack_id
                         AND pu.user_id = %s) AS CURRENT USING(blunder_id)
                      WHERE current.blunder_id IS NULL) AS f
                   GROUP BY f.blunder_id) AS grouped
                WHERE grouped.success_tries = 0
                  AND grouped.date_last < now() - interval %s
                ORDER BY grouped.date_last
                LIMIT %s;""" , (user_id, user_id, forgot_interval, count)
        )

        result = [
            blunder_id
            for (blunder_id,) in connection.cursor.fetchall()
        ]

        return result

def getAnalyze(blunder_id, user_line, user_move):
    with core.PostgreConnection('r') as connection:
        connection.cursor.execute(
            """SELECT ba.id,
                      ba.engine_line,
                      ba.engine_score,
                      ba.time_ms
               FROM blunder_analyze as ba
               WHERE ba.blunder_id = %s AND
                     ba.user_line = %s AND
                     ba.user_move = %s
            """, (blunder_id, user_line, user_move)
        )

        if connection.cursor.rowcount == 0:
            return None

        if connection.cursor.rowcount > 1:
            raise Exception('Multiple analyse lines for same blunder')

        (analyze_id, engine_line, engine_score, time_ms) = connection.cursor.fetchone()

    with core.PostgreConnection('w') as connection:
        connection.cursor.execute(
            """UPDATE blunder_analyze
               SET reuse_count = reuse_count + 1
               WHERE id = %s;
            """, (analyze_id,)
        )

    return (engine_line, engine_score, time_ms)

def saveAnalyze(user_id, blunder_id, user_line, user_move, engine_line, engine_score, time_ms):
    with core.PostgreConnection('w') as connection:
        connection.cursor.execute(
            """
            INSERT INTO blunder_analyze(
                    created_by,
                    blunder_id,
                    user_line,
                    user_move,
                    engine_line,
                    engine_score,
                    time_ms
                )
            VALUES(%s, %s, %s, %s, %s, %s, %s)
            """,(
                 user_id,
                 blunder_id,
                 user_line,
                 user_move,
                 engine_line,
                 dumps(engine_score),
                 time_ms
                )
        )

        if connection.cursor.rowcount  == 1:
            return True

        return False
