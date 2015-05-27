from flask import render_template, request, redirect, session, jsonify
from app import app

from app.db import postgre

@app.route('/signup', methods=['GET'])
def signup_get():
    return render_template('signup.html', title = 'Ztd.Blunders')

@app.route('/signup', methods=['POST'])
def signup_post():
    print(request.json)
    return jsonify({})