import pygame
from images import *
from player import Player
from block import Block
from crate import Crate
from platform import Platform
from spike import Spike
from door import Door
pygame.init()

# GAME INFORMATION
TITLE = "Hugo The Huge"
MAX_FPS = 60

# WINDOW
WIDTH, HEIGHT = 1000, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)

# COLORS
WHITE = (255, 255, 255)
BACKGROUND = BACKGROUND.convert_alpha()

# SCROLLING
MOVEMENT_BORDER_LEFT = 250
MOVEMENT_BORDER_RIGHT = 750
offset = 0


def draw(win, objects, offset):
    win.blit(BACKGROUND, (0, 0))
    for block in objects:
        block.draw(win, offset)

    pygame.display.update()


run = True

player = Player(700, 410, "left", WIDTH, HEIGHT)
clock = pygame.time.Clock()

floors = []

walls = []

crates = []

platforms = []

spikes = []

door = []

objects = floors + walls + crates + platforms + spikes + door

while run:
    clock.tick(MAX_FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

    keys = pygame.key.get_pressed()

    create = None
    if keys[pygame.K_f]:
        create = "floor"
    if keys[pygame.K_w]:
        create = "wall"
    if keys[pygame.K_c]:
        create = "crate"
    if keys[pygame.K_p]:
        create = "platform"
    if keys[pygame.K_s]:
        create = "spike"
    if keys[pygame.K_d]:
        create = "door"

    if keys[pygame.K_RIGHT]:
        offset += 5
    if keys[pygame.K_LEFT]:
        offset -= 5

    pressed = pygame.mouse.get_pressed()
    if any(pressed):
        x, y = pygame.mouse.get_pos()
        

    draw(WIN, objects, offset)

pygame.quit()
