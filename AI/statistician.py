import random
from math import comb

from AI.player import Player


class Statistician(Player):
    def __init__(self, frame, start_dice: int, position: int, human: bool):
        super().__init__(frame, start_dice, position, human)
        # Add some variance to the willingness to challenge
        self.prob_thresh = random.uniform(0.25, 0.5)

    @property
    def title(self) -> str:
        return "Prof. "

    @staticmethod
    def get_name() -> str:
        return "Teacher"

    def take_turn(self, game_state):
        # The statistician calculates the probability that the current bid is true.
        # It challenges if that probability is too low.
        # The statistician also tries to guess the exact number of dice for a given
        dice = self.my_dice(game_state.wild_mode)
        # Don't challenge on turn 1
        if game_state.current_bid != [0, 0]:
            base_prob = 1/6 if not game_state.wild_mode else 1/3
            unknown_dice = game_state.total_dice - self.num_dice
            bid_dice_to_predict = max(0, game_state.current_bid[0]
                                      - dice[game_state.current_bid[1]])
            # P(#dice >= bid - my_dice) = sum_i P(#dice == i)
            prob_correct_bid = 0
            for i in range(bid_dice_to_predict, unknown_dice+1):
                # P(#dice == bid - my_dice) = (unknown|bid) * base^bid * (1-base)^(unknown-bid)
                prob_i = (comb(unknown_dice, i)
                          * base_prob ** i
                          * (1-base_prob) ** (unknown_dice-i))
                prob_correct_bid += prob_i
            if prob_correct_bid < self.prob_thresh:
                return -1

        # Bid the expected value of the next
        divider = 3 if game_state.wild_mode else 6
        expected_dice = (game_state.total_dice - self.num_dice) // divider
        for value in range(1, 7):
            if value < game_state.current_bid[1]:
                continue
            # If the current bid is lower than the expected dice, bid the expected value
            if (value == game_state.current_bid[1]
                    and expected_dice + dice[value] > game_state.current_bid[0]):
                return [expected_dice + dice[value], value]
            elif value > game_state.current_bid[1] and expected_dice + dice[value] > 0:
                return [expected_dice + dice[value], value]
            # Bluff on 6
            if value == 6 and game_state.current_bid[0] == expected_dice + dice[value]:
                return [expected_dice + dice[value] + 1, value]
        return -1
