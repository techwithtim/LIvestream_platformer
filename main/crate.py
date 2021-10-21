from images import CRATE

class Crate:
    IMG = CRATE

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = Crate.IMG

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))
