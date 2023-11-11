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

# Surfaces
player = pygame.draw.rect(screen, '#ffffff', (10, 10))