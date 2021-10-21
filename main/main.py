import pygame
from images import *
from player import Player
from block import Block
from crate import Crate

# GAME INFORMATION
TITLE = "Hugo The Huge"
MAX_FPS = 60

# COLORS
WHITE = (255, 255, 255)

# WINDOW
WIDTH, HEIGHT = 900, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)


def draw(win, player, objects):
    win.blit()
    player.draw(win)
    for block in objects:
        block.draw(win)

    pygame.display.update()


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

crates = [Crate(500, 550)]

for i in range((WIDTH // 38) + 1):
    bloc = Block(i * 38, 652, BLOCKS[0])
    floors.append(bloc)

objects = floors + walls + crates

while run:
    clock.tick(MAX_FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

    keys = pygame.key.get_pressed()

    for block in floors:
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

    for crate in crates:
        result = player.collide(crate)
        if not result:
            continue

        if result[0] > crate.img.get_width() / 2:
            if player.action == "push":
                crate.x += player.vel
            break
        elif result[0] < crate.img.get_width() / 2:
            if player.action == "push":
                crate.x -= player.vel
            break

    player.move(keys)
    player.handle_jump(keys)

    player.apply_gravity()

    draw(WIN, player, objects)
