import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from game_stats import Gamestats
from button import Button
from scoreboard import Scoreboard

def run_game():
    # starts screen
    pygame.init()
    ai_settings=Settings()
    screen=pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    ship=Ship(ai_settings,screen)
    bullets=Group() # Group to store bullets
    aliens=Group() # Group to store aliens
    gf.create_fleet(ai_settings,screen,ship,aliens)
    stats=Gamestats(ai_settings)
    sb=Scoreboard(ai_settings,screen,stats)
    play_button=Button(ai_settings,screen,"Play")
    while True:
        # check for any events
        gf.check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets)
        # update ship object
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats , sb , screen, ship, aliens, bullets)
        gf.update_screen(ai_settings,screen,stats,sb,ship,bullets,aliens,play_button)
run_game()