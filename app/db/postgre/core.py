
import psycopg2

class PostgreConnection:
    def __init__(self, type):
        self.type = type
        assert type in 'rw'

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