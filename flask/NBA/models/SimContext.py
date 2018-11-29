

class SimContext:

	def __init__(self, state):
		self._state = state

	def request(self, teams, strategy):
		return self._state.handle(teams, strategy)