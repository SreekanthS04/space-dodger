import pygame
import sys
import os
import random

# Initialize
pygame.init()
pygame.mixer.init()

# Screen
WIDTH, HEIGHT = 480, 640
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dodger")
clock = pygame.time.Clock()
FPS = 60

# Paths
ASSETS_PATH = os.path.join(os.path.dirname(__file__), "assets")

# Load images
player_img = pygame.image.load(os.path.join(ASSETS_PATH, "spaceship.png")).convert_alpha()
player_img = pygame.transform.scale(player_img, (64, 64))
asteroid_img = pygame.image.load(os.path.join(ASSETS_PATH, "asteroid.png")).convert_alpha()
asteroid_img = pygame.transform.scale(asteroid_img, (50, 50))

# Load sounds
pygame.mixer.music.load(os.path.join(ASSETS_PATH, "bg_music.ogg"))
crash_sound = pygame.mixer.Sound(os.path.join(ASSETS_PATH, "crash.ogg"))
pygame.mixer.music.play(-1)  # play background music on loop

# Player setup
player_rect = player_img.get_rect()
player_rect.centerx = WIDTH // 2
player_rect.bottom = HEIGHT - 20
player_speed = 5

# Asteroid data
asteroids = []
spawn_interval = 1000
asteroid_speed = 5
ASTEROID_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(ASTEROID_EVENT, spawn_interval)

# Game state
score = 0
running = True
game_over = False
font = pygame.font.SysFont("Arial", 32, bold=True)

# Starfield setup
NUM_STARS = 100
stars = []

for _ in range(NUM_STARS):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    speed = random.uniform(0.5, 1.5)  # some stars move faster
    stars.append({'x': x, 'y': y, 'speed': speed})


def draw_restart_button():
    btn_font = pygame.font.SysFont("Arial", 28)
    btn_text = btn_font.render("Restart", True, (0, 0, 0))
    btn_rect = pygame.Rect(WIDTH // 2 - 60, HEIGHT // 2 + 50, 120, 40)
    pygame.draw.rect(screen, (255, 255, 255), btn_rect)
    pygame.draw.rect(screen, (0, 0, 0), btn_rect, 2)
    screen.blit(btn_text, (btn_rect.x + 25, btn_rect.y + 8))
    return btn_rect

restart_button = None

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_over and event.type == pygame.MOUSEBUTTONDOWN:
            if restart_button and restart_button.collidepoint(event.pos):
                score = 0
                asteroid_speed = 5
                spawn_interval = 1000
                pygame.time.set_timer(ASTEROID_EVENT, spawn_interval)
                asteroids.clear()
                player_rect.centerx = WIDTH // 2
                player_rect.bottom = HEIGHT - 20
                pygame.mixer.music.play(-1)  # Restart music
                game_over = False

        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                score = 0
                asteroid_speed = 5
                spawn_interval = 1000
                pygame.time.set_timer(ASTEROID_EVENT, spawn_interval)
                asteroids.clear()
                player_rect.centerx = WIDTH // 2
                player_rect.bottom = HEIGHT - 20
                pygame.mixer.music.play(-1)  # Restart music
                game_over = False

        if event.type == ASTEROID_EVENT and not game_over:
            x = random.randint(0, WIDTH - 50)
            rect = asteroid_img.get_rect(topleft=(x, -50))
            asteroids.append(rect)

    keys = pygame.key.get_pressed()
    if not game_over:
        if keys[pygame.K_LEFT] and player_rect.left > 0:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT] and player_rect.right < WIDTH:
            player_rect.x += player_speed

        for rect in asteroids[:]:
            rect.y += asteroid_speed
            if player_rect.colliderect(rect):
                if not game_over:
                    crash_sound.play()
                    pygame.mixer.music.stop()  # Stop music on crash
                game_over = True
            elif rect.top > HEIGHT:
                asteroids.remove(rect)
                score += 1
                asteroid_speed = 5 + score // 5
                new_spawn = max(300, 1000 - score * 20)
                if new_spawn != spawn_interval:
                    spawn_interval = new_spawn
                    pygame.time.set_timer(ASTEROID_EVENT, spawn_interval)

    # Drawing
    # Animate background stars
    screen.fill((0, 0, 0))
    for star in stars:
        star['y'] += star['speed']
        if star['y'] > HEIGHT:
            star['y'] = 0
            star['x'] = random.randint(0, WIDTH)
        pygame.draw.circle(screen, (255, 255, 255), (int(star['x']), int(star['y'])), 2)

    screen.blit(player_img, player_rect)

    for rect in asteroids:
        screen.blit(asteroid_img, rect)

    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    if game_over:
        game_text = font.render("Game Over", True, (255, 0, 0))
        screen.blit(game_text, (WIDTH // 2 - game_text.get_width() // 2, HEIGHT // 2))
        restart_button = draw_restart_button()
    else:
        restart_button = None

    pygame.display.flip()

# Cleanup
pygame.mixer.music.stop()
pygame.quit()
sys.exit()
