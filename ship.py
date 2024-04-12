import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self,ai_settings,screen):
        super(Ship,self).__init__()
        self.ai_settings=ai_settings
        # initalize ship and set its starting position
        self.screen=screen
        # loads ship image and get its rect
        self.image=pygame.image.load('images/ship.bmp')
        self.rect=self.image.get_rect()
        self.screen_rect=screen.get_rect()
        # start ship and bottom centre of screen
        self.rect.centerx=float(self.screen_rect.centerx)
        self.rect.bottom=self.screen_rect.bottom
        self.moving_right=False
        self.moving_left=False

    def blitme(self):
        # draw ship at its current location
        self.screen.blit(self.image,self.rect)

    def center_ship(self):
        self.center=self.screen_rect.centerx

    def update(self):
        # move ship to either right or left
        if self.moving_right==True and self.rect.right<self.screen_rect.right:
            self.rect.centerx+=self.ai_settings.ship_speed_factor
        if self.moving_left==True and self.rect.left>self.screen_rect.left:
            self.rect.centerx-=self.ai_settings.ship_speed_factor