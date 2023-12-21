import pygame
import random
import math
import sys

# Setup
pygame.init()
screen_info = pygame.display.Info()
ekraani_laius, ekraani_kõrgus = screen_info.current_w, screen_info.current_h
screen = pygame.display.set_mode((ekraani_laius, ekraani_kõrgus), pygame.FULLSCREEN)
pygame.display.set_caption('Broken Textorcist vol. 2')
clock = pygame.time.Clock()
georgia = pygame.font.Font('src/fonts/georgia.ttf', 25)  # font
mängu_staatus = "start_menu"
pygame.mouse.set_visible(False)

# Variables
FPS = 60
score = 0.0
BLACK = (0, 0, 0)
TBLACK = (0, 0, 0, 200)
WHITE = (255, 255, 255)

# Sounds
pygame.mixer.init()
#lask_hääl = pygame.mixer.Sound('src/sounds/lask.wav')

#Sprites
class Player(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect(center = (ekraani_laius/2, ekraani_kõrgus/2))
        self.speed = 10
    
    def reset(self):
         self.rect = self.image.get_rect(center = (ekraani_laius/2, ekraani_kõrgus/2))

    def update(self, keys):
        if any(keys[key] for key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]):
            self.movement(keys)
    
    def movement(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < ekraani_laius:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < ekraani_kõrgus:
            self.rect.y += self.speed

class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = pygame.image.load('src/graphics/ritual.jpeg').convert_alpha()
        self.image = pygame.transform.rotozoom(self.original_image, 0, 2)
        self.rect = self.image.get_rect(center=(ekraani_laius / 2, ekraani_kõrgus / 2))
        self.speed = 10
    
    def reset(self):
        self.rect = self.image.get_rect(center=(ekraani_laius / 2, ekraani_kõrgus / 2))
    
    def update(self, keys, rect):
        if any(keys[key] for key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]):
            self.move(keys, rect)

    def move(self, keys, rect):
        if keys[pygame.K_LEFT] and self.rect.left < 0 and rect.centerx < ekraani_laius / 3:
            self.rect.x += self.speed  # Adjust the background movement speed
            rect.x += self.speed
        if keys[pygame.K_RIGHT] and self.rect.right > ekraani_laius and rect.centerx > ekraani_laius * 2/3:
            self.rect.x -= self.speed  # Adjust the background movement speed
            rect.x -= self.speed
        if keys[pygame.K_UP] and self.rect.top < 0 and rect.centery < ekraani_kõrgus / 3:
            self.rect.y += self.speed  # Adjust the background movement speed
            rect.y += self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom > ekraani_kõrgus and rect.centery > ekraani_kõrgus * 2/3:
            self.rect.y -= self.speed  # Adjust the background movement speed
            rect.y -= self.speed
   
class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, speed):
        super().__init__()
        self.speed = speed
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()

class Chant(pygame.sprite.Sprite):
    def __init__(self, source):
        super().__init__()
        self.image = pygame.transform.rotozoom(pygame.image.load('src/graphics/paper.jpg'), 0, ekraani_laius*0.8 / 4500) #<a href="https://www.freepik.com/free-photo/grunge-style-background_1437198.htm#query=dark%20ancient%20paper&position=33&from_view=search&track=ais&uuid=e5ef9a6e-5142-4d94-af3b-c66b8ab7d0d2">Image by kjpargeter</a> on Freepik
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect(midtop = (ekraani_laius/2, ekraani_kõrgus-80))
        with open(source, encoding='utf-8') as info:
            self.text = [i.strip() for i in info.readlines()]
        self.line = 0
        self.word = 0
        self.letter = 0
        print(self.text)
    
    def reset(self):
        self.line = 0
        self.word = 0
        self.letter = 0
        self.render_text()
    
    def update(self, keys, player_rect):
        self.handle_input()
    
    def render_text(self):
        font = pygame.font.SysFont(None, 60)
        target_text_surface = font.render(self.text[self.line], True, (255, 255, 255, 255))
        screen.blit(target_text_surface, (ekraani_laius*0.1 + 20, ekraani_kõrgus - 70))
        
    def render_current_word(self):
        font = pygame.font.SysFont(None, 60)
        current_word_surface = font.render(self.text[self.line][self.word], True, (255, 255, 255, 255))
        current_word_rect = current_word_surface.get_rect(midtop=(player.rect.centerx, player.rect.y - 100))
        screen.blit(current_word_surface, current_word_rect)


    
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                pressed_key = pygame.key.name(event.key)
                if check_key_press(pressed_key, self.text[self.line][self.word][self.letter]):
                    if self.letter < len(self.text[self.line][self.word]) - 1:
                        self.letter += 1
                    elif self.word < len(self.text[self.line])-1:
                        self.word += 1
                        self.letter = 0
                    elif self.line < len(self.text)-1:
                        self.line += 1
                        self.word = 0
                        self.letter = 0
                    else:
                        global mängu_staatus
                        mängu_staatus = 'victory'
                else:
                    self.letter = 0
    
