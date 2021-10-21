class AbstractObject:
    IMG = None

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = self.IMG

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))
