import pygame
from .entity import Entity

class Drop(Entity):
    def __init__(self, x: int, y: int, img: pygame.Surface):
        super().__init__(x, y, img)
        self.rect = pygame.Rect(x-20, y-20, img.get_width()+40, img.get_height()+40)
        
        # spirits only
        self.speed = 0