

class Simulation:
	def __init__(self,strategy):
		self._strategy = strategy

	def simulation_interface(self,team1,team2):
		return self._strategy.algorithm_interface(team1,team2)