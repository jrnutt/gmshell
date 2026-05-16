#!/usr/bin/python
"""Tool for managing RPG game play."""
import cmd2
import sys
import readline

from player import Player
from mob import Mob


class GMShell(cmd2.Cmd):
    """Command driven utility for managing RPG game play."""

    intro = 'Welcome to the GM Shell, a utility to help manage game play'
    prompt = '(cmd) '
    file = None
    current = None
    round = 0
    combatants = set()
    players = list()
    mobs = dict()

    def __init__(self):
        """Initialize the Cmd super class."""
        cmd2.Cmd.__init__(self, include_py=True)

    def do_quit(self, arg):
        """Exit GM Shell."""
        return True

    def findCombatant(self, pn, t=Player):
        """Find a combatant by nick name."""
        try:
            for p in self.combatants:
                if (p.getNick() == pn or p.getName() == pn) and \
                   isinstance(p, t):
                    return p
            return None
        except Exception as ex:
            print("error locating combatant {}".format(pn), file=self.stdout)
            print(ex)
        return None

    def mngcombatant(self, arg, t):
        """Add a combatant."""
        try:
            arguments = arg.arg_list

            n = cmd2.utils.strip_quotes(arguments.pop(0))

            c = self.findCombatant(n, t)
            if len(arguments) > 0:
                if c is not None:
                    match arguments[0]:
                        case 'delete':
                            c.addCondition("dead3")
                            print("{} deleted".format(c.getName()),
                                  file=self.stdout)
                            return
                        case 'write':
                            c.write(self.stdout)
                            return
                        case 'copy':
                            m = c.copy()
                            i = 1
                            if '-' in n:
                                r = n.split('-')
                            else:
                                r = (n, "1")
                            if not r[len(r)-1].isnumeric():
                                r.append('1')
                            c = r[len(r)-1]
                            try:
                                i = int(c)
                            except Exception:
                                i = 1
                            r[len(r)-1] = str(i)
                            n = '-'.join(r)
                            m.setName(n)
                            while (self.findCombatant(n, (Player, Mob))
                                   is not None):
                                i += 1
                                r[len(r)-1] = str(i)
                                n = '-'.join(r)
                                m.setName(n)
                            self.combatants.add(m)
                            print("Mob \'{}\' added".format(n),
                                  file=self.stdout)
                            return

                else:
                    if t is Player:
                        print("Adding new player {}".format(n),
                              file=self.stdout)
                        c = Player(n, cls='', lvl='',
                                   ac=0, per=0, inv=0,
                                   ins=0, init=0.0, nick='')
                    else:
                        print("Adding new mob {}".format(n), file=self.stdout)
                        c = Mob(n, nick='', ac=0, hp=0, init=0.0, bonus=0)

                for i in arguments:
                    c.set(i)

                lc = self.findCombatant(n, t)
                if lc is None:
                    self.combatants.add(c)
                    print("combatant \'{}\' added".format(n),
                          file=self.stdout)
                else:
                    print("combatant \'{}\' updated".format(n),
                          file=self.stdout)

            if c is not None:
                c.print(file=self.stdout, summary=False)

        except Exception as ex:
            print("Got exception {} trying to process {}".format(ex, arg),
                  file=self.stdout)

    def do_player(self, arg):
        """Manage individual player information."""
        self.mngcombatant(arg, Player)

    def do_mob(self, arg):
        """Manage mob information."""
        self.mngcombatant(arg, Mob)

    def do_hit(self, arg):
        """Subtract hit points from a player or monster."""
        p = arg.arg_list
        if len(p) < 2:
            return
        c = self.findCombatant(p[0], (Player, Mob))
        if c is not None:
            c.setHP(c.getHP() - int(p[1]))
            c.print(self.stdout, summary=True)
        return

    def do_heal(self, arg):
        """Add hit points to a player or monster."""
        p = arg.arg_list
        if len(p) < 2:
            return
        c = self.findCombatant(p[0], (Player, Mob))
        if c is not None:
            c.setHP(c.getHP() + int(p[1]))
            c.print(self.stdout, summary=True)
        return

    def pcandmobs(self, arg, t):
        """Perform base combatant operations."""
        args = arg.arg_list
        try:
            if len(args) > 0:
                match(args[0]):
                    case "write":
                        for c in self.combatants:
                            if isinstance(c, t):
                                c.write(self.stdout)
                    case "save" if len(args) > 1:
                        print("saving to {}".format(args[1]),
                              file=self.stdout)
                        self.save(self.combatants, args[1])
                    case "save":
                        print("need a file name to save to")
                    case "load":
                        print("use '@filename' to load a player file",
                              file=self.stdout)
                    case "clear":
                        rl = set()
                        for c in self.combatants:
                            if isinstance(c, t):
                                rl.add(c)
                        self.combatants = self.combatants - rl
                        print("list has been cleared",
                              file=self.stdout)
                    case _:
                        for c in self.combatants:
                            if isinstance(c, t):
                                c.print(self.stdout, summary=False)
            else:
                for c in self.combatants:
                    if isinstance(c, t):
                        c.print(self.stdout)

        except Exception as ex:
            print("Got exception {} trying to process {}".format(ex, arg),
                  file=self.stdout)

    def do_players(self, arg):
        """Manage players (list, load, save, clear)."""
        self.pcandmobs(arg, Player)

    def save(self, obj, fn):
        """Save a combatant to a file."""
        try:
            with open(fn, "w") as f:
                for c in obj:
                    c.write(f)
        except Exception as ex:
            print(ex)
            print("Did not save file {}".format(fn),
                  file=self.stdout)

    def do_mobs(self, arg):
        """Manage monsters (load, save, list, roll, clear)."""
        self.pcandmobs(arg, Mob)
        args = arg.arg_list
        if len(args) > 0:
            if args[0] in ["roll", "r", "ro"]:
                print("rolling initiative for mobs")
                self.nextp = 0
                for m in self.combatants:
                    if isinstance(m, Mob):
                        m.rollInit()

    def initiative(self, arg):
        """Manage initiative."""
        try:
            initorder = sorted(self.combatants, reverse=True)

            match (arg):
                case "clear" | "reset":
                    self.round = 0
                    self.current = initorder[0]

                case "next":
                    found = False
                    cur = None
                    for c in initorder:
                        if found:
                            if "dead3" not in c.getConditions():
                                cur = c
                                found = False
                        else:
                            found = (self.current == c)
                    if cur is None:
                        self.round += 1
                        self.current = initorder[0]
                        print("Starting round {}".format(self.round),
                              file=self.stdout)
                    else:
                        self.current = cur

                    self.current.print(file=self.stdout)
                case _:
                    self.print_initiative(initorder)

        except Exception as ex:
            print("Got exception {} trying to process {}".format(ex, arg),
                  file=self.stdout)

    def print_initiative(self, iorder):
        """Print the current initiative."""
        for c in iorder:
            if "dead3" not in c.getConditions():
                print("*" if c == self.current else " ", end=" ",
                      file=self.stdout)
                c.print(file=self.stdout)

    def do_initiative(self, arg):
        """Manage initiative (list, next, clear|reset)."""
        self.initiative(arg)

    def do_init(self, arg):
        """Manage initiative (list, next, clear|reset)."""
        self.initiative(arg)

    def do_next(self, arg):
        """Show next combatant in initiative."""
        self.initiative("next")

    def default(self, arg):
        """Try to determine what the user actually wants."""
        c = self.findCombatant(arg.command, (Player, Mob))
        if c is not None:
            t = "player" if isinstance(c, Player) else "mob"
            line = t + " " + arg.command_and_args
            s = cmd2.parsing.StatementParser().parse(line)
            self.onecmd(statement=s)
        else:
            print('Unknown command: "{}"'.format(arg.command_and_args))


if __name__ == '__main__':
    try:
        readline.read_history_file('.gmshell.history')
    except IOError:
        with open('.gmshell.history', 'w'):
            print("no history to load",
                  file=sys.stderr)
    GMShell().cmdloop()
    try:
        readline.write_history_file('.gmshell.history')
    except IOError:
        print("failed to save history",
              file=sys.stderr)
