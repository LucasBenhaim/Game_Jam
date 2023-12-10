import pygame
import os

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600

# Colors
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)
WHITE = (255, 255, 255)

# Set up the Pong game
def setup_pong():
    global left_paddle, right_paddle, ball, score_1, score_2

    # Create Pygame screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("PONGO")

    # Paddle dimensions
    PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100

    # Paddle speed
    PADDLE_SPEED = 10

    # Create paddles
    left_paddle = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

    # Create ball
    ball = pygame.Rect(WIDTH // 2 - 15, HEIGHT // 2 - 15, 30, 30)
    ball_speed = [5, 5]

    # Scores
    score_1, score_2 = 0, 0

    # Font for scores
    font = pygame.font.Font(None, 36)

    gameloop_pong(screen, left_paddle, right_paddle, ball, score_1, score_2, PADDLE_SPEED, ball_speed, font)

# Pong game loop
def gameloop_pong(screen, left_paddle, right_paddle, ball, score_1, score_2, PADDLE_SPEED, ball_speed, font):
    clock = pygame.time.Clock()

    # Main game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                os._exit(0)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_z] and left_paddle.top > 0:
            left_paddle.y -= PADDLE_SPEED
        if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
            left_paddle.y += PADDLE_SPEED

        if keys[pygame.K_UP] and right_paddle.top > 0:
            right_paddle.y -= PADDLE_SPEED
        if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
            right_paddle.y += PADDLE_SPEED

        # Ball movement
        ball.x += ball_speed[0]
        ball.y += ball_speed[1]

        # Ball collision with paddles
        if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
            ball_speed[0] = -ball_speed[0]

        # Ball collision with top and bottom walls
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed[1] = -ball_speed[1]

        # Score update
        if ball.left <= 0:
            score_2 += 1
            reset_ball()
        elif ball.right >= WIDTH:
            score_1 += 1
            reset_ball()

        # Draw everything on the screen
        screen.fill(BLACK)
        pygame.draw.rect(screen, ORANGE, left_paddle)
        pygame.draw.rect(screen, ORANGE, right_paddle)
        pygame.draw.ellipse(screen, ORANGE, ball)

        # Display scores
        score_text = font.render(f"{score_1} - {score_2}", True, ORANGE)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))

        pygame.display.flip()
        clock.tick(30)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            return

def reset_ball():
    ball.center = (WIDTH // 2, HEIGHT // 2)