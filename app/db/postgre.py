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
            if issubclass(exception, Exception):
                self.cursor.rollback()
            else:
                self.cursor.commit()

        self.cursor.close()
        self.connection.close()

def autentithicateUser(username, password):
    with PostgreConnection('r') as connection:
        connection.cursor.execute(
            'SELECT * from users WHERE username = %s AND password = %s;'
            , (username, password)
        )

        users = connection.cursor.fetchall()

        return len(users) == 1