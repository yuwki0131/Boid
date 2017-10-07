import sys
import math
import random
import pygame
import pygame.gfxdraw
import pygame.locals as pyglocal

pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((1200, 600))

boids_size = 100
speed_limit = 8

class Field:
    left = 30
    top = 30
    x = 1200
    y = 680

    def random_x():
        return (Field.x - Field.left) * random.random() + Field.left

    def random_y():
        return (Field.y - Field.top) * random.random() + Field.top

class Boid:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, other):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    x = 0
    y = 0
    dx = 0
    dy = 0

class Destination:
    x = 0
    y = 0

class Distance:
    x = 0
    y = 0

field = Field()

boids = [Boid(Field.random_x(), Field.random_x()) for _ in range(boids_size)]

dest = Destination()

dists = [Distance() for _ in range(int(boids_size * (boids_size - 1) / 2))]

def get_index(i, j):
    if i == j:
        return 0
    elif j < i:
        return int((boids_size * 2 - j - 1) * j / 2 + i - j - 1)
    else:
        return int((boids_size * 2 - i - 1) * i / 2 + j - i - 1)

def update_distance():
    for i in range(boids_size):
        for j in range(boids_size):
            dists[get_index(i, j)] = boids[i].distance(boids[j])

def update_position():
    for boid in boids:
        x = boid.x + boid.dx
        y = boid.y + boid.dy
        if not field.left <= x <= field.x:
            x = boid.x - boid.dx
        if not field.top <= y <= field.y:
            y = boid.y - boid.dy
        boid.x = x
        boid.y = y

def accelerate():
    for i in range(boids_size):
        ax, ay = 0, 0
        ac = 0
        # fall earch other
        for j in range(boids_size):
            distance = dists[get_index(i, j)]
            if not (i == j) and not distance == 0:
                if abs(distance) < 100:
                    ax += (boids[i].x - boids[j].x) / distance
                    ay += (boids[i].y - boids[j].y) / distance
                elif 30 < abs(distance):
                    ax -= (boids[i].x - boids[j].x) / distance
                    ay -= (boids[i].y - boids[j].y) / distance
                else:
                    ax += boids[i].dx
                    ay += boids[i].dy
                ac += 1
        # mouse tracking
        ix = boids[i].x
        iy = boids[i].y

        if not ac == 0:
            distance = math.sqrt((ix - dest.x) ** 2 + (iy - dest.y) ** 2)
            boids[i].dx = boids[i].dx + ax / ac + (dest.x - ix) / distance
            boids[i].dy = boids[i].dy + ay / ac + (dest.y - iy) / distance


        # regularize speed
        speed = math.sqrt(boids[i].dx ** 2 + boids[i].dy ** 2)
        if speed_limit < speed:
            boids[i].dx = boids[i].dx / speed * speed_limit
            boids[i].dy = boids[i].dy / speed * speed_limit

def scinario():
    update_distance()
    accelerate()
    update_position()

def catch_events():
    for event in pygame.event.get():
        if event.type == pyglocal.QUIT:
            pygame.quit()
            sys.exit()
    dest.x, dest.y = pygame.mouse.get_pos()

def draw_all():
    # clean background
    screen.fill((255, 255, 255))
    for boid in boids:
        x, y = boid.x, boid.y
        pygame.draw.rect(screen, (0, 0, 225), pyglocal.Rect(x, y, 4, 4))
    pygame.display.update()

def routine():
    "game screen"
    while(True):
        scinario()
        # time delay
        clock.tick(1000)
        # event handler
        catch_events()
        # field draw
        draw_all()

# game process
if __name__ == '__main__':
    while(1):
        routine()
