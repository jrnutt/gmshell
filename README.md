# gmshell

## Introduction

gmshell is a simple command driven way to manage combat for D&D. It tracks a subset of player stats (armor class, level, class, initiative and passive perception, investigation and insight). It can save and load a set of player characters for continuity between sessions. It also tracks mob (monster) information: hit points, armor class and initiative. Right now, gmshell is mostly useful as an initiative tracker. You can list combatants (the combined list of players and mobs) in order of initiative and move to the next combatant with a simple command. This is not for mouse jockeys, all the commands are keyboard driven and I've attempted to make them fairly intuitive.

## Commands

* player - This command adds or updates a player character. The first argument is the character name or nickname (nick) which may be surrounded with quotation marks. All the parameters but the first are optional and may be filled in later. The are added in key/value format (name=value). The remaining parameters are:
** cls - The player class (no spaces)
** lvl - The player level
** ac - The player armor class
** init - The player's initiative roll
** per - The player's passive perception
** inv - The player's passive investigation
** ins - The player's passive insight
** nick - The player's nickname (no spaces!)

* players - This command manages the list of players. 
** list (or no argument) - List the players entered
** save - include a filename to save the player list for later
** load - include a filename to retrieve a saved player list

* mob - Allows you to enter a creature for combat. The first parameter is the mob name and may include spaces if in quotes. The remainder are:
** ac - The monster's armor class
** hp - Allows you to set the monster's hit points to a specific value
** -hp - subtracts the specified hit points
** +hp - adds the specified hit points
** init - sets the monster's initiative

* mobs - Lists the monsters in the current encounter.
** clear - removes all the mobs from combat
** save - include a filename to save the mob list for later
** load - include a filename to retrieve a saved list of mobs
** list (or no argument) - List the current mobs

* initiative - This is the initiative tracker, it allows you to see the initiative order and step to the next combantant
** list (or no argument) - list combatants in initiative order, starting with the next combatant up
** next - Step to the next combatant and display their name
** clear - Clear the initiative (reset to the top of the order)

