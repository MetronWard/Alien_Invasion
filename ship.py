import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """A class to manage the ship"""

    def __init__(self, ai_game):
        super().__init__()
        """Initialize the ship and set its starting position"""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        # todo set the screen and get its image
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # todo start a new ship at the bottom of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        # todo Directional Flags
        self.move_right = False
        self.move_left = False

        self.settings = ai_game.settings
        self.x = float(self.rect.x)

    def blitme(self):
        """Dray ship at its current location"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Updating the ship's position based on the movement flag"""
        if self.move_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.move_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        self.rect.x = self.x

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
