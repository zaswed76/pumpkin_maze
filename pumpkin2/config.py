
class Config:
    def __init__(self):
        self.width_in_tile = 12
        self.height_in_tile = 12
        self.tileheight = 32
        self.tilewidth = 32
        self.width = self.tilewidth * self.width_in_tile
        self.height = self.tileheight * self.height_in_tile
        self.start_x = 160
        self.start_y = 60
        self.player_rect = (25, 25)
        self._included_levels = [
            'level_1'
        ]

        self.initialize_dynamic_settings()

    @property
    def included_levels(self) -> list:
        return self._included_levels

    def initialize_dynamic_settings(self):
        self.speedx = 2
        self.speedy = 2