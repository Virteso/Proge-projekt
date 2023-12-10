import pygame as pg
from sys import exit
import random
import math

# Setup
pg.init()
screen_info = pg.display.Info()
screen_width, screen_height = screen_info.current_w, screen_info.current_h
suurus = 120
screen = pg.display.set_mode((screen_width, screen_height), pg.FULLSCREEN)
pg.display.set_caption('Actual game')
clock = pg.time.Clock()
georgia = pg.font.Font('src/fonts/georgia.ttf', 50)
game_state = "start_menu"

# Variables
fps = 60
score = 0

# Surfaces
player = pg.image.load('src/graphics/green.png').convert_alpha()
background = pg.transform.scale(pg.image.load('src/graphics/bg3.jpg').convert_alpha(), (screen_width, screen_height))
text_surface = georgia.render(f'Score: {score}', True, 'Black')
ctest = pg.image.load('src/graphics/red.jpg').convert_alpha()
projectile = pg.Surface((10, 10))
projectile.fill((255, 0, 0))
projectile_list = []

# Position
bg_box = background.get_rect(topleft=(0, 0))
bg_box2 = background.get_rect(topleft=(screen_width, 0))
player_box = player.get_rect(midbottom=(200, 600))
red_box = ctest.get_rect(topleft=(random.randint(0, screen_width - 50), random.randint(0, screen_height - 50)))
red_box_size = 25  # Half the size
red_box_speed = 5
text_box = text_surface.get_rect(topleft=(10, 10))  # Move to top-left corner

# Functions
def draw_start_menu():
    screen.fill((0, 0, 0))
    font = pg.font.SysFont(None, 40)
    title = font.render('Stickman', True, (255, 255, 255))
    start_button = font.render('Press *Space* to Start', True, (255, 255, 255))
    screen.blit(title, (screen_width / 2 - title.get_width() / 2, screen_height / 2 - title.get_height() / 2))
    screen.blit(start_button, (screen_width / 2 - start_button.get_width() / 2, screen_height / 2 + start_button.get_height() / 2))
    pg.display.update()

def draw_game_over():
    screen.fill((0, 0, 0))
    font = pg.font.SysFont(None, 40)
    title = font.render('Game over', True, (255, 0, 0))
    restart_button = font.render('R to restart', True, (255, 255, 255))
    screen.blit(title, (screen_width / 2 - title.get_width() / 2, screen_height / 2 - title.get_height() / 2))
    screen.blit(restart_button, (screen_width / 2 - restart_button.get_width() / 2, screen_height / 2 + restart_button.get_height() / 2))
    pg.display.update()

def draw_paused_menu():
    screen.fill((0, 0, 0))
    font = pg.font.SysFont(None, 40)
    title = font.render('Paused', True, (255, 255, 255))
    resume_button = font.render('R to resume', True, (255, 255, 255))
    quit_button = font.render('Q to quit', True, (255, 255, 255))
    screen.blit(title, (screen_width / 2 - title.get_width() / 2, screen_height / 2 - title.get_height() / 2 - 30))
    screen.blit(resume_button, (screen_width / 2 - resume_button.get_width() / 2, screen_height / 2 + 30))
    screen.blit(quit_button, (screen_width / 2 - quit_button.get_width() / 2, screen_height / 2 + quit_button.get_height() + 30))
    pg.display.update()

# Window animation
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()

    keys = pg.key.get_pressed()

    if game_state == "start_menu":
        draw_start_menu()
        if keys[pg.K_SPACE]:
            game_state = "game"

    if game_state == "game_over":
        draw_game_over()
        if keys[pg.K_r]:
            game_state = "game"

    if game_state == "paused_menu":
        draw_paused_menu()
        if keys[pg.K_q]:
            pg.quit()
            exit()
        if keys[pg.K_r]:
            game_state = "game"

    if game_state == "game":
        screen.blit(background, bg_box)
        screen.blit(background, bg_box2)
        screen.blit(player, player_box)
        screen.blit(ctest, red_box)
        screen.blit(text_surface, text_box)

        if player_box.right == screen_width:
            player_box.left = 0
            bg_box.left -= screen_width
            bg_box2.left -= screen_width
            if bg_box.right < 0:
                bg_box.left = bg_box2.right
            if bg_box2.right < 0:
                bg_box2.left = bg_box.right

        # Move red box only to avoid projectiles
        for proj, proj_speed in projectile_list:
            angle = math.atan2(red_box.centery - proj[1], red_box.centerx - proj[0])
            red_box.x += red_box_speed * math.cos(angle)
            red_box.y += red_box_speed * math.sin(angle)

            # Stay within screen boundaries
            red_box.left = max(red_box.left, 0)
            red_box.top = max(red_box.top, 0)
            red_box.right = min(red_box.right, screen_width)
            red_box.bottom = min(red_box.bottom, screen_height)

        # Score handling
        for proj, proj_speed in projectile_list:
            if red_box.colliderect(pg.Rect(proj[0], proj[1], 10, 10)):
                score += 1
                text_surface = georgia.render(f'Score: {score}', True, 'Black')
                projectile_list.remove((proj, proj_speed))

        # Shooting projectiles
        mouse_pos = pg.mouse.get_pos()
        if pg.mouse.get_pressed()[0]:
            proj = [player_box.centerx, player_box.centery]
            angle = math.atan2(mouse_pos[1] - proj[1], mouse_pos[0] - proj[0])
            speed = 10
            proj_speed = [speed * math.cos(angle), speed * math.sin(angle)]
            projectile_list.append((proj, proj_speed))

        # Move and draw projectiles
        for proj, proj_speed in projectile_list:
            proj[0] += proj_speed[0]
            proj[1] += proj_speed[1]
            pg.draw.rect(screen, (255, 0, 0), (proj[0], proj[1], 10, 10))

            # Remove projectiles that go out of bounds
            if proj[0] < 0 or proj[1] < 0 or proj[0] > screen_width or proj[1] > screen_height:
                projectile_list.remove((proj, proj_speed))

        if keys[pg.K_a] and player_box.left > 0:
            player_box.x -= 5
        if keys[pg.K_d] and player_box.right < screen_width:
            player_box.x += 5
        if keys[pg.K_w] and player_box.top > 0:
            player_box.y -= 5
        if keys[pg.K_s] and player_box.bottom < screen_height:
            player_box.y += 5

        if keys[pg.K_ESCAPE]:
            game_state = "paused_menu"

    pg.display.update()
    clock.tick(fps)
