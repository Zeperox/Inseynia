import pygame, math, time, random
from pygame.locals import *

from .entity import Entity
from scripts.data.json_functions import load_json
from .projectiles import *

class Enemy(Entity):
    def __init__(self, x, y, name, sprites_Enemies):
        super().__init__(x, y, sprites_Enemies[name])
        enemies = load_json(["scripts", "data", "enemies.json"])
        self.name = name
        self.stats = enemies[name]

        self.view_rect = pygame.Rect(x+self.rect.width*0.5-self.stats["View Radius"], y+self.rect.height*0.5-self.stats["View Radius"], self.stats["View Radius"]*2, self.stats["View Radius"]*2)
        self.unview_follow_timer = 0
        self.target = None

    def lose_hp(self, hp, enemies):
        if time.time() - self.i_frame_time >= self.i_frame_length:
            dmg = round(hp*hp/(hp+self.stats["Defense"]))
            if dmg == 0: dmg = 1

            self.stats["Health"] -= dmg
            self.i_frame_time = time.time()
            if self.stats["Health"] <= 0:
                enemies.remove(self)
        return enemies

class Ranged_Enemy(Enemy):
    def __init__(self, x, y, sprites_Enemies):
        super().__init__(x, y, "Ranged Enemy", sprites_Enemies)
        self.ai_type = "Archer"
        self.strafe_dir = 0
        self.strafe_timer = 0
        self.projectile_timer = 0

    def ai(self, player, dt, tiles, game_map):
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
            if math.dist((self.x+self.rect.width*0.5, self.y+self.rect.height*0.5), (player.x+player.rect.width*0.5, player.y+player.rect.height*0.5)) < 100:
                angle = math.atan2(player.y - self.y, player.x - self.x)
                dx = -math.cos(angle)*self.stats["Speed"]*dt
                dy = -math.sin(angle)*self.stats["Speed"]*dt
            elif math.dist((self.x+self.rect.width*0.5, self.y+self.rect.height*0.5), (player.x+player.rect.width*0.5, player.y+player.rect.height*0.5)) > 300:
                angle = math.atan2(player.y - self.y, player.x - self.x)
                dx = math.cos(angle)*self.stats["Speed"]*dt
                dy = math.sin(angle)*self.stats["Speed"]*dt
            else:
                angle = math.atan2(player.y - self.y, player.x - self.x)
                if self.strafe_dir:
                    dx = math.sin(angle)*self.stats["Speed"]*dt
                    dy = -math.cos(angle)*self.stats["Speed"]*dt
                else:
                    dx = -math.sin(angle)*self.stats["Speed"]*dt
                    dy = math.cos(angle)*self.stats["Speed"]*dt

                if time.time() - self.strafe_timer >= random.uniform(1.0, 2.0):
                    self.strafe_dir = random.randint(0, 1)
                    self.strafe_timer = time.time()
            self.target = [player.x, player.y]
            self.unview_follow_timer = time.time()

            if time.time()-self.projectile_timer >= .5:
                proj_data = {
                    "Proj Obj": "Arrow",
                    "Speed": 3,
                    "Proj Type": "normal",
                    "Range": 200,
                    "End Destroy": True,
                    "Collision Destroy": True
                }
                for x in range(3):
                    x -= 1
                    if x < 0:
                        angle = math.atan2(player.rect.centery - self.rect.centery, player.rect.centerx - self.rect.centerx)-math.radians(abs(x)*22.5)
                    elif x > 0:
                        angle = math.atan2(player.rect.centery - self.rect.centery, player.rect.centerx - self.rect.centerx)+math.radians(x*22.5)
                    else:
                        angle = math.atan2(player.rect.centery - self.rect.centery, player.rect.centerx - self.rect.centerx)
                    
                    self.projectiles.append(Projectiles(self.x+self.rect.width*0.5, self.y+self.rect.height*0.5, self.stats["Attack"], proj_data, ((self.x+self.rect.width*0.5)+100*math.cos(angle), (self.y+self.rect.height*0.5)+100*math.sin(angle))))
                    self.projectile_timer = time.time()

        else:
            if time.time()-self.unview_follow_timer <= self.stats["Unview Follow Time"]:
                angle = math.atan2(self.target[1] - self.y, self.target[0] - self.x)
                dx = math.cos(angle)*self.stats["Speed"]*dt
                dy = math.sin(angle)*self.stats["Speed"]*dt
                
            
        self.movement[1] += dy
        self.movement[0] += dx
        self.x += self.movement[0]; self.y += self.movement[1]
        self.rect.x, self.rect.y = self.x, self.y
            
        return self.movement_collision(tiles, update_apos=False, update_rect=False)

class Test_Enemy(Enemy):
    def __init__(self, x, y, sprites_Enemies):
        super().__init__(x, y, "Test Enemy", sprites_Enemies)
        self.ai_type = "Follower"

    def ai(self, player, dt, tiles, game_map):
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
            self.target = [player.x, player.y]
            angle = math.atan2(player.y - self.y, player.x - self.x)
            dx = math.cos(angle)*self.stats["Speed"]*dt
            dy = math.sin(angle)*self.stats["Speed"]*dt
            self.unview_follow_timer = time.time()
        else:
            if time.time()-self.unview_follow_timer <= self.stats["Unview Follow Time"]:
                angle = math.atan2(self.target[1] - self.y, self.target[0] - self.x)
                dx = math.cos(angle)*self.stats["Speed"]*dt
                dy = math.sin(angle)*self.stats["Speed"]*dt
                
            
        self.movement[1] += dy
        self.movement[0] += dx
        self.x += self.movement[0]; self.y += self.movement[1]
        self.rect.x, self.rect.y = self.x, self.y
            
        return self.movement_collision(tiles, update_apos=False, update_rect=False)
