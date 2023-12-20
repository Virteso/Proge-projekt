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

#Sprites
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, keys):
        pass


#Functoins
def check_key_press(target_letter):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            # Convert the key code to the corresponding character
            pressed_key = pygame.key.name(event.key)
            if pressed_key.lower() == target_letter.lower():
                return True
    return False

# Groups
all_sprites = pygame.sprite.Group()
bullets_group = pygame.sprite.Group()
player = Player(10, 10, size, size)
all_sprites.add(player)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    all_sprites.update(keys)

    screen.fill((0, 0, 0))
    all_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(fps)