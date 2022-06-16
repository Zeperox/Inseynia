import pygame

class Brightness:
    def __init__(self, loc, size, brightness = 0, color = None):
        self._loc = loc
        self._brightness = brightness
        self._color = color

        self._surf = pygame.Surface(size)

        self._setup()
    
    @property
    def loc(self):
        return self._loc

    @loc.setter
    def loc(self, loc):
        self._loc = loc
        self._setup()

    @property
    def brightness(self):
        return self._brightness

    @brightness.setter
    def brightness(self, brightness):
        self._brightness = brightness
        self._setup()

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = color
        self._setup()

    @property
    def size(self):
        return self._surf.get_size()

    @size.setter
    def size(self, size):
        self._surf = pygame.Surface(size)
        self._setup()

    def _setup(self):
        if not self._color:
            if self._brightness < 0:
                self._surf.fill((0,0,0))
            elif self._brightness > 0:
                self._surf.fill((255,255,255))
        else:
            if self._color < 0:
                self._surf.fill((0,0,0))
            elif self._color > 0:
                self._surf.fill((255,255,255))
        self._surf.set_alpha(abs(self._brightness))

    def draw(self, window):
        window.blit(self._surf, self._loc)

if __name__ == "__main__":
    win = pygame.display.set_mode((800, 600))
    br = 0
    bright = Brightness((0, 0), (800, 600))
    op = "a"
    clock = pygame.time.Clock()
    
    while True:
        win.fill((128,128,128))
        pygame.draw.rect(win, (255, 0, 0), (300, 200, 200, 200))
        clock.tick(60)
        if br == 255:
            op = "m"
        elif br == -255:
            op = "a"

        if op == "m":
            br -= 1
        else:
            br += 1

        bright.brightness = br
        bright.draw(win)
        print(bright._surf.get_alpha())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        pygame.display.flip()
