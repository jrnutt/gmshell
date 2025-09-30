import combatant
import secrets

class Mob(combatant.Combatant):
	def __init__(self, n, hp=0, ac=0, init=0, bonus=0):
		self.hp = hp
		self.n = n
		self.ac = ac
		self.init = init
		self.bonus = bonus

	def getHP(self):
		return self.hp

	def setHP(self, arg):
		self.hp = arg

	def getBonus(self):
		return self.bonus

	def setBonus(self, arg):
		try: 
			self.bonus = int(arg)
		except:
			self.bonus=0

	def rollInit(self):
		self.init = secrets.choice(range(20)) + 1 + self.bonus

	def print(self, out):
		print("Name: {}".format(self.n),file=out)
		print("AC: {} HP: {} Initiative: {} ".format(self.ac,self.hp, self.init),file=out)

