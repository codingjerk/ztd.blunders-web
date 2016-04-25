
import psycopg2

# Yes, this is real hostname and password, but it's guarded by firewall
hostname="blunders-master.clotqfqonef0.eu-west-1.rds.amazonaws.com"
database="chessdb"
username="postgres"
password="chessdb"

class PostgreConnection:
    def __init__(self, type):
        self.type = type
        assert type in 'rw'

        self.connection = psycopg2.connect('dbname=%s user=%s password=%s host=%s' % (database, username, password, hostname))
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
