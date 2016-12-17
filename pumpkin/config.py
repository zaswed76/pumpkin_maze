

class Config:
    def __init__(self):
        self.width = 96
        self.height = 96
        self.start_x = 64
        self.start_y = 64
        self.player_rect = (25, 25)
        self.included_level = [1, 2]

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.speedx = 2
        self.speedy = 2