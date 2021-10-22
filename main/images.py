from image_loader import load_player_sprites
import pygame
from os.path import join

PLAYER_WALK = load_player_sprites(
    join("main", "assets", "player", "walk-run", "normal", "walk"), 2)
PLAYER_RUN = load_player_sprites(
    join("main", "assets", "player", "walk-run", "normal", "run"), 2)
PLAYER_JUMP = load_player_sprites(
    join("main", "assets", "player", "walk-run", "normal", "jump"), 2)
PLAYER_PUSH = load_player_sprites(
    join("main", "assets", "player", "walk-run", "normal", "push"), 2)
PLAYER_STAND = load_player_sprites(
    join("main", "assets", "player", "walk-run", "normal", "stand"), 2)
PLAYER_FALLING = load_player_sprites(
    join("main", "assets", "player", "walk-run", "normal", "falling"), 2)

PLAYER_WALK_WEAPON = load_player_sprites(
    join("main", "assets", "player", "walk-run", "weapon", "walk_weapon"), 2)
PLAYER_RUN_WEAPON = load_player_sprites(
    join("main", "assets", "player", "walk-run", "weapon", "run_weapon"), 2)
PLAYER_JUMP_WEAPON = load_player_sprites(
    join("main", "assets", "player", "walk-run", "weapon", "jump_weapon"), 2)
PLAYER_PUSH_WEAPON = load_player_sprites(
    join("main", "assets", "player", "walk-run", "weapon", "push_weapon"), 2)
PLAYER_STAND_WEAPON = load_player_sprites(
    join("main", "assets", "player", "walk-run", "weapon", "stand_weapon"), 2)
PLAYER_FALLING_WEAPON = load_player_sprites(
    join("main", "assets", "player", "walk-run", "weapon", "falling_weapon"), 2)

PLAYER_ATTACK_CHOP = load_player_sprites(
    join("main", "assets", "player", "attack", "chop"), 2)

BACKGROUND = pygame.image.load(join("main", "assets", "background.png"))
BACKGROUND = pygame.transform.scale(BACKGROUND, (round(BACKGROUND.get_width(
) * 1.5), round(BACKGROUND.get_height() * 1.5)))

CRATE = pygame.image.load("main\\assets\\crate.png")
SMALL_CRATE = pygame.transform.scale(
    CRATE, (round(CRATE.get_width() * 0.25), round(CRATE.get_height() * 0.25)))
CRATE = pygame.transform.scale(
    CRATE, (round(CRATE.get_width() * 0.75), round(CRATE.get_height() * 0.75)))

DOOR = pygame.image.load(join("main", "assets", "door.png"))
DOOR = pygame.transform.scale(DOOR, (round(DOOR.get_width(
) * 0.25), round(DOOR.get_height() * 0.25)))

PLATFORM = pygame.image.load(join("main", "assets", "platform.png"))
PLATFORM = pygame.transform.scale(PLATFORM, (round(PLATFORM.get_width(
) * 0.6), round(PLATFORM.get_height() * 0.3)))

SPIKE = pygame.image.load(join("main", "assets", "spike.png"))
SPIKE = pygame.transform.scale(SPIKE, (round(SPIKE.get_width(
) * 0.5), round(SPIKE.get_height() * 0.5)))

TRAMPONLINE = [pygame.image.load(join("main", "assets", "jump", "jump1.png")), pygame.image.load(
    join("main", "assets", "jump", "jump2.png")), pygame.image.load(join("main", "assets", "jump", "jump3.png"))]

COIN = [pygame.image.load(join("main", "assets", "coin", "coin1.png")), pygame.image.load(
    join("main", "assets", "coin", "coin2.png")), pygame.image.load(join("main", "assets", "coin", "coin3.png"))]

# DEAD1 = pygame.image.load("main/assets/player/dead/dead.png")
DEAD2 = pygame.image.load(join("main", "assets", "player", "dead", "dead2.png"))

# DEAD1 = pygame.transform.scale(DEAD1, (round(DEAD1.get_width(
# ) * 2), round(DEAD1.get_height() * 2)))
DEAD2 = pygame.transform.scale(DEAD2, (round(DEAD2.get_width(
) * 2), round(DEAD2.get_height() * 2)))

DEAD = DEAD2

BLOCKS = [
]

for i in range(1, 12):
    file_path = join("main", "assets", "blocks", f"block{i}.png")
    image = pygame.image.load(file_path)
    image = pygame.transform.scale(
        image, (image.get_width() // 4, image.get_height() // 4))
    BLOCKS.append(image)
