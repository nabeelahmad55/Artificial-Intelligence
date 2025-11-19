# car_racing_game.py
import pygame
import random
import os
import sys

# ------------------------------
# Configuration
# ------------------------------
WIDTH, HEIGHT = 480, 700
FPS = 60

LANE_COUNT = 3
LANE_WIDTH = WIDTH // LANE_COUNT

PLAYER_WIDTH, PLAYER_HEIGHT = 40, 70
ENEMY_WIDTH, ENEMY_HEIGHT = 40, 70

BG_COLOR = (30, 30, 30)
ROAD_COLOR = (50, 50, 50)
LINE_COLOR = (200, 200, 200)
PLAYER_COLOR = (50, 200, 50)
ENEMY_COLOR = (200, 50, 50)
TEXT_COLOR = (240, 240, 240)
UI_BG = (20, 20, 20)

SPAWN_EVENT = pygame.USEREVENT + 1

HIGH_SCORE_FILE = "highscore.txt"

# ------------------------------
# Utilities
# ------------------------------
def load_highscore():
    try:
        if os.path.exists(HIGH_SCORE_FILE):
            with open(HIGH_SCORE_FILE, "r") as f:
                return int(f.read().strip() or 0)
    except Exception:
        pass
    return 0

def save_highscore(score):
    try:
        with open(HIGH_SCORE_FILE, "w") as f:
            f.write(str(score))
    except Exception:
        pass

def clamp(v, a, b):
    return max(a, min(b, v))


