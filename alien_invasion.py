import sys
from time import sleep

import pygame

from alien import Alien
from bullet import Bullet
from button import Button
from game_stats import GameStats
from score_board import Scoreboard
from settings import Settings
from ship import Ship


class AlienInvasion:
    """Overall class to manage game assets and behaviour"""

    def __init__(self):
        """Initialize the game, and create game resources"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_height = self.screen.get_rect().height
        self.settings.screen_width = self.screen.get_rect().width
        pygame.display.set_caption("Alien Invasion")
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)

        # todo set background color
        self.bg_color = self.settings.bg_color
        self.bullets = pygame.sprite.Group()
        self.alien = pygame.sprite.Group()

        self._create_fleet()
        self.play_button = Button(self, 'Play')

    def run_game(self):
        """Start main loop for the game"""
        self._update_screen()
        while True:
            # todo Watch keyboard and mouse events
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self._update_screen()

    def _check_events(self):
        """Respond to keyboard events and mouse clicks """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._key_down_events(event)
            elif event.type == pygame.KEYUP:
                self._key_up_events(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _update_screen(self):
        """Update images on the screen and flip to the new screen"""
        if not self.stats.game_active:
            self.screen.fill((0, 0, 0))
            self.play_button.draw_button()
        else:
            # todo redraw screen inside loop
            self.screen.fill(self.bg_color)
            self.ship.blitme()
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            self.alien.draw(self.screen)
            self.sb.show_score()
        # todo make the most recent drawn screen visible
        pygame.display.flip()

    def _key_down_events(self, event):
        if event.key == pygame.K_RIGHT:
            # todo move the spaceship right
            self.ship.move_right = True
        elif event.key == pygame.K_LEFT:
            # todo move the spaceship left
            self.ship.move_left = True
        elif event.key == pygame.K_q:
            self._store_scores()
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_e:
            self.settings.bullet_width = 100

    def _key_up_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.move_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.move_left = False
        elif event.key == pygame.K_e:
            self.settings.bullet_width = 3

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        self.bullets.update()
        # get rid of bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collision()

    def _create_alien(self, alien_number, row):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height * (1 + 2 * row)
        self.alien.add(alien)

    def _create_fleet(self):
        """Create a fleet of aliens"""
        # todo make an alien
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_of_rows = available_space_y // (2 * alien_height)

        # todo create the first row of aliens
        for row in range(number_of_rows):
            for alien_number in range(number_aliens_x):
                # todo create an alien and add it to the row
                self._create_alien(alien_number, row)

    def _update_aliens(self):
        """
        Check if the fleet is at the edge,
        Update the  position of all aliens in the fleet
        """
        self.alien.update()
        self._check_fleet_edges()
        if pygame.sprite.spritecollideany(self.ship, self.alien):
            self._ship_hit()
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        """Responds appropriately if any alien has reached the edge"""
        for alien in self.alien.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drops the entire fleet and changes its direction"""
        for alien in self.alien.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_bullet_alien_collision(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.alien, True, True)
        if collisions:
            for alien in collisions.values():
                self.stats.score += self.settings.alien_points * len(alien)
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.alien:
            self.bullets.empty()
            self._create_fleet()
            self.settings.bullets_allowed += 3
            self.settings.bullet_speed += 0.5
            self.settings.increase_speed()
            self.stats.level += 1
            self.sb.prep_level()

    def _ship_hit(self):
        """Respond to the ship being hit by aliens"""
        if self.stats.ship_left > 0:
            self.stats.ship_left -= 1
            self.sb.prep_ship()

            self.alien.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()

            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.alien.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True

            self.alien.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ship()
            pygame.mouse.set_visible(False)

    def _store_scores(self):
        information = self.stats.score
        with open('scores.txt', mode='a') as txt_file:
            txt_file.write(f"{information},")


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
