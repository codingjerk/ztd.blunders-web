import psycopg2

USER_ROLE = 3

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
        connection.cursor.execute(
            """SELECT *
               FROM users 
               WHERE username = %s AND password = %s;"""
            , (username, hash)
        )

        users = connection.cursor.fetchall()

        success = len(users) == 1

    if success:
        with PostgreConnection('w') as connection:
            connection.cursor.execute(
                """UPDATE users 
                   SET last_login = NOW()
                   WHERE username = %s;"""
                , (username,)
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
        connection.cursor.execute(
            """SELECT username
               FROM users 
               WHERE id = %s;"""
            , (user_id,)
        )

        result = connection.cursor.fetchone()
        if result is None: raise Exception('User with id %d is not exist' % user_id)

        return result[0]

def assignBlunderTask(user_id, blunder_id):
    if user_id is None: return

    with PostgreConnection('w') as connection:
        connection.cursor.execute(
            'INSERT INTO blunder_tasks (user_id, blunder_id) VALUES (%s, %s);'
            , (user_id, blunder_id)
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
        connection.cursor.execute(
            """INSERT INTO blunder_history (user_id, blunder_id, result, user_elo, blunder_elo, user_line, date_start)
               VALUES (%s, %s, %s, %s, %s, %s, %s);"""
            , (user_id, blunder_id, result, user_elo, blunder_elo, userLine, date_start)
        )

        if connection.cursor.rowcount != 1:
            raise Exception('Failed to assign new blunder')

def closeBlunderTask(user_id, blunder_id):
    if user_id is None: return

    with PostgreConnection('w') as connection:
        connection.cursor.execute(
            """DELETE FROM blunder_tasks
               WHERE user_id = %s AND blunder_id = %s;"""
            , (user_id, blunder_id)
        )

        return connection.cursor.rowcount == 1

def setRating(user_id, elo):
    if user_id is None: 
        raise Exception('postre.setRating for anonim')

    with PostgreConnection('w') as connection:
        connection.cursor.execute(
            """UPDATE users
               SET elo = %s
               WHERE id = %s;"""
            , (elo, user_id)
        )

        if connection.cursor.rowcount != 1:
            raise Exception('Failed to assign new blunder')


def getAssignedBlunder(user_id):
    if user_id is None: return None

    with PostgreConnection('r') as connection:
        connection.cursor.execute(
            """SELECT blunder_id
               FROM blunder_tasks
               WHERE user_id = %s;"""
            , (user_id,)
        )

        blunder_id = connection.cursor.fetchone()
        if blunder_id is None: return None

        return blunder_id[0]

def signupUser(username, salt, hash, email):
    # TODO: Validation
    if len(username) < 3: return {'status': 'error', 'field': 'username', 'message': "Username is too short"}

    with PostgreConnection('w') as connection:
        try:
            connection.cursor.execute(
                """INSERT INTO users (username, salt, password, role, email, registration, last_login)
                   VALUES (%s, %s, %s, %s, %s, NOW(), NOW());"""
                , (username, salt, hash, USER_ROLE, email)
            )
        except psycopg2.IntegrityError as e:
            return {'status': 'error', 'field': 'username', 'message': 'Already registered'}

        success = (connection.cursor.rowcount == 1)

        if not success: return {'status': 'error', 'message': "Unable to register user"}

    return {'status': 'ok'}

def getTries(blunder_id):
    with PostgreConnection('r') as connection:
        connection.cursor.execute(
            """SELECT * 
               FROM blunder_history
               WHERE blunder_id = %s;"""
            , (blunder_id,)
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
        connection.cursor.execute(
            """SELECT id, date, parent_id, user_id, comment
               FROM blunder_comments
               WHERE blunder_id = %s"""
            , (blunder_id,)
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

def getTaskStartDate(user_id, blunder_id):
    if user_id is None: return

    with PostgreConnection('w') as connection:
        connection.cursor.execute(
            """SELECT assign_date FROM blunder_tasks
               WHERE user_id = %s AND blunder_id = %s;"""
            , (user_id, blunder_id)
        )

        if(connection.cursor.rowcount != 1):
            return None

        (assign_date,) = connection.cursor.fetchone()

        return assign_date