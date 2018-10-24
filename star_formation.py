import random
import pygame
import math
import particles

class UniverseScreen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.dx, self.dy = 0,0
        self.mx, self.my = 0,0
        self.magnification = 1.0

        self.paused = False

    def scroll(self, dx = 0, dy = 0):
        self.dx += dx * width / (self.magnification * 10)
        self.dy += dy * height / (self.magnification * 10)

    def zoom(self, zoom):
        self.magnification *= zoom
        self.mx = (1 - self.magnification) * self.width / 2
        self.my = (1 - self.magnification) * self.height / 2

    def reset(self):
        self.dx, self.dy = 0, 0
        self.mx, self.my = 0, 0
        self.magnification = 1.0

width, height = 400, 400
window = pygame.display.set_mode((width, height))
universe_screen = UniverseScreen(width, height)
pygame.display.set_caption('Star Formation Simulation')

universe = particles.Environment((width, height))
universe.colour = (0,0,0)
universe.addFunctions(['move', 'attract', 'combine']) # no drag (no air in space), no bounce (no boundaries in space)

for p in range(100):
    particle_mass = random.randint(1,4)
    particle_radius = math.sqrt(0.4 * particle_mass)
    universe.addParticles(mass = particle_mass, size = particle_radius, colour = (255,255,255))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                universe_screen.scroll(dx = 1)
            elif event.key == pygame.K_RIGHT:
                universe_screen.scroll(dx = -1)
            elif event.key == pygame.K_UP:
                universe_screen.scroll(dy = 1)
            elif event.key == pygame.K_DOWN:
                universe_screen.scroll(dy = -1)
            elif event.key == pygame.K_MINUS:
                universe_screen.zoom(0.5)
            elif event.key == pygame.K_EQUALS:
                universe_screen.zoom(2)
            elif event.key == pygame.K_r:
                universe_screen.reset()
            elif event.key == pygame.K_SPACE:
                universe_screen.paused = not universe_screen.paused

    if not universe_screen.paused:
        universe.update()
    window.fill(universe.colour)

    particle_to_remove = []
    for p in universe.particles:
        if 'collide_with' in p.__dict__:
            particle_to_remove.append(p.collide_with)
            p.size = math.sqrt(0.4 * p.mass)
            del p.__dict__['collide_with']

        m = universe_screen.magnification
        x = int(universe_screen.mx + (p.x + universe_screen.dx) * m)
        y = int(universe_screen.my + (p.y + universe_screen.dy) * m)
        size = int(p.size * m)

        if p.size < 2:
            pygame.draw.rect(window, p.colour, (x, y, 2, 2))
        else:
            pygame.draw.circle(window, p.colour, (x, y), size, 0)

    for p in particle_to_remove:
        if p in universe.particles:
            universe.particles.remove(p)

    pygame.display.flip()
