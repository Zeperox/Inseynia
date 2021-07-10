import pygame, json, os, time
from pygame.locals import *
from .entity import Entity

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

    def draw_bars(self, window, hpbar_loc:list):
        bar_font = pygame.font.SysFont("comicsans", 24)
        health_label = bar_font.render(f"{self.stats['Health']}/{self.stats['Max Health']}", 1, (255,255,255))

        pygame.draw.rect(window, (175,0,0), (hpbar_loc[0], hpbar_loc[1], 200, 25))
        pygame.draw.rect(window, (0,175,0), (hpbar_loc[0], hpbar_loc[1], 200 * (self.stats["Health"]/self.stats["Max Health"]), 25))
        pygame.draw.rect(window, (200,200,200), (hpbar_loc[0]-2, hpbar_loc[1]-2, 203, 27), 3)
        pygame.draw.rect(window, (0,0,0), (hpbar_loc[0]-3, hpbar_loc[1]-3, 205, 29), 1)
        window.blit(health_label, (((200*0.5)-(health_label.get_width()*0.5))+(hpbar_loc[0]), ((25*0.5)-(health_label.get_height()*0.5))+hpbar_loc[1]))

    def move(self, player_rect, dt, tiles):
        self.movement = [0, 0]
        if self.view_rect.colliderect(player_rect):
            if player_rect.x < self.x:
                self.movement[0] -= round(self.stats["Speed"]*dt)
            if player_rect.x > self.x:
                self.movement[0] += round(self.stats["Speed"]*dt)
            if player_rect.y < self.y:
                self.movement[1] -= round(self.stats["Speed"]*dt)
            if player_rect.y > self.y:
                self.movement[1] += round(self.stats["Speed"]*dt)
            
        s =  self.movement_collision(tiles)
        self.view_rect.x, self.view_rect.y = self.x+self.rect.width*0.5-self.stats["View Radius"], self.y+self.rect.height*0.5-self.stats["View Radius"]
        return s