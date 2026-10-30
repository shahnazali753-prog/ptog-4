# Sky Hopper: a simple flap-through-the-gaps game.
# Needs pygame. Install it with:  pip install pygame
#
# Controls:
#   Space / Up arrow / mouse click  flap
#   P                               pause
#   Esc                             quit

import random
import pygame


class Settings:
    """All the settings for the game live here."""

    def __init__(self):
        # Screen
        self.screen_width = 400
        self.screen_height = 600
        self.sky_color = (120, 200, 235)
        self.ground_color = (110, 180, 80)
        self.ground_height = 70
        self.fps = 60

        # Bird
        self.bird_radius = 15
        self.gravity = 0.45
        self.flap_strength = -8
        self.max_fall_speed = 10

        # Pipes
        self.pipe_width = 60
        self.pipe_gap = 160
        self.pipe_speed = 3
        self.pipe_spacing = 220
        self.pipe_color = (60, 150, 60)
        self.pipe_edge_color = (30, 90, 30)


class Bird:
    """The round little bird the player keeps in the air."""

    def __init__(self, settings):
        self.settings = settings
        self.x = settings.screen_width // 3
        self.y = settings.screen_height / 2
        self.velocity = 0

    def flap(self):
        self.velocity = self.settings.flap_strength

    def update(self):
        self.velocity = min(self.velocity + self.settings.gravity,
                            self.settings.max_fall_speed)
        self.y += self.velocity

    def rect(self):
        r = self.settings.bird_radius - 2  # a little forgiving
        return pygame.Rect(self.x - r, self.y - r, r * 2, r * 2)

    def draw(self, screen):
        r = self.settings.bird_radius
        center = (self.x, int(self.y))
        pygame.draw.circle(screen, (250, 200, 40), center, r)
        pygame.draw.circle(screen, (0, 0, 0), center, r, 2)
        # Wing flips up while rising and down while falling
        wing_y = int(self.y) + (-4 if self.velocity < 0 else 4)
        pygame.draw.ellipse(screen, (240, 240, 240), (self.x - r, wing_y - 4, 14, 8))
        # Eye and beak
        pygame.draw.circle(screen, (255, 255, 255), (self.x + 6, int(self.y) - 5), 5)
        pygame.draw.circle(screen, (0, 0, 0), (self.x + 7, int(self.y) - 5), 2)
        pygame.draw.polygon(screen, (240, 110, 40), [
            (self.x + r - 2, int(self.y) - 1),
            (self.x + r + 9, int(self.y) + 2),
            (self.x + r - 2, int(self.y) + 5),
        ])


class Pipe:
    """A pair of pipes with a gap to fly through."""

    def __init__(self, settings, x):
        self.settings = settings
        self.x = x
        top_limit = 60
        bottom_limit = settings.screen_height - settings.ground_height - 60 - settings.pipe_gap
        self.gap_top = random.randint(top_limit, bottom_limit)
        self.passed = False

    def update(self):
        self.x -= self.settings.pipe_speed

    def rects(self):
        s = self.settings
        top = pygame.Rect(self.x, 0, s.pipe_width, self.gap_top)
        bottom_y = self.gap_top + s.pipe_gap
        bottom = pygame.Rect(self.x, bottom_y, s.pipe_width,
                             s.screen_height - s.ground_height - bottom_y)
        return top, bottom

    def draw(self, screen):
        s = self.settings
        top, bottom = self.rects()
        for body in (top, bottom):
            pygame.draw.rect(screen, s.pipe_color, body)
            pygame.draw.rect(screen, s.pipe_edge_color, body, 3)
        # Lips at the open ends
        lip_top = pygame.Rect(self.x - 5, top.bottom - 20, s.pipe_width + 10, 20)
        lip_bottom = pygame.Rect(self.x - 5, bottom.top, s.pipe_width + 10, 20)
        for lip in (lip_top, lip_bottom):
            pygame.draw.rect(screen, s.pipe_color, lip)
            pygame.draw.rect(screen, s.pipe_edge_color, lip, 3)

    def off_screen(self):
        return self.x + self.settings.pipe_width < 0


