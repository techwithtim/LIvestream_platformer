import pygame
from images import *
from player import Player
from block import Block
from crate import Crate
from platform import Platform
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


def draw(win, player, objects):
    win.blit(BACKGROUND, (0, 0))
    player.draw(win)
    for block in objects:
        block.draw(win)

    pygame.display.update()


def check_vertical_collision(player, objects):
    for block in objects:
        result = player.collide(block)
        if not result:
            continue

        # check vertical collision
        if result[1] < block.img.get_height():
            player.fall()
            break
        elif result[1] >= block.img.get_height() / 2 and not player.jumping:
            player.land(block)
            break
    else:
        if not player.jumping:
            player.fall()


def check_horizontal_collision(player, objects):
    for block in walls:
        result = player.collide(block)
        if not result:
            continue

        if result[0] > block.img.get_width() * 2:
            player.bounce("right", block)
            break
        elif result[0] < player.img[1].get_width():
            player.bounce("left", block)
            break
    else:
        player.blocked_direction = None


def check_crate_collision(player, objects):
    for crate in objects:
        result = player.collide(crate)
        if not result:
            continue

        if result[0] > crate.img.get_width() / 2:
            if player.action == "push":
                crate.x += player.vel
            else:
                player.bounce("right", crate)
            break
        elif result[0] < crate.img.get_width() / 2:
            if player.action == "push":
                crate.x -= player.vel
            else:
                player.bounce("left", crate)
            break


run = True

player = Player(700, 410, "left", WIDTH, HEIGHT)
clock = pygame.time.Clock()

floors = [
    Block(100, 530, BLOCKS[0]),
    Block(140, 530, BLOCKS[0]),
    Block(180, 530, BLOCKS[0]),
    Block(300, 550, BLOCKS[0], 90)
]

walls = [Block(300, 570, BLOCKS[0], 90),
         Block(300, 610, BLOCKS[0], 90)]

crates = []

for i in range((WIDTH // 38) + 1):
    bloc = Block(i * 38, 670, BLOCKS[0])
    floors.append(bloc)

platforms = [Platform(300, 500, 100, 0)]

objects = floors + walls + crates + platforms

while run:
    clock.tick(MAX_FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

    keys = pygame.key.get_pressed()

    player.move(keys)
    player.handle_jump(keys)

    check_vertical_collision(player, floors + platforms)
    check_horizontal_collision(walls)
    check_crate_collision(crate)

    player.apply_gravity()

    draw(WIN, player, objects)
