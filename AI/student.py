from AI.player import Player


class Student(Player):
    @property
    def title(self) -> str:
        return "Student "

    @staticmethod
    def get_name() -> str:
        return "Student"

    def take_turn(self, game_state):
        # Temp return
        return [39, 6]
