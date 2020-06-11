import pygame

from math import sqrt

# inicjalizuj grę
pygame.init()

# nazwa okna i logo
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)
background = pygame.image.load('space.jpg')

# wyświetlacz punktów
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)

#koniec gry
font2 = pygame.font.Font('freesansbold.ttf', 64)
game_over_fail = font2.render('G A M E    O V E R  :(', True, (237, 12, 31))
game_over_victory = font2.render('G A M E    O V E R  :)', True, (12, 237, 218))

#efekty dźwiękowe i muzyka
background_music = pygame.mixer.music.load('alien-invasion_creative-commons.ogg')
#background_music = pygame.mixer.music.load('golden-ocean_creative-commons.ogg')
fire_sound = pygame.mixer.Sound('laser.wav')
pygame.mixer.music.play(-1)

def show_score():
    score_text = font.render('Score: '+str(score), True, (111, 21, 171))
    screen.blit(score_text, (0, 0))

# ustawienia obiektów gry
class Player:
    def __init__(self):
        self.x = 380
        self.y = 520
        self.x_change = 0
        self.img = pygame.image.load('rocket-ship.png')

    def draw(self):
        screen.blit(self.img, (self.x, self.y))

    def move(self):
        self.x += self.x_change


class Enemy:
    def __init__(self, x):
        self.x = x
        self.y = 20
        self.x_change = 2
        self.y_change = 20
        self.img = pygame.image.load('alien-64.png')
        self.hit = False

    def draw(self):
        if not self.hit:
            screen.blit(self.img, (self.x, self.y))

    def move_x(self):
        self.x += self.x_change

    def move_y(self):
        self.y += self.y_change


class Bullet:
    def __init__(self):
        self.x = 0
        self.y = 522
        self.y_change = 0
        self.state = 'ready'  # can be 'ready' or 'fired', when ready, it's not drawn
        self.img = pygame.image.load('bulletblue1.png')

    def fire(self,x,y):
        self.state = 'fired'
        self.y_change = -5
        self.x = x
        self.y = y

    def draw(self):
        if self.state == 'fired':
            screen.blit(self.img, (self.x, self.y))

    def move(self):
        self.y += self.y_change

    def is_collision(self, enemy):
        distance = sqrt((enemy.x - self.x) ** 2 + (enemy.y - self.y) ** 2)
        if distance < 26:
            return True
        else:
            return False



# ustawienia okna gry
screen = pygame.display.set_mode((800, 600))

#ustawienia początkowe obiektów gry
player = Player()
enemies = [Enemy(x) for x in range(20, 721, 100)]
bullet = Bullet()
enemies_dead = 0
# główna pętla programu
running = True

while running:
    # Kolor RGB (red, green, blue)
    screen.fill((0, 10, 0))
    # obraz tła
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # jeśli naciśnięty klawisz
        if event.type == pygame.KEYDOWN:
            # jeśli klawisz to strzałka w lewo
            if event.key == pygame.K_LEFT:
                player.x_change = -2
            if event.key == pygame.K_RIGHT:
                player.x_change = 2
            if event.key == pygame.K_SPACE and bullet.state == 'ready':
                fire_sound.play()
                bullet.fire(player.x + 30, 522)
        # jeśli zwolniony klawisz
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.x_change = 0
    player.move()
    # warunki brzegowe
    if player.x <= 0:
        player.x = 0
    elif player.x > 732:
        player.x = 732
    for enemy in enemies:
        if not enemy.hit:
            if enemy.x <= 0:
                enemy.x = 0
                enemy.x_change = 2
                enemy.move_y()
            elif enemy.x > 732:
                enemy.x = 732
                enemy.x_change = -2
                enemy.move_y()
        # jeśli pocisk wyleciał za ekran
            if bullet.y < 0:
                bullet.state = 'ready'
                bullet.y = 522
                bullet.y_change = 0
            # jeśli pocisk uderzył w ufoka
            elif bullet.is_collision(enemy):
                bullet.state = 'ready'
                bullet.y = 522
                enemy.hit = True
                score += 1
            if enemy.y >= 490:
                screen.blit(game_over_fail,(100, 100))
                running = False
            enemy.move_x()
            enemy.draw()
    if score == len(enemies):
        screen.blit(game_over_victory, (100, 100))
    bullet.move()
    player.draw()
    bullet.draw()
    show_score()
    # odswieżenie ekranu
    pygame.display.update()
print(len(enemies))
