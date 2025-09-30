#!/usr/bin/python
import cmd, sys
import csv
import pickle
import readline

from io import StringIO
from player import Player
from mob import Mob

class GMShell(cmd.Cmd):
	intro = 'Welcome to the GM Shell, a utility to help Game Masters manage game play'
	prompt = '(cmd) '
	file = None
	nextp = 0
	players = list()
	mobs = dict()

	def do_quit(self, arg):
		'Exit GM Shell'
		return True

	def findPlayer(self, pn):
		'Find player by name'

		try:
			for p in self.players:
				if p.getNick() == pn or p.getName() == pn:
					return p
		except:
			print("error locating player {}".format(pn))
		return None


	def do_player(self, arg):
		'Set player information'

		try:
			p = parse(arg.replace("'",'"'))

			pn = p.pop(0).lower();
			c = "unknown"
			l = 0
			a = 0
			per = 0
			inv = 0
			ins = 0
			init = 0
			nick = None

			player = self.findPlayer(pn)
			for i in p:
				n,v = i.split('=')
				n = n.lower()
				if (n.startswith('c')):
					c = v
					if player is not None:
						  player.setClass(c)
				elif (n.startswith('l')):
					l = int(v)
					if player is not None:
						player.setLevel(l)
				elif (n.startswith('a')):
					a = int(v)
					if player is not None:
						player.setAC(a)
				elif (n.startswith('ini')):
					init = int(v)
					if player is not None:
						player.setInitiative(init)
				elif (n.startswith('per')):
					per = int(v)
					if player is not None:
						player.setPerception(per)
				elif (n.startswith('inv')):
					inv = int(v)
					if player is not None:
						player.setInvestigation(inv)
				elif (n.startswith('ins')):
					ins = int(v)
					if player is not None:
						player.setInsight(ins)
				elif (n.startswith('nick')):
					nick = v
					if player is not None:
						player.setNick(nick)

			if player is None:
				player = Player(pn, pclass=c, level=l, ac=a, per=per, inv=inv, ins=ins, init=init, nick=nick)
				self.players.append(player)
				print("Player \'{}\' added".format(pn))
			else:
				print("Player \'{}\' updated".format(pn))
			player.print(sys.stdout)
		except Exception as ex:
			print("Got exception {} trying to process {}".format(ex,arg))

	def do_mob(self, arg):
		'Set mob information'

		try: 
			p = parse(arg)

			mn = p.pop(0).lower();
			if p[0] == "delete" and mn in self.mobs:
				del self.mobs[mn]
				print("Mob \'{}\' removed".format(mn))
			else:
				a = 0
				h = 0
				init = 0
				exists = mn in self.mobs
				for i in p:
					try:
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
						elif (n.startswith('b')):
							b = int(v)
							if exists:
								self.mobs[mn].setBonus(b)
						elif (n.startswith('-h')):
							h = int(v)
							if exists:
								self.mobs[mn].setHP(self.mobs[mn].getHP() - h)
							if self.mobs[mn].getHP() < 1:
								print("{} is dead".format(mn))
								del self.mobs[mn]
						elif (n.startswith('+h')):
							h = int(v)
							if exists:
								self.mobs[mn].setHP(self.mobs[mn].getHP() + h)
					except ValueError:
						print("Missing or bad value in {}".format(i))

				if not exists:
					mob = Mob(mn, ac=a, hp=h, init=init)
					self.mobs[mob.getName()] = mob
				print("Mob \'{}\' {}".format(mn, 'updated' if exists else 'added'))
				if mn in self.mobs:
					self.mobs[mn].print(sys.stdout)
		except Exception as ex:
			print("Got exception {} trying to process {}".format(ex,arg))

	def do_players(self, arg):
		try:
			plist = sorted(self.players,reverse=True)
			if arg.startswith("save"):
				c,fn = arg.split(" ")
				print("saving players to {}".format(fn))
				self.save(self.players,fn)
			elif arg.startswith("load"):
				c,fn = arg.split(" ")
				print("loading players from {}".format(fn))
				pl = self.load(fn)
				if pl is not None:
					for p in pl:
						if self.findPlayer(p.getName()) is None:
							self.players.append(p)
				self.do_players("list")
			else:
				for p in plist:
					p.print(sys.stdout)
					print()
		except Exception as ex:
			print("Got exception {} trying to process {}".format(ex,arg))

	def save(self, obj, fn):
		try:
			with open(fn,"wb") as f:
				pickle.dump(obj,f)
		except:
			print("Did not save file {}".format(fn))

	def load(self, fn):
		try:
			with open(fn,"rb") as f:
				return pickle.load(f)
		except:
			print("Did not load file {}".format(fn))
			return None

	def do_mobs(self, arg):
		try:
			mlist = sorted(self.mobs.values(),reverse=True)
			if arg.startswith("save"):
				c,f = arg.split(" ")
				print("saving mobs to {}".format(f))
				self.save(self.mobs,f)
			elif arg.startswith("load"):
				c,f = arg.split(" ")
				print("loading mobs from {}".format(f))
				m = self.load(f)
				if m is not None:
					self.mobs.update(m)
				self.do_mobs("list")
			elif arg.startswith("cl"):
				self.mobs = dict()
			elif arg.startswith('ro'):
				for m in mlist:
					m.rollInit()
			else:
				for m in mlist:
					m.print(sys.stdout)
					print()
		except Exception as ex:
			print("Got exception {} trying to process {}".format(ex,arg))

	def initiative(self, arg):
		try:
			plist = sorted(self.players,reverse=True)
			mlist = sorted(self.mobs.values(),reverse=True)
			combatants = list(plist)
			combatants.extend(mlist)
			initorder = sorted(combatants, reverse=True)
			self.nextp = self.nextp % len(initorder)

			if arg == "list" or len(arg) == 0:
				for c in initorder[self.nextp:]:
					print("{} {}".format(c.getName(),c.getInitiative()))
				for c in initorder[:self.nextp]:
					print("{} {}".format(c.getName(),c.getInitiative()))
			
			elif arg == "clear" or arg == 'reset':
				self.nextp = 0

			elif arg == "next":
				print(initorder[self.nextp].getName())
				self.nextp += 1
		except Exception as ex:
			print("Got exception {} trying to process {}".format(ex,arg))

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
	try:
		readline.read_history_file('.gmshell.history')
	except:
		with open('.gmshell.history','w'):
			print("no history to load")
	GMShell().cmdloop()
	readline.write_history_file('.gmshell.history')

