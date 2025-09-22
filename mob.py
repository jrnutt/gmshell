import combatant

class Mob(combatant.Combatant):
	def __init__(self, n, hp=0, ac=0, init=0):
		self.hp = hp
		self.n = n
		self.ac = ac
		self.init = init

	def getHP(self):
		return self.hp

	def setHP(self, arg):
		self.hp = arg

	def print(self, out):
		print("Name: {}".format(self.n),file=out)
		print("AC: {} HP: {} Initiative: {} ".format(self.ac,self.hp, self.init),file=out)

