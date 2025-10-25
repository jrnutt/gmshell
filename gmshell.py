#!/usr/bin/python
import cmd2, sys
import csv
import pickle
import readline

from io import StringIO
from player import Player
from mob import Mob

from cmd2 import Cmd2ArgumentParser, with_argparser, with_argument_list

class GMShell(cmd2.Cmd):
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
			print("error locating player {}".format(pn),file=self.stdout)

		return None

	def do_player(self, arg):
		'Set player information'

		try:
			arguments = arg.arg_list

			pn = cmd2.utils.strip_quotes(arguments.pop(0))

			c = "unknown"
			l = 0
			a = 0
			per = 0
			inv = 0
			ins = 0
			init = 0
			nick = None

			player = self.findPlayer(pn)
			for i in arguments:
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
				print("Player \'{}\' added".format(pn),file=self.stdout)
			else:
				print("Player \'{}\' updated".format(pn),file=self.stdout)
		except Exception as ex:
			print("Got exception {} trying to process {}".format(ex,arg),file=self.stdout)

	def do_mob(self, arg):
		'Set mob information'

		try: 
			p = arg.arg_list

			mn = cmd2.utils.strip_quotes(p.pop(0).lower());
			if len(p) > 0:
				if p[0] == "delete" and mn in self.mobs:
					del self.mobs[mn]
					print("Mob \'{}\' removed".format(mn))
				elif p[0] == "copy" and mn in self.mobs:
					m = self.mobs[mn].copy()
					i = 1
					r = mn
					if '-' in mn:
						r,c = mn.split('-')
						if c.isnumeric():
							i = int(c)
					n = r + '-' + str(i)
					while (n in self.mobs):
						i += 1
						n = r + '-' + str(i)
					m.setName(n)
					self.mobs[n] = m
					print("Mob \'{}\' added".format(n),file=self.stdout)
					mn = n
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
									if  v.startswith('-') or v.startswith('+'):
										self.mobs[mn].setHP(self.mobs[mn].getHP() + h)
									else:
										self.mobs[mn].setHP(h)
							elif (n.startswith('b')):
								b = int(v)
								if exists:
									self.mobs[mn].setBonus(b)
							elif (n.startswith('-h')):
								h = int(v)
								if exists:
									self.mobs[mn].setHP(self.mobs[mn].getHP() - h)
							elif (n.startswith('+h')):
								h = int(v)
								if exists:
									self.mobs[mn].setHP(self.mobs[mn].getHP() + h)
						except ValueError:
							print("Missing or bad value in {}".format(i),file=self.stdout)

					if not exists:
						mob = Mob(mn, ac=a, hp=h, init=init)
						self.mobs[mob.getName()] = mob

					print("Mob \'{}\' {}".format(mn, 'updated' if exists else 'added'),file=self.stdout)

					if self.mobs[mn].getHP() <= 0:
						print("{} is dead".format(mn))
						del self.mobs[mn]

			if mn in self.mobs:
				self.mobs[mn].print(self.stdout)

		except Exception as ex:
			print("Got exception {} trying to process {}".format(ex,arg),file=self.stdout)

	def do_players(self, arg):
		'Manage players (list, load, save)'
		try:
			plist = sorted(self.players,reverse=True)

			match(arg):
				case "save":
					c,fn = arg.split(" ")
					print("saving players to {}".format(fn),file=self.stdout)
					self.save(self.players,fn)
				case "load":
					c,fn = arg.split(" ")
					print("loading players from {}".format(fn),file=self.stdout)
					pl = self.load(fn)
					if pl is not None:
						for p in pl:
							if self.findPlayer(p.getName()) is None:
								self.players.append(p)
					self.do_players("list")
				case _:
					for p in plist:
						p.print(self.stdout)

		except Exception as ex:
			print("Got exception {} trying to process {}".format(ex,arg),file=self.stdout)

	def save(self, obj, fn):
		try:
			with open(fn,"wb") as f:
				pickle.dump(obj,f)
		except:
			print("Did not save file {}".format(fn),file=self.stdout)

	def load(self, fn):
		try:
			with open(fn,"rb") as f:
				return pickle.load(f)
		except:
			print("Did not load file {}".format(fn),file=self.stdout)
			return None

	def do_mobs(self, arg):
		'manage monsters (load, save, list, roll, clear)'
		try:
			mlist = sorted(self.mobs.values(),reverse=True)
			if len(arg) == 0:
				arg = "list"
			args = arg.split(" ")
			match(args[0]):
				case "save":
					f = arg[1]
					print("saving mobs to {}".format(f),file=self.stdout)
					self.save(self.mobs,f)
				case "load":
					f = arg[1]
					print("loading mobs from {}".format(f),file=self.stdout)
					m = self.load(f)
					if m is not None:
						self.mobs.update(m)
					self.do_mobs("list")
				case "clear":
					self.mobs = dict()
				case "roll" | "r" | "ro":
					for m in mlist:
						m.rollInit()
				case _:
					for m in mlist:
						m.print(self.stdout)
		except Exception as ex:
			print("Got exception {} trying to process {}".format(ex,arg),file=self.stdout)

	def initiative(self, arg):
		'Manage initiative (list, next, clear|reset, roll (for mobs)'
		try:
			plist = sorted(self.players,reverse=True)
			mlist = sorted(self.mobs.values(),reverse=True)
			combatants = list(plist)
			combatants.extend(mlist)
			if len(combatants) < 1:
				return
			initorder = sorted(combatants, reverse=True)
			self.nextp = self.nextp % len(initorder)

			match (arg):
				case "clear" | "reset":	 		
					self.nextp = 0

				case "next":
					print(initorder[self.nextp].getName(),file=self.stdout)
					self.nextp += 1

				case _:
					for c in initorder[self.nextp:]:
						print("{} {}".format(c.getName(),c.getInitiative()),file=self.stdout)
					for c in initorder[:self.nextp]:
						print("{} {}".format(c.getName(),c.getInitiative()),file=self.stdout)

		except Exception as ex:
			print("Got exception {} trying to process {}".format(ex,arg),file=self.stdout)

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
			print("no history to load",file=self.stdout)
	GMShell().cmdloop()
	try: 
		readline.write_history_file('.gmshell.history')
	except:
		print("failed to save history",file=self.stdout)
