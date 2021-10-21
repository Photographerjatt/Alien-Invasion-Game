import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single alien in the fleet."""
    def __init__(self,ai_setting,screen):
        super().__init__()
        self.screen=screen
        self.ai_setting=ai_setting

        # Load the alien image and set its rect attribute
        self.image=pygame.image.load("C:/Users/Ashish Nirwal/Visual studio c/Python(Eric Mathews)/game/image/alien.bmp")
        self.rect=self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x=self.rect.width
        self.rect.y=self.rect.height

        # Store the alien's exact position.
        self.x=float(self.rect.x)

    def bltime(self):
        """Draw the alien at its current location."""
        self.screen.blit(self.image,self.rect)

    def update(self):
        self.x+=(self.ai_setting.alien_speed*self.ai_setting.fleet_direction)
        self.rect.x=self.x

    def check_edges(self):
        screen_rect=self.screen.get_rect()
        if self.rect.right>=screen_rect.right:
            return True
        elif self.rect.left<=0:
            return True