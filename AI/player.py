import names
import random
from abc import abstractmethod


class Player:
    def __init__(self, frame, starting_dice: int, position: int, human: bool):
        self.frame = frame
        self.num_dice = starting_dice
        self.dice = None
        self.human = human
        self.name = names.get_first_name() if not self.human else "You"
        self.pos = position

    def roll_dice(self):
        # Roll all their dice and maintain values
        self.dice = [random.randint(1, 6) for _ in range(self.num_dice)]
        self.dice.sort()

    def reveal_dice(self) -> str:
        result = ""
        for dice in self.dice:
            result += f"{dice} "
        return result

    @abstractmethod
    def take_turn(self, game_state):
        """
        Function for bots to determine what to do on their turn

        Returns a bid in the form of [dice count, dice value] or a challenge in the form of -1
        :param game_state: The game object with all information
        :return: A bid or -1
        """
        raise NotImplementedError("This is an abstractmethod and is implemented in children")
