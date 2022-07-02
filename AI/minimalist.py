from AI.player import Player


class Minimalist(Player):
    @property
    def title(self) -> str:
        return "Sailor "

    @staticmethod
    def get_name() -> str:
        return "Sailor"

    def take_turn(self, game_state):
        # The minimalist either
        #  increases the value to the nearest one they have
        #  or increase the count or value by 1
        divider = 3 if game_state.wild_mode else 6
        expected_dice = (game_state.total_dice - self.num_dice) // divider
        dice = self.my_dice(game_state.wild_mode)
        # Go to the nearest absolute safe bid
        for value in range(1, 7):
            if game_state.current_bid[1] > value:
                continue
            if game_state.current_bid[1] == value:
                if game_state.current_bid[0] < dice[value]:
                    return [game_state.current_bid[0] + 1, value]
            else:
                if dice[value] > 0:
                    return [1, value]
        # No absolute safe bid possible, increase count if in safe range (and possible)
        if dice[game_state.current_bid[1]] + expected_dice + 1 > game_state.current_bid[0]:
            return [game_state.current_bid[0] + 1, game_state.current_bid[1]]
        # Current bid is outside safe range, increase value
        elif game_state.current_bid[1] != 6:
            return [1, game_state.current_bid[1] + 1]
        # Value increase not possible, count outside safe range --> challenge
        return -1
