import pygame as pg
from sys import exit
import random


# Setup
pg.init()
suurus = 120
screen = pg.display.set_mode((16 * suurus, 9 * suurus))
pg.display.set_caption('Actual game')
clock = pg.time.Clock()
georgia = pg.font.Font('src/fonts/georgia.ttf', 50)

# Variables
fps = 60
score = 0


# Surfaces
player = pg.image.load('src/graphics/green.png').convert_alpha()
background = pg.transform.scale(pg.image.load('src/graphics/bg3.jpg').convert_alpha(), (1920, 1080))
background2 = pg.transform.scale(pg.image.load('src/graphics/bg3.jpg').convert_alpha(), (1920, 1080))
text_surface = georgia.render(f'Score: {score}', True, 'Black')
ctest = pg.image.load('src/graphics/red.jpg').convert_alpha()


# Position
bg_box = background.get_rect(bottomleft = (0, 1080))
bg_box2 = background2.get_rect(bottomleft = (1920, 1080))
player_box = player.get_rect(midbottom = (200, 600))
red_box = ctest.get_rect(bottomleft = (random.randint(0, 1620), random.randint(0, 1080)))
text_box = text_surface.get_rect(topleft = (50, 50))


# Window animation
while 1:
    # if window closed quit
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
    
    # Key presses
    # keys = pg.key.get_pressed()
    # space = keys[pg.K_SPACE]

    '''event.type == pg.KEYDOWN
    event.type == pg.KEYUP
    event.key == pg.K_SPACE'''


    # Drawing surfaces on the screen
    screen.blit(background,(bg_box))
    screen.blit(background2,(bg_box2))
    screen.blit(player,(player_box))
    screen.blit(ctest, (red_box))
    screen.blit(text_surface, (text_box))
    
    # Mowing loop
    if player_box.right == 1800:
        player_box.left = 120
        bg_box.left -= 1680
        bg_box2.left -= 1680
        if bg_box.right < 0:
            bg_box.left += 3840
        if bg_box2.right < 0:
            bg_box2.left += 3840
    player_box.right += 5

    # Collision and click test
    mouse_pos = pg.mouse.get_pos()
    if pg.mouse.get_pressed()[0]:
        if red_box.collidepoint(mouse_pos):
            red_box.right = (random.randint(300, 1920))
            red_box.top = (random.randint(0, 780))
            score += 1
            text_surface = georgia.render(f'Score: {score}', True, 'Black')

    # Quiting the game
    if score == 10:
        pg.quit()
        exit()

    
    
    pg.display.update()
    clock.tick(fps)