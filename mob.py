"""Module for managing mobs (monsters)."""
import combatant
import sys


class Mob(combatant.Combatant):
    """Class for maintaining mob information."""

    def __init__(self, n, nick=None, hp=0, ac=0, init=0.0, bonus=0,
                 conditions=[]):
        """Initialize the mob."""
        super().__init__(n=n, nick=nick, hp=hp, ac=ac, init=init,
                         conditions=conditions)
        self.bonus = bonus

    def getBonus(self):
        """Get the mob initiative modifier."""
        return self.bonus

    def setBonus(self, arg):
        """Set the mob initiative modifier."""
        try:
            self.bonus = int(arg)
        except Exception:
            print("initiative bonus must be numeric")
            return

    def print(self, file=sys.stdout, summary=False):
        """Print formatted mob info to file."""
        super().print(file=file)

    def copy(self):
        """Copy a mob to a new instance."""
        return Mob(n=self.n,
                   hp=self.hp,
                   ac=self.ac,
                   init=self.init,
                   bonus=self.bonus,
                   conditions=self.conditions.copy())

    def set(self, arg):
        """Set a mob parameter."""
        k, v = super().set(arg)
        match(k):
            case "bonus":
                self.setBonus(v)
            case _:
                return k, v
        return k, v
