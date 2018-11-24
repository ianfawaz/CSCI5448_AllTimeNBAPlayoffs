from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from NBA.auth import login_required
from NBA.db import get_db
import abc

bp = Blueprint('app', __name__)

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, team1, team2, team3, team4, strat, created, author_id, username'
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

import pandas as pd
import numpy as np
# import tempfile
# tempfile_path = tempfile.NamedTemporaryFile().name
# file.save(tempfile_path)
import os
abspath = os.path.join('NBA/2018nba.csv')
season = pd.read_csv(abspath)
# @bp.route('/create', methods=('GET', 'POST'))
# @login_required

class Simulation:
	def __init__(self,strategy):
		self._strategy = strategy

	def simulation_interface(self,team1,team2):
		return self._strategy.algorithm_interface(team1,team2)

    
class SimulationStrategy(object):
	__metaclass__=abc.ABCMeta
	@abc.abstractmethod
	def algorithm_interface(self,team1,team2):
		pass
		# output = 'hi'
		# return output
class ConcreteStrategyOld(SimulationStrategy):
	def algorithm_interface(self,team1,team2):
		team1row = season.loc[(season['Team']==team1)]
		team2row = season.loc[(season['Team']==team2)]
		team1val = team1row['TS%'].values[0]
		team2val = team2row['TS%'].values[0]
		team1prob = team1row['TS%'].values/(team1row['TS%'].values+team2row['TS%'].values)
		team2prob = team2row['TS%'].values/(team2row['TS%'].values+team1row['TS%'].values)

		if np.random.uniform()>team1prob:
			#output = team1+" won the simulation playoff round!"
			output = team1
		else:
        	#print(team1row,team2prob,np.random.uniform())
			#output = team2+" won the simulation playoff round!"
			output = team2
		return output

class ConcreteStrategyNew(SimulationStrategy): #later on, theses classes should be in their separate 'model' files
	def algorithm_interface(self,team1,team2):
		team1row = season.loc[(season['Team']==team1)]
		team2row = season.loc[(season['Team']==team2)]
		team1val = team1row['DRtg'].values[0]
		team2val = team2row['DRtg'].values[0]
		team1prob = team1row['DRtg'].values/(team1row['DRtg'].values+team2row['DRtg'].values)
		team2prob = team2row['DRtg'].values/(team2row['DRtg'].values+team1row['DRtg'].values)

		if np.random.uniform()>team1prob:
			#output = team1+" won the simulation playoff round!"
			output = team1
		else:
        	#print(team1row,team2prob,np.random.uniform())
			#output = team2+" won the simulation playoff round!"
			output = team2
		return output

class ConcreteIterator:
	def __init__(self, rounds):
		#self._concrete_aggregate = concrete_aggregate
		self.rounds = rounds
		self.ind = 0


	def hasNext(self):
		if (self.ind >= len(self.rounds)):
			return False
		else:
			return True

	def next(self):
		if len(self.rounds) > self.ind:  # if no_elements_to_traverse:
			retInd = self.ind
			self.ind += 1
			return (self.rounds[retInd], retInd)
		else:
			raise StopIteration
			# raise StopIteration
		#return None  # return element
class PlayoffRound:
	def __init__(self):
		self.rounds = []
	def addRound(self, pRound):
		self.rounds.append(pRound)
	def iterator(self):
		return ConcreteIterator(self.rounds)


