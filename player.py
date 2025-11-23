import combatant
import sys


class Player(combatant.Combatant):

    def __init__(self, n="", cls="", lvl='', hp=0, ac=0, per=0, inv=0, ins=0,
                 init=0.0, nick=None, conditions=[]):
        super().__init__(n=n, hp=hp, ac=ac, init=init, conditions=conditions)
        self.cls = cls
        self.lvl = lvl
        self.per = per
        self.inv = inv
        self.ins = ins
        self.nick = nick
        if nick is None:
            self.nick = n

    def print(self, file=sys.stdout, summary=True):
        super().print(file=file)
        if not summary:
            if len(self.getNick()) > 0 and not self.getNick().isspace():
                print("Nick: {} ".format(self.getNick()), file=file)
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
        self.cls = arg

    def getClass(self):
        return self.cls

    def setLevel(self, arg):
        self.lvl = arg

    def getLevel(self):
        return self.lvl

    def setPerception(self, arg):
        try:
            self.per = int(arg)
        except Exception:
            print("need a numeric value for perception")
            return

    def getPerception(self):
        return self.per

    def setInvestigation(self, arg):
        try:
            self.inv = int(arg)
        except Exception:
            print("need a numeric value for investigation")
            return

    def getInvestigation(self):
        return self.inv

    def setInsight(self, arg):
        try:
            self.ins = int(arg)
        except Exception:
            print("need a numeric value for insight")
            return

    def getInsight(self):
        return self.ins

    def getNick(self):
        return self.nick

    def setNick(self, arg):
        self.nick = arg

    def set(self, arg):
        k, v = super().set(arg)
        match(k):
            case "cls":
                self.setClass(v)
            case "lvl":
                self.setLevel(v)
            case "nick":
                self.setNick(v)
            case "per":
                self.setPerception(v)
            case "inv":
                self.setInvestigation(v)
            case "ins":
                self.setInsight(v)
            case _:
                return k, v
        return k, v
