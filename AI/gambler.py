from AI.player import Player


class Gambler(Player):
    @property
    def title(self) -> str:
        return "Gambler "

    @staticmethod
    def get_name() -> str:
        return "Gambler"

    def take_turn(self, game_state):
        pass
