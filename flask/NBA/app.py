from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from NBA.auth import login_required
from NBA.db import get_db
import abc
from flask.views import View
bp = Blueprint('app', __name__)

#this index function was adapted with help of flask tutorial http://flask.pocoo.org/docs/1.0/tutorial/
@bp.route('/')
def index():
	db = get_db()
	posts = db.execute(
		'SELECT p.id, team1, team2, team3, team4, team5, team6, team7, team8, strat, multsim, created, author_id, username'
		' FROM post p JOIN user u ON p.author_id = u.id'
		' ORDER BY created DESC'
	).fetchall()
	last = db.execute(
		'SELECT p.id'
		' FROM post p JOIN user u ON p.author_id = u.id'
		' ORDER BY created DESC'
	).fetchone()
	print('ahhahhhhh',last)
	return render_template('app/index.html', posts=posts, last=last)
#bp.add_url_rule('/',view_func=HomeView.as_view('index'))
import pandas as pd
import numpy as np

from models.SimAbstractFactory import *
from models.PlayoffIterator import PlayoffRound
#@bp.route('/<int:id>/results', methods=('GET','POST'))
#@login_required
class ResultsController(View):
	methods = ['GET', 'POST']
	decorators = [login_required]
	#def results(id):
	def dispatch_request(self, id):
		print('ukkbhhh helloooo')
		print(g.user['id'])
		post = get_post(id)
		print(post['id'])

		playoffs = PlayoffRound()
		playoffs.addRound([post['team1'],post['team2'],post['team3'],post['team4'],post['team5'],post['team6'],post['team7'],post['team8']])
		playoffiter = playoffs.iterator()
		winner1=''
		if request.method == 'POST':

			if request.form['rerun'] == "First Round Simulation": #so next step is iterator on rounds instead of matchups, will have to do something with json dump into database
				# so this button can be first round, next button can be 2nd round, etc.
				postStrat = post['strat']
				multsim = post['multsim']
				teamArr = playoffiter.next()[0]
				winner1 = FactoryCreator.getFactory(postStrat=postStrat,teams=teamArr[0:2],multsim=multsim)
				winner2 = FactoryCreator.getFactory(postStrat=postStrat,teams=teamArr[2:4],multsim=multsim)
				winner3 = FactoryCreator.getFactory(postStrat=postStrat,teams=teamArr[4:6],multsim=multsim)
				winner4 = FactoryCreator.getFactory(postStrat=postStrat,teams=teamArr[6:8],multsim=multsim)
				#winner1 = stratFactory(postStrat=postStrat,teams=teamArr[0:2])
				#winner2 = stratFactory(postStrat=postStrat,teams=teamArr[2:4])
				return render_template('app/results.html', post=post, output = winner1, output2 = winner2, output3 = winner3, output4 = winner4)


			if request.form['rerun'] == "Second Round Simulation":
				# print('uhhh helloooo')
				postStrat = post['strat']
				multsim = post['multsim']
				teamArr = playoffiter.next()[0]
				winner1 = FactoryCreator.getFactory(postStrat=postStrat,teams=teamArr[0:2],multsim=multsim)
				winner2 = FactoryCreator.getFactory(postStrat=postStrat,teams=teamArr[2:4],multsim=multsim)
				winner3 = FactoryCreator.getFactory(postStrat=postStrat,teams=teamArr[4:6],multsim=multsim)
				winner4 = FactoryCreator.getFactory(postStrat=postStrat,teams=teamArr[6:8],multsim=multsim)
				playoffs.addRound([winner1,winner2, winner3, winner4])
				roundtwo = playoffiter.next()[0]
				secondroundwinner1 = FactoryCreator.getFactory(postStrat=postStrat,teams=roundtwo[0:2],multsim=multsim)
				secondroundwinner2 = FactoryCreator.getFactory(postStrat=postStrat,teams=roundtwo[2:4],multsim=multsim)
				return render_template('app/results.html', post=post, output = winner1, output2 = winner2, output3 = winner3, output4 = winner4, secondRound1 = secondroundwinner1, secondRound2 = secondroundwinner2)

			if request.form['rerun'] == "Full Simulation":
				# print('uhhh helloooo')
				postStrat = post['strat']
				multsim = post['multsim']
				teamArr = playoffiter.next()[0]
				winner1 = FactoryCreator.getFactory(postStrat=postStrat,teams=teamArr[0:2],multsim=multsim)
				winner2 = FactoryCreator.getFactory(postStrat=postStrat,teams=teamArr[2:4],multsim=multsim)
				winner3 = FactoryCreator.getFactory(postStrat=postStrat,teams=teamArr[4:6],multsim=multsim)
				winner4 = FactoryCreator.getFactory(postStrat=postStrat,teams=teamArr[6:8],multsim=multsim)
				playoffs.addRound([winner1,winner2, winner3, winner4])
				roundtwo = playoffiter.next()[0]
				secondroundwinner1 = FactoryCreator.getFactory(postStrat=postStrat,teams=roundtwo[0:2],multsim=multsim)
				secondroundwinner2 = FactoryCreator.getFactory(postStrat=postStrat,teams=roundtwo[2:4],multsim=multsim)
				playoffs.addRound([secondroundwinner1,secondroundwinner2])
				finalsround = playoffiter.next()[0]
				finalswinner = FactoryCreator.getFactory(postStrat=postStrat,teams=finalsround[0:2],multsim=multsim)
				return render_template('app/results.html', post=post, output = winner1, output2 = winner2, output3 = winner3, output4 = winner4, secondRound1 = secondroundwinner1, secondRound2 = secondroundwinner2, finalsOutput = finalswinner)
			else:
				return redirect(url_for('app.results', id=post['id']))
		#else:
			#return redirect(url_for('app.results', id=post['id']))
		return render_template('app/results.html', post=post)
