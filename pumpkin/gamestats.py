

class GameStat:
    def __init__(self, cfg):
        self.cfg = cfg
        self._level = 0
        self.max_levels = len(self.cfg.included_level)
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
        if level < self.max_levels:
            self._level = level
        else:
            print('{}: включено только - {} уровней'.format(
                self.__class__.__name__,
                self.max_levels))
            print('------------------------------------------')