#!/usr/bin/env python3

import flask

app = flask.Flask(__name__, static_folder='')

@app.route('/grb')
def grb():
    return flask.jsonify({
        'fen': '5qk1/2Q2pp1/6p1/1N1Bp3/pn2P3/3n1P2/6PP/6K1 w - - 2 35', 
        'blunderMove': 'Nd6', 
        'pv': ['Nxd5', 'Qc6', 'N3b4', 'Qxa4', 'Qxd6'],
    })
    
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

app.run(host='localhost', port=80)