import pygame, os
from pygame.locals import *

class Text:
    def __init__(self, x, y, text:str, font:str, size:int, color:tuple, background:tuple=None):
        self.x = x
        self.y = y
        self.text = text
        try:
            self.font = pygame.font.Font(font, size)
        except FileNotFoundError:
            self.font = pygame.font.SysFont(font, size)
        self.color = color
        self.background = background

    def render(self, window):
        if self.background:
            window.blit(self.font.render(self.text, 1, self.color, self.background), (self.x, self.y))
        else:
            window.blit(self.font.render(self.text, 1, self.color), (self.x, self.y))

    def get_width(self):
        if self.background:
            return self.font.render(self.text, 1, self.color, self.background).get_width()
        else:
            return self.font.render(self.text, 1, self.color).get_width()

    def get_height(self):
        if self.background:
            return self.font.render(self.text, 1, self.color, self.background).get_height()
        else:
            return self.font.render(self.text, 1, self.color).get_height()
        