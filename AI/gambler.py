from AI.player import Player


class Gambler(Player):
    @property
    def title(self) -> str:
        return "Gambler "

    @staticmethod
    def get_name() -> str:
        return "Gambler"

    def take_turn(self, game_state):
        # Calculate the expected dice of each value
        divider = 3 if game_state.wild_mode else 6
        expected_dice = game_state.total_dice // divider
        # Gambler uses the bids of other people to predict what they have
        predictions = {pos: [] for pos in game_state.players if pos != self.pos}
        for bid, pos, num_dice in game_state.previous_bids:
            if pos == self.pos:
                continue
            # Don't add predicted dice to players whose dice are all 'accounted' for
            if len(predictions[pos]) >= game_state.players[pos].num_dice:
                continue
            # Don't add the same dice multiple times
            if bid[1] in predictions[pos]:
                continue
            # If a player places a bid, he probably has that value
            predictions[pos].append(bid[1])
            # If the bid is large (above expected), he might have multiple
            if bid[0] > expected_dice:
                predictions[pos].append(bid[1])

        # Calculate the expected unknowns, predicted counts and own dice
        dice = self.my_dice(game_state.wild_mode)
        predicted_count = sum([len(predictions[p]) for p in predictions])
        expected_dice = round((game_state.total_dice - self.num_dice - predicted_count) / divider)
        pred_dice = {i: 0 for i in range(1, 7)}
        for dices in predictions.values():
            for value in dices:
                pred_dice[value] += 1

        # Challenge when it is unlikely the bid is true based on all predictions and unknowns
        if (game_state.current_bid != [0, 0] and game_state.current_bid[0]
                > dice[game_state.current_bid[1]]
                + pred_dice[game_state.current_bid[1]]
                + expected_dice):
            return -1

        # Bid based on predictions and own dice
        for value in range(1, 7):
            if game_state.current_bid[1] > value:
                continue
            if game_state.current_bid[1] == value:
                if game_state.current_bid[0] < dice[value] + pred_dice[value]:
                    return [dice[value] + pred_dice[value], value]
                    # Optional: the gambler only increases bids by 1 like sailors
                    # return [game_state.current_bid[0] + 1, value]
            else:
                if dice[value] + pred_dice[value] > 0:
                    return [dice[value] + pred_dice[value], value]

        # No bid possible based on self and predictions
        # Make a bid that fits within the expected dice of this value
        if (game_state.current_bid[0]
                < dice[game_state.current_bid[1]]
                + pred_dice[game_state.current_bid[1]]
                + expected_dice):
            return [dice[game_state.current_bid[1]]
                    + pred_dice[game_state.current_bid[1]]
                    + expected_dice,
                    game_state.current_bid[1]]
        # Unlikely that there are more of the same value of the current bid, increase value by 1
        new_value = game_state.current_bid[1] + 1
        if new_value <= 6 and dice[new_value] + pred_dice[new_value] + expected_dice > 0:
            return [dice[new_value] + pred_dice[new_value] + expected_dice, new_value]
        # Out of probable options, challenge
        return -1
