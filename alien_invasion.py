import pygame

from settings import Settings
from ship import Ship
import game_function as gf
from pygame.sprite import Group
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

def run_game():
    #Initialize pygame,settings and screen object
    pygame.init()
    ai_settings=Settings()
    screen=pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    stats=GameStats(ai_settings)
    #Make ship
    ship=Ship(ai_settings,screen)
    bullets=Group()
    alien=Group()
    gf.create_fleet(ai_settings,screen,ship,alien)
    play_button=Button(ai_settings,screen,"Play")
    sb=Scoreboard(ai_settings,screen,stats)
 

    #start the main loop for the game
    while True:
        #Respond to keypresses and mouse events
        gf.check_events(ai_settings,screen,stats,sb,play_button,ship,alien,bullets)
        #Responds to keypress for ship movement
        if stats.game_active:
            ship.update()
            gf.update_bullet(ai_settings,screen,ship,sb,stats,alien,bullets)
            gf.update_aliens(ai_settings,stats,sb,screen,ship,alien,bullets)
        #Update images on the screen and flip to the new screen.
        gf.update_screen(ai_settings,screen,stats,sb,ship,alien,bullets,play_button)


run_game()