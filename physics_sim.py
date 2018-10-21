import pygame
import random
import math


width, height = 300, 200
bg_colour = (255,255,255)

gravity = (math.pi, 0.1)
drag = 0.99
elasticity = 0.75


def addVectors(vector1, vector2):
    angle1, len1 = vector1
    angle2, len2 = vector2
    x = math.sin(angle1) * len1 + math.sin(angle2) * len2 # calculates combined x vector using trig
    y = math.cos(angle1) * len1 + math.cos(angle2) * len2 # calculates combined y vector using trig

    len = math.hypot(x, y) # pythagoras to find distance from origin to point
    angle = math.pi * 0.5 - math.atan2(y, x) # works out angle with x=0 taken into consideration
    return (angle, len)

class Particle:
    def __init__(self, position, size):
        self.x, self.y = position
        self.size = size
        self.colour = (0,0,0)
        self.thickness = 1

        self.speed = 0.2
        self.angle = math.pi / 2

    def display(self):
        pygame.draw.circle(window, self.colour, (int(self.x), int(self.y)), self.size, self.thickness)

    def move(self):
        (self.angle, self.speed) = addVectors((self.angle, self.speed), gravity)
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed

        self.speed *= drag

    def bounce(self):
        if self.x > width - self.size:
            self.x = 2 * (width - self.size) - self.x
            self.angle = -self.angle

            self.speed *= elasticity
        elif self.x < self.size:
            self.x = 2 * self.size - self.x
            self.angle = -self.angle

            self.speed *= elasticity
        if self.y > height - self.size:
            self.y = 2 * (height - self.size) - self.y
            self.angle = math.pi - self.angle

            self.speed *= elasticity
        elif self.y < self.size:
            self.y = 2 * self.size - self.y
            self.angle = math.pi - self.angle

            self.speed *= elasticity


window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Physics Simulation')
window.fill(bg_colour)

particle_amount = 20
particles = []
for x in range(particle_amount):
    size = random.randint(10, 20)
    x, y = random.randint(size, width - size), random.randint(size, height - size)

    particle = Particle((x, y), size)
    particle.speed = random.random()
    particle.angle = random.uniform(0, math.pi*2)

    particles.append(particle)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    window.fill(bg_colour)
    for particle in particles:
        particle.move()
        particle.bounce()
        particle.display()

    pygame.display.flip()
