import tkinter as tk

from game import Game
from AI import ALL_AI

POSITIONS = {
    0: 4,
    1: 5,
    2: 6,
    3: 3,
    4: -1,
    5: 7,
    6: 2,
    7: 1,
    8: 0,
}


class Board:
    # Create a board with a game instance
    def __init__(self, game: Game, root: tk.Tk):
        self.game = game
        self.window = root
        self.controls_fr = None
        self.wild_mode = False
        self.tgl_wild = None
        self.lbl_dice_count = None
        self.lbl_dice_value = None

    def setup(self):
        # Create main frames
        self.window.title("Liar's Dice")
        board_fr = tk.Frame(master=self.window, height=600, bg="darkgreen")
        self.controls_fr = tk.Frame(master=self.window, borderwidth=6, relief=tk.GROOVE,
                                    height=150, bg="gray")
        board_fr.pack(fill=tk.BOTH, expand=True)
        self.controls_fr.pack(fill=tk.BOTH)
        # Create wild mode toggle
        self.wild_mode = tk.BooleanVar()
        self.tgl_wild = tk.Checkbutton(master=self.controls_fr, text="Toggle WILD-mode",
                                       variable=self.wild_mode, onvalue=True, offvalue=False,
                                       bg="gray", font=("Comic Sans MS", 12))
        self.tgl_wild.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        # Create player frames
        frm_players = []
        for i in range(3):
            # Window options
            board_fr.columnconfigure(i, weight=1, minsize=200)
            board_fr.rowconfigure(i, weight=1, minsize=150)
            for j in range(3):
                frm = tk.Frame(master=board_fr, width=200, height=200, bg="darkgreen",
                               highlightthickness=6, highlightcolor='darkgreen',
                               highlightbackground='darkgreen')
                frm.grid(row=i, column=j, ipadx=10, ipady=10)
                frm_players.append(frm)
                # Add start game to the center
                if i == 1 and j == 1:
                    btn_start = tk.Button(master=frm, text="Start the game")
                    btn_start["command"] = lambda f=frm, b=board_fr: self.game.start_game(f, b)
                    btn_start.pack()
                # The bottom center player is the human
                elif i == 2 and j == 1:
                    lbl_player = tk.Label(master=frm, text="This is your field")
                    lbl_player.pack()
                    self.game.set_player_frame(frame=frm)
                else:
                    # Positions range from 0 to 8, excluding 4 and 7
                    pos = POSITIONS[i * 3 + j]
                    btn_add = tk.Button(master=frm, text="Add player", fg="gray")
                    btn_add["command"] = lambda p=pos, b=btn_add, f=frm: self.pick_ai(f, b, p)
                    btn_add.pack()
        self.window.mainloop()

    def pick_ai(self, player_frame: tk.Frame, button: tk.Button, position: int):
        button.destroy()
        for i, AI in enumerate(ALL_AI):
            btn = tk.Button(master=player_frame, text=f"{AI.get_name()}",
                            height=1, width=6)
            btn["command"] = lambda bot=AI: self.game.add_player(position, player_frame, bot)
            btn.grid(row=i//3, column=i % 3)
        randomizer = tk.Button(master=player_frame, text="Stranger",
                               height=1, width=6)
        randomizer["command"] = lambda: self.game.add_player(position, player_frame, "Stranger")
        randomizer.grid(row=2, column=1)

    @staticmethod
    def player_frame(player):
        for child in player.frame.winfo_children():
            child.destroy()
        if player.human:
            lbl_name = tk.Label(master=player.frame, text="This is your field")
        else:
            lbl_name = tk.Label(master=player.frame, text=player.get_title() + player.name)
        lbl_name.pack()
        lbl_dice = tk.Label(master=player.frame, text="? " * player.num_dice)
        lbl_dice.pack()

    def bid_controls(self):
        self.controls_fr.columnconfigure(0, weight=1)
        self.controls_fr.columnconfigure(3, weight=1)
        self.controls_fr.columnconfigure(5, weight=1)
        self.controls_fr.columnconfigure(6, weight=1)
        button_liar = tk.Button(master=self.controls_fr, text="Liar!")
        button_submit = tk.Button(master=self.controls_fr, text="Bid")
        self.lbl_dice_count = tk.Label(master=self.controls_fr, text="1")
        self.lbl_dice_value = tk.Label(master=self.controls_fr, text="1")
        button_inc_count = tk.Button(master=self.controls_fr, text="Increase\nCount")
        button_dec_count = tk.Button(master=self.controls_fr, text="Decrease\nCount")
        button_inc_value = tk.Button(master=self.controls_fr, text="Increase\nValue")
        button_dec_value = tk.Button(master=self.controls_fr, text="Decrease\nValue")
        button_inc_count["command"] = self.inc_count
        button_dec_count["command"] = self.dec_count
        button_inc_value["command"] = self.inc_value
        button_dec_value["command"] = self.dec_value
        button_submit["command"] = (lambda count=self.lbl_dice_count, value=self.lbl_dice_value:
                                    self.game.submit_bid(count, value))
        button_liar["command"] = lambda: self.game.challenge(1)
        button_liar.grid(row=1, column=0, padx=5, pady=5)
        self.lbl_dice_count.grid(row=1, column=3, padx=5, pady=5)
        self.lbl_dice_value.grid(row=1, column=5, padx=5, pady=5)
        button_inc_count.grid(row=0, column=3, padx=5, pady=5)
        button_dec_count.grid(row=2, column=3, padx=5, pady=5)
        button_inc_value.grid(row=0, column=5, padx=5, pady=5)
        button_dec_value.grid(row=2, column=5, padx=5, pady=5)
        button_submit.grid(row=1, column=6, padx=5, pady=5)

    def inc_count(self):
        value = int(self.lbl_dice_count["text"])
        self.lbl_dice_count["text"] = f"{value + 1}"

    def dec_count(self):
        value = int(self.lbl_dice_count["text"])
        self.lbl_dice_count["text"] = f"{max(1, value - 1)}"

    def inc_value(self):
        value = int(self.lbl_dice_value["text"])
        self.lbl_dice_value["text"] = f"{min(6, value + 1)}"

    def dec_value(self):
        value = int(self.lbl_dice_value["text"])
        self.lbl_dice_value["text"] = f"{max(1, value - 1)}"
