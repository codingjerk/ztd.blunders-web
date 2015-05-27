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

def autentithicateUser(username, password):
    with PostgreConnection('r') as connection:
        connection.cursor.execute(
            'SELECT * from users WHERE username = %s AND password = %s;'
            , (username, password)
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

def getRating(username):
    with PostgreConnection('r') as connection:
        connection.cursor.execute(
            'SELECT elo from users WHERE username = %s;'
            , (username,)
        )

        elo = connection.cursor.fetchone()

        return elo[0]

def getUserId(username):
    with PostgreConnection('r') as connection:
        connection.cursor.execute(
            'SELECT id from users WHERE username = %s;'
            , (username,)
        )

        return connection.cursor.fetchone()[0]

def assignBlunderTask(username, blunder_id):
    user_id = getUserId(username)

    with PostgreConnection('w') as connection:
        connection.cursor.execute(
            'INSERT INTO blunder_tasks (user_id, blunder_id) VALUES (%s, %s);'
            , (user_id, blunder_id)
        )

def closeBlunderTask(username, blunder_id):
    user_id = getUserId(username)

    with PostgreConnection('w') as connection:
        connection.cursor.execute(
            'DELETE FROM blunder_tasks WHERE user_id = %s AND blunder_id = %s;'
            , (user_id, blunder_id)
        )

        return connection.cursor.rowcount == 1

def setRating(username, elo):
    user_id = getUserId(username)

    with PostgreConnection('w') as connection:
        connection.cursor.execute(
            'UPDATE users SET elo = %s WHERE id = %s;'
            , (elo, user_id)
        )

def getAssignedBlunder(username):
    user_id = getUserId(username)

    with PostgreConnection('r') as connection:
        connection.cursor.execute(
            'SELECT blunder_id from blunder_tasks WHERE user_id = %s;'
            , (user_id,)
        )

        blunder_id = connection.cursor.fetchone()
        if blunder_id is None: return None

        return blunder_id[0]