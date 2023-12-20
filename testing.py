import pygame as pg
import random
import math
import sys

# Setup
pg.init()
screen_info = pg.display.Info()
ekraani_laius, ekraani_kõrgus = screen_info.current_w, screen_info.current_h
screen = pg.display.set_mode((ekraani_laius, ekraani_kõrgus), pg.FULLSCREEN)
pg.display.set_caption('Meie mäng')
clock = pg.time.Clock()
georgia = pg.font.Font('src/fonts/georgia.ttf', 25)  # font
mängu_staatus = "start_menu"

# Variables
fps = 60
skoor = 0
high_skoor = 0
tulistamine_kiirus = 250  # self-explanatory

#pildid ja hääled
player = pg.image.load('src/graphics/shooter.png').convert_alpha()
player_original = player
enemy = pg.image.load('src/graphics/enemy.png').convert_alpha()
background = pg.transform.scale(pg.image.load('src/graphics/bg3.jpg').convert_alpha(), (ekraani_laius, ekraani_kõrgus))
text_surface = georgia.render(f'skoor: {skoor}', True, 'Black')
kuul = pg.image.load('src/graphics/03.png').convert_alpha()
projectile_list = []
enemy_list = []

# Sounds
pg.mixer.init()
lask_hääl = pg.mixer.Sound('src/sounds/lask.wav')

