import pygame, json, os, math
from pygame.locals import *

from .entity import Entity
from scripts.UI.text import Text

def load_json(location_list:list):
    location = location_list[0]
    for location_entry in location_list[1:]:
        location = os.path.join(location, location_entry)

    with open(location, "r") as f:
        return json.load(f)

class Enemy(Entity):
    def __init__(self, x, y, name, sprites_Enemies):
        super().__init__(x, y, sprites_Enemies[name])
        enemies = load_json(["scripts", "data", "enemies.json"])
        self.name = name
        self.stats = enemies[name]
        self.in_fight = False
        self.view_rect = pygame.Rect(x+self.rect.width*0.5-self.stats["View Radius"], y+self.rect.height*0.5-self.stats["View Radius"], self.stats["View Radius"]*2, self.stats["View Radius"]*2)

        #self.hp_text = Text(0, 0, f"{self.stats['Health']}/{self.stats['Max Health']}", os.path.join("assets", "Fonts", "DefaultFont.TTF"), int(25*0.5), (255,255,255))
        #self.hp_text = Text(0, 0, f"{self.stats['Health']}/{self.stats['Max Health']}", os.path.join("assets", "Fonts", "Font.png"), (255,255,255))

    '''def move(self, player_rect, dt, tiles):
        self.view_rect.center = self.rect.center

        self.movement = [0, 0]
        for index in range(2):
            if self.vel[index] > 0:
                if self.vel[index] - self.friction*dt < 0:
                    self.vel[index] = 0
                else:
                    self.vel[index] -= self.friction*dt
            elif self.vel[index] < 0:
                if self.vel[index] + self.friction*dt > 0:
                    self.vel[index] = 0
                else:
                    self.vel[index] += self.friction*dt

        if self.view_rect.colliderect(player_rect):
            if player_rect.x < self.x:
                if self.vel[0] > -2:
                    self.vel[0] -= 0.3*dt
            if player_rect.x > self.x:
                if self.vel[0] < 2:
                    self.vel[0] += 0.3*dt
            if player_rect.y < self.y:
                if self.vel[1] > -2:
                    self.vel[1] -= 0.3*dt
            if player_rect.y > self.y:
                if self.vel[1] < 2:
                    self.vel[1] += 0.3*dt
        self.movement[1] += round(self.vel[1]*dt)
        self.movement[0] += round(self.vel[0]*dt)
            
        return self.movement_collision(tiles)'''

class Test_Enemy(Enemy):
    def __init__(self, x, y, sprites_Enemies):
        super().__init__(x, y, "Test Enemy", sprites_Enemies)
        self.ai_type = "Follower"

    def draw(self, window, scroll):
        super().draw(window, scroll)
        pygame.draw.rect(window, (255,0,0), (self.view_rect.x-scroll[0], self.view_rect.y-scroll[1], self.view_rect.width, self.view_rect.height), 2)

    def ai(self, player, dt, tiles):
        self.view_rect.center = self.rect.center
        dx, dy = 0, 0

        self.movement = [0, 0]
        for index in range(2):
            if self.vel[index] > 0:
                if self.vel[index] - self.friction*dt < 0:
                    self.vel[index] = 0
                else:
                    self.vel[index] -= self.friction*dt
            elif self.vel[index] < 0:
                if self.vel[index] + self.friction*dt > 0:
                    self.vel[index] = 0
                else:
                    self.vel[index] += self.friction*dt

        if self.view_rect.colliderect(player.rect):
            angle = math.atan2(player.y - self.y, player.x - self.x)
            dx = math.cos(angle)*self.stats["Speed"]*dt
            dy = math.sin(angle)*self.stats["Speed"]*dt
            
        self.movement[1] += dy
        self.movement[0] += dx
        self.x += self.movement[0]; self.y += self.movement[1]
        self.rect.x, self.rect.y = self.x, self.y
            
        #return self.movement_collision(tiles, update_apos=False)