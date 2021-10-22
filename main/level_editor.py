import pygame
import math
import json
from datetime import datetime
pygame.init()

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
MOVEMENT_BORDER_LEFT = 250
MOVEMENT_BORDER_RIGHT = 750
offset = 0

LOAD_LEVEL = "level2.json"
with open(LOAD_LEVEL, "r") as json_file:
    level = json.load(json_file)["data"]


def draw(win, objects, offset):
    win.blit(BACKGROUND, (0, 0))
    for name, block in objects:
        block.draw(win, offset)

    pygame.display.update()


def round_to_10(x, base=10):
    return base * round(x/base)


def save_objects(objects):
    data = set()

    for name, obj in objects:
        data.add((name, obj.x, obj.y))

    new_data = []
    for name, x, y in data:
        new_data.append({"type": name, "x": x, "y": y})

    name = LOAD_LEVEL  # f"level-{str(datetime.now()).replace(':', '-')}.json"
    with open(name, "w") as f:
        json.dump({"data": new_data}, f)


run = True

player = Player(700, 410, "left", WIDTH, HEIGHT)
clock = pygame.time.Clock()

objects = []


create_objects = {
    "floor": Block,
    "wall": Block,
    "crate": Crate,
    "platform": Platform,
    "spike": Spike,
    "door": Door
}

for obj in level:
    create = obj["type"]
    if create == "floor":
        obj = create_objects[create](obj["x"], obj["y"], BLOCKS[0])
    elif create == "wall":
        obj = create_objects[create](obj["x"], obj["y"], BLOCKS[5])
    else:
        obj = create_objects[create](obj["x"], obj["y"])

    objects.append((create, obj))


for i in range(-200, 200):
    floor = Block(i * 38, 670, BLOCKS[0])
    objects.append(("floor", floor))


create = None
while run:
    clock.tick(MAX_FPS)

    left, middle, right = 0, 0, 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

        if event.type == pygame.MOUSEBUTTONDOWN:
            left, middle, right = pygame.mouse.get_pressed()

    keys = pygame.key.get_pressed()

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
    if keys[pygame.K_m]:
        create = "move"

    if keys[pygame.K_RIGHT]:
        offset += 5
    if keys[pygame.K_LEFT]:
        offset -= 5

    pos = pygame.mouse.get_pos()
    x, y = pos
    x += offset

    if create == "move":
        left, middle, right = pygame.mouse.get_pressed()
        if left:
            for name, obj in objects:
                if obj.clicked((x, y)):
                    obj.x = x - obj.img.get_width()/2
                    obj.y = y - obj.img.get_height()/2
    elif left and create:
        x, y = round_to_10(x), round_to_10(y)
        if create == "floor":
            obj = create_objects[create](x, y, BLOCKS[0])
        elif create == "wall":
            obj = create_objects[create](x, y, BLOCKS[5])
        else:
            obj = create_objects[create](x, y)

        objects.append((create, obj))

    elif right:
        for name, obj in objects:
            if obj.clicked((x, y)):
                objects.remove((name, obj))
                break

    draw(WIN, objects, offset)

save_objects(objects)
pygame.quit()
