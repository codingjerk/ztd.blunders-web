from flask import render_template
from app import app
from app.utils import session,const

@app.route('/explore/<blunderId>')
def explore(blunderId): #pylint: disable=unused-argument
    return render_template('explore.html', title = const.app.title, session = session)

@app.route('/explore')
def explore_empty():
    return explore(None)
