import math
import random
import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
PLAYER_START_X = 370
PLAYER_START_Y = 380
ENEMY_START_Y = 380
ENEMY_START_Y_MAX = 150
ENEMY_START_Y_MIN = 50
ENEMY_SPEED_X = 4
ENEMY_SPEED_Y = 40
BULLET_SPEED_Y = 10
COLLUSITION_DISTANCE = 27

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
background = pygame.image.load('background.png')
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)
pygame.display.set_caption("Space Invaders")
playerImg = pygame.image.load('player.png')
player_x = PLAYER_START_X
player_y = PLAYER_START_Y
player_x_change = 0
enemyImg = []
enemyX = []
enemyY = []
enemy_X_change = []
enemy_Y_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, SCREEN_WIDTH - 64))
    enemyY.append(random.randint(ENEMY_START_Y_MIN,ENEMY_START_Y_MAX))
    enemy_X_change.append(ENEMY_SPEED_X)
    enemy_Y_change.append(ENEMY_SPEED_Y)
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = PLAYER_START_Y
bulletX_change = 0
bulletY_change = BULLET_SPEED_Y
bullet_state = "ready"
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10
over_font = pygame.font.Font('freesansbold.ttf', 64)
def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))
def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))
def player(x, y):
    screen.blit(playerImg, (x, y))
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))
def is_collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((enemyX - bulletX) ** 2 + (enemyY - bulletY) ** 2)
    return distance < COLLUSITION_DISTANCE
running = True
while running: 
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -5
            if event.key == pygame.K_RIGHT:
                player_x_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = player_x
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0
    player_x += player_x_change
    if player_x <= 0:
        player_x = 0
    elif player_x >= SCREEN_WIDTH - 64:
        player_x = SCREEN_WIDTH - 64
    for i in range(num_of_enemies):
        if enemyY[i] > 300:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemy_X_change[i]
        if enemyX[i] <= 0:
            enemy_X_change[i] = ENEMY_SPEED_X
            enemyY[i] += enemy_Y_change[i]
        elif enemyX[i] >= SCREEN_WIDTH - 64:
            enemy_X_change[i] = -ENEMY_SPEED_X
            enemyY[i] += enemy_Y_change[i]
        collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = PLAYER_START_Y
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, SCREEN_WIDTH - 64)
            enemyY[i] = random.randint(ENEMY_START_Y_MIN,ENEMY_START_Y_MAX)
        enemy(enemyX[i], enemyY[i], i)
    if bulletY <= 0:
        bulletY = PLAYER_START_Y
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    player(player_x, player_y)
    show_score(textX, textY)
    pygame.display.update()