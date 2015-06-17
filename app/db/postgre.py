import psycopg2

from app.utils import Roles

class PostgreConnection:
    def __init__(self, type):
        self.type = type
        assert(type in 'rw')

        self.connection = psycopg2.connect('dbname=chessdb user=postgres')
        self.cursor = self.connection.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exception, _1, _2):
        if self.type == 'w':
            if exception is None:
                self.connection.commit()
            else:
                self.connection.rollback()

        self.cursor.close()
        self.connection.close()

def autentithicateUser(username, hash):
    if username is None: return False

    with PostgreConnection('r') as connection:
        connection.cursor.execute("""
            SELECT *
            FROM users 
            WHERE username = %s AND password = %s;
            """, (username, hash)
        )

        users = connection.cursor.fetchall()

        success = len(users) == 1

    if success:
        with PostgreConnection('w') as connection:
            connection.cursor.execute("""
                UPDATE users 
                SET last_login = NOW()
                WHERE username = %s;
                """, (username,)
            )

    return success

def getUserField(user_id, field):
    with PostgreConnection('r') as connection:
        connection.cursor.execute(
            'SELECT ' + field + ' from users WHERE id = %s;'
            , (user_id,)
        )

        return connection.cursor.fetchone()[0]

def getRating(user_id):
    if user_id is None: return 0

    return getUserField(user_id, 'elo')

def getSalt(username):
    if username is None:
        raise Exception('Getting salt for None user!')

    user_id = getUserId(username)

    return getUserField(user_id, 'salt')

def getUserId(username):
    if username is None: 
        raise Exception('postre.getUserId for anonim')

    with PostgreConnection('r') as connection:
        connection.cursor.execute(
            'SELECT id from users WHERE username = %s;'
            , (username,)
        )

        return connection.cursor.fetchone()[0]

def getUsernameById(user_id):
    with PostgreConnection('r') as connection:
        connection.cursor.execute("""
            SELECT username
            FROM users 
            WHERE id = %s;
            """, (user_id,)
        )

        result = connection.cursor.fetchone()
        if result is None: raise Exception('User with id %d is not exist' % user_id)

        return result[0]

def assignBlunderTask(user_id, blunder_id, type):
    if user_id is None: return

    with PostgreConnection('w') as connection:
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

def saveBlunderHistory(user_id, blunder_id, blunder_elo, success, userLine, date_start):
    if user_id is None: 
        raise Exception('postre.saveBlunderHistory for anonim')
    if(date_start is None):
        raise Exception('postre.saveBlunderHistory date start is not defined')

    user_elo = getRating(user_id)
    result = 1 if success else 0

    if success: userLine = ''

    with PostgreConnection('w') as connection:
        connection.cursor.execute("""
            INSERT INTO blunder_history 
                (user_id, blunder_id, result, user_elo, blunder_elo, user_line, date_start)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
            """, (user_id, blunder_id, result, user_elo, blunder_elo, userLine, date_start)
        )

        if connection.cursor.rowcount != 1:
            raise Exception('Failed to assign new blunder')

def closeBlunderTask(user_id, blunder_id, type):
    if user_id is None: return

    with PostgreConnection('w') as connection:
        connection.cursor.execute("""
            DELETE FROM blunder_tasks
            WHERE user_id = %s
                AND blunder_id = %s
                AND type_id = (SELECT id FROM blunder_task_type WHERE name = %s);
            """, (user_id, blunder_id, type)
        )

        return connection.cursor.rowcount == 1

def setRating(user_id, elo):
    if user_id is None: 
        raise Exception('postre.setRating for anonim')

    with PostgreConnection('w') as connection:
        connection.cursor.execute("""
            UPDATE users
            SET elo = %s
            WHERE id = %s;
            """, (elo, user_id)
        )

        if connection.cursor.rowcount != 1:
            raise Exception('Failed to assign new blunder')

