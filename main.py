import random

import pygame
import math

circle_radius = 250
initial_radius = 15

black = (0, 0, 0)
pink = (255, 0, 255)
white = (255, 255, 255)


class Circle:
    def __init__(self, pivot_x, pivot_y, color, radius):
        self.pivot = (pivot_x, pivot_y)
        self.radius = radius
        self.color = color

    def draw(self, surface):
        pygame.draw.circle(surface, white, self.pivot, self.radius, 4)


class SmallCircle:
    def __init__(self, pivot_x, pivot_y, color, radius, big_radius):
        self.pivot = (pivot_x, pivot_y)
        self.radius = radius
        self.color = color
        self.big_radius = big_radius

        self.x = pivot_x+45
        self.y = pivot_y+45

        self.vx = 0.5
        self.vy = 0.5

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.vx
        self.y += self.vy
        d = math.sqrt((self.pivot[0] - self.x) ** 2 + (self.pivot[1] - self.y) ** 2)

        if d >= self.big_radius - self.radius:
            if self.radius <= self.big_radius:
                self.radius += 2.5
            self.vx *= 1.01
            self.vy *= 1.01

            dx = self.x - self.pivot[0]
            dy = self.y - self.pivot[1]
            norm_length = math.sqrt(dx ** 2 + dy ** 2)
            normal = (dx / norm_length, dy / norm_length)

            dot_product = self.vx * normal[0] + self.vy * normal[1]
            self.vx -= 2 * dot_product * normal[0]
            self.vy -= 2 * dot_product * normal[1]

            angle_change = random.uniform(-0.5, 0.5)
            self.vx, self.vy = self.vx * math.cos(angle_change) - self.vy * math.sin(angle_change), \
                               self.vx * math.sin(angle_change) + self.vy * math.cos(angle_change)

            overlap = d - (self.big_radius - self.radius)
            self.x -= overlap * normal[0]
            self.y -= overlap * normal[1]


def init_surface(size, caption):
    pygame.init()
    pygame.display.set_caption(caption)
    surface = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    return surface, clock


def run():
    width, height = 1000, 1000

    fps = 60

    surface, clock = init_surface((width, height), "Simple Game")

    stop = False
    pygame.init()
    colors = ['red', 'green', 'blue', 'yellow', 'magenta', 'cyan', 'grey']
    small_circle_list = [SmallCircle(pivot_x=width // 2, pivot_y=height // 2, color=c, radius=initial_radius, big_radius=circle_radius) for c in colors]

    circle = Circle(width // 2, height // 2, white, circle_radius)
    small_circle = SmallCircle(width // 2, height // 2, pink, initial_radius, circle_radius)

    while not stop:
        surface.fill(black)
        circle.draw(surface)
        for small_circle in small_circle_list:
            for event in pygame.event.get():
                stop = event.type == pygame.QUIT
            small_circle.draw(surface)
            small_circle.move()
        pygame.display.flip()
    pygame.quit()


run()
