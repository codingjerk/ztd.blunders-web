from flask import render_template, request, jsonify

from app import app
from app.utils import session

@app.route('/login', methods=['GET'])
def login_get():
    return render_template('login.html', title = 'Ztd.Blunders', session = session)

@app.route('/login', methods=['POST'])
def login_post():
    result = session.authorize(request.json['username'], request.json['password'])

    return jsonify(result)

@app.route('/logout', methods = ['POST'])
def logout():
    session.deauthorize()
    return jsonify({
        'status': 'ok'
    })