def getAssignedBlunder(user_id, type):
    if user_id is None: return None

    with PostgreConnection('r') as connection:
        connection.cursor.execute("""
            SELECT blunder_id
            FROM blunder_tasks AS bt
            INNER JOIN blunder_task_type AS btt
                ON bt.type_id = btt.id
            WHERE bt.user_id = %s 
                AND btt.name = %s;
            """, (user_id, type)
        )

        blunder_id = connection.cursor.fetchone()
        if blunder_id is None: return None

        return blunder_id[0]

def signupUser(username, salt, hash, email):
    # TODO: Validation
    if len(username) < 3: return {
        'status': 'error', 
        'field': 'username', 
        'message': "Username is too short"
    }

    with PostgreConnection('w') as connection:
        try:
            connection.cursor.execute("""
                INSERT INTO users (username, salt, password, role, email, registration, last_login)
                VALUES (%s, %s, %s, %s, %s, NOW(), NOW());
                """, (username, salt, hash, Roles.USER, email)
            )
        except psycopg2.IntegrityError as e:
            return {
                'status': 'error', 
                'field': 'username', 
                'message': 'Already registered'
            }

        success = (connection.cursor.rowcount == 1)

        if not success: return {
            'status': 'error', 
            'message': "Unable to register user"
        }

    return {'status': 'ok'}

def getTries(blunder_id):
    with PostgreConnection('r') as connection:
        connection.cursor.execute("""
            SELECT * 
            FROM blunder_history
            WHERE blunder_id = %s;
            """, (blunder_id,)
        )

        total = connection.cursor.rowcount

    with PostgreConnection('r') as connection:
        connection.cursor.execute(
            'SELECT * from blunder_history where blunder_id = %s AND result = 1;'
            , (blunder_id,)
        )

        success = connection.cursor.rowcount

    return success, total

def getBlunderComments(blunder_id):
    result = []

    with PostgreConnection('r') as connection:
        connection.cursor.execute("""
            SELECT id, date, parent_id, user_id, comment
            FROM blunder_comments
            WHERE blunder_id = %s
            """, (blunder_id,)
        )

        comments = connection.cursor.fetchall()

        for comment in comments:
            comment_id, date, parent_id, user_id, text = comment
            username = getUsernameById(user_id) 
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
    if user_id is None: return False

    with PostgreConnection('r') as connection:
        connection.cursor.execute(
            """SELECT * from blunder_favorites
               WHERE blunder_id = %s
                 AND user_id = %s;"""
            , (blunder_id, user_id)
        )

        if connection.cursor.rowcount == 1:
            return True
        return False

def getBlunderPopularity(blunder_id):
    with PostgreConnection('r') as connection:
        connection.cursor.execute(
            """SELECT *
               FROM blunder_favorites
               WHERE blunder_id = %s;"""
            , (blunder_id,)
        )

        return connection.cursor.rowcount

def getBlunderVotes(blunder_id):
    with PostgreConnection('r') as connection:
        connection.cursor.execute(
            """SELECT *
               FROM blunder_votes
               WHERE blunder_id = %s and vote = 1;"""
            , (blunder_id,)
        )

        likes = connection.cursor.rowcount

    with PostgreConnection('r') as connection:
        connection.cursor.execute(
            """SELECT *
               FROM blunder_votes
               WHERE blunder_id = %s AND vote = -1;"""
            , (blunder_id,)
        )

        dislikes = connection.cursor.rowcount

    return likes, dislikes

def getBlunderCommentVotes(comment_id):
    with PostgreConnection('r') as connection:
        connection.cursor.execute(
            """SELECT *
               FROM blunder_comments_votes
               WHERE comment_id = %s
                 AND vote = 1;"""
            , (comment_id,)
        )

        likes = connection.cursor.rowcount

    with PostgreConnection('r') as connection:
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
    if user_id is None: return False

    with PostgreConnection('w') as connection:
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

    with PostgreConnection('w') as connection:
        connection.cursor.execute(
            """INSERT INTO blunder_votes(user_id, blunder_id, vote)
               VALUES (%s, %s, %s);"""
            , (user_id, blunder_id, vote)
        )

        if connection.cursor.rowcount != 1: 
            raise Exception('Can not add vote for user id %s with blunder id %s' % (user_id, blunder_id))

    return True

