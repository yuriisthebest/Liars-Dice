from playsound import playsound
from threading import Thread


class Sound:
    """
    The sound player

    If you have problems with playsound:
     ensure you have installed playsound version 1.2.2
     comment the import and turn sound off in settings
    """
    def __init__(self, sound_on: bool):
        self.sound_on = sound_on

    def play_dice(self):
        if not self.sound_on:
            return None
        try:
            sound = Thread(target=playsound, args=("sounds/Dice.mp3", ))
            sound.start()
        except Exception:
            pass

    def play_liar(self):
        if not self.sound_on:
            return None
        try:
            sound = Thread(target=playsound, args=("sounds/liar.mp3", ))
            sound.start()
        except Exception:
            pass
