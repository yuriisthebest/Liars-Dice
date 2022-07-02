import json
import random
import tkinter as tk

from AI import Human, ALL_AI
from AI.player import Player
from sound import Sound


class Game:
    """
    This class contains all the game logic and game loop
    """
    def __init__(self):
        # Set base settings
        with open("settings.json", 'r') as f:
            settings = json.load(f)
        self.sound = Sound(settings["sound"])
        self.starting_dice = settings["starting_dice"]
        self.visuals = settings["visual_indicators"]
        self.roll_delay = settings["roll_dice_delay"]
        self.player_delay = settings["player_delay"]
        self.challenge_delay = settings["challenge_delay"]
        self.error_msg_delay = settings["error_msg_delay"]
        # Initialize players and set variables for later
        self.players = {1: Human(None, self.starting_dice, 1, True)}
        self.board = None
        self.center_label = None
        self.current_bid = None
        self.previous_bids = None
        self.total_dice = None
        self.correct_dice = None
        self.wild_mode = None

    def add_board(self, board):
        """
        Add the board so the game can reference it
        """
        self.board = board

    def add_player(self, position: int, frame: tk.Frame, bot):
        # Create a new AI
        if bot == "Stranger":
            new_player = random.choice(ALL_AI)(frame, self.starting_dice, position, False, True)
        else:
            new_player = bot(frame, self.starting_dice, position, False)
        self.players[position] = new_player
        # Update GUI
        for child in frame.winfo_children():
            child.destroy()
        lbl_name = tk.Label(master=frame, text=new_player.get_title() + new_player.name)
        lbl_name.pack()

    def set_player_frame(self, frame: tk.Frame):
        self.players[1].frame = frame

    def start_game(self, frame: tk.Frame, board: tk.Frame):
        # Start the game by removing unneeded buttons
        lbl_error = tk.Label(master=frame, text="Need at least 2 players", fg="red")
        lbl_error.after(self.error_msg_delay, lbl_error.destroy)
        if len(self.players) < 2:
            lbl_error.pack()
        else:
            # Destroy wild mode button
            self.wild_mode = self.board.wild_mode.get()
            self.board.tgl_wild.destroy()
            # Destroy error messages?
            for child in frame.winfo_children():
                child.destroy()
            # Destroy unused "Add player" buttons
            for f in board.winfo_children():
                for child in f.winfo_children():
                    if type(child) == tk.Button:
                        child.destroy()
            # Place bidding
            self.board.bid_controls()
            # Remember center label
            lbl_center = tk.Label(master=frame, text="")
            lbl_center.pack()
            self.center_label = lbl_center
            # Pick a random position to start
            starting_position = random.choice(list(self.players.keys()))
            # Start the first round
            self.start_round(starting_position)

    def start_round(self, active_player: int):
        # Reset game states
        self.current_bid = [0, 0]
        self.previous_bids = []
        # Start by rolling dice
        self.center_label["text"] = "Rolling dice!"
        self.sound.play_dice()
        for player in self.players.values():
            player.roll_dice()
        # Reset and build the player frames
        for player_pos in self.players:
            player = self.players[player_pos]
            self.board.player_frame(player)
        # Update GUI for human player
        if 1 in self.players:
            self.players[1].frame.winfo_children()[-1]["text"] = self.players[1].reveal_dice()
        self.total_dice = sum([self.players[pos].num_dice for pos in self.players])
        # The players start taking turns
        self.center_label.after(self.roll_delay, lambda: self.find_next_player(active_player))

    def find_next_player(self, active_player: int):
        # Update center label
        t = "Time to bid!\n"
        t += f"Total number of dice: {self.total_dice}"
        if self.current_bid != [0, 0]:
            t += "\n\nCurrent bid:\n"
            t += f"{self.current_bid[0]} dice with value {self.current_bid[1]}"
        self.center_label["text"] = t
        while True:
            if active_player in self.players:
                if self.visuals:
                    self.players[active_player].frame.configure(highlightbackground="lightgreen")
                if self.players[active_player].human:
                    # Stop program and wait for human to make a move
                    break
                else:
                    # Let the bot 'think' then make a move
                    self.center_label.after(self.player_delay,
                                            lambda pos=active_player: self.bot_turn(pos))
                    break
            active_player += 1
            active_player %= 8

    def bot_turn(self, active_player: int):
        # Let the player take their turn
        bid = self.players[active_player].take_turn(self)
        # Challenge
        if bid == -1:
            self.challenge(active_player)
            return
        self.current_bid = bid
        self.previous_bids.append(bid)
        # Update GUI
        bid_text = f"I think there are {bid[0]} {bid[1]}'s" \
            if bid[0] > 1 \
            else f"I think there is {bid[0]} {bid[1]}"
        lbl_bid = tk.Label(master=self.players[active_player].frame,
                           text=bid_text)
        lbl_bid.pack()
        # End turn
        if self.visuals:
            self.players[active_player].frame.configure(highlightbackground="darkgreen")
        active_player += 1
        active_player %= 8
        self.find_next_player(active_player)

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

    def submit_bid(self, count_lbl: tk.Label, value_lbl: tk.Label):
        count = int(count_lbl["text"])
        value = int(value_lbl["text"])
        if not self.is_valid_bid([count, value]):
            error_label = tk.Label(master=self.center_label.master,
                                   text="That is not a valid bid",
                                   foreground='red')
            error_label.pack()
            error_label.after(self.error_msg_delay, error_label.destroy)
        else:
            # Update GUI
            if self.visuals:
                self.players[1].frame.configure(highlightbackground="darkgreen")
            bid = [count, value]
            bid_text = f"I think there are {bid[0]} {bid[1]}'s" \
                if bid[0] > 1 \
                else f"I think there is {bid[0]} {bid[1]}"
            lbl_bid = tk.Label(master=self.players[1].frame, text=bid_text)
            lbl_bid.pack()
            # Update bid
            self.current_bid = bid
            self.previous_bids.append(self.current_bid)
            self.find_next_player(active_player=2)

    def challenge(self, active_player: int):
        # Can only challenge after a bid
        if self.current_bid == [0, 0]:
            error_label = tk.Label(master=self.center_label.master,
                                   text="There must be bid before you can challenge",
                                   foreground='red')
            error_label.pack()
            error_label.after(self.error_msg_delay, error_label.destroy)
            return None
        # Play sound
        self.sound.play_liar()
        # Identify challengers
        challenger = self.players[active_player]
        defender = self.previous_player(active_player)
        challenger.frame.winfo_children()[0]["foreground"] = "orange"
        defender.frame.winfo_children()[0]["foreground"] = "orange"
        pronoun = 'has' if not challenger.human else 'have'
        t = f"{challenger.name} {pronoun} challenged {defender.name}!\n\n"
        t += "Current bid:\n"
        t += f"{self.current_bid[0]} dice with value {self.current_bid[1]}"
        self.center_label["text"] = t
        self.center_label.after(self.challenge_delay, lambda: self.end_round(challenger, defender))

    def end_round(self, challenger: Player, defender: Player):
        # Remove highlight from active player
        if self.visuals:
            challenger.frame.configure(highlightbackground="darkgreen")
        # Reveal dice
        for player_id in self.players:
            self.players[player_id].frame.winfo_children()[1]["text"] = \
                self.players[player_id].reveal_dice()
        # Determine winner
        if self.is_correct_bid():
            # Defender wins, Challenger loses
            loser = challenger
        else:
            # Challenger wins, Defender loses
            loser = defender
        loser.num_dice -= 1
        t = f"The bid is: {self.current_bid[0]} {self.current_bid[1]}"
        t += "'s\n" if self.current_bid[0] != 1 else "\n"
        wild = " (+ wild ones)" if self.wild_mode else ""
        if self.correct_dice == 1:
            t += f"There is 1 {self.current_bid[1]}{wild}\n"
        else:
            t += f"There are {self.correct_dice} {self.current_bid[1]}'s{wild}\n"
        pronoun = 'has' if not loser.human else 'have'
        t += f"{loser.name} {pronoun} lost one dice!"
        self.center_label["text"] = t
        # Remove loser from game
        if loser.num_dice == 0:
            del self.players[loser.pos]
            for child in loser.frame.winfo_children():
                child.destroy()
            pronoun = "are" if loser.human else "is"
            t += f"\n{loser.name} {pronoun} out of the game!"
            self.center_label["text"] = t
            # If the human lost, also remove all controls
            if loser.human:
                for child in self.board.controls_fr.winfo_children():
                    child.destroy()
        # Check if there is a winner
        if len(self.players) == 1:
            winner = list(self.players.values())[0]
            pronoun = 'has' if not winner.human else 'have'
            text = f"{winner.name} {pronoun} won!\n\nPress to exit!"
            button_next = tk.Button(master=self.center_label.master, text=text, fg="blue")
            button_next["command"] = self.board.window.destroy
            button_next.pack(padx=5, pady=10)
        # Ready next round
        else:
            button_next = tk.Button(master=self.center_label.master,
                                    text="Start next round", fg="red")
            button_next["command"] = lambda but=button_next:\
                self.next_round(but, loser.pos, challenger, defender)
            button_next.pack(padx=5, pady=10)

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

    def next_round(self, button: tk.Button, loser_pos: int, challenger: Player, defender: Player):
        try:
            challenger.frame.winfo_children()[0]["foreground"] = "black"
        except IndexError:
            pass
        try:
            defender.frame.winfo_children()[0]["foreground"] = "black"
        except IndexError:
            pass
        button.destroy()
        self.start_round(active_player=loser_pos)

    def previous_player(self, current_player: int) -> Player:
        while True:
            current_player -= 1
            current_player %= 8
            if current_player in self.players:
                return self.players[current_player]
