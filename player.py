import combatant

class Player(combatant.Combatant):
	def __init__(self, n="", pclass="", level=0, ac=0, per=0, inv=0, ins=0, init=0):
		self.n = n
		self.ac = ac
		self.init = init
		self.pclass = pclass
		self.level = level
		self.per = per
		self.inv = inv
		self.ins = ins

	def print(self, out):
		print("Name: {}".format(self.n),file=out)
		print("Class: Level {} {}".format(self.level,self.pclass),file=out)
		print("AC: {} Initiative: {}".format(self.ac,self.init),file=out)
		print("Passives:",file=out)
		print("\tPerception:    {}".format(self.per),file=out)
		print("\tInvestigation: {}".format(self.inv),file=out)
		print("\tInsight:       {}".format(self.ins),file=out)

	def setClass(self, arg):
		self.pclass = arg

	def setLevel(self, arg):
		self.level = arg

	def setPerception(self, arg):
		self.per = arg

	def setInvestigation(self, arg):
		self.inv = arg

	def setInsight(self, arg):
		self.ins = arg


