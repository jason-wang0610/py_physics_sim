import pygame
import random
import math


width, height = 300, 200
bg_colour = (255,255,255)

gravity = (math.pi, 0.1)
drag = 0.99
elasticity = 0.75

def collide(p1, p2):
    #diff in x,y
    dx = p1.x - p2.x
    dy = p1.y - p2.y

    distance = math.hypot(dx, dy) #distnace between points with pythag
    if distance < p1.size + p2.size:
        tangent = math.atan2(dx, dy) #find angle of tangent
        angle = 0.5 * math.pi + tangent

        angle1 = 2 * tangent - p1.angle
        angle2 = 2 * tangent - p2.angle
        speed1 = p2.speed * elasticity
        speed2 = p1.speed * elasticity

        (p1.angle, p1.speed) = (angle1, speed1)
        (p2.angle, p2.speed) = (angle2, speed2) #CONSERVATION OF MOMENTUM

        p1.x += math.sin(angle)
        p1.y -= math.cos(angle)
        p2.x -= math.sin(angle)
        p2.y += math.cos(angle)


def addVectors(vector1, vector2):
    angle1, len1 = vector1
    angle2, len2 = vector2
    x = math.sin(angle1) * len1 + math.sin(angle2) * len2 # calculates combined x vector using trig
    y = math.cos(angle1) * len1 + math.cos(angle2) * len2 # calculates combined y vector using trig

    len = math.hypot(x, y) # pythagoras to find distance from origin to point
    angle = math.pi * 0.5 - math.atan2(y, x) # works out angle with x=0 taken into consideration
    return (angle, len)

def findParticle(particles, x, y):
    for p in particles:
        if math.hypot(p.x - x, p.y - y) <= p.size:
            return p
    return None

class Particle:
    def __init__(self, position, size):
        self.x, self.y = position
        self.size = size
        self.colour = (0,0,0)
        self.thickness = 1

        self.speed = 0.2
        self.angle = math.pi / 2 # angle in radians; pi/2 = 90º

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

particle_amount = 3
particles = []
for x in range(particle_amount):
    size = random.randint(10, 20)
    x, y = random.randint(size, width - size), random.randint(size, height - size)

    particle = Particle((x, y), size)
    particle.speed = random.random()
    particle.angle = random.uniform(0, math.pi*2)

    particles.append(particle)


running = True
selected_particle = None
while running:
    window.fill(bg_colour)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = pygame.mouse.get_pos()
            selected_particle = findParticle(particles, mouseX, mouseY)
        elif event.type == pygame.MOUSEBUTTONUP:
            selected_particle = None

    if selected_particle:
        (mouseX, mouseY) = pygame.mouse.get_pos()
        dx = mouseX - selected_particle.x
        dy = mouseY - selected_particle.y
        selected_particle.angle = math.atan2(dy, dx) + 0.5 * math.pi
        selected_particle.speed = math.hypot(dx, dy) * 0.1
        pygame.draw.line(window, (255,0,0), (mouseX, mouseY), (selected_particle.x, selected_particle.y), 1)
        pygame.display.flip()


    for i, particle in enumerate(particles):
        if particle != selected_particle:
            particle.move()
            particle.bounce()
            for particle2 in particles[i + 1:]:
                collide(particle, particle2)
        particle.display()

    pygame.display.flip()
