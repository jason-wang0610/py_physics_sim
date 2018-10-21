import pygame
import random
import math


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
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed

width, height = 300, 200
bg_colour = (255,255,255)

window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Physics Simulation')
window.fill(bg_colour)

particle_amount = 10
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
        particle.display()

    pygame.display.flip()
