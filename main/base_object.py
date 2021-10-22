class AbstractObject:
    IMG = None

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = self.IMG

    def draw(self, win, offset):
        win.blit(self.img, (self.x - offset, self.y))

    def __repr__(self):
        return self.__name__

    def clicked(self, pos):
        current_mask = pygame.mask.from_surface(self.img)
        offset = pos[0] - self.x, pos[1] - self.y
        return current_mask.get_at(offset) != None
