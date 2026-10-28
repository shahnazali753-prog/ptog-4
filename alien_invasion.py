# Alien Invasion: shoot down the alien fleet before it reaches you!
# Needs pygame. Install it with:  pip install pygame
#
# Controls:
#   Left / Right arrows (or A / D)  move the ship
#   Space                           shoot
#   P                               pause
#   Esc                             back to the menu (or quit from the menu)

import random
import pygame


class Settings:
    """All the settings for the game live here."""

    def __init__(self):
        # Screen
        self.screen_width = 900
        self.screen_height = 650
        self.bg_color = (10, 10, 30)
        self.show_stars = True
        self.fps = 60

        # Player
        self.lives = 3
        self.ship_speed = 6
        self.ship_color = "Blue"

        # Your bullets
        self.bullet_speed = 9
        self.bullet_width = 4
        self.bullet_height = 15
        self.bullets_allowed = 3

        # Aliens
        self.alien_rows = 4
        self.alien_columns = 8
        self.alien_speed = 2
        self.fleet_drop_speed = 12
        self.aliens_shoot = True
        self.alien_fire_chance = 1   # chance per frame, out of 1000, for each alien
        self.alien_bullet_speed = 5

        # How fast the game gets harder after each wave
        self.speedup_scale = 1.1
        self.points_per_alien = 50

        # The menu uses this list to show and change the settings above.
        # Each entry is: (label shown on screen, setting name, choices)
        self.options = [
            ("Difficulty", None, ["Easy", "Normal", "Hard", "Insane"]),
            ("Lives", "lives", [1, 2, 3, 5, 9]),
            ("Ship speed", "ship_speed", [3, 4, 6, 8, 10]),
            ("Ship color", "ship_color", ["Blue", "Green", "Red", "Yellow"]),
            ("Bullet speed", "bullet_speed", [5, 7, 9, 12, 15]),
            ("Bullet width", "bullet_width", [2, 4, 8, 16, 40]),
            ("Bullets on screen", "bullets_allowed", [1, 2, 3, 5, 10]),
            ("Alien rows", "alien_rows", [1, 2, 3, 4, 5, 6]),
            ("Alien columns", "alien_columns", [4, 6, 8, 10, 12]),
            ("Alien speed", "alien_speed", [1, 2, 3, 4, 6]),
            ("Fleet drop speed", "fleet_drop_speed", [5, 8, 12, 20, 30]),
            ("Aliens shoot back", "aliens_shoot", [True, False]),
            ("Alien fire rate", "alien_fire_chance", [1, 2, 3, 5]),
            ("Speed-up per wave", "speedup_scale", [1.0, 1.05, 1.1, 1.2, 1.3]),
            ("Starry background", "show_stars", [True, False]),
        ]

        # Remember the starting speeds so a new game can reset them.
        self.difficulty = "Normal"
        self.save_start_speeds()

    def apply_difficulty(self, name):
        """Change several settings at once to match a difficulty level."""
        self.difficulty = name
        if name == "Easy":
            self.lives, self.alien_speed, self.alien_rows = 5, 1, 3
            self.aliens_shoot, self.speedup_scale = False, 1.05
        elif name == "Normal":
            self.lives, self.alien_speed, self.alien_rows = 3, 2, 4
            self.aliens_shoot, self.speedup_scale = True, 1.1
            self.alien_fire_chance = 1
        elif name == "Hard":
            self.lives, self.alien_speed, self.alien_rows = 2, 3, 5
            self.aliens_shoot, self.speedup_scale = True, 1.2
            self.alien_fire_chance = 2
        elif name == "Insane":
            self.lives, self.alien_speed, self.alien_rows = 1, 4, 6
            self.aliens_shoot, self.speedup_scale = True, 1.3
            self.alien_fire_chance = 5
        self.save_start_speeds()

    def save_start_speeds(self):
        self.start_alien_speed = self.alien_speed
        self.start_alien_bullet_speed = self.alien_bullet_speed

    def reset_speeds(self):
        self.alien_speed = self.start_alien_speed
        self.alien_bullet_speed = self.start_alien_bullet_speed

    def speed_up(self):
        """Make the aliens faster for the next wave."""
        self.alien_speed = self.alien_speed * self.speedup_scale
        self.alien_bullet_speed = self.alien_bullet_speed * self.speedup_scale

    def get_value(self, option):
        label, name, choices = option
        if name is None:
            return self.difficulty
        return getattr(self, name)

    def change_option(self, option, step):
        """Move a setting to the next (step=1) or previous (step=-1) choice."""
        label, name, choices = option
        current = self.get_value(option)
        if current in choices:
            index = choices.index(current)
        else:
            index = 0
        new_value = choices[(index + step) % len(choices)]

        if name is None:
            self.apply_difficulty(new_value)
        else:
            setattr(self, name, new_value)
            self.save_start_speeds()


