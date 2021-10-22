from images import *
import pygame

ACTIONS = {
    "normal": {
        "walk": PLAYER_WALK,
        "run": PLAYER_RUN,
        "jump": PLAYER_JUMP,
        "push": PLAYER_PUSH,
        "stand": PLAYER_STAND,
        "falling": PLAYER_FALLING
    },
    "weapon": {
        "walk": PLAYER_WALK_WEAPON,
        "run": PLAYER_RUN_WEAPON,
        "jump": PLAYER_JUMP_WEAPON,
        "push": PLAYER_PUSH_WEAPON,
        "stand": PLAYER_STAND_WEAPON,
        "falling": PLAYER_FALLING_WEAPON
    },
    "attack": {
        "chop": PLAYER_ATTACK_CHOP
    },
    "dead": [DEAD, DEAD, DEAD]
}


for key in ACTIONS:
    if key == "dead":
        continue

    for other_key in ACTIONS[key]:
        for lr in ACTIONS[key][other_key]:
            for i, layer in enumerate(ACTIONS[key][other_key][lr]):
                new_layer = []
                for item in layer:
                    img = item.convert_alpha()
                    new_layer.append(img)
                ACTIONS[key][other_key][lr][i] = new_layer


class Player:
    ACTIONS = ACTIONS

    WALK_VEL = 3
    RUN_VEL = 5
    GRAVITY = 6
    JUMP_VEL = 15
    BIG_FACTOR = 2

    def __init__(self, x, y, direction, window_width=0, window_height=0):
        self.x = self.start_x = x
        self.y = self.start_y = y
        self.window_width = window_width
        self.window_height = window_height

        self.direction = self.starting_direction = direction
        self.action = "run"
        self.action_type = "weapon"

        self.animation_count = 0
        self.frame_duration = 5
        self.img = None
        self.vel = self.WALK_VEL

        self.jumping = False
        self.jump_count = 0
        self.jump_duration = 20

        self.grounded = False
        self.blocked_direction = None

        self.big = False
        self.set_image()

    def land(self, obj):
        self.jumping = False
        self.jump_count = 0
        if self.action == "falling":
            self.action = "stand"
        while (result := self.collide(obj)):
            if result[1] < obj.img.get_height() / 2:
                break
            self.y -= 1
        self.y += 1
        self.grounded = True

    def die(self):
        self.action = "dead"
        self.set_image()

    def reset(self):
        self.x = self.start_x
        self.y = self.start_y
        self.jumping = False
        self.jump_count = 0
        self.jump_duration = 20
        self.vel = self.WALK_VEL

        self.grounded = False
        self.blocked_direction = None

        self.direction = self.starting_direction
        self.action = "run"
        self.action_type = "weapon"

        self.big = False

    def toggle_big(self):
        self.big = not self.big

    def fall(self):
        self.jumping = False
        self.jump_count = 0
        if not self.action_type == "attack":
            self.action = "falling"
        self.grounded = False

    def apply_gravity(self):
        if not self.grounded:
            self.y += self.GRAVITY
        elif self.jump_count == 0 and self.action == "falling":
            self.action = "stand"

    def set_image(self):
        if self.action == "dead":
            self.img = self.ACTIONS["dead"]
        else:
            action = self.ACTIONS[self.action_type][self.action][self.direction]
            flip = False
            if self.action == "push" and self.direction == "right":
                flip = True
                action = self.ACTIONS[self.action_type][self.action]["left"]

            if self.animation_count // self.frame_duration >= len(action[1]):
                self.animation_count = 0

                if self.jumping:
                    self.action = "falling"

                if self.action_type == "attack":
                    self.action_type = "weapon"
                    self.action = "stand"

            self.img = [layer[self.animation_count//self.frame_duration]
                        for layer in action if layer]

            if flip:
                new_img = []
                for image in self.img:
                    image = pygame.transform.flip(image, True, False)
                    new_img.append(image)
                self.img = new_img

        if self.big:
            new_img = []
            for image in self.img:
                image = pygame.transform.scale(image, (round(image.get_width(
                ) * self.BIG_FACTOR), round(image.get_height() * self.BIG_FACTOR)))
                new_img.append(image)
            self.img = new_img

    def draw(self, win, offset):
        for layer in self.img:
            win.blit(layer, (self.x - offset, self.y))

        self.animation_count += 1
        self.set_image()

    def bounce(self, direction, obj):
        self.blocked_direction = direction

    def move(self, keys):
        if self.action == "dead":
            return

        prev_action, prev_direction = self.action, self.direction

        self.handle_attack()

        if keys[pygame.K_a] and self.blocked_direction != "left":  # left
            if self.action not in ["push",  "jump", "falling"] and self.action_type != "attack":
                self.action = "walk"
            self.direction = "left"
            self.x -= self.vel
        elif keys[pygame.K_d] and self.blocked_direction != "right":  # right
            if self.action not in ["push", "jump",  "falling"] and self.action_type != "attack":
                self.action = "walk"
            self.direction = "right"
            self.x += self.vel
        elif self.action_type != "attack" and not self.action in ["jump", "falling"]:
            self.action = "stand"

        if keys[pygame.K_LSHIFT] and self.action in ["walk", "run"]:  # run
            self.action = "run"
            self.vel = self.RUN_VEL

        if self.jumping:
            return

        if keys[pygame.K_f] and self.action_type != "attack":
            self.action = "push"

        if self.action != prev_action or self.direction != prev_direction:
            self.animation_count = 0

    def handle_jump(self, keys):
        if self.jumping:
            self.jump_count += 1
            self.y -= self.JUMP_VEL
            if self.jump_count >= self.jump_duration:
                self.jumping = False
                self.jump_count = 0
        elif keys[pygame.K_SPACE] and self.grounded and self.action_type != "attack":
            self.action = "jump"
            self.jumping = True
            self.jump_count = 1
            self.grounded = False

    def handle_attack(self):
        pressed = pygame.mouse.get_pressed()

        if any(pressed) and not self.action_type == "attack":
            self.action_type = "attack"
            self.action = "chop"

    def collide(self, obj):
        current_mask = pygame.mask.from_surface(self.img[1])
        other_mask = pygame.mask.from_surface(obj.img)
        offset = obj.x - self.x, obj.y - self.y
        return current_mask.overlap(other_mask, offset)
