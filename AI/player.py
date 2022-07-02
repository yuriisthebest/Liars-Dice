import names
import random
from abc import abstractmethod
# Import game for typehints and code-completion
# Gate it after a False if-statement to avoid cyclic imports
if not names:
    from game import Game


class Player:
    def __init__(self, frame, start_dice: int, position: int, human: bool, hidden: bool = False):
        """
        Create a

        @param frame: The frame that contains this players info and playing field
        @param start_dice: The amount of dice to start the game with
        @param position: The players position in the game
        @param human: Whether the player is human
        @param hidden: Whether to show or hide the title
        """
        self.frame = frame
        self.num_dice = start_dice
        self.dice = None
        self.human = human
        self.name = names.get_first_name() if not self.human else "You"
        self.pos = position
        self.hidden = hidden

    def roll_dice(self):
        # Roll all their dice and maintain values
        self.dice = [random.randint(1, 6) for _ in range(self.num_dice)]
        self.dice.sort()

    def reveal_dice(self) -> str:
        result = ""
        for dice in self.dice:
            result += f"{dice} "
        return result

    def my_dice(self, wild_mode: bool) -> dict:
        dice = {i: 0 for i in range(1, 7)}
        for d in self.dice:
            dice[d] += 1
        if wild_mode:
            for i in range(2, 7):
                dice[i] += dice[1]
        return dice

    def get_title(self) -> str:
        """
        Return the prefix title of the player, unless the title should be hidden
        """
        if self.hidden:
            return ""
        else:
            return self.title

    @property
    @abstractmethod
    def title(self) -> str:
        raise NotImplementedError("This is an abstractmethod and is implemented in children")

    @staticmethod
    @abstractmethod
    def get_name() -> str:
        """
        Return the name of AI that should be in options menu
        """
        raise NotImplementedError("This is an abstractmethod and is implemented in children")

    @abstractmethod
    def take_turn(self, game_state: 'Game'):
        """
        Function for bots to determine what to do on their turn

        Returns a bid in the form of [dice count, dice value] or a challenge in the form of -1
        :param game_state: The game object with all information
        :return: A bid or -1
        """
        raise NotImplementedError("This is an abstractmethod and is implemented in children")
