from Simulation import Simulation
from SimulationStrategy import SimulationStrategy, ConcreteStrategyOld, ConcreteStrategyNew
from SimContext import SimContext
from SimState import SimState, SingleSimState, MultiSimState
import abc

class SimAbstractFactory(object):
	__metaclass__=abc.ABCMeta
	@abc.abstractmethod
	def getNewStrategy(self):
		pass

	@abc.abstractmethod
	def getOldStrategy(self):
		pass

class NewStrategyFactory(SimAbstractFactory):
	"""
        Concrete class for Abstract Factory design pattern, to get New Strategy
        Params:
        teams: list of team names
        multsim: string which is either 'yes' or 'no'


        return: string team name
    """
	def getNewStrategy(self, teams, multsim):
		
		concrete_strategy_new = ConcreteStrategyNew()
		simulation = Simulation(concrete_strategy_new)
		if (multsim == 'yes'):
			multisim = MultiSimState()
			multicontext = SimContext(multisim)
			winner = multicontext.request(teams=teams,strategy=simulation)
			return winner
		else:
			singlesim = SingleSimState()
			singlecontext = SimContext(singlesim)
			winner = singlecontext.request(teams=teams,strategy=simulation)
			return winner

		
	def getOldStrategy(self):
		return None

class OldStrategyFactory(SimAbstractFactory):
	"""
        Concrete class for Abstract Factory design pattern, to get Old Strategy
        Params:
        teams: list of team names
        multsim: string which is either 'yes' or 'no'


        return: string team name
    """
	def getNewStrategy(self):
		return None
	def getOldStrategy(self,teams,multsim):
		concrete_strategy_old = ConcreteStrategyOld()
		simulation = Simulation(concrete_strategy_old)
		if (multsim == 'yes'):
			multisim = MultiSimState()
			multicontext = SimContext(multisim)
			winner = multicontext.request(teams=teams,strategy=simulation)
			return winner
		else:
			singlesim = SingleSimState()
			singlecontext = SimContext(singlesim)
			winner = singlecontext.request(teams=teams,strategy=simulation)
			return winner
class FactoryCreator:
	"""
        Static method which is called in ResultsController in app.py
        Params:
        teams: list of team names
        multsim: string which is either 'yes' or 'no'
        posTStrat: string of strategy name which is either 'old' or 'new'


        return: abstract factory class
    """
	@staticmethod
	def getFactory(postStrat,teams,multsim):
		if postStrat == 'new':
			newstrat = NewStrategyFactory()
			return newstrat.getNewStrategy(teams,multsim)
		elif postStrat == 'old':
			oldstrat = OldStrategyFactory()
			return oldstrat.getOldStrategy(teams,multsim)
		else:
			return None