import cmd, sys
import csv
import pickle

from io import StringIO
from player import Player
from mob import Mob

class GMShell(cmd.Cmd):
	intro = 'Welcome to the GM Shell, a utility to help Game Masters manage game play'
	prompt = '(cmd) '
	file = None
	last = 0
	players = dict()
	mobs = dict()

	def do_quit(self, arg):
		'Exit GM Shell'
		return True

	def do_player(self, arg):
		'Set player information'
		p = parse(arg)

		pn = p.pop(0).lower();
		c = "unknown"
		l = 0
		a = 0
		per = 0
		inv = 0
		ins = 0
		init = 0
		exists = pn in self.players
		for i in p:
			n,v = i.split('=')
			n = n.lower()
			if (n.startswith('c')):
				c = v
				if exists:
					  self.players[pn].setClass(c)
			elif (n.startswith('l')):
				l = int(v)
				if exists:
					self.players[pn].setLevel(l)
			elif (n.startswith('a')):
				a = int(v)
				if exists:
					self.players[pn].setAC(a)
			elif (n.startswith('ini')):
				init = int(v)
				if exists:
					self.players[pn].setInitiative(init)
			elif (n.startswith('per')):
				per = int(v)
				if exists:
					self.players[pn].setPerception(per)
			elif (n.startswith('inv')):
				inv = int(v)
				if exists:
					self.players[pn].setInvestigation(inv)
			elif (n.startswith('ins')):
				ins = int(v)
				if exists:
					self.players[pn].setInsight(ins)

		if not exists:
			player = Player(pn, pclass=c, level=l, ac=a, per=per, inv=inv, ins=ins, init=init)
			self.players[player.getName()] = player
		print("Player \'{}\' {}".format(pn, 'updated' if exists else 'added'))

	def do_mob(self, arg):
		'Set mob information'
		p = parse(arg)

		mn = p.pop(0).lower();
		if p[0] == "delete" and mn in mobs:
			del self.mobs[mn]
			print("Mob \'{}\' removed".format(mn))
		else:
			a = 0
			h = 0
			init = 0
			exists = mn in self.mobs
			for i in p:
				n,v = i.split('=')
				n = n.lower()
				if (n.startswith('a')):
					a = int(v)
					if exists:
						self.mobs[mn].setAC(a)
				elif (n.startswith('i')):
					init = int(v)

					if exists:
						self.mobs[mn].setInitiative(init)
				elif (n.startswith('h')):
					h = int(v)
					if exists:
						self.mobs[mn].setHP(h)
				elif (n.startswith('-h')):
					h = int(v)
					if exists:
						self.mobs[mn].setHP(self.mobs[mn].getHP() - h)
				elif (n.startswith('+h')):
					h = int(v)
					if exists:
						self.mobs[mn].setHP(self.mobs[mn].getHP() + h)

			if not exists:
				mob = Mob(mn, ac=a, hp=h, init=init)
				self.mobs[mob.getName()] = mob
			print("Mob \'{}\' {}".format(mn, 'updated' if exists else 'added'))

	def do_players(self, arg):
		plist = sorted(self.players.values(),reverse=True)
		if arg.startswith("save"):
			c,fn = arg.split(" ")
			print("saving players to {}".format(fn))
			self.save(self.players,fn)
		elif arg.startswith("load"):
			c,fn = arg.split(" ")
			print("loading players from {}".format(fn))
			self.players = self.load(fn)
			self.do_players("list")
		else:
			for p in plist:
				p.print(sys.stdout)
				print()

	def save(self, obj, fn):
		with open(fn,"wb") as f:
			pickle.dump(obj,f)

	def load(self, fn):
		with open(fn,"rb") as f:
			return pickle.load(f)

	def do_mobs(self, arg):
		mlist = sorted(self.mobs.values(),reverse=True)
		if arg.startswith("save"):
			c,f = arg.split(" ")
			print("saving mobs to {}".format(f))
			self.save(self.mobs,f)
		elif arg.startswith("load"):
			c,f = arg.split(" ")
			print("loading mobs from {}".format(f))
			self.mobs = self.load(f)
			self.do_mobs("list")
		else:
			for m in mlist:
				m.print(sys.stdout)
				print()

	def initiative(self, arg):
		plist = sorted(self.players.values(),reverse=True)
		mlist = sorted(self.mobs.values(),reverse=True)
		combatants = list(plist)
		combatants.extend(mlist)
		initorder = sorted(combatants, reverse=True)
		if self.last >= len(initorder):
			self.last = 0

		if arg == "list" or len(arg) == 0:
			i = 1
			for c in initorder:
				print("{} {}".format(i, c.getName()))
				i += 1
		
		elif arg == "clear":
			self.last = 0

		elif arg == "next":
			print(initorder[self.last].getName())
			self.last += 1

	def do_initiative(self,arg):
		self.initiative(arg)

	def do_init(self, arg):
		self.initiative(arg)

	def do_next(self, arg):
		self.initiative("next")

def parse(arg):
    'Convert a string to an argument tuple'
    reader = csv.reader(StringIO(arg),delimiter=' ') 
    return reader.__next__()

if __name__ == '__main__':
    GMShell().cmdloop()

