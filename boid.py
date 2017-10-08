import sys
import math
import random
import pygame
import pygame.gfxdraw
import pygame.locals as pyglocal

class Parameter:
    too_close = 100
    too_far = 30
    # speed of boid
    speed_limit = 5
    # number of boids
    boids_size = 100

class Field:
    x = 1200
    y = 680

    def random_x():
        return (Field.x) * random.random()

    def random_y():
        return (Field.y) * random.random()

class Boid:
    x = 0
    y = 0
    dx = 0
    dy = 0
    color = (0, 0, 0)

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def distance(self, other):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def regularize_speed(self):
        speed = math.sqrt(self.dx ** 2 + self.dy ** 2)
        if Parameter.speed_limit < speed:
            self.dx = self.dx / speed * Parameter.speed_limit
            self.dy = self.dy / speed * Parameter.speed_limit

    def set_vector(self, ax, ay, ac):
        if not ac == 0:
            distance = math.sqrt((self.x - dest.x) ** 2 + (self.y - dest.y) ** 2)
            self.dx = self.dx + ax / ac + (dest.x - self.x) / distance
            self.dy = self.dy + ay / ac + (dest.y - self.y) / distance

class Destination:
    x = 0
    y = 0

class Distance:
    x = 0
    y = 0

def get_index(i, j):
    if i == j:
        return 0
    elif j < i:
        return int((Parameter.boids_size * 2 - j - 1) * j / 2 + i - j - 1)
    else:
        return int((Parameter.boids_size * 2 - i - 1) * i / 2 + j - i - 1)

def update_distance():
    for i, boid in enumerate(boids):
        for j, other in enumerate(boids):
            dists[get_index(i, j)] = boid.distance(other)

def accelerate():
    for i, boid in enumerate(boids):
        ax, ay = 0, 0
        ac = 0
        # fall earch other
        for j, other in enumerate(boids):
            distance = dists[get_index(i, j)]
            if not (i == j) and not distance < 0.01:
                if abs(distance) < Parameter.too_close:
                    ax += (boid.x - other.x) / distance
                    ay += (boid.y - other.y) / distance
                    ac += 1
                elif Parameter.too_far < abs(distance):
                    # too far
                    ax -= (boid.x - other.x) / distance
                    ay -= (boid.y - other.y) / distance
                    ac += 1
                else:
                    # move in paralell
                    ax += other.dx
                    ay += other.dy
                    ac += 1
        # mouse tracking
        boid.set_vector(ax, ay, ac)
        # regularize speed
        boid.regularize_speed()

def update_position():
    for boid in boids:
        x = boid.x + boid.dx
        y = boid.y + boid.dy
        if not 0 <= x <= Field.x:
            x = boid.x - boid.dx
        if not 0 <= y <= Field.y:
            y = boid.y - boid.dy
        boid.x = x
        boid.y = y

def scinario():
    update_distance()
    accelerate()
    update_position()

def catch_events():
    # for exit
    for event in pygame.event.get():
        if event.type == pyglocal.QUIT:
            pygame.quit()
            sys.exit()
    # update mouse position
    dest.x, dest.y = pygame.mouse.get_pos()

def draw_all():
    # flash background
    screen.fill((255, 255, 255))
    # draw boids
    for boid in boids:
        xy = int(boid.x), int(boid.y)
        pygame.draw.circle(screen, boid.color, xy, 2)
    # mouse position
    pygame.draw.rect(screen, (255, 0, 0), pyglocal.Rect(dest.x, dest.y, 4, 4))
    pygame.display.update()

def routine():
    clock = pygame.time.Clock()
    while(True):
        scinario()
        clock.tick(1000)
        catch_events()
        draw_all()

if __name__ == '__main__':
    boids = [Boid(Field.random_x(), Field.random_x()) for _ in range(Parameter.boids_size)]
    dest = Destination()
    dists = [Distance() for _ in range(int(Parameter.boids_size * (Parameter.boids_size - 1) / 2))]
    pygame.init()
    screen = pygame.display.set_mode((1200, 600))
    routine()
