import pygame

#inicjalizuj grę
pygame.init()

#nazwa okna i logo
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)
background = pygame.image.load('space.jpg')
#ustawienia gracza
playerImg = pygame.image.load('rocket-ship.png')
playerX = 380
playerY = 520
playerX_change = 0 #zmiana pozycji gracza
def player(x,y):
    screen.blit(playerImg,(x, y))

#ustawienia wrogów (obcych)
enemyImg = pygame.image.load('alien-64.png')
enemyX = 0
enemyY = 10
enemyX_change = 0 #zmiana pozycji wroga
enemyY_change = 20
def enemy(x,y):
    screen.blit(enemyImg,(x,y))

#ustawienia pocisku
bulletImg = pygame.image.load('bulletblue1.png')
bulletX = 0
bulletY = 522
bulletY_change = 0
bullet_state = 'ready' #can be 'ready' or 'fired', when ready, it's not drawn

def fire_bullet(x,y):
    global bullet_state
    if bullet_state == 'fired':
        screen.blit(bulletImg,(x,y))

#ustawienia okna gry
screen = pygame.display.set_mode((800,600))

#główna pętla programu
running = True

while running:
    # Kolor RGB (red, green, blue)
    screen.fill((0, 10, 0))
    #obraz tłą
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #jeśli naciśnięty klawisz
        if event.type == pygame.KEYDOWN:
            #jeśli klawisz to strzałka w lewo
            if event.key == pygame.K_LEFT:
                playerX_change = -0.2
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.2
            if event.key == pygame.K_SPACE and bullet_state == 'ready':
                bullet_state = 'fired'
                bulletX = playerX + 30
                bulletY_change = 2
        #jeśli zwolniony klawisz
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    playerX += playerX_change
    #warunki brzegowe
    if playerX <= 0:
        playerX = 0
    elif playerX > 732:
        playerX = 732
    if enemyX <= 0:
        enemyX = 0
        enemyX_change = 0.1
        enemyY += enemyY_change
    elif enemyX > 732:
        enemyX = 732
        enemyX_change = -0.1
        enemyY += enemyY_change
    if bulletY < 0:
        bullet_state = 'ready'
        bulletY = 522
    enemyX += enemyX_change
    bulletY -= bulletY_change
    player(playerX, playerY)
    enemy(enemyX,enemyY)
    fire_bullet(bulletX,bulletY)
    #odswieżenie ekranu
    pygame.display.update()
