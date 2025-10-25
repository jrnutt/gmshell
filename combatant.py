class Combatant:
	def __init__(self, n, hp=0, ac=0, init=0.0):
		self.n = n
		self.ac = ac
		self.init = init

	def getName(self):
		return self.n

	def setName(self, arg):
		self.n = arg

	def getAC(self):
		return self.ac

	def setAC(self, arg):
		self.ac = arg

	def getInitiative(self):
		return self.init

	def setInitiative(self,arg):
		self.init = arg

	def print(self, out):
		print("Name: {}".format(self.n),file=out)
		print("AC: {} HP: {} Initiative: {} ".format(self.ac, self.init),file=out)

	def __lt__(self, arg):
		return self.getInitiative() < arg.getInitiative()
