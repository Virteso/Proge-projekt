import pygame as pg
from sys import exit


# Setup
pg.init()
screen = pg.display.set_mode((800, 400))
pg.display.set_caption('nimi')
clock = pg.time.Clock()




# Aken
while 1:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
    

    
    pg.display.update()
    clock.tick(60)