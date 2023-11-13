import pygame
from sys import exit
import random


# Setup
pygame.init()
suurus = 120
screen = pygame.display.set_mode((16 * suurus, 9 * suurus))
pygame.display.set_caption('Actual game')
clock = pygame.time.Clock()

# Variables
fps = 60

# Sprites




running = 1

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    


    pygame.display.flip()
    '''pygame.display.update(rect_object)
    can be faster but updates only the specified area(s)'''

    clock.tick(fps)