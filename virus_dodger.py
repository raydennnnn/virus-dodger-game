import pygame
import random

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🦠 Virus Dodger")

# Fonts & Clock
font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 64)
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
RED = (220, 20, 60)
BLUE = (30, 144, 255)
BLACK = (0, 0, 0)

# Player setup
player_size = 50
player_x = WIDTH // 2
player_y = HEIGHT - player_size - 20
player_speed = 8

# Virus setup
virus_size = 20  # Smaller virus
viruses = []
virus_speed = 2
spawn_rate = 30

# Game state
score = 0
lives = 3
frame_count = 0
running = True
game_over = False

def draw_player(x, y):
    pygame.draw.rect(screen, BLUE, (x, y, player_size, player_size))

def draw_virus(x, y):
    pygame.draw.circle(screen, RED, (x + virus_size // 2, y + virus_size // 2), virus_size // 2)

def reset_game():
    global viruses, score, lives, virus_speed, spawn_rate, player_x, frame_count, game_over
    viruses = []
    score = 0
    lives = 3
    virus_speed = 5
    spawn_rate = 30
    player_x = WIDTH // 2
    frame_count = 0
    game_over = False

def circle_rect_collision(cx, cy, radius, rx, ry, rw, rh):
    # Find the closest point to the circle within the rectangle
    closest_x = max(rx, min(cx, rx + rw))
    closest_y = max(ry, min(cy, ry + rh))
    # Calculate the distance between the circle's center and this closest point
    distance_x = cx - closest_x
    distance_y = cy - closest_y
    # If the distance is less than the circle's radius, there's a collision
    return (distance_x ** 2 + distance_y ** 2) < (radius ** 2)

# Main Game Loop
while running:
    screen.fill(WHITE)
    frame_count += 1

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                elif event.key == pygame.K_ESCAPE:
                    running = False

    keys = pygame.key.get_pressed()

    try:
        if not game_over:
            # Move player
            if keys[pygame.K_LEFT] and player_x > 0:
                player_x -= player_speed
            if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
                player_x += player_speed

            # Spawn viruses
            if frame_count % spawn_rate == 0:
                x = random.randint(0, WIDTH - virus_size)
                viruses.append([x, -virus_size])

            # Move viruses
            for v in viruses:
                v[1] += virus_speed

            # Collision detection (circle-rectangle)
            new_viruses = []
            for v in viruses:
                vx, vy = v
                cx = vx + virus_size // 2
                cy = vy + virus_size // 2
                if circle_rect_collision(cx, cy, virus_size // 2, player_x, player_y, player_size, player_size):
                    lives -= 1
                    continue
                if vy < HEIGHT:
                    new_viruses.append(v)
            viruses = new_viruses

            # Increase difficulty
            if frame_count % 300 == 0:
                virus_speed += 1
                if virus_speed > 20:
                    virus_speed = 20
                if spawn_rate > 10:
                    spawn_rate -= 2

            # Draw everything
            draw_player(player_x, player_y)
            for v in viruses:
                draw_virus(v[0], v[1])

            # UI: Score & Lives
            if frame_count % 6 == 0:
                score += 1
            screen.blit(font.render(f"Score: {score}", True, BLACK), (10, 10))
            screen.blit(font.render(f"Lives: {lives}", True, BLACK), (10, 40))

            if lives <= 0:
                game_over = True

        else:
            # Game Over Screen
            screen.blit(big_font.render("Game Over", True, RED), (WIDTH//2 - 150, HEIGHT//2 - 80))
            screen.blit(font.render(f"Final Score: {score}", True, BLACK), (WIDTH//2 - 90, HEIGHT//2 - 30))
            screen.blit(font.render("Press R to Retry or ESC to Quit", True, BLACK), (WIDTH//2 - 180, HEIGHT//2 + 20))

    except Exception as e:
        print("Unexpected error:", e)
        running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
