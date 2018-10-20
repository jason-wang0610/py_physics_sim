import pygame
import random

class Particle:
    def __init__(self, position, size):
        self.x, self.y = position
        self.size = size
        self.colour = (0,0,0)
        self.thickness = 1

    def display(self):
        pygame.draw.circle(window, self.colour, (self.x, self.y), self.size, self.thickness)

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
    particles.append(Particle((x, y), size))

for particle in particles:
    particle.display()

pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
