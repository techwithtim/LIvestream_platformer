from images import CRATE, SMALL_CRATE
from base_object import AbstractObject
import pygame


class Crate(AbstractObject):
    IMG = CRATE

    def __init__(self, x, y):
        super().__init__(x, y)
        self.small = False

    def collide(self, obj):
        current_mask = pygame.mask.from_surface(self.img)
        other_mask = pygame.mask.from_surface(obj.img)
        offset = obj.x - self.x, obj.y - self.y
        return current_mask.overlap(other_mask, offset)

class SmallCrate(Crate):
    IMG = SMALL_CRATE

    def __init__(self, x, y):
        super().__init__(x, y)
        self.small = True
    