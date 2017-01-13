

class Config:
    def __init__(self):
        self.width = 640
        self.height = 640
        self.start_x = 160
        self.start_y = 60
        self.player_rect = (25, 25)
        self.included_levels = ['level_1']

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.speedx = 2
        self.speedy = 2