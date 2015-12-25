
from app.db.postgre import core

def saveFeedback(message):
    if len(message.strip()) == 0:
        return {
            'status': 'error',
            'message': "Can't store empty feedback"
        }

    if len(message) >= 100 * 50:
        return {
            'status': 'error',
            'message': "Message too long"
        }

    with core.PostgreConnection('w') as connection:
        connection.cursor.execute("""
            INSERT INTO feedback (message)
            VALUES (%s);
            """, (message,)
        )

        if connection.cursor.rowcount != 1:
            return {
                'status': 'error',
                'message': "Can't store feedback"
            }

    return {
        'status': 'ok'
    }