import pymongo

def startMongo():
    global mongo
    global blunderCollection
    global games_collection

    mongo = pymongo.MongoClient('localhost', 27017)
    db = mongo['chessdb']
    games_collection = db['games']
    blunderCollection = db['blunders']

startMongo()