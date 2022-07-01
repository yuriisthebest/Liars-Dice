from AI.player import Player


class Human(Player):
    def take_turn(self, game_state):
        raise ReferenceError("Humans should never be asked to do their turn here")