@bp.route('/<int:id>/results', methods=('GET','POST'))
@login_required
def results(id):
	print('ukkbhhh helloooo')
	print(g.user['id'])
	post = get_post(id)
	print(post['id'])
	# db = get_db()
	# db.execute('SELECT id, team1, team2 FROM post WHERE id = ?', (id, team1,team2))
	# print('he')
	# print(team1,team2)
	# print('he')
	# db.commit()
	playoffs = PlayoffRound()
	playoffs.addRound([post['team1'],post['team2'],post['team3'],post['team4']])
	playoffiter = playoffs.iterator()
	winner1=''
	if request.method == 'POST':
		if request.form['rerun'] == "Rerun Simulation": #so next step is iterator on rounds instead of matchups, will have to do something with json dump into database
			# so this button can be first round, next button can be 2nd round, etc.
			if post['strat'] == 'new':
				concrete_strategy_new = ConcreteStrategyNew()
				simulation = Simulation(concrete_strategy_new)


				teamArr = playoffiter.next()[0]
				winner1 = simulation.simulation_interface(team1=teamArr[0], team2=teamArr[1])
				winner2 = simulation.simulation_interface(team1=teamArr[2], team2=teamArr[3])
				#playoffs.addRound([winner1,winner2])
				# print(g.user['id'])
				# return render_template('app/results.html', post=post, output=simulation.simulation_interface(team1=team1, team2=team2))
				return render_template('app/results.html', post=post, output = winner1, output2 = winner2)
			if post['strat'] == 'old':
				concrete_strategy_old = ConcreteStrategyOld()
				simulation = Simulation(concrete_strategy_old)
				teamArr = playoffiter.next()[0]
				winner1 = simulation.simulation_interface(team1=teamArr[0], team2=teamArr[1])
				winner2 = simulation.simulation_interface(team1=teamArr[2], team2=teamArr[3])
				# print(g.user['id'])
				# return render_template('app/results.html', post=post, output=simulation.simulation_interface(team1=team1, team2=team2))
				return render_template('app/results.html', post=post, output = winner1, output2=winner2)
			#return render_template('app/results.html', output=simulation.simulation_interface(team1=g.user['team1'], team2=g.user['team2']))
		if request.form['rerun'] == "Next Simulation":
			# print('uhhh helloooo')
			if post['strat'] == 'new':
				concrete_strategy_new = ConcreteStrategyNew()
				simulation = Simulation(concrete_strategy_new)
				teamArr = playoffiter.next()[0]
				winner1 = simulation.simulation_interface(team1=teamArr[0], team2=teamArr[1])
				winner2 = simulation.simulation_interface(team1=teamArr[2], team2=teamArr[3])
				playoffs.addRound([winner1,winner2])
				roundtwo = playoffiter.next()[0]
				winner3 = simulation.simulation_interface(team1=winner1, team2=winner2)
				# print(g.user['id'])
				# return render_template('app/results.html', post=post, output=simulation.simulation_interface(team1=team1, team2=team2))
				return render_template('app/results.html', post=post,output = winner1, output2 = winner2, output3 = winner3)
			if post['strat'] == 'old':
				concrete_strategy_old = ConcreteStrategyOld()
				simulation = Simulation(concrete_strategy_old)
				teamArr = playoffiter.next()[0]
				winner1 = simulation.simulation_interface(team1=teamArr[0], team2=teamArr[1])
				winner2 = simulation.simulation_interface(team1=teamArr[2], team2=teamArr[3])
				playoffs.addRound([winner1,winner2])
				roundtwo = playoffiter.next()[0]
				winner3 = simulation.simulation_interface(team1=winner1, team2=winner2)
				# print(g.user['id'])
				# return render_template('app/results.html', post=post, output=simulation.simulation_interface(team1=team1, team2=team2))
				return render_template('app/results.html', post=post,output = winner1, output2 = winner2, output3 = winner3)
		else:
			redirect(url_for('app.results'))
	else:
		#return redirect(url_for('app.results', id=post['id']))
		return render_template('app/results.html', post=post)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create(): #belongs in controller, in this app.py file
	#self._strategy.algorithm_interface()
	#post = get_post(id)
	if request.method == 'POST':
		team1 = request.form['team1']
		team2 = request.form['team2']
		team3 = request.form['team3']
		team4 = request.form['team4']
		strat = request.form['strat']

		# playoffs = PlayoffRound()
		# playoffs.__init__()
		# playoffs.addRound([team1,team2,team3,team4])

		error = None
	    #output = season.loc[team1]
		print(team1)
		if not team1:
			error = 'team1 is required.'
	    #season = pd.read_csv('mfawaz/CSCI5448_AllTimeNBAPlayoffs/flask/NBA/2018nba.csv')
		# if team1 in season['Team']:

		# 	output = season.loc[(season['Team']==team1)]
		# 	return render_template('app/results.html',output=output)
		if error is not None:
			flash(error)
		else:
			db = get_db()
			db.execute(
				'INSERT INTO post (team1, team2, team3, team4, strat, author_id)'
				' VALUES (?, ?, ?, ?, ?, ?)',
				(team1, team2, team3, team4, strat, g.user['id'])
			)
			db.commit()
	        # team1row = season.loc[(season['Team']==team1)]
	        # team2row = season.loc[(season['Team']==team2)]
	        # team1val = team1row['TS%'].values[0]
	        # team2val = team2row['TS%'].values[0]
	        # team1prob = team1row['TS%'].values/(team1row['TS%'].values+team2row['TS%'].values)
	        # team2prob = team2row['TS%'].values/(team2row['TS%'].values+team1row['TS%'].values)

	        # if np.random.uniform()>team1prob:
	        # 	output = team1+" won the simulation playoff round!"
	        # else:
	        # 	#print(team1row,team2prob,np.random.uniform())
	        # 	output = team2+" won the simulation playoff round!"
	        return redirect(url_for('index'))
			# if strat == 'new':
			# 	concrete_strategy_new = ConcreteStrategyNew()
			# 	simulation = Simulation(concrete_strategy_new)

			# 	print(concrete_strategy_new.algorithm_interface(team1=team1, team2=team2))
			# 	simulation.simulation_interface(team1=team1, team2=team2)
			# 	#simulation.simulation_interface(team1=team1, team2=team2)
			# 	#return results(id=g.user['id'])
			# 	#return redirect(url_for('app.results', id=post['id']))
			# 	#return redirect(url_for('app.results', output=simulation.simulation_interface(team1=team1, team2=team2), id = g.user['id']))
			# 	return render_template('app/results.html', output=simulation.simulation_interface(team1=team1, team2=team2))
			# if strat == 'old':
			# 	concrete_strategy_old = ConcreteStrategyOld()
			# 	simulation = Simulation(concrete_strategy_old)

			# 	print(concrete_strategy_old.algorithm_interface(team1=team1, team2=team2))
			# 	simulation.simulation_interface(team1=team1, team2=team2)
			# 	#simulation.simulation_interface(team1=team1, team2=team2)
			# 	return render_template('app/results.html', output=simulation.simulation_interface(team1=team1, team2=team2))
			#return redirect(url_for('app.results', output=simulation.simulation_interface(team1=team1, team2=team2)))

            #return redirect(url_for('app.index'))
    #season = pd.read_csv('mfawaz/CSCI5448_AllTimeNBAPlayoffs/flask/NBA/2018nba.csv')
    #output = season.loc[(season['Team']==team1)]
	output = 'hello'
	return render_template('app/create.html', output=output)



def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, team1, team2, team3, team4, strat, created, author_id, username'
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
        team3 = request.form['team3']
        team4 = request.form['team4']
        strat = request.form['strat']
        error = None

        if not team1:
            error = 'team1 is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET team1 = ?, team2 = ?, team3 = ?, team4 = ?, strat = ?'
                ' WHERE id = ?',
                (team1, team2, team3, team4, strat, id)
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












