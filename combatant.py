import sys

class Combatant:
	def __init__(self, n, hp=0, ac=0, init=0.0, conditions=[]):
		self.n = n
		self.ac = ac
		self.hp = hp
		self.init = init
		self.conditions = set(conditions)

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

	def setHP(self,arg):
		self.hp = arg

	def getHP(self):
		return self.hp

	def getConditions(self):
		return self.conditions

	def setConditions(self, conditions):
		self.conditions = conditions

	def addCondition(self, condition):
		self.conditions.add(condition)

	def remCondition(self, condition):
		self.conditions.remove(condition)

	def print(self, file=sys.stdout):
		print("Name: {}".format(self.getName()), file=file)
		print("AC: {} HP: {} Initiative: {} ".format(self.getAC(), self.getHP(), self.getInitiative()), file=file)
		if len(self.conditions) > 0: 
			print("Conditions: ", end="", file=file)
			for c in self.conditions:
				print(c, end=" ", file=file)
			print("", file=file)

	def write(self, file=sys.stdout):
		print("{} {}".format(type(self).__name__.lower(), self.n), end=' ', file =file)
		d = vars(self)
		for a in d:
			if a == 'n':
				continue
			if a == 'conditions':
				for c in d[a]:
					print("+{}".format(c), end=" ", file=file)
				continue

			print("{}={}".format(a,d[a]), end=" ", file=file)
		print()

	def __lt__(self, arg):
		return self.getInitiative() < arg.getInitiative()
