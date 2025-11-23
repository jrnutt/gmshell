#!/usr/bin/python
import cmd2
import sys
import readline

from player import Player
from mob import Mob


class GMShell(cmd2.Cmd):
    intro = 'Welcome to the GM Shell, a utility to help manage game play'
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

        try:
            for p in self.players:
                if p.getNick() == pn or p.getName() == pn:
                    return p
        except Exception:
            print("error locating player {}".format(pn), self.stdout)

        return None

    def do_player(self, arg):
        'Manage individual player information'

        try:
            arguments = arg.arg_list

            pn = cmd2.utils.strip_quotes(arguments.pop(0))

            player = self.findPlayer(pn)
            if len(arguments) > 0:
                if player is not None:
                    match arguments[0]:
                        case 'delete':
                            self.players.remove(player)
                            print("{} deleted".format(player.getName()),
                                  file=self.stdout)
                            return
                        case 'write':
                            player.write(self.stdout)
                            return
                else:
                    print("Adding new player {}".format(pn), file=self.stdout)
                    player = Player(pn, cls='', lvl='',
                                    ac=0, per=0, inv=0,
                                    ins=0, init=0.0, nick='')

                for i in arguments:
                    player.set(i)

                p = self.findPlayer(pn)
                if p is None:
                    self.players.append(player)
                    p = player
                    print("Player \'{}\' added".format(pn),
                          file=self.stdout)
                else:
                    print("Player \'{}\' updated".format(pn),
                          file=self.stdout)

            if player is not None:
                player.print(file=self.stdout, summary=False)

        except Exception as ex:
            print("Got exception {} trying to process {}".format(ex, arg),
                  file=self.stdout)

    def do_mob(self, arg):
        'Manage mob information'

        try:
            p = arg.arg_list

            mn = cmd2.utils.strip_quotes(p.pop(0).lower())
            if len(p) > 0:
                if mn in self.mobs:
                    match(p[0]):
                        case "delete":
                            del self.mobs[mn]
                            print("Mob \'{}\' removed".format(mn))
                            return

                        case "copy":
                            m = self.mobs[mn].copy()
                            i = 1
                            if '-' in mn:
                                r = mn.split('-')
                            else:
                                r = (mn, "1")
                            if not r[len(r)-1].isnumeric():
                                r.append('1')
                            c = r[len(r)-1]
                            try:
                                i = int(c)
                            except Exception:
                                i = 1
                            r[len(r)-1] = str(i)
                            n = '-'.join(r)
                            while (n in self.mobs):
                                i += 1
                                r[len(r)-1] = str(i)
                                n = '-'.join(r)
                            m.setName(n)
                            self.mobs[n] = m
                            print("Mob \'{}\' added".format(n),
                                  file=self.stdout)
                            mn = n
                            return

                        case "write":
                            self.mobs[mn].write(self.stdout)
                            return

                    print("Updating mob {}".format(mn), file=self.stdout)
                    mob = self.mobs[mn]
                else:
                    mob = Mob(mn, ac=0, hp=0, init=0.0, bonus=0)
                    print("Adding new mob {}".format(mn), file=self.stdout)

                if p[0] in ["copy", "delete", "write"]:
                    print("mob {} does not exist".format(mn), file=self.stdout)
                    return

                for i in p:
                    mob.set(i)

                if mn not in self.mobs:
                    self.mobs[mob.getName()] = mob
                    print("{} added".format(mob.getName()))
                else:
                    print("Mob \'{}\' updated".format(mn),
                          file=self.stdout)

            if mn in self.mobs:
                self.mobs[mn].print(self.stdout)

        except Exception as ex:
            print("Got exception {} trying to process {}".format(ex, arg),
                  file=self.stdout)

    def do_hit(self, arg):
        'Subtract hit points from a player or monster'

        p = arg.arg_list
        if len(p) < 2:
            return
        c = self.findPlayer(p[0])
        if c is None and p[0] in self.mobs:
            c = self.mobs[p[0]]
        if c is not None:
            c.setHP(c.getHP() - int(p[1]))
            c.print(self.stdout, summary=True)
        return

    def do_heal(self, arg):
        'Add hit points to a player or monster'

        p = arg.arg_list
        if len(p) < 2:
            return
        c = self.findPlayer(p[0])
        if c is None and p[0] in self.mobs:
            c = self.mobs[p[0]]
        if c is not None:
            c.setHP(c.getHP() + int(p[1]))
            c.print(self.stdout, summary=True)
        return

    def do_players(self, arg):
        'Manage players (list, load, save, clear)'

        args = arg.arg_list
        try:
            plist = sorted(self.players, reverse=True)

            if len(args) > 0:
                match(args[0]):
                    case "write":
                        for p in self.players:
                            p.write(self.stdout)
                    case "save" if len(args) > 1:
                        print("saving players to {}".format(args[1]),
                              file=self.stdout)
                        self.save(self.players, args[1])
                    case "save":
                        print("need a file name to save to")
                    case "load":
                        print("use '@filename' to load a player file",
                              file=self.stdout)
                    case "clear":
                        self.players = list()
                        print("player list has been cleared",
                              file=self.stdout)
                    case _:
                        for p in plist:
                            p.print(self.stdout, summary=False)
            else:
                for p in plist:
                    p.print(self.stdout)

        except Exception as ex:
            print("Got exception {} trying to process {}".format(ex, arg),
                  file=self.stdout)

    def save(self, obj, fn):
        try:
            with open(fn, "w") as f:
                for c in obj:
                    c.write(f)
        except Exception as ex:
            print(ex)
            print("Did not save file {}".format(fn),
                  file=self.stdout)

    def do_mobs(self, arg):
        'manage monsters (load, save, list, roll, clear)'

        try:
            mlist = sorted(self.mobs.values(), reverse=True)
            if len(arg) > 0:
                args = arg.arg_list
                match(args[0]):
                    case "write":
                        for m in mlist:
                            m.write(self.stdout)
                    case "save":
                        f = args[1]
                        print("saving mobs to {}".format(f),
                              file=self.stdout)
                        self.save(mlist, f)
                    case "load":
                        print("use '@filename' to load a mob file",
                              file=self.stdout)
                    case "clear":
                        self.mobs = dict()
                    case "roll" | "r" | "ro":
                        print("rolling initiative for mobs")
                        self.nextp = 0
                        for m in mlist:
                            m.rollInit()
                    case _:
                        for m in mlist:
                            m.print(self.stdout)
            else:
                for m in mlist:
                    m.print(self.stdout)

        except Exception as ex:
            print("Got exception {} trying to process {}".format(ex, arg),
                  file=self.stdout)

    def initiative(self, arg):
        try:
            plist = sorted(self.players, reverse=True)
            mlist = sorted(self.mobs.values(), reverse=True)
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
                    initorder[self.nextp].print(file=self.stdout)
                    self.nextp += 1

                case _:
                    for c in initorder[self.nextp:]:
                        c.print(file=self.stdout)
                    for c in initorder[:self.nextp]:
                        c.print(file=self.stdout)

        except Exception as ex:
            print("Got exception {} trying to process {}".format(ex, arg),
                  file=self.stdout)

    def do_initiative(self, arg):
        'Manage initiative (list, next, clear|reset)'

        self.initiative(arg)

    def do_init(self, arg):
        'Manage initiative (list, next, clear|reset)'
        self.initiative(arg)

    def do_next(self, arg):
        'Show next combatant in initiative'
        self.initiative("next")

    def default(self, arg):
        t = None
        c = self.findPlayer(arg.command)
        if c is not None:
            t = "player"
        elif arg.command in self.mobs:
            t = "mob"

        if t is not None:
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
