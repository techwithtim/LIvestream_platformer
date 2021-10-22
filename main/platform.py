from images import PLATFORM
from base_object import AbstractObject


class Platform(AbstractObject):
    IMG = PLATFORM
    VEL = 2

    def __init__(self, x, y, horizontal_travel=150, vertical_travel=0):
        self.start_x = self.x = x
        self.start_y = self.y = y
        self.x_vel = self.VEL
        self.y_vel = self.VEL
        self.horizontal_travel = horizontal_travel
        self.vertical_travel = vertical_travel
        self.img = self.IMG.convert_alpha()

    def move(self):
        if abs(self.start_x - (self.x + self.x_vel)) >= self.horizontal_travel:
            self.x_vel *= - 1

        if self.horizontal_travel != 0:
            self.x += self.x_vel

        if abs(self.start_y - (self.y + self.y_vel)) >= self.vertical_travel:
            self.y_vel *= - 1

        if self.vertical_travel != 0:
            self.y += self.y_vel

    def draw(self, win, offset):
        win.blit(self.img, (self.x - offset, self.y))
        self.move()
