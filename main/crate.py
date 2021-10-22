from images import CRATE
from base_object import AbstractObject
import pygame


class Crate(AbstractObject):
    IMG = CRATE

    def collide(self, obj):
        current_mask = pygame.mask.from_surface(self.img)
        other_mask = pygame.mask.from_surface(obj.img)
        offset = obj.x - self.x, obj.y - self.y
        return current_mask.overlap(other_mask, offset)
