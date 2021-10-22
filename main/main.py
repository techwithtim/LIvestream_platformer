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


def draw(win, player, objects):
    win.blit(BACKGROUND, (0, 0))
    for block in objects:
        block.draw(win)

    player.draw(win)

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

        if result[0] >= block.img.get_width() * 2 - 10:
            player.bounce("right", block)
            break
        elif result[0] < player.img[1].get_width():
            player.bounce("left", block)
            break
    else:
        player.blocked_direction = None


def check_crate_collision(player, objects, walls):
    for crate in objects:
        result = player.collide(crate)
        if not result:
            continue

        if result[0] > crate.img.get_width() / 2:
            if player.action == "push":  # right
                crate.x += player.vel

                for wall in walls:
                    if crate.collide(wall):
                        crate.x -= player.vel
                        player.bounce("right", crate)
                        break
            else:
                player.bounce("right", crate)
            break
        elif result[0] < crate.img.get_width() / 2:
            if player.action == "push": # left
                crate.x -= player.vel
                
                for wall in walls:
                    if crate.collide(wall):
                        crate.x += player.vel
                        player.bounce("left", crate)
                        break
            else:
                player.bounce("left", crate)
            break


def check_platform_collision(player, objects):
    for block in objects:
        result = player.collide(block)
        if not result:
            continue

        # check vertical collision
        print(result[1])
        if result[1] >= 32 and result[1] <= 50:
            player.fall()
            break
        elif result[1] >= 80 and not player.jumping:
            player.land(block)
            player.x += block.x_vel
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

crates = [Crate(700, 570)]

for i in range((WIDTH // 38) + 1):
    bloc = Block(i * 38, 670, BLOCKS[0])
    floors.append(bloc)

platforms = [Platform(300, 500, 100, 0)]

spikes = []

door = Door(400, 600)

objects = floors + walls + crates + platforms + spikes + [door]

while run:
    clock.tick(MAX_FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

    keys = pygame.key.get_pressed()

    player.move(keys)
    player.handle_jump(keys)

    check_vertical_collision(player, floors)
    check_horizontal_collision(player, walls)
    check_crate_collision(player, crates, walls)
    check_platform_collision(player, platforms)

    for spike in spikes:
        if player.collide(spike):
            player.die()
            # TODO GAME IS OVER!

    if player.collide(door):
        if keys[pygame.K_w]:
            print("run")
            # next level
            pass

    player.apply_gravity()

    draw(WIN, player, objects)

pygame.quit()
