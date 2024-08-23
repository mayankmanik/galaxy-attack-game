import math
import random
import pygame


#  initialise pygame
pygame.init()

#  create screen
screen = pygame.display.set_mode((800, 600))

#  title icon
pygame.display.set_caption("Galaxy Attack")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemy = 5

for i in range(num_of_enemy):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 730))
    enemyY.append(random.randint(30, 130))
    enemyX_change.append(0.3)
    enemyY_change.append(30)

# bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 0.8
bullet_state = "ready"  # ready state : we cant see bullet. fire state : bullet is moving

# score
score = 0
font = pygame.font.Font('freesansbold.ttf', 28)
textX = 10
textY = 10

over_text = pygame.font.Font('freesansbold.ttf', 60)

def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x+16, y+10))


def is_Collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX-bulletX, 2) +
                         math.pow(enemyY-bulletY, 2))
    if(distance < 27):
        return True
    else:
        return False

def showScore(x, y):
    score_val = font.render("Score : " + str(score), True, (255, 0, 0))
    screen.blit(score_val, (x, y))

def gameOver():
    over_font = over_text.render("GAME OVER", True, (255, 0, 0))
    screen.blit(over_font, (220,250))



#  game loop
running = True
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.4
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.4
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                fire_bullet(bulletX+100, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # setting player boundary
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    playerX += playerX_change

    # enemy movement
    for i in range(num_of_enemy):
        if enemyY[i] > 440:
            for j in range(num_of_enemy):
                enemyY[j] = 1000
            gameOver()
            break
        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX[i] = 0
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX[i] = 736
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]

        # collision
        collision = is_Collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if(collision):
            bulletY = 480
            bullet_state = "ready"
            score += 1
            enemyX[i] = random.randint(0, 730)
            enemyY[i] = random.randint(30, 130)

        enemy(enemyX[i], enemyY[i], i)

    showScore(textX, textY)

    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)

    # update screen
    pygame.display.update()