SHIP_COLORS = {
    "Blue": (80, 160, 255),
    "Green": (80, 230, 120),
    "Red": (255, 90, 90),
    "Yellow": (255, 220, 70),
}


class Ship:
    def __init__(self, game):
        self.settings = game.settings
        self.rect = pygame.Rect(0, 0, 50, 30)
        self.center_ship()

    def center_ship(self):
        self.rect.midbottom = (self.settings.screen_width // 2,
                               self.settings.screen_height - 15)
        self.x = float(self.rect.x)

    def update(self, keys):
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x = self.x + self.settings.ship_speed
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x = self.x - self.settings.ship_speed
        # Do not let the ship leave the screen.
        self.x = max(0, min(self.x, self.settings.screen_width - self.rect.width))
        self.rect.x = int(self.x)

    def draw(self, screen):
        color = SHIP_COLORS[self.settings.ship_color]
        r = self.rect
        points = [(r.centerx, r.top), (r.left, r.bottom), (r.right, r.bottom)]
        pygame.draw.polygon(screen, color, points)
        pygame.draw.rect(screen, (255, 255, 255), (r.centerx - 3, r.top + 8, 6, 8))


class Bullet:
    def __init__(self, x, y, width, height, speed, color):
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.midbottom = (x, y)
        self.y = float(self.rect.y)
        self.speed = speed   # negative goes up, positive goes down
        self.color = color

    def update(self):
        self.y = self.y + self.speed
        self.rect.y = int(self.y)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


