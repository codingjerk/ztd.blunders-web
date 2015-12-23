

from app.db.postgre import core

def authorize(username, hash):
    if username is None:
        return False

    with core.PostgreConnection('r') as connection:
        connection.cursor.execute("""
            SELECT *
            FROM users
            WHERE username = %s AND password = %s;
            """, (username, hash)
        )

        users = connection.cursor.fetchall()

        success = len(users) == 1

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

        return connection.cursor.fetchone()[0]

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
                """, (username, salt, hash, roles.USER, email)
            )
        except psycopg2.IntegrityError:
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