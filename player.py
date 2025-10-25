import combatant
import sys

class Player(combatant.Combatant):
	def __init__(self, n="", pclass="", level='', ac=0, per=0, inv=0, ins=0, init=0.0, nick = None):
		self.n = n
		self.ac = ac
		self.init = init
		self.pclass = pclass
		self.level = level
		self.per = per
		self.inv = inv
		self.ins = ins
		self.nick = nick
		if nick is None:
			self.nick = n			


	def print(self, file=sys.stdout):
		print("Name: {} Nick: {}".format(self.n,self.nick),file=file)
		print("Class: {} Level: {}".format(self.pclass,self.level),file=file)
		print("AC: {} Initiative: {}".format(self.ac,self.init),file=file)
		print("Passives:",file=file)
		print("\tPerception:    {}".format(self.per),file=file)
		print("\tInvestigation: {}".format(self.inv),file=file)
		print("\tInsight:       {}".format(self.ins),file=file)

	def write(self, file=sys.stdout):
		print("player '{self.n}' cls={self.pclass} lvl={self.level} ac={self.ac} init={self.init} per={self.per} inv={self.inv} ins={self.ins} nick={self.nick}".format(self=self),file=file)

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

	def getNick(self):
		return self.nick

	def setNick(self, arg):
		self.nick = arg


