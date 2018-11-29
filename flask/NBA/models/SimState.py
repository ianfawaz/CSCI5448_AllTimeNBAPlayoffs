import abc
from scipy import stats
class SimState(object):
	"""
        Parent class for State design pattern
    """


	__metaclass__=abc.ABCMeta
	@abc.abstractmethod
	def handle(self, teams, strategy):
		pass


class SingleSimState(SimState):
	"""
        Concrete class for State design pattern, to run single simulation
        Params:
        teams: list of team names
        strategy: SimulationStrategy class


        return: string team name
    """

	def handle(self,teams,strategy):
		#concrete_strategy_new = ConcreteStrategyNew()
		#simulation = Simulation(concrete_strategy_new)
		winner = strategy.simulation_interface(teams[0], teams[1])

		return winner


class MultiSimState(SimState):
	"""
        Concrete class for State design pattern, to run multiple simulations (fifty of them here)
        Params:
        teams: list of team names
        strategy: SimulationStrategy class


        return: string team name
    """

	def handle(self,teams,strategy):
		winner1Arr = []

		for i in range(50):
			#concrete_strategy_new = ConcreteStrategyNew()
			#simulation = Simulation(concrete_strategy_new)
			winner1Arr.append(strategy.simulation_interface(teams[0], teams[1]))


		return stats.mode(winner1Arr)[0][0]