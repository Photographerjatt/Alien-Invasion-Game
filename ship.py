import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
   
    def __init__(self,ai_settings,screen):
        super().__init__()
        """Initialize the ship and set its starting position"""
        self.screen=screen
        self.ai_settings=ai_settings

        #Load the ship image and get its rect
        self.image=pygame.image.load('C:/Users/Ashish Nirwal/Visual studio c/Python(Eric Mathews)/game/image/ship.bmp')
        self.rect=self.image.get_rect()
        self.screen_rect=screen.get_rect()

        #Start each new ship at the bottom of the screen
        self.rect.centerx=self.screen_rect.centerx
        self.rect.bottom=self.screen_rect.bottom

        #Movement Flag
        self.moving_right=False
        self.moving_left=False

        #Store the Decimal value for ship center
        self.center=float(self.rect.centerx)

    def update(self):
        #Update the ship's position based on the movement flag
        if self.moving_right and self.rect.right<self.screen_rect.right:
            self.center+=self.ai_settings.ship_speed_factor
        elif self.moving_left and self.rect.left>0:
            self.center-=self.ai_settings.ship_speed_factor

        #Updating rect object from self.center
        self.rect.centerx=self.center

    def center_ship(self):
        self.center=self.screen_rect.centerx

    def bltime(self):
        #Draw ship at its current location
        self.screen.blit(self.image,self.rect)