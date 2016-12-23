

class Config:
    def __init__(self):
        self.width = 320
        self.height = 320
        self.start_x = 90
        self.start_y = 100
        self.player_rect = (25, 25)
        self.included_levels = ('first', 'second')

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.speedx = 1
        self.speedy = 1