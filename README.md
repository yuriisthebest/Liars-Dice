# The Liar's Dice Game

The lair's dice is a game played in the movie: *"Pirates of the Caribbean: Dead Man's Chest"*.

This project aims to create the game using a simple graphical interface. Only one human can play against up to 7 AIs.
These AIs have different strategies to mix up play-style.

## Rules of the game

Five dice are used per player with dice cups used for concealment.
This digital version does not use cups, instead the dice are digitally hidden.
The game is round-based.

Each round, each player rolls a "hand" of dice under their cup and looks at their hand while keeping it concealed from the other players.
The first player begins bidding. A bid consists of any face value and a number of dice that the player believes are showing that value, under all the cups on the table.
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

There are 6 distinct AI styles for your opponents from which you can choose when adding them to the game.
These AIs don't necessarily use an optimized strategy. This is to make them more or less risk taking, add more variation in the bid and because I didn't want to change it.
A small explanation is given for each AI:

* The Fool: They have no idea how the game works or how to win. They offer valid bids but that does not mean that they are correct. The fool also likes to challenge whenever the bids starts to increase.
* The Sailor: Cautious and unwilling to take risks, they are quite resilient against challenges. They will only make small bid increases and only challenge when stuck.
* The Gambler: A real veteran of hidden information games. They remember everything that everyone does and will use it to their advantage.
* [TODO] The Student: They may lack any sound logic, but the student has played this game more than anyone else and has learned some valuable lessons. They will beat you armed with a trained recurrent neural network.
* The Teacher: As a professor of statistics, they know the most likely scenarios, and they aren't afraid to capitulate on that. They take calculated risks and can be quite aggressive on their challenges.
* The Captain: Davy Jones himself, or another captain, joins your table. They seem to know everything and will challenge you whenever you lie. The Captain truly is the most difficult to beat.
* The Stranger: It is unknown where the stranger came from or how it plays. It will change his playing everytime you play against him. In reality, it mimics one of the other 6 AI.

## Experiments

First impressions: The captain is perfect. The sailor is surprisingly good, the teacher and gambler aren't as good as expected. The fool has a ~1/20000 chance of winning
Gambler and professor need some more work...

[TODO some fun stats on how the AI plays]
