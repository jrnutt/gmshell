import combatant
import secrets
import sys

class Mob(combatant.Combatant):
	def __init__(self, n, hp=0, ac=0, init=0.0, bonus=0):
		self.hp = hp
		self.n = n
		self.ac = ac
		self.init = init
		self.bonus = bonus

	def getBonus(self):
		return self.bonus

	def setBonus(self, arg):
		self.bonus = arg

	def rollInit(self):
		self.init = secrets.choice(range(20)) + 1 + self.bonus

	def print(self, file=sys.stdout):
		print("Name: {}".format(self.n),file=file)
		print("AC: {} HP: {} Initiative: {} ".format(self.ac,self.hp, self.init),file=file)

	def write(self, file=sys.stdout):
		print("mob {self.n} ac={self.ac} hp={self.hp} bonus={self.bonus} init={self.init}".format(self=self),file=file)

	def copy(self):
		return Mob(self.n, self.hp, self.ac, self.init, self.bonus)