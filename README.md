
# gmshell

## Introduction

gmshell is a simple command driven way to manage combat for D&D. It tracks a subset of player stats (armor class, level, class, initiative and passive perception, investigation and insight). It can save and load a set of player characters for continuity between sessions. It also tracks mob (monster) information: hit points, armor class and initiative. Right now, gmshell is mostly useful as an initiative tracker. You can list combatants (the combined list of players and mobs) in order of initiative and move to the next combatant with a simple command. This is not for mouse jockeys, all the commands are keyboard driven and I've attempted to make them fairly intuitive.

## Commands

* player - This command adds or updates a player character. The first argument is the character name or nickname (nick) which may be surrounded with quotation marks. All the parameters but the first are optional and may be filled in later. They are added in key/value format (name=value). If no parameter is given, the information for that player is displayed. The remaining parameters are:

  * cls - The player class (use quotes to include spaces)
  * lvl - The player level
  * ac - The player armor class
  * init - The player's initiative roll
  * per - The player's passive perception
  * inv - The player's passive investigation
  * ins - The player's passive insight
  * bonus - The player's initiative bonus
  * hp - The player's hit points
  * nick - The player's nickname, place in quotes if it contains spaces.
  * write - display the player information in a format that can be reloaded later
  * delete - remove the player from the list
  * +_condition_ - add _condition_ to the player information
  * -_condition_ - remove _condition_ from the player information

* players - This command manages the list of players. 
  * list (or no argument) - List the players entered
  * save - include a filename to save the player list for later
  * clear - clears the player list
  
* mob - Allows you to enter a creature for combat. The first parameter is the mob name and may include spaces if in quotes. If no additional parameters are provided, the monster information is displayed. The remainder are:

  * ac - The monster's armor class
  * hp - Allows you to set the monster's hit points to a specific value
  * bonus - The monster's initiative bonus
  * init - sets the monster's initiative
  * write - display the monster information in a format that can be reloaded later.
  * delete - remove the monster from the mob list
  * +_condition_ - add _condition_ to the mob information
  * -_condition_ - remove _condition_ from the mob information

* mobs - Lists the monsters in the current encounter.

  * clear - removes all the mobs from combat
  * save - include a filename to save the mob list for later
  * roll - roll initiative for all mobs (also resets initiative order)
  * list (or no argument) - List the current mobs
  
* heal - given a player or mob id and a number of hit points, adds that many hit points to the combatant's current hitpoints.

* hit - given a player or mob id and a number of hit points, subtracts that many hit points from the combatants current hit points.

* initiative - This is the initiative tracker, it allows you to see the initiative order and step to the next combantant
  
  * list (or no argument) - list combatants in initiative order, starting with the next combatant up
  * next - Step to the next combatant and display their name
  * clear - Clear the initiative (reset to the top of the order)

* \@_scriptname_ - loads the script in the file specified by _scriptname_. This can be player or monster information created by the save or write commands. Or it can be an arbitrary list of the above commands.

* _player_ or _mob_ - For already existing player or mob records, you can just use the player or mob id instead of prefixing it with *player* or *mob*.
