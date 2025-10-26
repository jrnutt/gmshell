import combatant
import secrets
import sys

class Mob(combatant.Combatant):
	def __init__(self, n, hp=0, ac=0, init=0.0, bonus=0, conditions=[]):
		super().__init__(n=n, hp=hp, ac=ac, init=init, conditions=conditions)
		self.bonus = bonus

	def getBonus(self):
		return self.bonus

	def setBonus(self, arg):
		self.bonus = arg

	def rollInit(self):
		self.init = secrets.choice(range(20)) + 1 + self.bonus

	def print(self, file=sys.stdout):
		super().print(file=file)
		print("Name: {}".format(self.getName()),file=file)

	def write(self, file=sys.stdout):
		print("mob {self.n} ac={self.ac} hp={self.hp} bonus={self.bonus} init={self.init}".format(self=self),end=" ",file=file)
		if len(self.conditions) > 0:
			for c in self.conditions:
				print("+{}".format(c), end=" ", file=file)
		print("",file=file)

	def copy(self):
		return Mob(self.n, self.hp, self.ac, self.init, self.bonus)