from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
@app.route('/training')
def training():
    return render_template('training.html', title = 'Ztd.Blunders')