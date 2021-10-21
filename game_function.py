import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

def check_keydown_events(event,ai_settings,screen,ship,bullets):
    """Respond to keypresses."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key==pygame.K_SPACE:
        fire_bullets(bullets,ai_settings,screen,ship)
    elif event.key==pygame.K_q:
        sys.exit()

        

def check_keyup_events(event, ship):
    """Respond to keypresses"""
    if event.key==pygame.K_RIGHT:
        ship.moving_right=False
    elif event.key==pygame.K_LEFT:
        ship.moving_left=False

def check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets):
    """Respond to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type==pygame.KEYDOWN:
           check_keydown_events(event,ai_settings,screen,ship,bullets)
        elif event.type==pygame.KEYUP:
            check_keyup_events(event,ship)
        elif event.type==pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y=pygame.mouse.get_pos()
            check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y)

def check_play_button(ai_setting,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y):
    button_clicked=play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not stats.game_active:
        ai_setting.initialize_dynamic_setting()
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active=True

        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        aliens.empty()
        bullets.empty()

        create_fleet(ai_setting,screen,ship,aliens)
        ship.center_ship()

"""Update images on the screen and flip to the new screen."""
def update_screen(ai_settings,screen,stats,sb,ship,alien,bullets,play_button):
    #Redraw the screen during each pass throug the loop
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.bltime()
    alien.draw(screen)
    sb.show_scoreboard()
    if not stats.game_active:
        play_button.draw_button()


    #Make the most recently drawn screen visible
    pygame.display.flip()

def update_bullet(ai_setting,screen,ship,sb,stats,alien,bullets):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom<=0:
            bullets.remove(bullet)
    bullet_collision(ai_setting,screen,ship,sb,stats,alien,bullets)

def bullet_collision(ai_setting,screen,ship,sb,stats,alien,bullets):
    collisions=pygame.sprite.groupcollide(bullets,alien,True,True)
    if collisions:
        for alien in collisions.values():
            stats.score+=ai_setting.alien_points*len(alien)
            sb.prep_score()
        check_high_score(stats,sb)
    if len(alien)==0:
        bullets.empty()
        ai_setting.increase_speed()
        stats.level+=1
        sb.prep_level()  
        create_fleet(ai_setting,screen,ship,alien)

def fire_bullets(bullets,ai_settings,screen,ship):
    if len(bullets)<ai_settings.bullet_limit:
            new_bullet=Bullet(ai_settings,screen,ship)
            bullets.add(new_bullet)
    

def create_fleet(ai_setting,screen,ship,aliens):
    alien=Alien(ai_setting,screen)
    alien_width=alien.rect.width
    a=get_no_of_alien_x(ai_setting,alien_width)
    number_rows=get_no_of_rows(ai_setting,ship.rect.height,alien.rect.height)
    for row_number in range(number_rows):
        for alien_no in range(a):
            create_alien(ai_setting,screen,alien_width,alien_no,aliens,row_number)
        

def get_no_of_alien_x(ai_setting,alien_width):
    available_space_x=ai_setting.screen_width-2*alien_width
    no_of_alien_x=int(available_space_x/(2*alien_width))
    return no_of_alien_x

def create_alien(ai_setting,screen,alien_width,alien_no,aliens,row_number):
    alien=Alien(ai_setting,screen)
    alien.x=alien_width+2*alien_width*alien_no
    alien.rect.x=alien.x
    alien.rect.y=alien.rect.height+2*alien.rect.height*row_number
    aliens.add(alien)

def get_no_of_rows(ai_setting,ship_height,alien_height):
    available_space_y=(ai_setting.screen_height-(3*alien_height)-ship_height)
    no_of_rows=int(available_space_y/(2*alien_height))
    return no_of_rows

def update_aliens(ai_setting,stats,sb,screen,ship,aliens,bullets):
    check_fleet_edges(ai_setting,aliens)
    aliens.update()
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_setting,stats,sb,screen,ship,aliens,bullets)
    check_aliens_bottom(ai_setting,stats,sb,screen,ship,aliens,bullets)

def check_fleet_edges(ai_settings, aliens):
    """Respond appropriately if any aliens have reached an edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet and change the fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, stats,sb, screen, ship, aliens, bullets):
    """Respond to ship being hit by alien."""
    # Decrement ships_left.
    if stats.ships_left>0:       
        stats.ships_left -= 1
        sb.prep_ships()
        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()
        sleep(0.5)
    
    else:
        stats.game_active=False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, stats,sb, screen, ship, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(ai_settings, stats,sb, screen, ship, aliens, bullets)
            break

def check_high_score(stats,sb):
    if stats.score>stats.high_score:
        stats.high_score=stats.score
        sb.prep_high_score()