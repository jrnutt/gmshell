import combatant
import sys

class Mob(combatant.Combatant):
        def __init__(self, n, hp=0, ac=0, init=0.0, bonus=0, conditions=[]):
                super().__init__(n=n, hp=hp, ac=ac, init=init, conditions=conditions)
                self.bonus = bonus

        def getBonus(self):
                return self.bonus

        def setBonus(self, arg):
                self.bonus = arg

        def print(self, file=sys.stdout):
                super().print(file=file)

        def copy(self):
                return Mob(n=self.n, hp=self.hp, ac=self.ac, init=self.init, bonus=self.bonus, conditions=self.conditions)
