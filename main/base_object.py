import pygame


class AbstractObject:
    IMG = None

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = self.IMG

    def draw(self, win, offset):
        win.blit(self.img, (self.x - offset, self.y))

    def clicked(self, pos):
        rect = pygame.Rect(
            self.x, self.y, self.img.get_width(), self.img.get_height())
        return rect.collidepoint(pos)
