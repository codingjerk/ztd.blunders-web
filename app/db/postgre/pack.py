from app.db.postgre import core, blunder
from app.utils import tasks

def getAssignedPacks(user_id):
    with core.PostgreConnection('r') as connection:
        connection.cursor.execute("""
            SELECT pu.pack_id
            FROM pack_users as pu
            WHERE pu.user_id = %s
            """, (user_id,)
        )

        packs = connection.cursor.fetchall()

        result = [
            pack_id
            for (pack_id,) in packs
        ]

        return result

# Returns all pack types user can request in this time
# This function must limit user from doing crazy
# Total limit, dependencies etc
def getUnlockedPacks(user_id):
    with core.PostgreConnection('r') as connection:
        connection.cursor.execute("""
            SELECT id, name, description
            FROM pack_type as pt
            """
        )

        pack_types = connection.cursor.fetchall()

        result = [{
            'type_name': name,
            'description': description
        }
        for (id, name,description) in pack_types]

        return result

def getPackTypeId(pack_type_name):
    with core.PostgreConnection('r') as connection:
        connection.cursor.execute("""
            SELECT id
            FROM pack_type as pt
            WHERE pt.name = %s
            """, (pack_type_name,)
        )

        pack_type_id = connection.cursor.fetchone()
        return pack_type_id

# created_by is the user id, who phisically created the pack. This user
# may not have this pack assigned to him and, in face, will not after calling
# this function
def createPack(created_by, blunder_ids, pack_type_name):
    pack_type_id = getPackTypeId(pack_type_name)

    with core.PostgreConnection('w') as connection:
        connection.cursor.execute("""
            INSERT INTO packs(description,created_by,type_id,type_args)
            VALUES ('', %s, %s, '{}')
            RETURNING id
            """, (created_by, pack_type_id)
        )
        if connection.cursor.rowcount != 1:
            raise Exception('Failed to create pack')
        pack_id = connection.cursor.fetchone()[0]

    with core.PostgreConnection('w') as connection:
        for blunder_id in blunder_ids: #TODO: optimize to make this with one query
            connection.cursor.execute("""
                INSERT INTO pack_blunders(pack_id, blunder_id)
                VALUES (%s, %s)
                """, (pack_id, blunder_id)
            )
            if connection.cursor.rowcount != 1:
                raise Exception('Failed to create pack')

    return pack_id

def assignPack(user_id, pack_id):
    with core.PostgreConnection('w') as connection:
        connection.cursor.execute("""
            INSERT INTO pack_users(pack_id, user_id)
            VALUES (%s, %s)
            """, (pack_id, user_id)
        )
        if connection.cursor.rowcount != 1:
            raise Exception('Failed to assign pack to user')

    #TODO: getUserPackById - get blunders and write them into blunder_tasks
    # writing tasks into blunder tasks
    blunder_ids = getPackBlundersById(pack_id)
    for blunder_id in blunder_ids:
        blunder.assignBlunderTask(user_id, blunder_id, tasks.PACK)

def getPackBlundersById(pack_id):
    with core.PostgreConnection('r') as connection:
        connection.cursor.execute("""
            SELECT blunder_id
            FROM pack_blunders as pb
            WHERE pb.pack_id = %s
            """, (pack_id,)
        )

        pack_blunders = [
                blunder_id
                for (blunder_id,) in connection.cursor.fetchall()
            ]
        return pack_blunders

# Returns assigned blunders of some pack, not yet solved by user
def getAssignedBlunders(user_id, pack_id):
    #TODO: not include blunders, already solved by user
    pack_ids = getAssignedPacks(user_id)
    if not pack_id in pack_ids:
        return None

    blunders = getPackBlundersById(pack_id)

    return blunders
