

class PlayoffConcreteIterator:
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
		return PlayoffConcreteIterator(self.rounds)