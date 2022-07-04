import tkinter as tk

from board import Board
from game import Game


def main(root):
    # Initialize game and board
    game = Game()
    board = Board(game, root)
    game.add_board(board)
    # Set up the board and start the game loop
    board.setup()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    root_window = tk.Tk()
    main(root_window)
