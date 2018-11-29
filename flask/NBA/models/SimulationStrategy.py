import abc
import pandas as pd
import numpy as np

import os

class SimulationStrategy(object):
	"""
        Abstract class for Strategy design pattern
    """
	def __init__(self):

		self.abspath = os.path.join('NBA/2018nba.csv')
		self.season = pd.read_csv(self.abspath)

	__metaclass__=abc.ABCMeta
	@abc.abstractmethod
	def algorithm_interface(self,team1,team2):
		pass

class ConcreteStrategyOld(SimulationStrategy):
	"""
        Concrete class for Strategy design pattern, to run alg for old Strategy
        Params:
        team1: string of one team name
        team2: string of second team name


        return: string team name
    """
	def algorithm_interface(self,team1,team2):

		team1row = self.season.loc[(self.season['Team']==team1)]
		team2row = self.season.loc[(self.season['Team']==team2)]
		team1val = team1row['TS%'].values[0]
		team2val = team2row['TS%'].values[0]
		team1prob = team1row['TS%'].values/(team1row['TS%'].values+team2row['TS%'].values)
		team2prob = team2row['TS%'].values/(team2row['TS%'].values+team1row['TS%'].values)

		if np.random.uniform()>team1prob:
			output = team1
		else:
			output = team2
		return output

class ConcreteStrategyNew(SimulationStrategy):
	"""
        Concrete class for Strategy design pattern, to run alg for new Strategy
        Params:
        team1: string of one team name
        team2: string of second team name


        return: string team name
    """
	def algorithm_interface(self,team1,team2):
		team1row = self.season.loc[(self.season['Team']==team1)]
		team2row = self.season.loc[(self.season['Team']==team2)]
		team1val = team1row['DRtg'].values[0]
		team2val = team2row['DRtg'].values[0]
		team1prob = team1row['DRtg'].values/(team1row['DRtg'].values+team2row['DRtg'].values)
		team2prob = team2row['DRtg'].values/(team2row['DRtg'].values+team1row['DRtg'].values)

		if np.random.uniform()>team1prob:
			output = team1
		else:
			output = team2
		return output