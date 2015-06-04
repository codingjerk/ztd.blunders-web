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
            'SELECT * from users WHERE username = %s AND password = %s;'
            , (username, hash)
        )

        users = connection.cursor.fetchall()

        success = len(users) == 1

    if success:
        with PostgreConnection('w') as connection:
            connection.cursor.execute(
                'UPDATE users SET last_login = NOW() WHERE username = %s;'
                , (username,)
            )

    return success

def getUserField(username, field):
    with PostgreConnection('r') as connection:
        connection.cursor.execute(
            'SELECT ' + field + ' from users WHERE username = %s;'
            , (username,)
        )

        return connection.cursor.fetchone()[0]

def getRating(username):
    if username is None: return 0

    return getUserField(username, 'elo')

def getSalt(username):
    if username is None:
        raise Exception('Getting salt for None user!')

    return getUserField(username, 'salt')

def getUserId(username):
    if username is None: 
        raise Exception('postre.getUserId for anonim')

    return getUserField(username, 'id')

def getUsernameById(user_id):
    with PostgreConnection('r') as connection:
        connection.cursor.execute(
            'SELECT username from users WHERE id = %s;'
            , (user_id,)
        )

        result = connection.cursor.fetchone()
        if result is None: raise Exception('User with id %d is not exist' % user_id)

        return result[0]

def assignBlunderTask(username, blunder_id):
    if username is None: return

    user_id = getUserId(username)

    with PostgreConnection('w') as connection:
        connection.cursor.execute(
            'INSERT INTO blunder_tasks (user_id, blunder_id) VALUES (%s, %s);'
            , (user_id, blunder_id)
        )

        if connection.cursor.rowcount != 1:
            raise Exception('Failed to assign new blunder')

def saveBlunderHistory(username, blunder_id, blunder_elo, success, userLine):
    if username is None: 
        raise Exception('postre.setRating for anonim')

    user_id = getUserId(username)
    user_elo = getRating(username)
    result = 1 if success else 0

    if success: userLine = ''

    with PostgreConnection('w') as connection:
        connection.cursor.execute(
            'INSERT INTO blunder_history (user_id, blunder_id, result, user_elo, blunder_elo, user_line) VALUES (%s, %s, %s, %s, %s, %s);'
            , (user_id, blunder_id, result, user_elo, blunder_elo, userLine)
        )

        if connection.cursor.rowcount != 1:
            raise Exception('Failed to assign new blunder')

def closeBlunderTask(username, blunder_id):
    if username is None: return

    user_id = getUserId(username)

    with PostgreConnection('w') as connection:
        connection.cursor.execute(
            'DELETE FROM blunder_tasks WHERE user_id = %s AND blunder_id = %s;'
            , (user_id, blunder_id)
        )

        return connection.cursor.rowcount == 1

def setRating(username, elo):
    if username is None: 
        raise Exception('postre.setRating for anonim')

    user_id = getUserId(username)

    with PostgreConnection('w') as connection:
        connection.cursor.execute(
            'UPDATE users SET elo = %s WHERE id = %s;'
            , (elo, user_id)
        )

        if connection.cursor.rowcount != 1:
            raise Exception('Failed to assign new blunder')


def getAssignedBlunder(username):
    if username is None: return None

    user_id = getUserId(username)

    with PostgreConnection('r') as connection:
        connection.cursor.execute(
            'SELECT blunder_id from blunder_tasks WHERE user_id = %s;'
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
                'INSERT INTO users (username, salt, password, role, email, registration, last_login) VALUES (%s, %s, %s, %s, %s, NOW(), NOW());'
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
            'SELECT * from blunder_history where blunder_id = %s;'
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
            'SELECT id, date, parent_id, user_id, comment from blunder_comments WHERE blunder_id = %s'
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
                'parent_id': parent_id,
                'username': username,
                'text': text,

                'likes': likes,
                'dislikes': dislikes,
            }

            result.append(pythonComment)

    return result

def myFavorite(username, blunder_id):
    if username is None: return False

    user_id = getUserId(username)

    with PostgreConnection('r') as connection:
        connection.cursor.execute(
            'SELECT * from blunder_favorites where blunder_id = %s and user_id = %s;'
            , (blunder_id, user_id)
        )

        if connection.cursor.rowcount == 1:
            return True
        elif connection.cursor.rowcount == 0:
            return False

    raise Exception('Duplicate favorites for user %s with blunder id %s' % (username, blunder_id))

def getBlunderPopularity(blunder_id):
    with PostgreConnection('r') as connection:
        connection.cursor.execute(
            'SELECT * from blunder_favorites where blunder_id = %s;'
            , (blunder_id,)
        )

        return connection.cursor.rowcount

