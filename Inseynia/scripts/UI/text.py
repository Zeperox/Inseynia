import pygame
from pygame.locals import *

class Text:
    def __init__(self, x, y, text, font, size, color, background=None):
        self.x = x
        self.y = y
        self._text = text
        self._size = size
        self._font_name = font
        try:
            self._font = pygame.font.Font(font, size)
        except FileNotFoundError:
            self._font = pygame.font.SysFont(font, size)
        self._color = color
        self._background = background

        if self._background:
            self._text_surf = self._font.render(self._text, True, self._color, self._background)
        else:
            self._text_surf = self._font.render(self._text, True, self._color)

    @property
    def text(self):
        return self._text
    
    @text.setter
    def text(self, text):
        self._text = text
        if self._background:
            self._text_surf = self._font.render(self._text, True, self._color, self._background)
        else:
            self._text_surf = self._font.render(self._text, True, self._color)
    
    @property
    def size(self):
        return self._size
    
    @size.setter
    def size(self, size):
        self._size = size
        try:
            self._font = pygame.font.Font(self._font_name, self._size)
        except FileNotFoundError:
            self._font = pygame.font.SysFont(self._font_name, self._size)
        if self._background:
            self._text_surf = self._font.render(self._text, True, self._color, self._background)
        else:
            self._text_surf = self._font.render(self._text, True, self._color)
    
    @property
    def font(self):
        return self._font_name
    
    @font.setter
    def font(self, font):
        self._font_name = font
        try:
            self._font = pygame.font.Font(self._font_name, self._size)
        except FileNotFoundError:
            self._font = pygame.font.SysFont(self._font_name, self._size)
        if self._background:
            self._text_surf = self._font.render(self._text, True, self._color, self._background)
        else:
            self._text_surf = self._font.render(self._text, True, self._color)
    
    @property
    def color(self):
        return self._color
    
    @color.setter
    def color(self, color):
        self._color = color
        if self._background:
            self._text_surf = self._font.render(self._text, True, self._color, self._background)
        else:
            self._text_surf = self._font.render(self._text, True, self._color)
    
    @property
    def background(self):
        return self._background
    
    @background.setter
    def background(self, background):
        self._background = background
        if self._background:
            self._text_surf = self._font.render(self._text, True, self._color, self._background)
        else:
            self._text_surf = self._font.render(self._text, True, self._color)
    
    

    def render(self, window, scroll=[0, 0]):
        window.blit(self._text_surf, (self.x-scroll[0], self.y-scroll[1]))

    def get_width(self):
        return self._text_surf.get_width()

    def get_height(self):
        return self._text_surf.get_height()
        