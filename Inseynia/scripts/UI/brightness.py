import pygame

class Brightness:
    def __init__(self, loc, size, brightness = 0, color = None):
        self.loc = loc
        self.brightness = brightness
        self.color = color

        self.surf = pygame.Surface(size)

        self._setup()

    def reconfigure(self, loc = None, size = None, brightness = None, color = None):
        if loc: self.loc = loc
        if brightness: self.brightness = brightness
        if color: self.color = color

        if size: self.surf = pygame.Surface(size)

        self._setup()

    def _setup(self):
        if not self.color:
            if self.brightness < 0:
                self.surf.fill((0,0,0))
            elif self.brightness > 0:
                self.surf.fill((255,255,255))
        else:
            if self.color < 0:
                self.surf.fill((0,0,0))
            elif self.color > 0:
                self.surf.fill((255,255,255))
        self.surf.set_alpha(abs(self.brightness))

    def draw(self, window):
        window.blit(self.surf, self.loc)
