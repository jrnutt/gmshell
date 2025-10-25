import combatant
import sys

class Player(combatant.Combatant):
	def __init__(self, n="", pclass="", level='', hp=0, ac=0, per=0, inv=0, ins=0, init=0.0, nick = None, conditions=[]):
		super().__init__(n=n, hp=hp, ac=ac, init=init, conditions=conditions)
		self.pclass = pclass
		self.level = level
		self.per = per
		self.inv = inv
		self.ins = ins
		self.nick = nick
		if nick is None:
			self.nick = n			


	def print(self, file=sys.stdout):
		super().print(file=file)
		print("Nick: {} ".format(self.getNick()), file=file)
		print("Class: {} Level: {}".format(self.getClass(),self.getLevel()), file=file)
		print("Passives:", file=file)
		print("\tPerception:    {}".format(self.getPerception()), file=file)
		print("\tInvestigation: {}".format(self.getInvestigation()), file=file)
		print("\tInsight:       {}".format(self.getInsight()), file=file)

	def write(self, file=sys.stdout):
		print("player '{self.n}' cls={self.pclass} lvl={self.level} ac={self.ac} init={self.init} per={self.per} inv={self.inv} ins={self.ins} nick={self.nick}".format(self=self),file=file)

	def setClass(self, arg):
		self.pclass = arg

	def getClass(self):
		return self.pclass

	def setLevel(self, arg):
		self.level = arg

	def getLevel(self):
		return self.level

	def setPerception(self, arg):
		self.per = arg

	def getPerception(self):
		return self.per

	def setInvestigation(self, arg):
		self.inv = arg

	def getInvestigation(self):
		return self.inv

	def setInsight(self, arg):
		self.ins = arg

	def getInsight(self):
		return self.ins

	def getNick(self):
		return self.nick

	def setNick(self, arg):
		self.nick = arg