def getBlunderVotes(blunder_id):
    with PostgreConnection('r') as connection:
        connection.cursor.execute(
            'SELECT * from blunder_votes where blunder_id = %s and vote = 1;'
            , (blunder_id,)
        )

        likes = connection.cursor.rowcount

    with PostgreConnection('r') as connection:
        connection.cursor.execute(
            'SELECT * from blunder_votes where blunder_id = %s AND vote = -1;'
            , (blunder_id,)
        )

        dislikes = connection.cursor.rowcount

    return likes, dislikes

def getBlunderCommentVotes(comment_id):
    if comment_id == 0: raise Exception('Getting votes for root comment')

    with PostgreConnection('r') as connection:
        connection.cursor.execute(
            'SELECT * from blunder_comments_votes where comment_id = %s and vote = 1;'
            , (comment_id,)
        )

        likes = connection.cursor.rowcount

    with PostgreConnection('r') as connection:
        connection.cursor.execute(
            'SELECT * from blunder_comments_votes where comment_id = %s and vote = -1;'
            , (comment_id,)
        )

        dislikes = connection.cursor.rowcount

    return likes, dislikes

def voteBlunder(username, blunder_id, vote):
    if username is None: return False

    user_id = getUserId(username)

    with PostgreConnection('w') as connection:
        connection.cursor.execute(
            'UPDATE blunder_votes SET vote = %s, assign_date = NOW() WHERE blunder_id = %s AND user_id = %s;'
            , (vote, blunder_id, user_id)
        )

        count = connection.cursor.rowcount 

        if count > 1:
            raise Exception('Duplicate votes for user %s with blunder id %s' % (username, blunder_id))
        elif count == 1:
            return True

    with PostgreConnection('w') as connection:
        connection.cursor.execute(
            'INSERT INTO blunder_votes(user_id, blunder_id, vote) VALUES (%s, %s, %s);'
            , (user_id, blunder_id, vote)
        )

        if connection.cursor.rowcount != 1: 
            raise Exception('Can not add vote for user %s with blunder id %s' % (username, blunder_id))

    return True

def favoriteBlunder(username, blunder_id):
    if username is None: return False

    user_id = getUserId(username)

    with PostgreConnection('w') as connection:
        connection.cursor.execute(
            'DELETE FROM blunder_favorites WHERE blunder_id = %s AND user_id = %s;'
            , (blunder_id, user_id)
        )

        count = connection.cursor.rowcount

        if count > 1:
            raise Exception('Duplicate favorites for user %s with blunder id %s' % (username, blunder_id))
        elif count == 1:
            return True

    with PostgreConnection('w') as connection:
        connection.cursor.execute(
            'INSERT INTO blunder_favorites(user_id, blunder_id) VALUES (%s,%s);'
            , (user_id, blunder_id)
        )

        if connection.cursor.rowcount != 1:
            raise Exception('Error inserting favorite for user %s with blunder id %s' % (username, blunder_id))

    return True

def commentBlunder(username, blunder_id, parent_id, user_input):
    if username is None: return False

    user_id = getUserId(username)

    if parent_id != 0:
        with PostgreConnection('r') as connection:
            connection.cursor.execute(
                'SELECT * from blunder_comments where id = %s AND blunder_id = %s;'
                , (parent_id, blunder_id)
            )

            if connection.cursor.rowcount != 1:
                raise Exception('Adding reply to not existing comment')

    with PostgreConnection('w') as connection:
        connection.cursor.execute(
            'INSERT INTO blunder_comments(user_id, blunder_id, parent_id, comment) VALUES (%s, %s, %s, %s);'
            , (user_id, blunder_id, parent_id, user_input)
        )

        if connection.cursor.rowcount != 1:
            raise Exception('Can\'t insert comment')

    return True

def voteBlunderComment(username, comment_id, vote):
    if username is None: return False

    user_id = getUserId(username)

    with PostgreConnection('w') as connection:
        connection.cursor.execute(
            'UPDATE blunder_comments_votes SET vote = %s, assign_date = NOW() WHERE comment_id = %s AND user_id = %s;'
            , (vote, comment_id, user_id)
        )

        count = connection.cursor.rowcount 

        if count > 1:
            raise Exception('Duplicate comment vote for user %s' % (username))
        elif count == 1:
            return True

    with PostgreConnection('w') as connection:
        connection.cursor.execute(
            'INSERT INTO blunder_comments_votes(user_id, comment_id, vote) VALUES (%s, %s, %s);'
            , (user_id, comment_id, vote)
        )

        if connection.cursor.rowcount != 1: 
            raise Exception('Can not add comment vote for user %s' % (username))

    return True

def blunderCommentAuthor(comment_id):
    with PostgreConnection('r') as connection:
        connection.cursor.execute(
            'SELECT user_id from blunder_comments where id = %s;'
            , (comment_id,)
        )

        if connection.cursor.rowcount != 1:
            raise Exception('Trying to get not exist comment')

        (user_id,) = connection.cursor.fetchone()

        return getUsernameById(user_id)