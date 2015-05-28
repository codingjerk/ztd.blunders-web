import psycopg2

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

def assignBlunderTask(username, blunder_id):
    if username is None: return

    user_id = getUserId(username)

    with PostgreConnection('w') as connection:
        connection.cursor.execute(
            'INSERT INTO blunder_tasks (user_id, blunder_id) VALUES (%s, %s);'
            , (user_id, blunder_id)
        )

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