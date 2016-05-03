use chessdb;
db.cache.createIndex( { "minute": 1 }, { expireAfterSeconds: 60 } )
db.cache.createIndex( { "hour": 1 }, { expireAfterSeconds: 3600 } )
db.cache.createIndex( { "day": 1 }, { expireAfterSeconds: 86400 } )
