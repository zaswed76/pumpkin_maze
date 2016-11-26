

class GameStat:
    def __init__(self):
        self._level = 0
        self.max_levels = 3
        self.reset_level()

    def reset_level(self):
        self._level = 0

    def increase_level(self):
        if self._level < self.max_levels:
            self._level +=1

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, level):
        self._level = level