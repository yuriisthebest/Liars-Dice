import random


class ShadowGame:
    """
    This class contains all the game logic and game loop
    """
    def __init__(self, players: dict, wild_mode: bool):
        # Initialize players and set variables for later
        self.wild_mode = wild_mode
        self.players = players
        self.num_players = len(players)
        self.current_bid = None
        self.previous_bids = None
        self.total_dice = None
        self.correct_dice = None
        # Keep track of game events for game improvement:
        #  Positions in form [..., 3rd place name, 2nd place name, winner name]
        #  Challenges in form [..., [name, got challenged, current, actual], ...]
        self.game_info = {"positions": [],
                          "challenges": []}

    def start_game(self):
        # Pick a random position to start
        starting_position = random.choice(list(self.players.keys()))
        # Start the first round
        return self.start_round(starting_position)

    def start_round(self, active_player: int):
        # Reset game states
        self.current_bid = [0, 0]
        self.previous_bids = []
        for player in self.players.values():
            player.roll_dice()
        self.total_dice = sum([self.players[pos].num_dice for pos in self.players])
        # Start taking turns
        while True:
            if active_player in self.players:
                bid = self.players[active_player].take_turn(self)
                # Challenge
                if bid == -1:
                    return self.challenge(active_player)
                elif not self.is_valid_bid(bid):
                    t = self.players[active_player].title
                    n = self.players[active_player].name
                    text = f"Bid of {bid} of {t}{n} is not valid with current: {self.current_bid}"
                    raise ValueError(text)
                # Set new bid
                else:
                    self.current_bid = bid
                    self.previous_bids.append([bid,
                                               self.players[active_player].pos,
                                               self.players[active_player].num_dice])
            active_player += 1
            active_player %= self.num_players

    def challenge(self, active_player: int):
        # Can only challenge after a bid
        if self.current_bid == [0, 0]:
            t = self.players[active_player].title
            n = self.players[active_player].name
            text = f"{t}{n} cannot challenge without a first bid"
            raise ValueError(text)
        # Find challengers
        challenger = self.players[active_player]
        defender = self.previous_player(active_player)
        # Determine winner
        if self.is_correct_bid():
            # Defender wins, Challenger loses
            loser = challenger
            win = defender
            lost_how = "wrong call"
        else:
            # Challenger wins, Defender loses
            loser = defender
            win = challenger
            lost_how = "bad bid"
        loser.num_dice -= 1
        # [name, got challenged, who won, current, actual]
        self.game_info["challenges"].append([loser.get_name(), lost_how, win.get_name(),
                                             self.current_bid, self.correct_dice, self.total_dice])
        # Remove loser from game when dead
        if loser.num_dice == 0:
            self.game_info["positions"].append(loser.get_name())
            del self.players[loser.pos]
        # Check if there is a winner
        if len(self.players) == 1:
            winner = list(self.players.values())[0]
            self.game_info["positions"].append(winner.get_name())
            return winner
        # Ready next round
        else:
            return self.start_round(loser.pos)

    def previous_player(self, current_player: int):
        while True:
            current_player -= 1
            current_player %= self.num_players
            if current_player in self.players:
                return self.players[current_player]

    def is_valid_bid(self, new_bid: list) -> bool:
        """
        Checks if a given bid is valid, compared to the current bid
        It is valid if:
         The value is in the range 1-6
         The count is a positive integer
         The value is increased compared to current bid
         The value is the same as current bid but count is higher
        :param new_bid: [dice count, dice value]
        :return: Whether the bid is valid
        """
        if new_bid[1] not in range(1, 7) or new_bid[0] < 1:
            return False
        if new_bid[1] > self.current_bid[1]:
            return True
        if new_bid[1] == self.current_bid[1] and new_bid[0] > self.current_bid[0]:
            return True
        return False

    def is_correct_bid(self) -> bool:
        """
        Takes the current bid and checks if it is correct or not
        @return: True if the current bid is correct, False otherwise
        """
        # Count the dice
        num_dice = 0
        for player_id in self.players:
            for dice in self.players[player_id].dice:
                if dice == self.current_bid[1] or (self.wild_mode and dice == 1):
                    num_dice += 1
        self.correct_dice = num_dice
        return num_dice >= self.current_bid[0]
