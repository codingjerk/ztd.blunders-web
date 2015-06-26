from flask import render_template
from app import app
from app.utils import session

@app.route('/training')
def training():
    return render_template('training.html', title = 'Ztd.Blunders', session = session)
