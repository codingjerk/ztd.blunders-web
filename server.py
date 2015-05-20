#!/usr/bin/env python3

import flask
import pymongo
import random

app = flask.Flask(__name__, static_folder='')

@app.route('/getRandomBlunder')
def getRandomBlunder():
    randomIndex = random.randint(0, blunders.count())

    data = blunders.find().skip(randomIndex).limit(1)[0]
    data['_id'] = str(data['_id'])
    data['pgn_id'] = str(data['pgn_id'])

    return flask.jsonify(data)
    
@app.route('/js/<path:path>')
def send_js(path):
    print(path)
    return flask.send_from_directory('js', path)
    
@app.route('/css/<path:path>')
def send_css(path):
    print(path)
    return flask.send_from_directory('css', path)

@app.route('/chessboardjs/js/<path:path>')
def send_chess_js(path):
    print(path)
    return flask.send_from_directory('chessboardjs/js', path)

@app.route('/chessboardjs/css/<path:path>')
def send_chess_css(path):
    print(path)
    return flask.send_from_directory('chessboardjs/css', path)

@app.route('/img/chesspieces/wikipedia/<path:path>')
def send_chess_img(path):
    data = open('./chessboardjs/img/chesspieces/wikipedia/' + path, 'rb').read()
    response = flask.make_response(data)
    response.headers['Content-Type'] = 'image/png'
    response.headers['Content-Disposition'] = 'attachment; filename=%s' % path
    return response

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/compressed')
def compressedRoot():
    return app.send_static_file('compressed.html')

def startMongo():
    global mongo
    global blunders
    global games_collection

    mongo = pymongo.MongoClient('localhost', 27017)
    db = mongo['chessdb']
    games_collection = db['games']
    blunders = db['blunders']

startMongo()
app.run(host='localhost', port=80, debug=True)