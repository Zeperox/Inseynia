import pygame
from pygame.locals import *

class Entity:
    def __init__(self, x, y, entity):
        self.x = x
        self.y = y
        self.movement = [0, 0]

        self.vel = [0, 0]
        self.friction = 0.2

        self.entity = entity
        self.rect = pygame.Rect(self.x, self.y, self.entity.get_width(), self.entity.get_height())

    def collision_test(self, tiles):
        hit_list = []
        for tile in tiles:
            if self.rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list

    def movement_collision(self, tiles, update_apos=True):
        collision_types = {"top": False, "bottom": False, "left": False, "right": False}
        self.rect.x += self.movement[0]
        hit_list = self.collision_test(tiles)
        for tile in hit_list:
            if self.movement[0] > 0:
                self.rect.right = tile.left
                collision_types["right"] = True
            if self.movement[0] < 0:
                self.rect.left = tile.right
                collision_types["left"] = True
        self.rect.y += self.movement[1]
        hit_list = self.collision_test(tiles)
        for tile in hit_list:
            if self.movement[1] > 0:
                self.rect.bottom = tile.top
                collision_types["bottom"] = True
            if self.movement[1] < 0:
                self.rect.top = tile.bottom
                collision_types["top"] = True

        if update_apos:
            self.x, self.y = self.rect.x, self.rect.y

        return collision_types

    def draw(self, window, scroll=[0, 0]):
        window.blit(self.entity, (self.x-scroll[0], self.y-scroll[1]))

    def collision(self, obj):
        return self.rect.colliderect(obj)
