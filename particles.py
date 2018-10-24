import random
import math



def collide(p1, p2):
    """ Calculates the speed, angle, vel, etc. of two objects if they collide (overlap)"""
    #diff in x,y
    dx = p1.x - p2.x
    dy = p1.y - p2.y

    distance = math.hypot(dx, dy) #distnace between points with pythag
    if distance < p1.size + p2.size:
        tangent = math.atan2(dx, dy) #find angle of tangent
        angle = 0.5 * math.pi + tangent
        total_mass = p1.mass + p2.mass

        # 1d elastic collision equations calculating velocity
        p1.angle, p1.speed = addVectors((p1.angle, p1.speed * (p1.mass - p2.mass) / total_mass), (angle, 2 * p2.speed * p2.mass / total_mass))
        p2.angle, p2.speed = addVectors((p2.angle, p2.speed * (p2.mass - p1.mass) / total_mass), (angle + math.pi, 2 * p1.speed * p1.mass / total_mass))
        elasticity = p1.elasticity * p2.elasticity
        p2.speed *= elasticity
        p1.speed *= elasticity
        #CONSERVATION OF MOMENTUM

        overlap = 0.5 * (p1.size + p2.size - distance + 1) # extra steps to reduce overlapping
        p1.x += math.sin(angle) * overlap
        p1.y -= math.cos(angle) * overlap
        p2.x -= math.sin(angle) * overlap
        p2.y += math.cos(angle) * overlap

def combine(p1, p2):
    if math.hypot(p1.x - p2.x, p1.y - p2.y) < p1.size + p2.size:
        total_mass = p1.mass + p2.mass
        p1.x = (p1.x * p1.mass + p2.x * p2.mass) / total_mass
        p1.y = (p1.y * p1.mass + p2.y * p2.mass) / total_mass
        p1.angle, p1.speed = addVectors((p1.angle, p1.speed * p1.mass / total_mass), (p2.angle, p2.speed * p2.mass / total_mass))
        p1.speed *= p1.elasticity * p2.elasticity
        p1.mass += p2.mass
        p1.collide_with = p2


def addVectors(vector1, vector2):
    """ Adds two vectors """
    angle1, len1 = vector1
    angle2, len2 = vector2
    x = math.sin(angle1) * len1 + math.sin(angle2) * len2 # calculates combined x vector using trig
    y = math.cos(angle1) * len1 + math.cos(angle2) * len2 # calculates combined y vector using trig

    len = math.hypot(x, y) # pythagoras to find distance from origin to point
    angle = math.pi * 0.5 - math.atan2(y, x) # works out angle with x=0 taken into consideration
    return (angle, len)

def findParticle(particles, x, y):
    """ Tests if a particle is present at given x,y location """
    for p in particles:
        if math.hypot(p.x - x, p.y - y) <= p.size:
            return p
    return None

class Particle:
    """ A circle with properties of mass, size, vel, etc """
    def __init__(self, position, size, mass = 0.5):
        self.x, self.y = position
        self.size = size
        self.mass = mass
        self.colour = (0,0,0)
        self.thickness = 0

        self.speed = 1
        self.angle = math.pi / 2 # angle in radians; pi/2 = 90º
        self.drag = 0
        self.elasticity = 0.9

        self.prev_pos = []
        self.tracer_len = 100


    def move(self):
        """ Calculates position with angle and velocity """
        # (self.angle, self.speed) = addVectors((self.angle, self.speed), (math.pi, 0.6))
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed


    def mouseMove(self, x, y):
        """ Moves object towards a given location (used when using mouse interations) """
        dx = x - self.x
        dy = y - self.y
        self.angle = math.atan2(dy, dx) + 0.5 * math.pi
        self.speed = math.hypot(dx, dy) * 0.1

    def experienceDrag(self):
        """ Slow particle through air resistance (drag) """
        self.speed *= self.drag

    def accelerate(self, vector):
        """ Set angle and speed depending on given vector """
        self.angle, self.speed = addVectors((self.angle, self.speed), vector)

    def attract(self, p2):
        dx = self.x - p2.x
        dy = self.y - p2.y
        distance = math.hypot(dx, dy)

        theta = math.atan2(dy, dx)
        force = 0.2 * self.mass * p2.mass / distance ** 2

        self.accelerate((theta - 0.5 * math.pi, force / self.mass))
        p2.accelerate((theta + 0.5 * math.pi, force / p2.mass))


