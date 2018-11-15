from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from NBA.auth import login_required
from NBA.db import get_db

bp = Blueprint('app', __name__)

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, team1, team2, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('app/index.html', posts=posts)

import pandas as pd
import numpy as np
# import tempfile
# tempfile_path = tempfile.NamedTemporaryFile().name
# file.save(tempfile_path)
import os
abspath = os.path.join('NBA/2018nba.csv')
season = pd.read_csv(abspath)
@bp.route('/create', methods=('GET', 'POST'))
@login_required

def create():
    if request.method == 'POST':
        team1 = request.form['team1']
        team2 = request.form['team2']
        error = None
        #output = season.loc[team1]
        print(team1)
        if not team1:
            error = 'team1 is required.'
        #season = pd.read_csv('mfawaz/CSCI5448_AllTimeNBAPlayoffs/flask/NBA/2018nba.csv')
        if team1 in season['Team']:

        	output = season.loc[(season['Team']==team1)]
        	return render_template('app/results.html',output=output)
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (team1, team2, author_id)'
                ' VALUES (?, ?, ?)',
                (team1, team2, g.user['id'])
            )
            db.commit()
            team1row = season.loc[(season['Team']==team1)]
            team2row = season.loc[(season['Team']==team2)]
            team1val = team1row['TS%'].values[0]
            team2val = team2row['TS%'].values[0]
            team1prob = team1row['TS%'].values/(team1row['TS%'].values+team2row['TS%'].values)
            team2prob = team2row['TS%'].values/(team2row['TS%'].values+team1row['TS%'].values)

            if np.random.uniform()>team1prob:
            	output = team1+" won the simulation playoff round!"
            else:
            	#print(team1row,team2prob,np.random.uniform())
            	output = team2+" won the simulation playoff round!"
            return render_template('app/results.html', output=output)
            #return redirect(url_for('app.index'))
    #season = pd.read_csv('mfawaz/CSCI5448_AllTimeNBAPlayoffs/flask/NBA/2018nba.csv')
    #output = season.loc[(season['Team']==team1)]
    output = 'hello'
    return render_template('app/create.html', output=output)


def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, team1, team2, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        team1 = request.form['team1']
        team2 = request.form['team2']
        error = None

        if not team1:
            error = 'team1 is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET team1 = ?, team2 = ?'
                ' WHERE id = ?',
                (team1, team2, id)
            )
            db.commit()
            return redirect(url_for('app.index'))

    return render_template('app/update.html', post=post)



@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('app.index'))












