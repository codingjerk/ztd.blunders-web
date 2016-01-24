from app.db.postgre import core, blunder
from app.utils import const
from json import dumps

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

def getUnlockedRandom(name, description):
    return [{
        'type_name': name,
        'description': description
    }]

def getUnlockedMateInN(name, description):
    result = [{
        'type_name': name,
        'description': description % (N,),
        'args' : {
            'N' : N
        }
    }
    for N in [1,2,3,4,5,6,7,8,9,10]]

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

        result = []
        for (id, name, description) in pack_types:
            if name == const.pack_type.RANDOM:
                result.extend(getUnlockedRandom(name, description))
            elif name == const.pack_type.MATEINN:
                result.extend(getUnlockedMateInN(name, description))
            #else:
            #    raise Exception('')

        return result

def getPackTypeId(pack_type_name):
    with core.PostgreConnection('r') as connection:
        connection.cursor.execute("""
            SELECT id
            FROM pack_type as pt
            WHERE pt.name = %s
            """, (pack_type_name,)
        )

        if connection.cursor.rowcount != 1:
            raise Exception('Wrong pack type name')

        pack_type_id = connection.cursor.fetchone()

        return pack_type_id

# created_by is the user id, who phisically created the pack. This user
# may not have this pack assigned to him and, in fact, will not after calling
# this function
#TODO: filter blunder_ids to remove already exist
def createPack(created_by, blunder_ids, pack_type_name, pack_type_args, pack_description):
    pack_type_id = getPackTypeId(pack_type_name)

    with core.PostgreConnection('w') as connection:
        connection.cursor.execute("""
            INSERT INTO packs(description,created_by,type_id,type_args)
            VALUES (%s, %s, %s, %s)
            RETURNING id
            """, (pack_description, created_by, pack_type_id, dumps(pack_type_args))
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

    # When working in pack mode, this is ok to have same blunders in different packs
    # and user can assign them both. We need to check if blunder already assigned
    # This will fail and not right to do. Duplicated blunder will be added only once.
    # When user will try to solve second duplication blunder, it will get validation error
    # This is ok because it is very rare situation
    #TODO: In PostgreSQL 9.5 INSERT ... ON CONFLICT DO NOTHING added, rewrite after update?
    blunder_ids = getPackBlundersByIdAll(pack_id)
    for blunder_id in blunder_ids:
        if blunder.isBlunderTaskExist(user_id, blunder_id, const.tasks.PACK):
            continue
        blunder.assignBlunderTask(user_id, blunder_id, const.tasks.PACK)

# gets all blunders in pack
def getPackBlundersByIdAll(pack_id):
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

def getPackBlundersByIdAssignedOnly(user_id, pack_id):
    with core.PostgreConnection('r') as connection:
        connection.cursor.execute("""
            SELECT pb.blunder_id
            FROM pack_blunders AS pb
            INNER JOIN blunder_tasks AS bt
                USING(blunder_id)
            WHERE pb.pack_id = %s AND
                  bt.user_id = %s AND
                  bt.type_id =
                    (
                        SELECT bty.id
                        FROM blunder_task_type AS bty
                        WHERE bty.name = %s
                    ) ;
            """, (pack_id, user_id, const.tasks.PACK)
        )

        pack_blunders = [
                blunder_id
                for (blunder_id,) in connection.cursor.fetchall()
            ]
        return pack_blunders

# Returns assigned blunders of some pack, not yet solved by user
def getAssignedBlunders(user_id, pack_id):
    pack_ids = getAssignedPacks(user_id)
    if not pack_id in pack_ids:
        return None

    blunders = getPackBlundersByIdAssignedOnly(user_id, pack_id)

    return blunders

def getPackInfo(pack_id):
    with core.PostgreConnection('r') as connection:
        connection.cursor.execute("""
            SELECT p.description
            FROM packs as p
            WHERE p.id = %s
            """, (pack_id,)
        )

        if connection.cursor.rowcount != 1:
            return None

        description, = connection.cursor.fetchone()
        result = {
            'description': description
        }
        return result

def removePack(user_id, pack_id):
    ##TODO: optimize?
    ##delete from blunder_tasks as bt using pack_blunders as pb where bt.blunder_id = pb.blunder_id
    ##and pb.pack_id = 74 and bt.user_id = 282 and type_id = 3;
    blunder_ids = getAssignedBlunders(user_id, pack_id)
    if blunder_ids is None:
        return

    for blunder_id in blunder_ids:
        blunder.closeBlunderTask(user_id, blunder_id, const.tasks.PACK)

    with core.PostgreConnection('w') as connection:
        connection.cursor.execute("""
            DELETE FROM pack_users as pu
            WHERE pu.user_id = %s AND
                  pu.pack_id = %s
            """, (user_id, pack_id)
        )
