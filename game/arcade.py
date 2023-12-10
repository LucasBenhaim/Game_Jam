##
## EPITECH PROJECT, 2023
## Jam
## File description:
## main
##

import pygame
import sys
import os
from snake import gameLoop_snake
from space_invader import gameloop_space
from pong import gameloop_pong

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
PLAYER_SIZE = 50
ARCADE_SIZE = 50
PLAYER_SPEED = 5
PLAY_TEXT_SIZE = 20
SCALE_FACTOR = 3
ANIMATION_ROWS = 4  # Number of rows in the player_animations.png
ANIMATION_COLUMNS = 4  # Number of columns in each row

# Colors
WHITE = (255, 255, 255)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interactive Map")

# Load player, arcade borne, and floor images (replace with your own assets)
player_image = pygame.image.load(os.path.join("game/data/assets", "player_animations.png"))
player_image = pygame.transform.scale(player_image, (ANIMATION_COLUMNS * PLAYER_SIZE, ANIMATION_ROWS * PLAYER_SIZE))

# Adjust the player image size
PLAYER_WIDTH, PLAYER_HEIGHT = PLAYER_SIZE, PLAYER_SIZE

# Cut the player image into individual frames
player_frames = [[player_image.subsurface(pygame.Rect(j * PLAYER_WIDTH, i * PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT))
                  for j in range(ANIMATION_COLUMNS)] for i in range(ANIMATION_ROWS)]

arcade_borne_image = pygame.image.load(os.path.join("game/data/assets", "arcade.png"))
arcade_borne_image = pygame.transform.scale(arcade_borne_image, (ARCADE_SIZE * 2, ARCADE_SIZE * 2))

floor_image_path = os.path.join("game/data/assets", "floor.png")
floor_image = pygame.image.load(floor_image_path)
floor_image = pygame.transform.scale(floor_image, (WIDTH // SCALE_FACTOR, HEIGHT // SCALE_FACTOR))

# Set initial player position and animation index
player_pos = [WIDTH // 2 - PLAYER_SIZE // 2, HEIGHT // 2 - PLAYER_SIZE // 2]
current_animation = 1  # Default to the down animation

# Create arcade borne positions and associated games
arcade_borne_info = [
    {"position": (100, 100), "game": "Pong", "function": gameloop_pong},
    {"position": (350, 100), "game": "Snake", "function": gameLoop_snake},
    {"position": (600, 100), "game": "Space Invader", "function": gameloop_space},
]

# Font setup
font = pygame.font.Font(None, PLAY_TEXT_SIZE)

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Get key states
    keys = pygame.key.get_pressed()

    # Update player position and animation based on key input
    if keys[pygame.K_z] and player_pos[1] > 0:
        player_pos[1] -= PLAYER_SPEED
        current_animation = 3  # Upward animation
    if keys[pygame.K_s] and player_pos[1] < HEIGHT - PLAYER_SIZE:
        player_pos[1] += PLAYER_SPEED
        current_animation = 0  # Downward animation
    if keys[pygame.K_q] and player_pos[0] > 0:
        player_pos[0] -= PLAYER_SPEED
        current_animation = 2  # Leftward animation
    if keys[pygame.K_d] and player_pos[0] < WIDTH - PLAYER_SIZE:
        player_pos[0] += PLAYER_SPEED
        current_animation = 1  # Rightward animation

    # Draw everything on the screen
    for i in range(6):
        for j in range(6):
            screen.blit(floor_image, (i * WIDTH // 3, j * HEIGHT // 3))  # Draw the floor image multiple times

    # Draw arcade borne
    for arcade_info in arcade_borne_info:
        arcade_pos = arcade_info["position"]
        screen.blit(arcade_borne_image, arcade_pos)

        # Display the name of the game permanently above each arcade
        game_name = arcade_info["game"]
        play_text = font.render(game_name, True, WHITE)
        play_text_rect = play_text.get_rect(center=(arcade_pos[0] + ARCADE_SIZE, arcade_pos[1] - 20))
        screen.blit(play_text, play_text_rect)

    # Draw player animation
    screen.blit(player_frames[current_animation][0], player_pos)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            # Check if the player is near an arcade borne
            for arcade_info in arcade_borne_info:
                arcade_pos = arcade_info["position"]
                distance = pygame.math.Vector2(arcade_pos[0] - player_pos[0], arcade_pos[1] - player_pos[1]).length()
                if distance < PLAYER_SIZE + ARCADE_SIZE:
                    arcade_info["function"]()

    pygame.display.flip()

    # Control the frame rate
    pygame.time.Clock().tick(30)