def favoriteBlunder(user_id, blunder_id):
    if user_id is None: return False

    with PostgreConnection('w') as connection:
        connection.cursor.execute(
            """DELETE FROM blunder_favorites
               WHERE blunder_id = %s
                 AND user_id = %s;"""
            , (blunder_id, user_id)
        )

        count = connection.cursor.rowcount

        if count == 1:
            return True

    with PostgreConnection('w') as connection:
        connection.cursor.execute(
            """INSERT INTO blunder_favorites(user_id, blunder_id)
               VALUES (%s,%s);"""
            , (user_id, blunder_id)
        )

        if connection.cursor.rowcount != 1:
            raise Exception('Error inserting favorite for user id %s with blunder id %s' % (user_id, blunder_id))

    return True

def commentBlunder(user_id, blunder_id, parent_id, user_input):
    if user_id is None: return False

    with PostgreConnection('w') as connection:
        connection.cursor.execute(
            """INSERT INTO blunder_comments(user_id, blunder_id, parent_id, comment)
               VALUES (%s, %s, %s, %s);"""
            , (user_id, blunder_id, parent_id, user_input)
        )

        if connection.cursor.rowcount != 1:
            raise Exception('Failed to comment')

    return True

def voteBlunderComment(user_id, comment_id, vote):
    if user_id is None: return False

    with PostgreConnection('w') as connection:
        connection.cursor.execute(
            """UPDATE blunder_comments_votes
               SET vote = %s, assign_date = NOW()
               WHERE comment_id = %s
                 AND user_id = %s;"""
            , (vote, comment_id, user_id)
        )

        if connection.cursor.rowcount  == 1:
            return True

    with PostgreConnection('w') as connection:
        connection.cursor.execute(
            """INSERT INTO blunder_comments_votes(user_id, comment_id, vote)
               VALUES (%s, %s, %s);"""
            , (user_id, comment_id, vote)
        )

        if connection.cursor.rowcount != 1: 
            raise Exception('Can not add comment vote for user id %s' % (user_id))

    return True

def blunderCommentAuthor(comment_id):
    with PostgreConnection('r') as connection:
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

def getTaskStartDate(user_id, blunder_id, type):
    if user_id is None: return

    with PostgreConnection('w') as connection:
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

        if(connection.cursor.rowcount != 1):
            return None

        (assign_date,) = connection.cursor.fetchone()

        return assign_date

def getUserProfile(username):
    with PostgreConnection('r') as connection:
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

       
    with PostgreConnection('r') as connection:
        connection.cursor.execute("""
            SELECT SUM(bcv.vote)
            FROM blunder_comments as bc INNER JOIN blunder_comments_votes as bcv 
                ON bc.id = bcv.comment_id WHERE bc.user_id = %s;"""
            , (user_id,))

        (commentLikeSum,) = connection.cursor.fetchone()
        if commentLikeSum is None:
            commentLikeSum = 0

        karma = commentLikeSum * 2 + 10

    userJoinDate = getUserField(user_id, "to_char(registration, 'Month DD, YYYY')")

    return {
        'status': 'ok',
        'data': {
            'user-rating-value':     user_elo,
            'user-karma-value':      karma,
            'username-value':        username,
            'user-join-value':       userJoinDate
        }
    }

