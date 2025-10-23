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

	def setName(self,n):
		self.n = n

	def getName(self):
		return self.n

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

	def copy(self):
		return Mob(self.n, self.hp, self.ac, self.init, self.bonus)