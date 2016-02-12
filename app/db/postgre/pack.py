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

def getUnlockedAsIs(name, description):
    return [{
        'type_name': name,
        'description': description
    }]

def getUnlockedMateInN(name, description):
    # all N 1-10 should work now, however, we artificially limit N to 3
    result = [{
        'type_name': name,
        'description': description % (N,),
        'args' : {
            'N' : N
        }
    }
    for N in [1,2,3]]

    return result

# Returns all pack types user can request in this time
# This function must limit user from doing crazy
# Total limit, dependencies etc
# Function receives packs
def getUnlockedPacks(user_id, packs):
    if len(packs) >= 4: #Limit packs user can have
        return []

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
                result.extend(getUnlockedAsIs(name, description))
            elif name == const.pack_type.MATEINN:
                result.extend(getUnlockedMateInN(name, description))
            elif name == const.pack_type.OPENING:
                result.extend(getUnlockedAsIs(name, description))
            elif name == const.pack_type.ENDGAME:
                result.extend(getUnlockedAsIs(name, description))
            elif name == const.pack_type.PROMOTION:
                result.extend(getUnlockedAsIs(name, description))
            elif name == const.pack_type.CLOSEDGAME:
                result.extend(getUnlockedAsIs(name, description))
            #else:
            #    raise Exception('')

        return result

# Get both assigned and unlocked packs
def getPacks(user_id):
    packs = getAssignedPacks(user_id)
    unlocked = getUnlockedPacks(user_id, packs)

    return packs, unlocked

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
                    )
            ORDER BY pb.blunder_id ;
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

def getPackAssignDate(user_id, pack_id):
    with core.PostgreConnection('r') as connection:
        connection.cursor.execute("""
            SELECT pu.assign_date FROM pack_users as pu
            WHERE pu.user_id = %s AND
                  pu.pack_id = %s
            """, (user_id, pack_id)
        )

        if connection.cursor.rowcount != 1:
            raise Exception('Pack not found, table is not in proper state')

        assign_date, = connection.cursor.fetchone()

        return assign_date

def removePack(user_id, pack_id, success):
    ##TODO: optimize?
    ##delete from blunder_tasks as bt using pack_blunders as pb where bt.blunder_id = pb.blunder_id
    ##and pb.pack_id = 74 and bt.user_id = 282 and type_id = 3;
    blunder_ids = getAssignedBlunders(user_id, pack_id)
    if blunder_ids is None:
        return

    assign_date = getPackAssignDate(user_id, pack_id)

    for blunder_id in blunder_ids:
        blunder.closeBlunderTask(user_id, blunder_id, const.tasks.PACK)

    with core.PostgreConnection('w') as connection:
        connection.cursor.execute("""
            DELETE FROM pack_users as pu
            WHERE pu.user_id = %s AND
                  pu.pack_id = %s
            """, (user_id, pack_id)
        )

    savePackHistory(user_id, pack_id, assign_date, success)

def savePackHistory(user_id, pack_id, assign_date, success):
    result = 1 if success else 0

    with core.PostgreConnection('w') as connection:
        connection.cursor.execute("""
            INSERT INTO pack_history
            (user_id, pack_id, date_start, result)
            VALUES (%s, %s, %s, %s);
            """,
            (user_id, pack_id, assign_date, result)
        )

        if connection.cursor.rowcount != 1:
            raise Exception('Failed to write into pack history table')

 #
 # Scan all user assigned packs and closes them if no blunders left to solve
 #
def gcHistoryPacks(user_id):
    if user_id is None:
        raise Exception('postre.savePackHistory for anonim')

    # returns packs with 1 or more assigned blunders
    with core.PostgreConnection('r') as connection:
        connection.cursor.execute("""
            SELECT pack_id,
                   COUNT(pb.blunder_id)
            FROM pack_users AS pu
            INNER JOIN pack_blunders AS pb
                USING(pack_id)
            INNER JOIN blunder_tasks AS bt
                USING(blunder_id)
            WHERE pu.user_id = %s AND
                  bt.type_id = (
                                  SELECT bty.id
                                  FROM blunder_task_type AS bty
                                  WHERE bty.name = %s
                               )
            GROUP BY pack_id;
            """,
            (user_id, const.tasks.PACK)
        )

        nonEmptyPacks = [pack_id for pack_id,count in connection.cursor.fetchall()]
        allPacks = getAssignedPacks(user_id)

        emptyPacks = [pack for pack in allPacks if pack not in list(nonEmptyPacks)]

        for pack_id in emptyPacks:
            removePack(user_id, pack_id, True)

 #
 #
 #
def reusePack(user_id, pack_type_name, pack_type_args):
    pack_type_id = getPackTypeId(pack_type_name)

    with core.PostgreConnection('r') as connection:
        connection.cursor.execute("""
            SELECT p.id
            FROM packs AS p
            LEFT JOIN (
                        SELECT pu.pack_id AS id
                        FROM pack_users AS pu
                        WHERE pu.user_id = %s
                        UNION
                        SELECT ph.pack_id AS id
                        FROM pack_history AS ph
                        WHERE ph.user_id = %s
                      ) AS pa
            USING(id)
            WHERE pa.id IS NULL AND
                  p.type_id = %s AND
                  p.type_args = %s
            ORDER BY p.id
            LIMIT 1;
        """, (user_id, user_id, pack_type_id, dumps(pack_type_args))
        )

        if connection.cursor.rowcount == 0:
            return None

        pack_id, = connection.cursor.fetchone()

        return pack_id