class Alien:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 28)
        self.x = float(x)

    def draw(self, screen, frame):
        r = self.rect
        pygame.draw.ellipse(screen, (120, 255, 120), r)
        # Eyes
        pygame.draw.circle(screen, (0, 0, 0), (r.centerx - 8, r.centery - 2), 4)
        pygame.draw.circle(screen, (0, 0, 0), (r.centerx + 8, r.centery - 2), 4)
        # Legs wiggle every few frames.
        wiggle = 3 if (frame // 15) % 2 == 0 else -3
        pygame.draw.line(screen, (120, 255, 120), (r.left + 8, r.bottom - 2),
                         (r.left + 8 + wiggle, r.bottom + 6), 3)
        pygame.draw.line(screen, (120, 255, 120), (r.right - 8, r.bottom - 2),
                         (r.right - 8 - wiggle, r.bottom + 6), 3)


class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        self.clock = pygame.time.Clock()
        self.big_font = pygame.font.SysFont(None, 72)
        self.font = pygame.font.SysFont(None, 34)
        self.small_font = pygame.font.SysFont(None, 26)

        self.stars = [(random.randint(0, self.settings.screen_width),
                       random.randint(0, self.settings.screen_height),
                       random.randint(1, 2)) for _ in range(120)]

        self.ship = Ship(self)
        self.bullets = []
        self.alien_bullets = []
        self.aliens = []
        self.fleet_direction = 1   # 1 is right, -1 is left

        self.state = "menu"        # menu, settings, playing, paused, game_over
        self.menu_choice = 0
        self.settings_choice = 0
        self.frame = 0
        self.score = 0
        self.high_score = 0
        self.wave = 1
        self.lives_left = 0
        self.message = ""

    # ---------- Starting and running the game ----------

    def run(self):
        while True:
            self.handle_events()
            if self.state == "playing":
                self.update_game()
            self.draw()
            self.clock.tick(self.settings.fps)
            self.frame = self.frame + 1

    def new_game(self):
        self.settings.reset_speeds()
        self.score = 0
        self.wave = 1
        self.lives_left = self.settings.lives
        self.start_wave()
        self.state = "playing"

    def start_wave(self):
        self.bullets = []
        self.alien_bullets = []
        self.ship.center_ship()
        self.create_fleet()

    def create_fleet(self):
        self.aliens = []
        self.fleet_direction = 1
        gap_x, gap_y = 60, 50
        fleet_width = self.settings.alien_columns * gap_x
        start_x = max(10, (self.settings.screen_width - fleet_width) // 2)
        for row in range(self.settings.alien_rows):
            for col in range(self.settings.alien_columns):
                self.aliens.append(Alien(start_x + col * gap_x, 60 + row * gap_y))

    # ---------- Keyboard ----------

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type != pygame.KEYDOWN:
                continue

            if self.state == "menu":
                self.menu_keys(event.key)
            elif self.state == "settings":
                self.settings_keys(event.key)
            elif self.state == "playing":
                if event.key == pygame.K_SPACE:
                    self.fire_bullet()
                elif event.key == pygame.K_p:
                    self.state = "paused"
                elif event.key == pygame.K_ESCAPE:
                    self.state = "menu"
            elif self.state == "paused":
                if event.key == pygame.K_p:
                    self.state = "playing"
                elif event.key == pygame.K_ESCAPE:
                    self.state = "menu"
            elif self.state == "game_over":
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self.new_game()
                elif event.key == pygame.K_ESCAPE:
                    self.state = "menu"

    def menu_keys(self, key):
        if key == pygame.K_UP:
            self.menu_choice = (self.menu_choice - 1) % 3
        elif key == pygame.K_DOWN:
            self.menu_choice = (self.menu_choice + 1) % 3
        elif key in (pygame.K_RETURN, pygame.K_SPACE):
            if self.menu_choice == 0:
                self.new_game()
            elif self.menu_choice == 1:
                self.state = "settings"
            else:
                pygame.quit()
                raise SystemExit
        elif key == pygame.K_ESCAPE:
            pygame.quit()
            raise SystemExit

    def settings_keys(self, key):
        options = self.settings.options
        if key == pygame.K_UP:
            self.settings_choice = (self.settings_choice - 1) % len(options)
        elif key == pygame.K_DOWN:
            self.settings_choice = (self.settings_choice + 1) % len(options)
        elif key == pygame.K_RIGHT:
            self.settings.change_option(options[self.settings_choice], 1)
        elif key == pygame.K_LEFT:
            self.settings.change_option(options[self.settings_choice], -1)
        elif key in (pygame.K_ESCAPE, pygame.K_RETURN):
            self.state = "menu"

    # ---------- Game logic ----------

    def fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            s = self.settings
            self.bullets.append(Bullet(self.ship.rect.centerx, self.ship.rect.top,
                                       s.bullet_width, s.bullet_height,
                                       -s.bullet_speed, (255, 255, 120)))

    def update_game(self):
        self.ship.update(pygame.key.get_pressed())

        for bullet in self.bullets + self.alien_bullets:
            bullet.update()
        self.bullets = [b for b in self.bullets if b.rect.bottom > 0]
        self.alien_bullets = [b for b in self.alien_bullets
                              if b.rect.top < self.settings.screen_height]

        self.update_aliens()
        self.check_hits()

    def update_aliens(self):
        s = self.settings

        # If any alien touches a side, the whole fleet drops and turns around.
        for alien in self.aliens:
            if alien.rect.right >= s.screen_width or alien.rect.left <= 0:
                for a in self.aliens:
                    a.rect.y = a.rect.y + s.fleet_drop_speed
                self.fleet_direction = self.fleet_direction * -1
                break

        for alien in self.aliens:
            alien.x = alien.x + s.alien_speed * self.fleet_direction
            alien.rect.x = int(alien.x)

            # Aliens shoot back at random.
            if s.aliens_shoot and random.randint(1, 1000) <= s.alien_fire_chance:
                self.alien_bullets.append(Bullet(alien.rect.centerx,
                                                 alien.rect.bottom + 10, 4, 12,
                                                 s.alien_bullet_speed,
                                                 (255, 80, 80)))

        # An alien reaching the bottom counts as a hit on the ship.
        for alien in self.aliens:
            if alien.rect.bottom >= self.ship.rect.top:
                self.ship_hit(reset_fleet=True)
                return

    def check_hits(self):
        # Your bullets hitting aliens.
        for bullet in self.bullets[:]:
            for alien in self.aliens[:]:
                if bullet.rect.colliderect(alien.rect):
                    self.aliens.remove(alien)
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    self.score = self.score + self.settings.points_per_alien * self.wave
                    self.high_score = max(self.high_score, self.score)
                    break

        # Alien bullets hitting you.
        for bullet in self.alien_bullets:
            if bullet.rect.colliderect(self.ship.rect):
                self.ship_hit(reset_fleet=False)
                return

        # Whole fleet destroyed: next wave, a bit faster.
        if not self.aliens:
            self.wave = self.wave + 1
            self.settings.speed_up()
            self.start_wave()

    def ship_hit(self, reset_fleet):
        self.lives_left = self.lives_left - 1
        if self.lives_left <= 0:
            self.state = "game_over"
        elif reset_fleet:
            self.start_wave()
        else:
            # Clear the bullets and give the player a fresh start.
            self.bullets = []
            self.alien_bullets = []
            self.ship.center_ship()

    # ---------- Drawing ----------

    def draw_text(self, text, font, color, center):
        image = font.render(text, True, color)
        self.screen.blit(image, image.get_rect(center=center))

    def draw(self):
        s = self.settings
        self.screen.fill(s.bg_color)
        if s.show_stars:
            for x, y, size in self.stars:
                pygame.draw.circle(self.screen, (200, 200, 255), (x, y), size)

        middle = s.screen_width // 2
        if self.state == "menu":
            self.draw_menu(middle)
        elif self.state == "settings":
            self.draw_settings(middle)
        else:
            self.draw_play_screen()
            if self.state == "paused":
                self.draw_text("PAUSED", self.big_font, (255, 255, 255),
                               (middle, s.screen_height // 2))
                self.draw_text("Press P to keep playing", self.font,
                               (200, 200, 200), (middle, s.screen_height // 2 + 50))
            elif self.state == "game_over":
                self.draw_text("GAME OVER", self.big_font, (255, 80, 80),
                               (middle, s.screen_height // 2))
                self.draw_text("Enter: play again   Esc: menu", self.font,
                               (200, 200, 200), (middle, s.screen_height // 2 + 50))

        pygame.display.flip()

    def draw_menu(self, middle):
        self.draw_text("ALIEN INVASION", self.big_font, (120, 255, 120), (middle, 160))
        self.draw_text("Difficulty: " + self.settings.difficulty, self.small_font,
                       (180, 180, 180), (middle, 220))
        for i, item in enumerate(["Play", "Settings", "Quit"]):
            color = (255, 255, 0) if i == self.menu_choice else (255, 255, 255)
            text = "> " + item + " <" if i == self.menu_choice else item
            self.draw_text(text, self.font, color, (middle, 320 + i * 55))
        self.draw_text("High score: " + str(self.high_score), self.small_font,
                       (180, 180, 180), (middle, 540))
        self.draw_text("Arrows to choose, Enter to select", self.small_font,
                       (150, 150, 150), (middle, 580))

    def draw_settings(self, middle):
        self.draw_text("SETTINGS", self.big_font, (120, 255, 120), (middle, 50))
        for i, option in enumerate(self.settings.options):
            value = self.settings.get_value(option)
            if value is True:
                value = "On"
            elif value is False:
                value = "Off"
            selected = i == self.settings_choice
            color = (255, 255, 0) if selected else (255, 255, 255)
            y = 105 + i * 32
            label = self.small_font.render(option[0], True, color)
            self.screen.blit(label, (middle - 260, y))
            text = "< " + str(value) + " >" if selected else str(value)
            shown = self.small_font.render(text, True, color)
            self.screen.blit(shown, (middle + 120, y))
        self.draw_text("Up/Down: pick   Left/Right: change   Enter/Esc: back",
                       self.small_font, (150, 150, 150),
                       (middle, self.settings.screen_height - 25))

    def draw_play_screen(self):
        for alien in self.aliens:
            alien.draw(self.screen, self.frame)
        for bullet in self.bullets + self.alien_bullets:
            bullet.draw(self.screen)
        self.ship.draw(self.screen)

        hud = ("Score: " + str(self.score) + "    Wave: " + str(self.wave) +
               "    Lives: " + str(self.lives_left) +
               "    High: " + str(self.high_score))
        self.screen.blit(self.small_font.render(hud, True, (255, 255, 255)), (10, 10))


if __name__ == "__main__":
    game = AlienInvasion()
    game.run()
