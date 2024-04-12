import pygame
import sys
from bullet import Bullet
from alien import Alien
from time import sleep

def check_aliens_bottom(ai_settings,stats,sb,screen,ship,bullets,aliens):
    screen_rect=screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom>=screen_rect.bottom:
            ship_hit(ai_settings,stats,sb,screen,ship,aliens,bullets)
            break

def ship_hit(ai_settings,stats,sb,screen,ship,aliens,bullets):
    if stats.ship_left>1:
        # decrements ship_limit
        stats.ship_left -= 1
        sb.prep_ships()
        # remove all aliens and bullets remaining
        bullets.empty()
        aliens.empty()
        # create new fleet
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        sleep(1)
    else:
        stats.game_active=False
        pygame.mouse.set_visible(True)


def get_number_alines_x(ai_settings,alien_width):
    # calculates number of aliens in row
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x=int(available_space_x/(2*alien_width))
    return number_aliens_x

def get_number_rows(ai_settings,alien_height,ship_height):
    # claculate number of rows
    available_space_y=ai_settings.screen_height-3*alien_height-ship_height
    number_rows=int(available_space_y/(2*alien_height))
    return number_rows

def create_alien(ai_settings,screen,aliens,alien_number,row_number):
    alien = Alien(ai_settings, screen)
    alien_width=alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y=alien.rect.height+2*alien.rect.height*row_number
    aliens.add(alien)

def firing_bullets(ai_settings,screen,ship,bullets):
    if len(bullets) < ai_settings.bullet_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
def manage_keydown_events(event,ai_settings,screen,ship,bullets):
    # set moving of ship to either left or right according to key pressed
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    # adds new bullet every time space bar is pressed
    elif event.key == pygame.K_SPACE:
        firing_bullets(ai_settings,screen,ship,bullets)
    elif event.key == pygame.K_ESCAPE:
        sys.exit()


def manage_keyup_events(event,ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        # check whether any key is pressed or not
        elif event.type == pygame.KEYDOWN:
            manage_keydown_events(event,ai_settings,screen,ship,bullets)
        elif event.type == pygame.KEYUP:
            manage_keyup_events(event,ship)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y=pygame.mouse.get_pos()
            check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y)

def check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y):
    button_clicked=play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not stats.game_active:
        ai_settings.initialize_dynamic_settings()
        stats.reset_stats()
        stats.game_active=True
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()
        pygame.mouse.set_visible(False)

def update_screen(ai_settings,screen,stats,sb,ship,bullets,aliens,play_button):
    screen.fill(ai_settings.bg_color)
    # draw a bullet form bullet in bullets group
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    sb.show_score()
    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()

def update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collision(ai_settings,screen,stats,sb,ship,aliens,bullets)

def check_bullet_alien_collision(ai_settings,screen,stats,sb,ship,aliens,bullets):
    # delete alien if bullet alien collison occur
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points*len(aliens)
            sb.prep_score()
        check_high_score(stats,sb)
    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, ship, aliens)
        stats.level+=1
        sb.prep_level()


def create_fleet(ai_settings,screen,ship,aliens):
    # create aliens
    alien=Alien(ai_settings,screen)
    number_aliens_x=get_number_alines_x(ai_settings,alien.rect.width)
    number_rows=get_number_rows(ai_settings,alien.rect.height,ship.rect.height)
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings,screen,aliens,alien_number,row_number)

def update_aliens(ai_settings,stats,sb,screen,ship,aliens,bullets):
    check_fleet_edges(ai_settings,aliens)
    aliens.update()
    check_aliens_bottom(ai_settings, stats, sb, screen, ship, bullets, aliens)
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings,stats,sb,screen,ship,aliens,bullets)
    check_aliens_bottom(ai_settings,stats,sb,screen,ship,bullets,aliens)


def check_fleet_edges(ai_settings,aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break

def change_fleet_direction(ai_settings,aliens):
    # drop entire fleet and change direction
    for alien in aliens.sprites():
        alien.rect.y+=ai_settings.fleet_drop_speed
    ai_settings.fleet_direction*=-1

def check_high_score(stats,sb):
    if stats.score>stats.high_score:
        stats.high_score=stats.score
        sb.prep_high_score()