# ------------------------------
# Game Classes
# ------------------------------
class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(0, 0, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = 6
        self.lane = self.get_lane_from_x(self.rect.centerx)

    def get_lane_from_x(self, x):
        lane = x // LANE_WIDTH
        return int(clamp(lane, 0, LANE_COUNT-1))

    def update(self, keys):
        # Smooth movement with arrow keys or WASD
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed

        # Keep inside road bounds
        self.rect.left = clamp(self.rect.left, 0 + 10, WIDTH - self.rect.width - 10)
        self.rect.top = clamp(self.rect.top, HEIGHT//3, HEIGHT - self.rect.height - 10)
        self.lane = self.get_lane_from_x(self.rect.centerx)

    def draw(self, surface):
        pygame.draw.rect(surface, PLAYER_COLOR, self.rect, border_radius=6)
        # simple windows
        w = self.rect.width
        h = self.rect.height
        glass = pygame.Rect(self.rect.x + w*0.15, self.rect.y + h*0.08, w*0.7, h*0.28)
        pygame.draw.rect(surface, (180, 220, 255), glass, border_radius=4)

class Enemy:
    def __init__(self, x, y, speed):
        self.rect = pygame.Rect(0, 0, ENEMY_WIDTH, ENEMY_HEIGHT)
        self.rect.centerx = x
        self.rect.top = y
        self.speed = speed

    def update(self, dt):
        self.rect.y += int(self.speed * dt)

    def draw(self, surface):
        pygame.draw.rect(surface, ENEMY_COLOR, self.rect, border_radius=6)
        # small details
        w = self.rect.width
        h = self.rect.height
        pygame.draw.rect(surface, (40, 40, 40), (self.rect.x + 6, self.rect.y + h - 12, w - 12, 8), border_radius=3)


# ------------------------------
# Main Game
# ------------------------------
def draw_road(surface):
    # background area
    surface.fill(BG_COLOR)
    # road rectangle centered
    pygame.draw.rect(surface, ROAD_COLOR, (0, HEIGHT//3 - 20, WIDTH, HEIGHT - (HEIGHT//3 - 20)))
    # lane dividers
    for i in range(1, LANE_COUNT):
        x = i * LANE_WIDTH
        # dashed line
        dash_h = 20
        gap = 20
        y = HEIGHT//3
        while y < HEIGHT - 20:
            pygame.draw.rect(surface, LINE_COLOR, (x-2, y, 4, dash_h))
            y += dash_h + gap

def draw_ui(surface, font, score, high_score):
    # top panel
    panel_h = HEIGHT//10
    panel_rect = pygame.Rect(0, 0, WIDTH, panel_h)
    pygame.draw.rect(surface, UI_BG, panel_rect)
    # Score text
    score_surf = font.render(f"Score: {score}", True, TEXT_COLOR)
    hs_surf = font.render(f"High: {high_score}", True, TEXT_COLOR)
    surface.blit(score_surf, (12, 8))
    surface.blit(hs_surf, (WIDTH - hs_surf.get_width() - 12, 8))

def create_enemy_for_lane(lane_idx, speed):
    x_center = lane_idx * LANE_WIDTH + LANE_WIDTH // 2
    x_center = int(x_center)
    return Enemy(x_center, -ENEMY_HEIGHT - random.randint(10, 300), speed)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Car Racing Game by Nabeel")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("Arial", 20)
    big_font = pygame.font.SysFont("Arial", 42, bold=True)

    # Player start in middle lane, bottom
    start_x = (LANE_COUNT // 2) * LANE_WIDTH + LANE_WIDTH // 2
    player = Player(start_x, HEIGHT - 30)
    enemies = []

    running = True
    paused = False
    game_over = False

    score = 0
    distance = 0.0
    high_score = load_highscore()
    base_enemy_speed = 0.18  # pixels per ms
    enemy_spawn_interval = 1200  # ms
    min_spawn_interval = 450
    last_spawn = pygame.time.get_ticks()
    difficulty_timer = pygame.time.get_ticks()

    # Spawn timer event
    pygame.time.set_timer(SPAWN_EVENT, enemy_spawn_interval)

    while running:
        dt_ms = clock.tick(FPS)
        dt = dt_ms  # using milliseconds scaling for enemy speed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == SPAWN_EVENT and not paused and not game_over:
                # spawn enemy at random lane, maybe multiple
                lanes = list(range(LANE_COUNT))
                random.shuffle(lanes)
                # spawn 1 or occasionally 2 cars
                spawn_count = 1 if random.random() < 0.9 else 2
                for i in range(spawn_count):
                    lane = lanes[i % LANE_COUNT]
                    speed = base_enemy_speed + random.random() * 0.12
                    enemies.append(create_enemy_for_lane(lane, speed))
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                if event.key == pygame.K_r and game_over:
                    # restart
                    enemies.clear()
                    score = 0
                    distance = 0.0
                    game_over = False
                    player = Player(start_x, HEIGHT - 30)
                    base_enemy_speed = 0.18
                    enemy_spawn_interval = 1200
                    pygame.time.set_timer(SPAWN_EVENT, enemy_spawn_interval)
                if event.key == pygame.K_ESCAPE:
                    running = False

        keys = pygame.key.get_pressed()
        if not paused and not game_over:
            player.update(keys)

            # update enemies
            for e in enemies:
                e.update(dt)
            # remove off-screen enemies
            enemies = [e for e in enemies if e.rect.top < HEIGHT + 50]

            # collision detection
            for e in enemies:
                if e.rect.colliderect(player.rect):
                    game_over = True
                    paused = False
                    if score > high_score:
                        high_score = score
                        save_highscore(high_score)

            # increase score with distance/time
            distance += (dt * (1 + base_enemy_speed)) * 0.02
            new_score = int(distance // 10)
            if new_score > score:
                score = new_score

            # difficulty scaling every 8 seconds
            if pygame.time.get_ticks() - difficulty_timer > 8000:
                difficulty_timer = pygame.time.get_ticks()
                base_enemy_speed += 0.02
                # spawn faster but clamp
                enemy_spawn_interval = max(min_spawn_interval, int(enemy_spawn_interval * 0.92))
                pygame.time.set_timer(SPAWN_EVENT, enemy_spawn_interval)

        # Drawing
        draw_road(screen)
        for e in enemies:
            e.draw(screen)
        player.draw(screen)
        draw_ui(screen, font, score, high_score)

        # instructions bottom
        hint = font.render("Arrows/WASD to move • P to pause • R to restart after crash • ESC to quit", True, (180,180,180))
        screen.blit(hint, (12, HEIGHT - 28))

        if paused:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0,0,0,140))
            screen.blit(overlay, (0,0))
            t = big_font.render("PAUSED", True, (255,255,255))
            screen.blit(t, ((WIDTH - t.get_width())//2, HEIGHT//2 - 30))
        if game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0,0,0,180))
            screen.blit(overlay, (0,0))
            t = big_font.render("CRASH!", True, (255,100,100))
            screen.blit(t, ((WIDTH - t.get_width())//2, HEIGHT//2 - 70))
            s = font.render(f"Score: {score}", True, (255,255,255))
            screen.blit(s, ((WIDTH - s.get_width())//2, HEIGHT//2 - 10))
            r = font.render("Press R to restart or ESC to exit", True, (220,220,220))
            screen.blit(r, ((WIDTH - r.get_width())//2, HEIGHT//2 + 20))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