# Positions and sizes
bg_box = background.get_rect(topleft=(0, 0))
bg_box2 = background.get_rect(topleft=(ekraani_laius, 0))
player_box = player.get_rect(midbottom=(ekraani_laius // 2, ekraani_kõrgus - 25))
text_box = text_surface.get_rect(topleft=(10, 10))

# Enemy-related variables
enemy_size = (player.get_width() * 3 / 10, player.get_height() * 3 / 10) #enemy size tuleb kordajaga mängija suurusest aga idk ei pea 
enemy_hitbox_size = (enemy_size[0] * 0.9, enemy_size[1] * 0.9)  #hitbox peaks timmima veel :3
enemy_speed = 3
enemy_tekkimise_viivitus = 1000
last_enemy_spawn_time = 0
last_fire_time = 0

# muutujad seoses mängu "kiiremaks muutumisega", 
laskekiiruse_tõus = 1.2  # 20% tõus 
vaenlase_kiiruse_tõus = 1.05  # 5% tõus
skoori_piir = 20 #iga skoori_piir punkti tagant muutub eelmise kahe võrra kiiremaks vm
praegune_laske_kiirus = tulistamine_kiirus
praegune_vaenlase_kiirus = enemy_speed

# High skoor display
high_skoor_text = georgia.render(f'High skoor: {high_skoor}', True, 'Black')
high_skoor_box = high_skoor_text.get_rect(topleft=(10, 40))

# game loop
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    keys = pg.key.get_pressed()

    if mängu_staatus == "start_menu":
        screen.fill((0, 0, 0))
        font = pg.font.SysFont(None, 20)
        title = font.render('Meie mäng', True, (255, 255, 255))
        start_button = font.render('Press *Space* to Start', True, (255, 255, 255))
        screen.blit(title, (ekraani_laius / 2 - title.get_width() / 2, ekraani_kõrgus / 2 - title.get_height() / 2))
        screen.blit(start_button, (ekraani_laius / 2 - start_button.get_width() / 2, ekraani_kõrgus / 2 + start_button.get_height() / 2))
        pg.display.update()
        if keys[pg.K_SPACE]:
            mängu_staatus = "game"

    if mängu_staatus == "game_over":
        screen.fill((0, 0, 0))
        font = pg.font.SysFont(None, 20)
        title = font.render('Game over', True, (255, 0, 0))
        restart_button = font.render('R to restart', True, (255, 255, 255))
        screen.blit(title, (ekraani_laius / 2 - title.get_width() / 2, ekraani_kõrgus / 2 - title.get_height() / 2))
        screen.blit(restart_button, (ekraani_laius / 2 - restart_button.get_width() / 2, ekraani_kõrgus / 2 + restart_button.get_height() / 2))
        pg.display.update()
        if keys[pg.K_r]:
            mängu_staatus = "game"
            skoor = 0
            praegune_laske_kiirus = tulistamine_kiirus
            praegune_vaenlase_kiirus = enemy_speed
            enemy_list = []

    if mängu_staatus == "paused_menu":
        screen.fill((0, 0, 0))
        font = pg.font.SysFont(None, 20)
        title = font.render('Paused', True, (255, 255, 255))
        resume_button = font.render('R to resume', True, (255, 255, 255))
        quit_button = font.render('Q to quit', True, (255, 255, 255))
        screen.blit(title, (ekraani_laius / 2 - title.get_width() / 2, ekraani_kõrgus / 2 - title.get_height() / 2 - 15))
        screen.blit(resume_button, (ekraani_laius / 2 - resume_button.get_width() / 2, ekraani_kõrgus / 2 + 15))
        screen.blit(quit_button, (ekraani_laius / 2 - quit_button.get_width() / 2, ekraani_kõrgus / 2 + quit_button.get_height() + 15))
        pg.display.update()
        if keys[pg.K_q]:
            pg.quit()
            sys.exit()
        if keys[pg.K_r]:
            mängu_staatus = "game"

    if mängu_staatus == "game":
        screen.blit(background, bg_box)
        screen.blit(background, bg_box2)

        # mängija keerutamine
        angle = math.atan2(pg.mouse.get_pos()[1] - player_box.centery,pg.mouse.get_pos()[0] - player_box.centerx)
        rotated_player = pg.transform.scale(pg.transform.rotate(player_original, -math.degrees(angle)),(player.get_width() // 2, player.get_height() // 2))
        player_box = rotated_player.get_rect(center=player_box.center)

        screen.blit(rotated_player, player_box)
        screen.blit(text_surface, text_box)
        screen.blit(high_skoor_text, high_skoor_box)

        # mängija liikumine
        mängija_kiirus = 5
        if keys[pg.K_a] and player_box.left > 0:
            player_box.x -= mängija_kiirus
        if keys[pg.K_d] and player_box.right < ekraani_laius:
            player_box.x += mängija_kiirus
        if keys[pg.K_w] and player_box.top > 0:
            player_box.y -= mängija_kiirus
        if keys[pg.K_s] and player_box.bottom < ekraani_kõrgus:
            player_box.y += mängija_kiirus

        # Enemy tekkimine
        current_time = pg.time.get_ticks()
        if current_time - last_enemy_spawn_time >= enemy_tekkimise_viivitus:
            enemy_box = enemy.get_rect(
                topleft=(random.randint(0, int(ekraani_laius - enemy_size[0])),
                         random.randint(0, int(ekraani_kõrgus - enemy_size[1]))))
            while enemy_box is None or player_box.colliderect(enemy_box):
                enemy_box = enemy.get_rect(topleft=(random.randint(0, int(ekraani_laius - enemy_size[0])),random.randint(0, int(ekraani_kõrgus - enemy_size[1]))))
            enemy_list.append(enemy_box)
            last_enemy_spawn_time = current_time

        # enemy loogika
        for enemy_box in enemy_list:
            angle_to_player = math.atan2(player_box.centery - enemy_box.centery, player_box.centerx - enemy_box.centerx)
            enemy_speed_vector = [praegune_vaenlase_kiirus * math.cos(angle_to_player),praegune_vaenlase_kiirus * math.sin(angle_to_player)]
            enemy_box.x += int(enemy_speed_vector[0])
            enemy_box.y += int(enemy_speed_vector[1])
            enemy_box.width, enemy_box.height = enemy_size
            rotated_enemy = pg.transform.rotate(enemy, -math.degrees(angle_to_player))
            screen.blit(rotated_enemy, enemy_box)

            # kas enemy läks vastu mängijale
            if player_box.colliderect(enemy_box):
                mängu_staatus = "game_over"

            # lasud pihtas?
            for rotated_projectile, (proj, proj_speed) in projectile_list:
                rotated_rect = rotated_projectile.get_rect(center=(proj[0], proj[1]))
                if enemy_box.colliderect(rotated_rect):
                    skoor += 1
                    text_surface = georgia.render(f'skoor: {skoor}', True, 'Black')
                    # see täiustab ka high score nn live
                    if skoor > high_skoor:
                        high_skoor = skoor
                        high_skoor_text = georgia.render(f'High skoor: {high_skoor}', True, 'Black')
                    enemy_list.remove(enemy_box)
                    projectile_list.remove((rotated_projectile, (proj, proj_speed)))

        # skoor 
        for (rotated_projectile, (proj, proj_speed)) in projectile_list:
            rotated_rect = rotated_projectile.get_rect(center=(proj[0], proj[1]))
            for enemy_box in enemy_list:
                if enemy_box.colliderect(rotated_rect):
                    skoor += 1
                    text_surface = georgia.render(f'skoor: {skoor}', True, 'Black')
                    # best tulemuse uuendamine kui suurem
                    if skoor > high_skoor:
                        high_skoor = skoor
                        high_skoor_text = georgia.render(f'High skoor: {high_skoor}', True, 'Black')
                    enemy_list.remove(enemy_box)
                    projectile_list.remove((rotated_projectile, (proj, proj_speed)))

        # laskmine, space bar
        if keys[pg.K_SPACE] and current_time - last_fire_time >= praegune_laske_kiirus:
            rotated_player_width, rotated_player_height = rotated_player.get_size()
            offset_ratio = 0.2  # um kogu see värk peaks aitama seda offset paika saada kust lasud tulevad aga ma ei oska välja mõelda
            offset_x = int(rotated_player_width * offset_ratio)
            offset_y = -int(rotated_player_height * offset_ratio)
            rotated_offset = pg.Vector2(offset_x, offset_y).rotate(-math.degrees(angle))
            proj = [player_box.centerx + rotated_offset.x, player_box.centery + rotated_offset.y]
            speed = 20  # laskmise kiirus
            proj_speed = [speed * math.cos(angle), speed * math.sin(angle)]
            rotated_projectile = pg.transform.rotate(kuul, -math.degrees(angle))
            projectile_list.append((rotated_projectile, (proj, proj_speed)))
            last_fire_time = current_time
            lask_hääl.play()

        # lastud asjade visualiseerimine
        for rotated_projectile, (proj, proj_speed) in projectile_list:
            proj[0] += proj_speed[0]
            proj[1] += proj_speed[1]
            rotated_rect = rotated_projectile.get_rect(center=(proj[0], proj[1]))
            screen.blit(rotated_projectile, rotated_rect.topleft)

            # ekraanivaliste laskude kustutamine
            if proj[0] < 0 or proj[1] < 0 or proj[0] > ekraani_laius or proj[1] > ekraani_kõrgus:
                projectile_list.remove((rotated_projectile, (proj, proj_speed)))

        # pausi kontroll
        if keys[pg.K_ESCAPE]:
            mängu_staatus = "paused_menu"

        # vaenlased tugevamaks 
        if skoor >= skoori_piir and skoor % skoori_piir == 0:
            praegune_laske_kiirus = int(praegune_laske_kiirus / laskekiiruse_tõus)
            praegune_vaenlase_kiirus *= vaenlase_kiiruse_tõus
            skoori_piir += 20

    pg.display.update()
    clock.tick(fps)
