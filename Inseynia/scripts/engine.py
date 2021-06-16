import pygame
from pygame.locals import *

class Entity:
    def __init__(self, x, y, entity):
        self.x = x
        self.y = y

        self.entity = entity
        self.rect = pygame.Rect(self.x, self.y, self.entity.get_width(), self.entity.get_height())

    def draw(self, window, scroll=[0, 0]):
        window.blit(self.entity, (self.x-scroll[0], self.y-scroll[1]))

    def collision(self, obj):
        return self.rect.colliderect(obj)
