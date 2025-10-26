#!/usr/bin/python
import cmd2, sys
import pickle
import readline

from io import StringIO
from player import Player
from mob import Mob

class GMShell(cmd2.Cmd):
	intro = 'Welcome to the GM Shell, a utility to help Game Masters manage game play'
	prompt = '(cmd) '
	file = None
	nextp = 0
	players = list()
	mobs = dict()

	def __init__(self):
		cmd2.Cmd.__init__(self, include_py=True)

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
			print("error locating player {}".format(pn), self.stdout)

		return None

	def do_player(self, arg):
		'Set player information'

		try:
			arguments = arg.arg_list

			pn = cmd2.utils.strip_quotes(arguments.pop(0))

			player = self.findPlayer(pn)
			for i in arguments:
				if player is not None:
					if i == 'delete':
						self.players.remove(player)
						print("{} deleted".format(player.getName()), file=self.stdout)
						return

					if i == 'write':
						player.write(self.stdout)
						return
				else:
					print("Adding new player {}".format(pn), file=self.stdout)
					player = Player(pn, pclass='', level='', ac=0, per=0, inv=0, ins=0, init=0.0, nick='')

				if i in ['delete','write']:
					print("player {} does not exist".format(pn), file=self.stdout)
					return

				if not '=' in i:
					if (i.startswith('+')):
						player.addCondition(i.lstrip('+'))
					elif (i.startswith('-')):
						player.remCondition(i.lstrip('-'))

				else:
					n,v = i.split('=')
					n = n.lower()
					if (n.startswith('c')):
						player.setClass(v)
					elif (n.startswith('l')):
						player.setLevel(v)
					elif (n.startswith('a')):
						player.setAC(int(v))
					elif (n.startswith('h')):
						player.setHP(int(v))
					elif (n.startswith('ini')):
						player.setInitiative(float(v))
					elif (n.startswith('per')):
						player.setPerception(int(v))
					elif (n.startswith('inv')):
						player.setInvestigation(int(v))
					elif (n.startswith('ins')):
						player.setInsight(int(v))
					elif (n.startswith('nick')):
						player.setNick(v)

			p = self.findPlayer(pn)
			if self.findPlayer(p) is None:
				self.players.append(player)
				p = player
				print("Player \'{}\' added".format(pn),file=self.stdout)
			else:
				print("Player \'{}\' updated".format(pn),file=self.stdout)

			p.print(file=self.stdout)

		except Exception as ex:
			print("Got exception {} trying to process {}".format(ex,arg),file=self.stdout)

	def do_mob(self, arg):
		'Set mob information'

		try: 
			p = arg.arg_list

			mn = cmd2.utils.strip_quotes(p.pop(0).lower());
			if len(p) > 0:
				if mn in self.mobs:
					if p[0] == "delete":
						del self.mobs[mn]
						print("Mob \'{}\' removed".format(mn))
						return

					if p[0] == "copy":
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
						return

					if p[0] == "write":
						self.mobs[mn].write(self.stdout)
						return

					print("Updating mob {}".format(mn), file=self.stdout)
					mob = self.mobs[mn]
				else:
					mob = Mob(mn, ac=0, hp=0, init=0.0, bonus=0)
					print("Adding new mob {}".format(mn), file=self.stdout)



				if p[0] in ["copy","delete","write"]:
					print("mob {} does not exist".format(mn), file=self.stdout)
					return


				for i in p:
					try:
						if not '=' in i:
							if (i.startswith('+')):
								mob.addCondition(i.lstrip('+'))
							elif (i.startswith('-')):
								mob.remCondition(i.lstrip('-'))
						else:
							n,v = i.split('=')
							n = n.lower()
							if (n.startswith('a')):
								mob.setAC(int(v))
							elif (n.startswith('i')):
								mob.setInitiative(float(v))
							elif (n.startswith('h')):
								if  v.startswith('-') or v.startswith('+'):
									mob.setHP(self.mobs[mn].getHP() + int(v))
								else:
									mob.setHP(int(v))
							elif (n.startswith('b')):
								mob.setBonus(int(v))
					except ValueError:
						print("Missing or bad value in {}".format(i),file=self.stdout)

				if mn not in self.mobs:
					self.mobs[mob.getName()] = mob
					print("{} added".format(mob.getName()))
				else:
					print("Mob \'{}\' updated".format(mn),file=self.stdout)

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
				case "write":
					for p in self.players:
						p.write(self.stdout)
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
				case "write":
					for m in mlist:
						m.write(self.stdout)
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

if __name__ == '__main__':
	try:
		readline.read_history_file('.gmshell.history')
	except:
		with open('.gmshell.history','w'):
			print("no history to load",file=sys.stderr)
	GMShell().cmdloop()
	try: 
		readline.write_history_file('.gmshell.history')
	except:
		print("failed to save history",file=sys.stderr)
