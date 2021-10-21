class Settings():
    """A class to store all settings for Alien Invasion"""

    def __init__(self):
        """Initialize the game settings"""
        #Screen settings
        self.screen_width=1200
        self.screen_height=800
        self.bg_color=(100,139,247)
        self.ship_speed_factor=1.5
        self.bullet_width=3
        self.bullet_height=15
        self.bullet_color=(255,211,40)
        self.bullet_limit=3
        self.fleet_drop_speed=10
        self.ship_limit=3
        self.speedup_scale=1.1
        self.score_scale=1.5
        self.initialize_dynamic_setting()

    def initialize_dynamic_setting(self):
        self.ship_speed=1.5
        self.bullet_speed=3
        self.alien_speed=1
        self.fleet_direction=1
        self.alien_points=50
    
    def increase_speed(self):
        self.ship_speed*=self.speedup_scale
        self.bullet_speed*=self.speedup_scale
        self.alien_speed*=self.speedup_scale
        self.alien_points=int(self.alien_points*self.score_scale)
