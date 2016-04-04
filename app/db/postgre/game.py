
from app.db.postgre import core

def getGameById(game_id):
    with core.PostgreConnection('r') as connection:
        connection.cursor.execute("""
                    SELECT g.id,
                           g.white,
                           g.white_elo,
                           g.black,
                           g.black_elo,
                           g.result,
                           g.moves
                    FROM games as g
                    WHERE g.id = %s;"""
                    , (game_id,)
                )

        if connection.cursor.rowcount != 1:
            raise Exception('Failed to find associated game')

        (
            id,
            white,
            white_elo,
            black,
            black_elo,
            result,
            moves
        ) = connection.cursor.fetchone()

        return {
            'white': white,
            'white_elo': white_elo,
            'black': black,
            'black_elo': black_elo,
            'result': result,
            'moves': moves
        }
