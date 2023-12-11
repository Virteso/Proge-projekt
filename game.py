import pygame
from sys import exit
import random


# Setup
pygame.init()
size = 120
screen = pygame.display.set_mode((16 * size, 9 * size))
pygame.display.set_caption('Actual game')
clock = pygame.time.Clock()

# Variables
fps = 60

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, keys):
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx = -5
        if keys[pygame.K_RIGHT]:
            dx = 5
        if keys[pygame.K_UP]:
            dy = -5
        if keys[pygame.K_DOWN]:
            dy = 5

        self.rect.x += dx
        self.rect.y += dy

        # Collision with the screen boundaries
        self.rect.x = max(0, min(self.rect.x, screen.get_width() - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, screen.get_height() - self.rect.height))

        # Collision with the ground
        if pygame.sprite.spritecollide(self, ground_group, False):
            self.rect.x -= dx
            self.rect.y -= dy

class Ground(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(topleft=(x, y))

# Groups
all_sprites = pygame.sprite.Group()
ground_group = pygame.sprite.Group()
player = Player(10, 10, size, size)
all_sprites.add(player)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    all_sprites.update(keys)

    screen.fill((0, 0, 0))  # Fill the screen with a black background
    all_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(fps)