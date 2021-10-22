import pygame
import json
pygame.init()
pygame.font.init()

# GAME INFORMATION
TITLE = "Hugo The Huge"
MAX_FPS = 60

# WINDOW
WIDTH, HEIGHT = 1000, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)

from images import *
from player import Player
from block import Block
from crate import Crate
from platform import Platform
from spike import Spike
from door import Door

# COLORS
WHITE = (255, 255, 255)
BACKGROUND = BACKGROUND.convert_alpha()

# SCROLLING
MOVEMENT_BORDER_LEFT = 200
MOVEMENT_BORDER_RIGHT = 800
offset = 0

# LEVELS
LEVEL1 = "level1.json"
LEVEL2 = "level2.json"
LEVEL3 = "level3.json"
LEVELS = [LEVEL1, LEVEL2, LEVEL3]
current_level = 0

# FONTS
FONT_30 = pygame.font.SysFont('comicsans', 30)
FONT_90 = pygame.font.SysFont('comicsans', 90)

def blit_text_center(text, win, color):
    render = FONT_90.render(text, 1, color)
    win.blit(render, (WIDTH // 2 - render.get_width() // 2, HEIGHT // 2 - render.get_height() // 2))
    pygame.display.update()


def draw(win, player, objects, offset):
    win.blit(BACKGROUND, (0, 0))
    for block in objects:
        block.draw(win, offset)

    player.draw(win, offset)

    pygame.display.update()


def check_vertical_collision(player, objects):
    for block in objects:
        if abs(player.y - block.y) > 100 or abs(player.x - block.x) > 100:
            continue

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
        if abs(player.y - block.y) > 100 or abs(player.x - block.x) > 100:
            continue

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
        if abs(player.y - crate.y) > 100 or abs(player.x - crate.x) > 100:
            continue

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
            if player.action == "push":  # left
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
        if abs(player.y - block.y) > 100 or abs(player.x - block.x) > 100:
            continue

        result = player.collide(block)
        if not result:
            continue

        # check vertical collision
        if result[1] >= 32 and result[1] <= 50:
            player.fall()
            break
        elif result[1] >= 80 and not player.jumping:
            player.land(block)
            player.x += block.x_vel
            break


create_objects = {
    "floor": Block,
    "wall": Block,
    "crate": Crate,
    "platform": Platform,
    "spike": Spike,
    "door": Door
}

run = True

player = Player(100, 410, "left", WIDTH, HEIGHT)
clock = pygame.time.Clock()


def load_level(name):
    floors = []
    walls = []
    crates = []
    platforms = []
    spikes = []
    doors = []

    with open(name, "r") as json_file:
        level = json.load(json_file)["data"]


    for obj in level:
        x, y = round(obj['x']), round(obj['y'])
        create = obj["type"]
        if create == "floor":
            obj = Block(x, y, BLOCKS[0])
            floors.append(obj)
        elif create == "wall":
            obj = Block(x, y, BLOCKS[5])
            walls.append(obj)
        elif create == "crate":
            obj = Crate(x, y)
            crates.append(obj)
        elif create == "platform":
            obj = Platform(x, y)
            platforms.append(obj)
        elif create == "spike":
            obj = Spike(x, y)
            spikes.append(obj)
        elif create == "door":
            obj = Door(x, y)
            doors.append(obj)

    return floors, walls, crates, platforms, spikes, doors


floors, walls, crates, platforms, spikes, doors = load_level(LEVEL1)

objects = floors + walls + crates + platforms + spikes + doors

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
            draw(WIN, player, objects, offset)
            blit_text_center("You died... Try again!", WIN, (0, 0, 0))
            pygame.time.delay(3000)
            player.reset()

    for door in doors:
        if player.collide(door):
            if keys[pygame.K_w]:
                current_level += 1 
                load_level(LEVELS[current_level])
                break

    if player.x <= MOVEMENT_BORDER_LEFT:
        offset = player.x - MOVEMENT_BORDER_LEFT
    elif player.x + player.img[1].get_width() >= MOVEMENT_BORDER_RIGHT:
        offset = player.x - MOVEMENT_BORDER_RIGHT

    player.apply_gravity()

    draw(WIN, player, objects, offset)

pygame.quit()
