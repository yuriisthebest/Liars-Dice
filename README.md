# The Liar's Dice Game

The lair's dice is a game played in the movie: *"Pirates of the Caribbean: Dead Man's Chest"*.

This project aims to create the game using a simple graphical interface. Only one human can play against up to 7 AIs.
These AIs have different strategies to mix up playstyle.

## Rules of the game

Five dice are used per player with dice cups used for concealment.
This digital version does not use cups, instead the dice are digitally hidden.
The game is round-based.

Each round, each player rolls a "hand" of dice under their cup and looks at their hand while keeping it concealed from the other players.
The first player begins bidding. A bid consists of any face value and a number of dice that the player believes are showing that value, under all of the cups on the table.
Turns rotate in clockwise order.

Each player has two choices during their turn:
* to make a higher bid;
* to challenge the previous bid, by calling the last bidder a 'liar'.

A higher bid means that the quantity is raised of the same face, or any particular quantity is named of a higher face.
(variations exists but these are not implemented here)

If the current player challenges the bid, all dice are revealed.
If the bid is valid (there are at least as many of the face value as were bid), the challenger loses.
Otherwise, the bidder loses. The player who lost the round loses one of their dice.
The loser of the last round starts the next round. If they were eliminated, the next player starts.
The last player with dice left is the winner.

During wild-mode, all "ones" are counted as the face of the current bid.


## Requirements and Installation

The requirements and dependencies of this project can be found in ```requirements.txt```.
Install and load all required dependencies using ```pip install -r requirements.txt```.

Warning: the 'playsound' package only works on version 1.2.2, but the game can run without this package.


## Run the game

Run ```main.py```, this should open a window with the game running.
Choose your opponents and mode before pressing "Start the game"

## Artificial Intelligence

todo
