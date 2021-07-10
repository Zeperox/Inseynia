import pygame
from pygame.locals import *
from .entity import Entity

class Drop(Entity):
    def __init__(self, x, y, drop):
        super().__init__(x, y, drop)
        self.rect = pygame.Rect(x-20, y-20, drop.get_width()+40, drop.get_height()+40)
