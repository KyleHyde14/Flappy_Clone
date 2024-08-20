import pygame
from pygame.locals import *
import random

pygame.init()

# Game Variables setup
clock = pygame.time.Clock()
fps = 60
WIDTH, HEIGHT = 650, 750
background = pygame.image.load('images/background.png')
ground = pygame.image.load('images/ground.png')
ground_x = 0
scrolling = 4
gravity = 1
bird_y = int(HEIGHT / 2.5)
time_between_pipes = 1500 # MiliS
gap = 100
WHITE = (255, 255, 255)
points = 0
flag = False


def restart():
    global game_over, flying, down, bird_y, flappy, points
    bird_y = int(HEIGHT/2.5)
    flappy = Bird(130, bird_y)
    bird_group.empty()
    pipe_group.empty()
    bird_group.add(flappy)
    flying = False
    game_over = False
    down = False
    points = 0

def show_text(text, x, y, color):
    font = pygame.font.SysFont('Bahnschrift', 30)
    screen.blit(font.render(text, True, color), (x, y))
    pygame.display.update()



class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.arr = [pygame.image.load('images/bird1.png'), 
                    pygame.image.load('images/bird2.png'),
                    pygame.image.load('images/bird3.png')]
        self.index = 0
        self.count = 0
        self.image = self.arr[self.index]
        self.rect = self.image.get_rect()
        self.rect.inflate_ip(self.rect.width * 0.05, self.rect.height * 0.05)
        self.rect.center = [x, y]

    def update(self):
        global gravity
        if self.rect.bottom <= 550:
            self.rect.y += gravity
            gravity += 0.1
        self.count += 1
        if self.count > 5:
            self.count = 0
            self.index += 1
            if self.index >= len(self.arr):
                self.index = 0
        self.image = self.arr[self.index]
        


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, spin):
        super().__init__()
        self.image = pygame.image.load('images/pipe.png')
        self.rect = self.image.get_rect()
        self.rect.bottomleft = [x, y - gap]
        self.rect.x = x
        self.creation = pygame.time.get_ticks()
        if spin == -1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, self.rect.y - gap]

    def update(self):
        self.rect.x -= scrolling
        if self.rect.x < -40:
            self.kill()



bird_group = pygame.sprite.Group()
flappy = Bird(130, bird_y)
bird_group.add(flappy)
pipe_group = pygame.sprite.Group()



screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Flappy Bird')

run = True
game_over = False
flying = False
while run:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
            pygame.quit()
        if event.type == KEYDOWN:
            if game_over == False and event.key == pygame.K_SPACE:
                flying = True
                gravity = 1
                flappy.rect.y -= 35

    if (len(pipe_group) == 0 or \
        abs(int(pipe_group.sprites()[-1].creation - pygame.time.get_ticks()))\
         >= time_between_pipes) and flying == True and game_over == False:
        pipe_pos = random.randrange(HEIGHT+50, HEIGHT+350)
        pipe_up = Pipe(WIDTH, pipe_pos, 1)
        pipe_down = Pipe(WIDTH, pipe_pos, -1)
        pipe_group.add(pipe_up, pipe_down)

    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
        and bird_group.sprites()[0].rect.left < pipe_group.sprites()[0].rect.right\
        and flag == False:
            flag = True
        if flag == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                points += 1
                flag = False



    # Draw Background and bird
    screen.blit(background, (0,0))
    pipe_group.draw(screen)
    bird_group.draw(screen)
    # Draw ground
    screen.blit(ground, (ground_x, HEIGHT - 200))
    if abs(ground_x) >= 42:
        ground_x = 0
    
    # Checks when to start creating pipes
    if flying == True:
        show_text(str(points), WIDTH/2 -10, 20, WHITE)
        bird_group.update()
        pipe_group.update()
        ground_x -= scrolling


    

    if game_over == True and flappy.rect.bottom <= 573:
        flappy.rect.y += gravity
        gravity += 0.2
        if flappy.rect.bottom >= 575:
            gravity = 0
        if flappy.rect.bottom >= 573:
            down = True
            while down:
                show_text(str(points), WIDTH/2 -10, 20, WHITE)
                show_text('Press Space to reestart or C to close', WIDTH * 0.15,
                          HEIGHT/2.5, WHITE)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    elif event.type == KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            restart()
                            break
                        if event.key == pygame.K_c:
                            pygame.quit()
        
    
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False)\
        or flappy.rect.bottom >= 550:
        flying = False
        game_over = True


    pygame.display.update()