class Environment:
    """ Creates the boundaries of an instance of a simulation """
    def __init__(self, dimensions):
        self.width, self.height = dimensions
        self.particles = []

        self.bg_colour = (255,255,255)
        self.mass_of_air = 0.2
        self.elasticity = 0.75
        self.acceleration = (0,0)

        self.particle_functions1 = []
        self.particle_functions2 = []
        self.function_dict = {
        'move': (1, lambda p: p.move()),
        'drag': (1, lambda p: p.experienceDrag()),
        'bounce': (1, lambda p: self.bounce(p)),
        'accelerate': (1, lambda p: p.accelerate(self.acceleration)),
        'collide': (2, lambda p1, p2: collide(p1, p2)),
        'attract': (2, lambda p1, p2: p1.attract(p2)),
        'combine': (2, lambda p1, p2: combine(p1, p2))
        }

    def addFunctions(self, func_list):
        """ Adds given functions to respective lists of functions """
        for func in func_list:
            n, f = self.function_dict.get(func, (-1, None))
            if n == 1:
                self.particle_functions1.append(f)
            elif n == 2:
                self.particle_functions2.append(f)
            else:
                print("Function does not exist: %s" % f)

    def addParticles(self, n = 1, **kargs):
        """ Adds given amount of particles """
        for i in range(n):
            size = kargs.get('size', random.randint(10,20))
            mass = kargs.get('mass', random.randint(100, 10000))
            x = kargs.get('x', random.uniform(size, self.width - size))
            y = kargs.get('y', random.uniform(size, self.height - size))

            p = Particle((x, y), size, mass)
            p.speed = kargs.get('speed', random.random())
            p.angle = kargs.get('angle', random.uniform(0, math.pi * 2))
            p.colour = kargs.get('colour', (0,0,255))
            p.drag = (p.mass / (p.mass + self.mass_of_air)) ** p.size

            self.particles.append(p)


    def bounce(self, particle):
        """ Tests if particle hits boundaries of environment and reflects particle """
        if particle.x > self.width - particle.size:
            particle.x = 2 * (self.width - particle.size) - particle.x
            particle.angle = -particle.angle

            particle.speed *= self.elasticity
        elif particle.x < particle.size:
            particle.x = 2 * particle.size - particle.x
            particle.angle = -particle.angle

            particle.speed *= self.elasticity
        if particle.y > self.height - particle.size:
            particle.y = 2 * (self.height - particle.size) - particle.y
            particle.angle = math.pi - particle.angle

            particle.speed *= self.elasticity
        elif particle.y < particle.size:
            particle.y = 2 * particle.size - particle.y
            particle.angle = math.pi - particle.angle

            particle.speed *= self.elasticity

    def update(self):
        """ Updates position of every particle """
        for i, particle in enumerate(self.particles):
            for f in self.particle_functions1:
                if len(particle.prev_pos) < particle.tracer_len:
                    for empty in range(0, particle.tracer_len):
                        particle.prev_pos.append([int(particle.x), int(particle.y)])
                particle.prev_pos.append([int(particle.x), int(particle.y)])
                if len(particle.prev_pos) > particle.tracer_len:
                    del particle.prev_pos[0]


                f(particle) #move, drag, bounce
            for particle2 in self.particles[i + 1:]:
                for f in self.particle_functions2:
                    f(particle, particle2) #collide

    def findParticle(self, x, y):
        """ Returns particle if one is present at given location """
        for p in self.particles:
            if math.hypot(p.x - x, p.y - y) <= p.size:
                return p
        return None