class TextSprite(pygame.sprite.Sprite):
    def __init__(self, text, font, color, position):
        super().__init__()
        self.image = font.render(text, True, color)
        self.rect = self.image.get_rect(midtop=position)

#Functions
def check_key_press(input, target_letter):
    if input.lower() == target_letter.lower():
        return True
    return False

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

#Initial sprites
player = Player('src/graphics/red.jpg')
title_text = TextSprite('Meie mäng', pygame.font.SysFont(None, 60), WHITE, (ekraani_laius // 2, ekraani_kõrgus // 2 - 50))
start_text = TextSprite('Press *Space* to Start', pygame.font.SysFont(None, 40), WHITE, (ekraani_laius // 2, ekraani_kõrgus // 2 + 20))
game_over_text = TextSprite('Game over\n The Demon has beaten you', pygame.font.SysFont(None, 60), WHITE, (ekraani_laius / 2, ekraani_kõrgus / 2 - 40))
restart_button = TextSprite('R to restart', pygame.font.SysFont(None, 40), WHITE, (ekraani_laius / 2, ekraani_kõrgus / 2 + 20))
pause_text = TextSprite('Paused', pygame.font.SysFont(None, 60), WHITE, (ekraani_laius / 2, ekraani_kõrgus / 2 - 40))
pause_resume = TextSprite('R to resume', pygame.font.SysFont(None, 40), WHITE, (ekraani_laius / 2, ekraani_kõrgus / 2 + 20))
pause_quit = TextSprite('Q to quit', pygame.font.SysFont(None, 40), WHITE, (ekraani_laius / 2, ekraani_kõrgus / 2 + 60))
victory = TextSprite('You bested the demon', pygame.font.SysFont(None, 60), WHITE, (ekraani_laius / 2, ekraani_kõrgus / 2 - 120))
score_text = TextSprite(f'It took you: {score} seconds', pygame.font.SysFont(None, 60), WHITE, (ekraani_laius / 2, ekraani_kõrgus / 2 - 40))
ritual = Background()
text = Chant('src/lvl1/chant.txt')

# Groups
character_sprites = pygame.sprite.Group()
start_menu_text = pygame.sprite.Group()
restart_menu_text = pygame.sprite.Group()
pause_menu_text = pygame.sprite.Group()
victory_text = pygame.sprite.Group()
backgrounds = pygame.sprite.Group()
chant = pygame.sprite.Group()


character_sprites.add(player)
start_menu_text.add(start_text, title_text)
restart_menu_text.add(game_over_text, restart_button)
pause_menu_text.add(pause_text, pause_resume, pause_quit)
victory_text.add(victory, score_text, restart_button, pause_quit)
backgrounds.add(ritual)
chant.add(text)


# Main game loop
while True:
    handle_events()
    keys = pygame.key.get_pressed()

    if mängu_staatus == "start_menu":
        screen.fill(BLACK)
        start_menu_text.draw(screen)

        if keys[pygame.K_SPACE]:
            mängu_staatus = "game"

    elif mängu_staatus == "game_over":
        screen.fill(TBLACK)
        restart_menu_text.draw(screen)
        if keys[pygame.K_r]:
            mängu_staatus = "game"
            score = 0
            player.reset()
            ritual.reset()
            text.reset()

    elif mängu_staatus == "paused_menu":
        screen.fill(TBLACK)
        pause_menu_text.draw(screen)
        if keys[pygame.K_q]:
            pygame.quit()
            sys.exit()
        if keys[pygame.K_r]:
            mängu_staatus = "game"

    elif mängu_staatus == "game":
        screen.fill('#3b1e20')
        backgrounds.update(keys, player.rect)
        backgrounds.draw(screen)
        player.update(keys)
        character_sprites.draw(screen)
        chant.update(keys, player.rect)
        chant.draw(screen)
        text.render_text()
        text.render_current_word()

        if keys[pygame.K_ESCAPE]:
            mängu_staatus = "paused_menu"
    
    elif mängu_staatus  == 'victory':
        screen.fill(TBLACK)
        victory_text.draw(screen)
        if keys[pygame.K_q]:
            pygame.quit()
            sys.exit()
        if keys[pygame.K_r]:
            mängu_staatus = "game"
            score = 0
            player.reset()
            ritual.reset()
            text.reset()
            

    pygame.display.update()
    score += 1/FPS
    clock.tick(FPS)