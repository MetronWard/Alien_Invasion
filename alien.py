import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """A class to represent a single alien on the screen"""

    def __init__(self, ai_game):
        """Initialize the alien and set its starting position"""
        super().__init__()
        self.screen = ai_game.screen
        # todo Load the alien and set its rect position
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()
        # todo start a new alien at the top of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        # todo Store alien's exact position
        self.x = float(self.rect.x)

        self.settings = ai_game.settings

    def update(self):
        """Move alien to the right"""
        self.x += (self.settings.fleet_direction * self.settings.alien_speed)
        self.rect.x = self.x

    def check_edges(self):
        """Returns true if the alien has reached the edge"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left < 0:
            return True
