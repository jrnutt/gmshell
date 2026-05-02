"""Player management module."""

import combatant
import sys


class Player(combatant.Combatant):
    """This class encapsulates the extras needed for players."""

    def __init__(self, n="", cls="", lvl='', hp=0, ac=0, per=0, inv=0, ins=0,
                 init=0.0, nick=None, conditions=[]):
        """Initialize the player class."""
        super().__init__(n=n, nick=nick, hp=hp, ac=ac, init=init, conditions=conditions)
        self.cls = cls
        self.lvl = lvl
        self.per = per
        self.inv = inv
        self.ins = ins

    def print(self, file=sys.stdout, summary=True):
        """Print the player information to the specified file."""
        super().print(file=file)
        if not summary:
            print("Class: {} lvl: {}".format(self.getClass(), self.getLevel()),
                  file=file)
            print("Passives:", file=file)
            print("\tPerception:    {}".format(self.getPerception()),
                  file=file)
            print("\tInvestigation: {}".format(self.getInvestigation()),
                  file=file)
            print("\tInsight:       {}".format(self.getInsight()),
                  file=file)

    def setClass(self, arg):
        """Set the player class."""
        self.cls = arg

    def getClass(self):
        """Get the player class."""
        return self.cls

    def setLevel(self, arg):
        """Set the player level."""
        self.lvl = arg

    def getLevel(self):
        """Get the player level."""
        return self.lvl

    def setPerception(self, arg):
        """Set passive perception."""
        try:
            self.per = int(arg)
        except Exception:
            print("need a numeric value for perception")
            return

    def getPerception(self):
        """Get passive perception."""
        return self.per

    def setInvestigation(self, arg):
        """Set passive investigation."""
        try:
            self.inv = int(arg)
        except Exception:
            print("need a numeric value for investigation")
            return

    def getInvestigation(self):
        """Get passive investigation."""
        return self.inv

    def setInsight(self, arg):
        """Set passive insight."""
        try:
            self.ins = int(arg)
        except Exception:
            print("need a numeric value for insight")
            return

    def getInsight(self):
        """Get passive insight."""
        return self.ins

    def set(self, arg):
        """Set player characteristics."""
        k, v = super().set(arg)
        match(k):
            case "cls":
                self.setClass(v)
            case "lvl":
                self.setLevel(v)
            case "per":
                self.setPerception(v)
            case "inv":
                self.setInvestigation(v)
            case "ins":
                self.setInsight(v)
            case _:
                return k, v
        return k, v
