import random

from AI.player import Player


class Oracle(Player):
    @property
    def title(self) -> str:
        return "Captain "

    @staticmethod
    def get_name() -> str:
        return "Captain"

    def take_turn(self, game_state):
        # The oracle cheats and will always know what everyone has
        # If the current bid is invalid, it always challenges
        if not game_state.is_correct_bid():
            return -1
        # Count all dice
        dice = {i: 0 for i in range(1, 7)}
        for player in game_state.players.values():
            for d in player.dice:
                dice[d] += 1
        # Get all possible correct bids
        possible_bids = []
        for value in dice:
            # The current bid value is higher than this loop iteration
            if game_state.current_bid[1] > value:
                continue
            max_count = dice[value] + 1
            if game_state.wild_mode and value != 1:
                max_count += dice[1]
            if game_state.current_bid[1] == value:
                for i in range(game_state.current_bid[0] + 1, max_count):
                    possible_bids.append([i, value])
            else:
                for i in range(1, max_count):
                    possible_bids.append([i, value])
        # If there are no possible bids, increase the value by 1 unless the bid value is 6
        if len(possible_bids) == 0:
            if game_state.current_bid[1] == 6:
                return [game_state.current_bid[0] + 1, game_state.current_bid[1]]
            return [1, game_state.current_bid[1] + 1]
        # Pick a random possible bid
        return random.choice(possible_bids)
