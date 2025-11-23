import sys
import secrets


class Combatant:
    def __init__(self, n, hp=0, ac=0, init=0.0, conditions=[]):
        self.n = n
        self.ac = ac
        self.hp = hp
        self.init = init
        self.mhp = hp
        self.conditions = set(conditions)

    def getName(self):
        return self.n

    def setName(self, arg):
        self.n = arg

    def getAC(self):
        return self.ac

    def setAC(self, arg):
        try:
            self.ac = int(arg)
        except Exception:
            print("Need an integer value for armor class")

    def getInitiative(self):
        return self.init

    def setInitiative(self, arg):
        try:
            self.init = float(arg)
        except Exception:
            print("need a numeric value for initiative")

    def setHP(self, arg):
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
        return self.hp

    def getMaxHP(self):
        return self.mhp

    def setMaxHP(self, arg):
        try:
            self.hp = int(arg)
        except Exception:
            print("Need a numeric value for hit points")
            return

        self.mhp = self.hp
        self.remCondition('bloodied')

    def getConditions(self):
        return self.conditions

    def setConditions(self, conditions):
        self.conditions = conditions

    def addCondition(self, condition):
        self.conditions.add(condition)

    def remCondition(self, condition):
        self.conditions.discard(condition)

    def rollInit(self):
        self.init = secrets.choice(range(1, 21)) + self.bonus
        print(self.n, self.init)

    def set(self, arg):
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

    def printSummary(self, full=False, file=sys.stdout):
        print("{}".format(self.getName()), end=" ", file=file)
        print("AC: {} HP: {}/{} Initiative: {} ".format(self.getAC(),
                                                        self.getHP(),
                                                        self.getMaxHP(),
                                                        self.getInitiative()),
              end=" ", file=file)

        if len(self.conditions) > 0:
            if full:
                print("Conditions: ", end="", file=file)
                for c in self.conditions:
                    print(c, end=" ", file=file)
        print("", file=file)

    def print(self, file=sys.stdout):
        self.printSummary(full=True, file=file)

    def write(self, file=sys.stdout):
        print("{}".format(type(self).__name__.lower()),
              end=' ',
              file=file)
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
        return self.getInitiative() < arg.getInitiative()
