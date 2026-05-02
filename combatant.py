"""Combatant management module."""

import sys
import secrets


class Combatant:
    """Manage combatants."""

    def __init__(self, n, nick=None, hp=0, ac=0, init=0.0, conditions=[]):
        """Initialize base values for class."""
        self.n = n
        self.nick = nick
        self.ac = ac
        self.hp = hp
        self.init = init
        self.mhp = hp
        self.conditions = set(conditions)

    def getNick(self):
        """Get nickname."""
        return self.nick

    def setNick(self, arg):
        """Set nickname."""
        self.nick = arg

    def getName(self):
        """Get combatant name."""
        return self.n

    def setName(self, arg):
        """Set combatant name."""
        self.n = arg

    def getAC(self):
        """Get armor class."""
        return self.ac

    def setAC(self, arg):
        """Set armor class."""
        try:
            self.ac = int(arg)
        except Exception:
            print("Need an integer value for armor class")

    def getInitiative(self):
        """Get initiative."""
        return self.init

    def setInitiative(self, arg):
        """Set initiative."""
        try:
            self.init = float(arg)
        except Exception:
            print("need a numeric value for initiative")

    def setHP(self, arg):
        """Set hit points."""
        try:
            self.hp = int(arg)
        except Exception:
            print("Need a numeric value for hit points")
            return

        if self.hp <= (self.mhp / 2):
            self.addCondition('bloodied')
        else:
            self.remCondition('bloodied')
        if self.hp <= 0:
            self.addCondition('dead')
        else:
            self.remCondition('dead')
        if self.hp <= -self.mhp:
            self.addCondition('really dead')
        else:
            self.remCondition('really dead')

    def getHP(self):
        """Get hit points."""
        return self.hp

    def getMaxHP(self):
        """Get max hit points."""
        return self.mhp

    def setMaxHP(self, arg):
        """Set max hit points."""
        try:
            self.hp = int(arg)
        except Exception:
            print("Need a numeric value for hit points")
            return

        self.mhp = self.hp
        self.remCondition('bloodied')

    def getConditions(self):
        """Get conditions."""
        return self.conditions

    def setConditions(self, conditions):
        """Set conditions."""
        self.conditions = conditions

    def addCondition(self, condition):
        """Add a condition."""
        self.conditions.add(condition)

    def remCondition(self, condition):
        """Remove a condition."""
        self.conditions.discard(condition)

    def rollInit(self):
        """Roll initiative."""
        self.init = secrets.choice(range(1, 21)) + self.bonus
        print(self.n, self.init)

    def set(self, arg):
        """Set a combatant property."""
        if '=' in arg:
            k, v = arg.split('=')
        else:
            k = arg
            v = None

        match(k):
            case "hp":
                self.setMaxHP(v)
            case "ac":
                self.setAC(v)
            case "init":
                self.setInitiative(v)
            case _ if k.startswith('+'):
                self.addCondition(k.removeprefix('+'))
            case _ if k.startswith('-'):
                self.remCondition(k.removeprefix('-'))
            case _:
                return k, v
        return k, v

    def print(self, file=sys.stdout):
        """Print formatted combatant information to a file."""
        print("{}".format(self.getName()), end=" ", file=file)
        if len(self.getNick()) > 0 and not self.getNick().isspace():
            print("Nick: {} ".format(self.getNick()), file=file)
        print("AC: {} HP: {}/{} Initiative: {} ".format(self.getAC(),
                                                        self.getHP(),
                                                        self.getMaxHP(),
                                                        self.getInitiative()),
              end=" ", file=file)

        if len(self.conditions) > 0:
            print("Conditions: ", end="", file=file)
            for c in self.conditions:
                print(c, end=" ", file=file)
        print("", file=file)

    def write(self, file=sys.stdout):
        """Write parsable combatant information to a file."""
        print("{}".format(type(self).__name__.lower()),
              end=' ', file=file)
        na = self.n
        if ' ' in na:
            na = '"' + na + '"'
        print("{}".format(na), end=' ', file=file)
        d = vars(self)
        for a in d:
            if a == 'n':
                continue
            elif a == 'conditions':
                for c in d[a]:
                    print("+{}".format(c), end=" ", file=file)
            else:
                print("{}={}".format(a, d[a]), end=" ", file=file)
        print(file=file)

    def __lt__(self, arg):
        """Compare based on initiative."""
        return self.getInitiative() < arg.getInitiative()
