import random

from AI.player import Player


class Randy(Player):
    @property
    def title(self) -> str:
        return "Cabinboy "

    @staticmethod
    def get_name() -> str:
        return "Fool"

    def take_turn(self, game_state):
        # Decide what to bid or challenge
        bid = [0, 0]
        # Random numbers
        while not game_state.is_valid_bid(bid):
            # 12% chance to challenge
            if random.randint(1, 100) <= 12 and game_state.current_bid != [0, 0]:
                return -1
            bid = [random.randint(1, game_state.total_dice), random.randint(1, 6)]
        return bid
