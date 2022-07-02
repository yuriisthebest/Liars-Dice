from AI.player import Player


class Human(Player):
    @property
    def title(self) -> str:
        return ""

    @staticmethod
    def get_name() -> str:
        return ""

    def take_turn(self, game_state):
        raise ReferenceError("Humans should never be asked to do their turn here")
