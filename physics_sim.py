import pygame

width, height = 300, 200
bg_colour = (255,255,255)

window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Physics Simulation')
window.fill(bg_colour)

pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