bp.add_url_rule('/<int:id>/results', view_func=ResultsController.as_view('results'))

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create(): #belongs in controller, in this app.py file

	if request.method == 'POST':
		team1 = request.form['team1']
		team2 = request.form['team2']
		team3 = request.form['team3']
		team4 = request.form['team4']
		team5 = request.form['team5']
		team6 = request.form['team6']
		team7 = request.form['team7']
		team8 = request.form['team8']
		strat = request.form['strat']
		multsim = request.form['multsim']


		error = None
	    #output = season.loc[team1]
		print(team1)
		if not team1:
			error = 'team1 is required.'

		if error is not None:
			flash(error)
		else:
			db = get_db()
			db.execute(
				'INSERT INTO post (team1, team2, team3, team4, team5, team6, team7, team8, strat, multsim, author_id)'
				' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
				(team1, team2, team3, team4, team5, team6, team7, team8, strat, multsim, g.user['id'])
			)
			db.commit()

			return redirect(url_for('index'))

	output = 'hello'
	return render_template('app/create.html', output=output)



def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, team1, team2, team3, team4, team5, team6, team7, team8, strat, multsim, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

#@bp.route('/<int:id>/update', methods=('GET', 'POST'))
#@login_required
class UpdateController(View):
	methods = ['GET', 'POST']
	decorators = [login_required]
	#def update(id):
	def dispatch_request(self,id):
		post = get_post(id)

		if request.method == 'POST':
			team1 = request.form['team1']
			team2 = request.form['team2']
			team3 = request.form['team3']
			team4 = request.form['team4']
			team5 = request.form['team5']
			team6 = request.form['team6']
			team7 = request.form['team7']
			team8 = request.form['team8']
			strat = request.form['strat']
			multsim = request.form['multsim']
			error = None

			if not team1:
				error = 'team1 is required.'

			if error is not None:
				flash(error)
			else:
				db = get_db()
				db.execute(
					'UPDATE post SET team1 = ?, team2 = ?, team3 = ?, team4 = ?, team5 = ?, team6 = ?, team7 = ?, team8 = ?, strat = ?, multsim = ?'
					' WHERE id = ?',
					(team1, team2, team3, team4, team5, team6, team7, team8, strat, multsim, id)
				)
				db.commit()
				return redirect(url_for('app.index'))

		return render_template('app/update.html', post=post)
bp.add_url_rule('/<int:id>/update', view_func=UpdateController.as_view('update'))



#@bp.route('/<int:id>/delete', methods=('POST',))
#@login_required
class DeleteController(View):
	methods = ['POST',]
	decorators = [login_required]
	#def delete(id):
	def dispatch_request(self,id):
		get_post(id)
		db = get_db()
		db.execute('DELETE FROM post WHERE id = ?', (id,))
		db.commit()
		return redirect(url_for('app.index'))
bp.add_url_rule('/<int:id>/delete', view_func=DeleteController.as_view('delete'))












