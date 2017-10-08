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
speed_limit = 5

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
        if speed_limit < speed:
            self.dx = self.dx / speed * speed_limit
            self.dy = self.dy / speed * speed_limit

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
        if not 0 <= x <= field.x:
            x = boid.x - boid.dx
        if not 0 <= y <= field.y:
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
            if not (i == j) and not distance < 0.01:
                if abs(distance) < 100:
                    ax += (boids[i].x - boids[j].x) / distance
                    ay += (boids[i].y - boids[j].y) / distance
                    ac += 1
                elif 30 < abs(distance):
                    # too far
                    ax -= (boids[i].x - boids[j].x) / distance
                    ay -= (boids[i].y - boids[j].y) / distance
                    ac += 1
                else:
                    # move in paralell
                    ax += boids[j].dx
                    ay += boids[j].dy
                    ac += 1
        # mouse tracking
        boids[i].set_vector(ax, ay, ac)
        # regularize speed
        boids[i].regularize_speed()

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
    while(True):
        scinario()
        clock.tick(1000)
        catch_events()
        draw_all()

if __name__ == '__main__':
    routine()
