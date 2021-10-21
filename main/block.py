import pygame


class Block:
    def __init__(self, x, y, img, rotation=0):
        self.x = x
        self.y = y
        self.img = img
        self.rotation = rotation
        self.rotate_image()

    def rotate_image(self):
        self.img = pygame.transform.rotate(self.img, self.rotation)

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))
