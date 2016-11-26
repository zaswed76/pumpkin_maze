class Config:
    def __init__(self):
        self.width = 640
        self.height = 640
        self.included_level = (1,)

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.speedx = 2
        self.speedy = 2