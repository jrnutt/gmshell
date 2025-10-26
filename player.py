import combatant
import sys

class Player(combatant.Combatant):
	def __init__(self, n="", cls="", lvl='', hp=0, ac=0, per=0, inv=0, ins=0, init=0.0, nick = None, conditions=[]):
		super().__init__(n=n, hp=hp, ac=ac, init=init, conditions=conditions)
		self.cls = cls
		self.lvl = lvl
		self.per = per
		self.inv = inv
		self.ins = ins
		self.nick = nick
		if nick is None:
			self.nick = n			


	def print(self, file=sys.stdout):
		super().print(file=file)
		print("Nick: {} ".format(self.getNick()), file=file)
		print("Class: {} lvl: {}".format(self.getClass(), self.getLevel()), file=file)
		print("Passives:", file=file)
		print("\tPerception:    {}".format(self.getPerception()), file=file)
		print("\tInvestigation: {}".format(self.getInvestigation()), file=file)
		print("\tInsight:       {}".format(self.getInsight()), file=file)

	def setClass(self, arg):
		self.cls = arg

	def getClass(self):
		return self.cls

	def setLevel(self, arg):
		self.lvl = arg

	def getLevel(self):
		return self.lvl

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


