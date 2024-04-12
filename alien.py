import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    def __init__(self,ai_settings,screen):
        # initalize alien
        super(Alien,self).__init__()
        self.screen=screen
        self.ai_settings=ai_settings
        self.image=pygame.image.load('images/alien.bmp')
        self.rect=self.image.get_rect()
        self.rect.x=self.rect.width
        self.rect.y=self.rect.height
        self.x=float(self.rect.x) # stores alien current position

    def blitme(self):
        # draw alien at its current position
        self.screen.blit(self.image,self.rect)

    def update(self):
        # move aliens right or left
        self.x+=(self.ai_settings.alien_speed_factor*self.ai_settings.fleet_direction)
        self.rect.x=self.x

    def check_edges(self):
        screen_rect=self.screen.get_rect()
        if self.rect.right>=screen_rect.right or self.rect.left<=0:
            return True