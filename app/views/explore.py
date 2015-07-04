from flask import render_template
from app import app
from app.utils import session

@app.route('/explore')
@app.route('/explore/')
@app.route('/explore/<blunderId>')
def explore(blunderId): #pylint: disable=unused-argument
    return render_template('download.html', title = 'Ztd.Blunders', session = session)
