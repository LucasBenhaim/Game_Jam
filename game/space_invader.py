import pygame
import random
import math
from pygame import mixer

# initializing pygame
pygame.init()

# creating screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# caption and icon
pygame.display.set_caption("Welcome to Space Invaders")

# Score
score_val = 0
scoreX = 5
scoreY = 5
font = pygame.font.Font('freesansbold.ttf', 20)

# Game Over
game_over_font = pygame.font.Font('freesansbold.ttf', 64)

# Restart/Quit
restart_quit_font = pygame.font.Font('freesansbold.ttf', 32)
restart_quit_text = restart_quit_font.render("Press R to Restart or Q to Quit", True, (255, 255, 255))

restart_quit_X = 150
restart_quit_Y = 350

restart_quit_active = False

def show_score(x, y):
    score = font.render("Points: " + str(score_val), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over():
    game_over_text = game_over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game_over_text, (190, 250))

    screen.blit(restart_quit_text, (restart_quit_X, restart_quit_Y))

def restart_game():
    global player_X, player_Y, invader_X, invader_Y, invader_Xchange, invader_Ychange, restart_quit_active

    player_X = 370
    player_Y = 523

    for i in range(no_of_invaders):
        invader_X[i] = random.randint(64, 737)
        invader_Y[i] = random.randint(30, 180)
        invader_Xchange[i] = 1.2
        invader_Ychange[i] = 50

    score_val = 0
    restart_quit_active = False

# Background Sound
mixer.music.load('game/data/space_invader/background.wav')
mixer.music.play(-1)

# player
playerImage = pygame.image.load('game/data/space_invader/spaceship.png')
player_X = 370
player_Y = 523
player_Xchange = 0

# Invader
invaderImage = []
invader_X = []
invader_Y = []
invader_Xchange = []
invader_Ychange = []
no_of_invaders = 8

for num in range(no_of_invaders):
    invaderImage.append(pygame.image.load('game/data/space_invader/alien.png'))
    invader_X.append(random.randint(64, 737))
    invader_Y.append(random.randint(30, 180))
    invader_Xchange.append(0.6)
    invader_Ychange.append(50)

# Bullet
# rest - bullet is not moving
# fire - bullet is moving
bulletImage = pygame.image.load('game/data/space_invader/bullet.png')
bullet_X = 0
bullet_Y = 500
bullet_Xchange = 0
bullet_Ychange = 3
bullet_state = "rest"

# Collision Concept
def isCollision(x1, x2, y1, y2):
    distance = math.sqrt((math.pow(x1 - x2, 2)) + (math.pow(y1 - y2, 2)))
    return distance <= 50

def player(x, y):
    screen.blit(playerImage, (x - 16, y + 10))

def invader(x, y, i):
    screen.blit(invaderImage[i], (x, y))

def bullet(x, y):
    global bullet_state
    screen.blit(bulletImage, (x, y))
    bullet_state = "fire"

# game loop
def gameloop_space():
    global player_X, player_Xchange, bullet_Y, bullet_state, bullet_X, score_val, restart_quit_active

    bullet_state = "rest"
    bullet_X = 0
    score_val = 0
    restart_quit_active = False

    running = True
    while running:
        # RGB
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_Xchange = -1
                elif event.key == pygame.K_RIGHT:
                    player_Xchange = 1
                elif event.key == pygame.K_SPACE:
                    if bullet_state == "rest":
                        bullet_X = player_X
                        bullet(bullet_X, bullet_Y)
                        bullet_sound = mixer.Sound('game/data/space_invader/bullet.wav')
                        bullet_sound.play()
                elif event.key == pygame.K_q:
                    if restart_quit_active:
                        running = False
                elif event.key == pygame.K_r:
                    if restart_quit_active:
                        restart_game()
            elif event.type == pygame.KEYUP:
                player_Xchange = 0


        # adding the change in the player position
        player_X += player_Xchange
        for i in range(no_of_invaders):
            invader_X[i] += invader_Xchange[i]

        # bullet movement
        if bullet_Y <= 0:
            bullet_Y = 600
            bullet_state = "rest"
        if bullet_state == "fire":
            bullet(bullet_X, bullet_Y)
            bullet_Y -= bullet_Ychange

        # movement of the invader
        for i in range(no_of_invaders):
            if invader_Y[i] >= 450:
                if abs(player_X - invader_X[i]) < 80:
                    for j in range(no_of_invaders):
                        invader_Y[j] = 2000
                        explosion_sound = mixer.Sound('game/data/space_invader/explosion.wav')
                        explosion_sound.play()
                    game_over()
                    restart_quit_active = True
                    break

            if invader_X[i] >= 735 or invader_X[i] <= 0:
                invader_Xchange[i] *= -1
                invader_Y[i] += invader_Ychange[i]

            # Collision
            collision = isCollision(bullet_X, invader_X[i], bullet_Y, invader_Y[i])
            if collision:
                score_val += 1
                bullet_Y = 600
                bullet_state = "rest"
                invader_X[i] = random.randint(64, 736)
                invader_Y[i] = random.randint(30, 200)
                invader_Xchange[i] *= -1

            invader(invader_X[i], invader_Y[i], i)

        # restricting the spaceship so that
        # it doesn't go out of screen
        if player_X <= 16:
            player_X = 16
        elif player_X >= 750:
            player_X = 750

        player(player_X, player_Y)
        show_score(scoreX, scoreY)

        if restart_quit_active:
            screen.blit(restart_quit_text, (restart_quit_X, restart_quit_Y))

        pygame.display.update()

# # Run the game
# gameloop_space()
# pygame.quit()
