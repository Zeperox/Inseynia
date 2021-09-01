from .entity import Entity
import pygame, math
from pygame.locals import *
from scripts.assets.sprites import sprites_Proj

class Projectiles(Entity):
    def __init__(self, x, y, attack, attack_type, speed, end_loc, image):
        self.start_loc = (x, y)
        self.end_loc = end_loc

        self.rotation = math.atan2(self.start_loc[1]-self.end_loc[1], self.end_loc[0]-self.start_loc[0]); self.rotation = math.degrees(self.rotation)

        self.img = pygame.transform.rotate(image, self.rotation)

        super().__init__(x, y, self.img)
        self.attack = attack
        self.speed = speed
        self.attack_type = attack_type

        self.V_start = pygame.Vector2(self.start_loc)
        self.V_end = pygame.Vector2(self.end_loc)

        self.rect = pygame.Rect(x, y, image.get_width(), image.get_height())
        self.start = False

    def draw(self, window, scroll, player_rect):
        if not self.rect.colliderect(player_rect):
            self.start = True
        if self.start:
            super().draw(window, scroll)

    def move(self, tiles, dt, mouse_pos=None, entities=[]):
        self.movement = [0, 0]
        if self.attack_type == "normal":
            vel = (self.V_end - self.V_start).normalize()*self.speed
            self.movement[0] += vel.x*dt; self.movement[1] += vel.y*dt
            
        elif self.attack_type == "mouse follow":
            vel = (pygame.Vector2(mouse_pos) - pygame.Vector2(self.x, self.y)).normalize()*self.speed
            self.movement[0] += vel.x*dt; self.movement[1] += vel.y*dt

        elif self.attack_type == "nearest follow":
            if len(entities) > 0:
                entity_dist = []
                for entity in entities:
                    entity_dist.append(math.dist([self.x, self.y], [entity.x, entity.y]))
                i = entity_dist.index(min(entity_dist))
                vel = (pygame.Vector2(entities[i].x, entities[i].y) - pygame.Vector2(self.x, self.y)).normalize()*self.speed
                self.movement[0] += vel.x*dt; self.movement[1] += vel.y*dt
            else:
                vel = (self.V_end - self.V_start).normalize()*self.speed
                self.movement[0] += vel.x*dt; self.movement[1] += vel.y*dt

        self.x += self.movement[0]; self.y += self.movement[1]
        self.rect.x, self.rect.y = self.x, self.y
        self.movement_collision(tiles, False, False)

class Arrow(Projectiles):
    def __init__(self, x, y, attack, attack_type, speed, end_loc):
        super().__init__(x, y, attack, attack_type, speed, end_loc, sprites_Proj["Arrow"])