from flask import render_template
from app import app
from app.utils import session,const

@app.route('/training')
def training():
    return render_template('training.html', title = const.app.title, session = session)