def getBlundersStatistics(username):

    with PostgreConnection('r') as connection:
        connection.cursor.execute("""
            SELECT u.id,
                   COUNT(b.id) as total,
                   COUNT(b.id) FILTER (WHERE b.result = 1) as solved,
                   COUNT(b.id) FILTER (WHERE b.result = 0) as failed
            FROM users AS u INNER JOIN blunder_history AS b ON u.id = b.user_id
            GROUP BY u.id, u.elo HAVING u.username = %s;"""
            , (username,)
        )

        if connection.cursor.rowcount != 1:
            return {
                'status': 'error',
                'message': 'Trying to get not exist user with name %s' % username
            }

        (user_id, total, solved, failed) = connection.cursor.fetchone()

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

    with PostgreConnection('r') as connection:
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
            'rating-statistics': rating
        }
    }

def getBlundersByDate(username):
    user_id = getUserId(username)

    with PostgreConnection('r') as connection:
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

        total = [[date, total] for (date, total, _1, _2) in data]
        solved = [[date, solved] for (date, _1, solved, _2) in data]
        failed = [[date, failed] for (date, _1, _2, failed) in data]

    return {
        'status': 'ok',
        'username': username,
        'data': {
            'blunder-count-statistics': {
                'total' : total,
                'solved': solved,
                'failed': failed
            }
        }
    }

def getBlundersHistory(username, offset, limit):
    user_id = getUserId(username)

    with PostgreConnection('r') as connection:
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

    with PostgreConnection('r') as connection:
        connection.cursor.execute("""
            SELECT h.blunder_id,
                   h.result,
                   h.blunder_elo,
                   h.user_elo,
                   h.date_start,
                   h.date_finish
            FROM blunder_history AS h
            WHERE h.user_id = %s
            LIMIT %s OFFSET %s"""
            , (user_id, limit, offset, )
        )

        data = connection.cursor.fetchall()

        blunders = [{
                     "blunder_id": blunder_id,
                     "result": result,
                     "blunder_elo": blunder_elo,
                     "user_elo": user_elo,
                     "date_start": date_start,
                     "date_finish": date_finish,
                    } for (blunder_id, result, blunder_elo, user_elo, date_start, date_finish) in data]

    return {
        'status': 'ok',
        'username': username,
        'data': {
            "total": total,
            "blunders": blunders
        }
    }

def lastActiveUsers(interval):
    with PostgreConnection('r') as connection:
        connection.cursor.execute("""
            SELECT u.username,
                   MAX(h.date_finish) AS date_last
            FROM blunder_history AS h
            INNER JOIN users AS u 
                ON h.user_id = u.id
            WHERE h.date_finish > NOW() - INTERVAL %s
            GROUP BY u.username;"""
            , (interval,)
        )

        data = connection.cursor.fetchall()

        users = [username for (username, _1) in data]

        return users;

def getUsersTop(number):
    with PostgreConnection('r') as connection:
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

    return top;

def getUsersStatistics():
    with PostgreConnection('r') as connection:
        connection.cursor.execute("""
                SELECT COUNT(id)
                FROM users AS u"""
            )
        (users_registered_value, ) = connection.cursor.fetchone()

    users_day = lastActiveUsers('1 HOUR')
    users_week = lastActiveUsers('1 WEEK')
    users_top = getUsersTop(10)
    
    return {
        'status': 'ok',
        'data': {
            "users-registered-value": users_registered_value,
            "users-online-value": len(users_day),
            "users-online-list" : users_day,
            "users-top-list": users_top,
            "users-active-value": len(users_week)
        }
    }

def getUsersByRating(interval):
    with PostgreConnection('r') as connection:
        connection.cursor.execute("""
            SELECT u.elo - MOD(u.elo, %s) AS elo_category,
                   COUNT(u.id) 
            FROM users AS u 
            GROUP BY elo_category;"""
            , (interval,)
        )

        data = connection.cursor.fetchall()

        destribution = [[elo_category, count] for (elo_category, count) in data]

    return {
        'status': 'ok',
        'data': {
            'users-rating-destribution': destribution
        }
    }