class Game:
    """Runs the game: input, updates and drawing."""

    def __init__(self):
        pygame.init()
        self.settings = Settings()
        s = self.settings
        self.screen = pygame.display.set_mode((s.screen_width, s.screen_height))
        pygame.display.set_caption("Sky Hopper")
        self.clock = pygame.time.Clock()
        self.big_font = pygame.font.SysFont(None, 64)
        self.font = pygame.font.SysFont(None, 30)
        self.high_score = 0
        self.ground_offset = 0
        self.reset()

    def reset(self):
        self.bird = Bird(self.settings)
        self.pipes = []
        self.score = 0
        self.state = "ready"  # ready, playing, paused, over

    def spawn_pipe(self):
        s = self.settings
        if not self.pipes or self.pipes[-1].x < s.screen_width - s.pipe_spacing:
            self.pipes.append(Pipe(s, s.screen_width))

    def handle_flap(self):
        if self.state == "ready":
            self.state = "playing"
            self.bird.flap()
        elif self.state == "playing":
            self.bird.flap()
        elif self.state == "over":
            self.reset()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key in (pygame.K_SPACE, pygame.K_UP):
                    self.handle_flap()
                elif event.key == pygame.K_p and self.state in ("playing", "paused"):
                    self.state = "paused" if self.state == "playing" else "playing"
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_flap()
        return True

    def update(self):
        s = self.settings
        if self.state in ("ready", "playing"):
            self.ground_offset = (self.ground_offset + s.pipe_speed) % 24

        if self.state == "ready":
            # Gentle bobbing while waiting to start
            self.bird.y = s.screen_height / 2 + 6 * pygame.math.Vector2(1, 0).rotate(
                pygame.time.get_ticks() / 4).y
            return
        if self.state != "playing":
            return

        self.bird.update()
        self.spawn_pipe()
        for pipe in self.pipes:
            pipe.update()
            if not pipe.passed and pipe.x + s.pipe_width < self.bird.x:
                pipe.passed = True
                self.score += 1
        self.pipes = [p for p in self.pipes if not p.off_screen()]

        bird_rect = self.bird.rect()
        hit_pipe = any(bird_rect.colliderect(r) for p in self.pipes for r in p.rects())
        hit_ground = self.bird.y + s.bird_radius >= s.screen_height - s.ground_height
        if self.bird.y < -s.bird_radius:
            self.bird.y = -s.bird_radius  # can't fly over the pipes
        if hit_pipe or hit_ground:
            self.state = "over"
            self.high_score = max(self.high_score, self.score)

    def draw_text(self, text, font, y, color=(255, 255, 255)):
        shadow = font.render(text, True, (0, 0, 0))
        label = font.render(text, True, color)
        x = (self.settings.screen_width - label.get_width()) // 2
        self.screen.blit(shadow, (x + 2, y + 2))
        self.screen.blit(label, (x, y))

    def draw(self):
        s = self.settings
        self.screen.fill(s.sky_color)
        for pipe in self.pipes:
            pipe.draw(self.screen)

        # Ground with moving stripes
        ground_y = s.screen_height - s.ground_height
        pygame.draw.rect(self.screen, s.ground_color, (0, ground_y, s.screen_width, s.ground_height))
        pygame.draw.rect(self.screen, (220, 200, 140), (0, ground_y + 18, s.screen_width, s.ground_height))
        for x in range(-self.ground_offset, s.screen_width, 24):
            pygame.draw.line(self.screen, (90, 160, 60), (x, ground_y), (x + 12, ground_y + 18), 4)
        pygame.draw.line(self.screen, (40, 90, 30), (0, ground_y), (s.screen_width, ground_y), 3)

        self.bird.draw(self.screen)

        if self.state == "ready":
            self.draw_text("Sky Hopper", self.big_font, 120)
            self.draw_text("Space or click to flap", self.font, 400)
        else:
            self.draw_text(str(self.score), self.big_font, 40)
        if self.state == "paused":
            self.draw_text("Paused", self.big_font, 220)
        if self.state == "over":
            self.draw_text("Game Over", self.big_font, 180, (255, 90, 90))
            self.draw_text(f"Score: {self.score}   Best: {self.high_score}", self.font, 250)
            self.draw_text("Space or click to play again", self.font, 290)

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.check_events()
            self.update()
            self.draw()
            self.clock.tick(self.settings.fps)
        pygame.quit()


if __name__ == "__main__":
    Game().run()
