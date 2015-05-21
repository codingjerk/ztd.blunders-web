import pymongo

mongo = pymongo.MongoClient('localhost', 27017)
db = mongo['chessdb']