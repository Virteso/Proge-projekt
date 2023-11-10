import pygame as pg
from sys import exit
import random


# Setup
pg.init()
suurus = 120
screen = pg.display.set_mode((16 * suurus, 9 * suurus))
pg.display.set_caption('Stickman')
clock = pg.time.Clock()
georgia = pg.font.Font('src/fonts/georgia.ttf', 50)

# Surfaces
player = pg.image.load('src/graphics/green.png').convert_alpha()
background = pg.image.load('src/graphics/bg3.jpg').convert_alpha()
background2 = pg.image.load('src/graphics/bg3.jpg').convert_alpha()
text_surface = georgia.render('Stickman', True, 'Black')
ctest = pg.image.load('src/graphics/red.jpg').convert_alpha()

# Variables
fps = 60

# Position

bg_box = background.get_rect(bottomleft = (0, 1080))
bg_box2 = background2.get_rect(bottomleft = (3840, 1080))
player_box = player.get_rect(midbottom = (200, 600))
red_box = ctest.get_rect(bottomleft = (random.randint(0, 1620), random.randint(0, 780)))

# Window
while 1:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
    


    screen.blit(background,(bg_box))
    screen.blit(background2,(bg_box2))
    screen.blit(player,(player_box))
    screen.blit(ctest, (red_box))
    
    if player_box.right == 1800:
        player_box.left = 120
        bg_box.left -= 1680
        bg_box2.left -= 1680
        if bg_box.right < 0:
            bg_box.left += 3840 * 2
        if bg_box2.right < 0:
            bg_box2.left += 3840 * 2
    player_box.right += 5
    # screen.blit(text_surface, (100, 100))

    
    pg.display.update()
    clock.tick(fps)