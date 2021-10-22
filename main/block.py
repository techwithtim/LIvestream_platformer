import pygame
from base_object import AbstractObject


class Block(AbstractObject):
    def __init__(self, x, y, img, rotation=0):
        super().__init__(x, y)
        self.img = img.convert_alpha()
        self.rotation = rotation
        self.rotate_image()

    def rotate_image(self):
        self.img = pygame.transform.rotate(self.img, self.rotation)
