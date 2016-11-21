

class GameStat:
    def __init__(self):
        self.max_levels = 1
        self.reset_starts()

    def reset_starts(self):
        self.level = 0

    def increase_level(self):
        if self.level < self.max_levels:
            self.level +=1