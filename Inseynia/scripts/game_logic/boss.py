import pygame, math, time, random
from pygame.locals import *

from .enemy import Enemy
from .projectiles import Projectiles
from scripts.assets.sprites import images

class Test_Boss(Enemy):
    def __init__(self, x, y, sprites_enemy):
        super().__init__(x, y, "Big Eye", sprites_enemy)
        self.attack_queue = []
        self.attack_change_timer = 0
        self.current_attack = None
        self.previous_attack = None

        self.proj_cooldown = 0

        self.movement_dir = [0, 2]
        self.offset = 0

        self.phase = 1

    def draw(self, window, scroll=[0, 0]):
        super().draw(window, scroll)
        
        pygame.draw.rect(window, (175,0,0), (window.get_width()*0.5-(window.get_width()-200)*0.5, window.get_height()-60, window.get_width()-200, 50))
        pygame.draw.rect(window, (0, 175, 0), (window.get_width()*0.5-(window.get_width()-200)*0.5, window.get_height()-60, (window.get_width()-200) * (self.stats["Health"]/self.stats["Max Health"]), 50))
        pygame.draw.rect(window, (200,200,200), (window.get_width()*0.5-(window.get_width()-200)*0.5-2, window.get_height()-60-2, window.get_width()-200+4, 54), 3)
        pygame.draw.rect(window, (1,1,1), (window.get_width()*0.5-(window.get_width()-200)*0.5-3, window.get_height()-60-3, window.get_width()-200+6, 56), 1)

    def ai(self, player, dt, _, map):
        self.collide =  True

        if self.stats["Health"] <= round(self.stats["Max Health"]*0.5):
            self.phase = 2
            self.entity = images["Big Eye 2"]

        if len(self.attack_queue) == 0:
            for _ in range(5):
                n = 3 if self.phase == 1 else 6
                self.attack_queue.append(random.randint(1, n))
                if self.attack_queue[-1] == 6 and random.randint(0, 1) == 0:
                    del self.attack_queue[-1]; self.attack_queue.append(random.randint(1, n-1))

        if time.time() - self.attack_change_timer >= random.uniform(5, 10):
            self.previous_attack = self.current_attack
            self.current_attack = self.attack_queue.pop(0)
            self.attack_change_timer = time.time()
            

        if self.current_attack == 1:
            proj_data = {
                "Proj Obj": "Fireball",
                "Speed": 3,
                "Proj Type": "normal",
                "Range": 1000,
                "End Destroy": True,
                "Collision Destroy": True
            }
            t = .5 if self.phase == 1 else .35
            if time.time() - self.proj_cooldown > t:
                self.x, self.y = random.randint(map.x, map.w), random.randint(map.y, map.h)
                n = 8 if self.phase == 1 else 12
                for x in range(n):
                    angle = math.radians(x*360/n)
                    self.projectiles.append(Projectiles(self.x+self.rect.width*0.5, self.y+self.rect.height*0.5, self.stats["Attack"], proj_data, ((self.x+self.rect.width*0.5)+100*math.cos(angle), (self.y+self.rect.height*0.5)+100*math.sin(angle))))
                    self.proj_cooldown = time.time()

        elif self.current_attack == 2:
            self.collide = False
            proj_data = {
                "Proj Obj": "Fireball",
                "Speed": 7 if self.phase == 1 else 10,
                "Proj Type": "normal",
                "Range": map.h+100,
                "End Destroy": True,
                "Collision Destroy": True
            }
            self.x, self.y = -self.rect.width, -self.rect.height
            if time.time() - self.proj_cooldown >= .5:
                n = 8 if self.phase == 1 else 20
                for _ in range(random.randint(3, n)):
                    x = random.randint(map.x, map.w)
                    self.projectiles.append(Projectiles(x, 1, self.stats["Attack"], proj_data, (x, map.h)))
                    self.proj_cooldown = time.time()

        elif self.current_attack == 3:
            t = .5 if self.phase == 1 else .25
            if time.time()-self.proj_cooldown >= t:
                proj_data = {
                    "Proj Obj": "Fireball",
                    "Speed": 5,
                    "Proj Type": "normal",
                    "Range": 1000,
                    "End Destroy": True,
                    "Collision Destroy": True
                }
                n = 12 if self.phase == 1 else 16
                for x in range(n):
                    angle = math.radians(x*360/n)
                    self.projectiles.append(Projectiles(self.x+self.rect.width*0.5, self.y+self.rect.height*0.5, self.stats["Attack"], proj_data, ((self.x+self.rect.width*0.5)+100*math.cos(angle), (self.y+self.rect.height*0.5)+100*math.sin(angle))))
                    self.proj_cooldown = time.time()

            if time.time() - self.attack_change_timer <= .3 and self.previous_attack != 3:
                self.x, self.y = map.x+map.w*0.5, map.y+map.h*0.5
            else:
                self.x += self.movement_dir[0]*dt
                self.y += self.movement_dir[1]*dt

            if math.dist((self.x, self.y), (map.x+map.w*0.5, map.y+map.h*0.5)) <= 1.5:
                x = random.randint(0, 3)
                s = 2 if self.phase == 1 else 5
                if x == 0:
                    self.movement_dir = [-s, 0]
                elif x == 1:
                    self.movement_dir = [s, 0]
                elif x == 2:
                    self.movement_dir = [0, -s]
                elif x == 3:
                    self.movement_dir = [0, s]

            if self.phase == 2 and (abs(self.movement_dir[0]) == 2 or abs(self.movement_dir[1]) == 2):
                if self.movement_dir[0] == -2:
                    self.movement_dir = [-7, 0]
                elif self.movement_dir[0] == 2:
                    self.movement_dir = [7, 0]
                elif self.movement_dir[1] == -2:
                    self.movement_dir = [0, -7]
                elif self.movement_dir[1] == 2:
                    self.movement_dir = [0, 7]
            
            if self.x <= map.x:
                self.movement_dir[0] = 2
            elif self.x >= map.x+map.w-self.rect.width:
                self.movement_dir[0] = -2
            if self.y <= map.y:
                self.movement_dir[1] = 2
            elif self.y >= map.y+map.h-self.rect.height:
                self.movement_dir[1] = -2

        elif self.current_attack == 4:
            angle = math.atan2(player.y - self.y, player.x - self.x)
            dx = math.cos(angle)*self.stats["Speed"]*dt
            dy = math.sin(angle)*self.stats["Speed"]*dt

            self.x += dx; self.y += dy

        elif self.current_attack == 5:
            self.x, self.y = map.x+map.w*0.5, map.y+map.h*0.5
            if time.time() - self.attack_change_timer <= .3 and self.previous_attack != 5:
                self.offset = 0
            if time.time()-self.proj_cooldown >= .25:
                proj_data = {
                    "Proj Obj": "Fireball",
                    "Speed": 5,
                    "Proj Type": "normal",
                    "Range": 1000,
                    "End Destroy": True,
                    "Collision Destroy": True
                }
                for x in range(16):
                    angle = math.radians(x*360/16)+self.offset
                    self.projectiles.append(Projectiles(self.x+self.rect.width*0.5, self.y+self.rect.height*0.5, self.stats["Attack"], proj_data, ((self.x+self.rect.width*0.5)+100*math.cos(angle), (self.y+self.rect.height*0.5)+100*math.sin(angle))))
                    self.proj_cooldown = time.time()
                self.offset += 0.1

        elif self.current_attack == 6:
            self.x, self.y = map.x+map.w*0.5, map.y+map.h*0.5
            if time.time()-self.proj_cooldown >= .25:
                proj_data = {
                    "Proj Obj": "Fireball",
                    "Speed": 5,
                    "Proj Type": "normal",
                    "Range": 1000,
                    "End Destroy": True,
                    "Collision Destroy": True
                }
                for x in range(5):
                    x -= 2
                    if x < 0:
                        angle = math.atan2(player.rect.centery - self.rect.centery, player.rect.centerx - self.rect.centerx)-math.radians(abs(x)*22.5)
                    elif x > 0:
                        angle = math.atan2(player.rect.centery - self.rect.centery, player.rect.centerx - self.rect.centerx)+math.radians(x*22.5)
                    else:
                        angle = math.atan2(player.rect.centery - self.rect.centery, player.rect.centerx - self.rect.centerx)
                    
                    self.projectiles.append(Projectiles(self.x+self.rect.width*0.5, self.y+self.rect.height*0.5, self.stats["Attack"], proj_data, ((self.x+self.rect.width*0.5)+100*math.cos(angle), (self.y+self.rect.height*0.5)+100*math.sin(angle))))
                    self.proj_cooldown = time.time()

            for projectile in self.projectiles:
                if math.dist((projectile.x, projectile.y), (self.rect.centerx, self.rect.centery)) >= 300 and not projectile.changed_loc:
                    projectile.changed_loc = True
                    projectile.end_loc = (player.rect.centerx, player.rect.centery); projectile.V_end = pygame.Vector2(projectile.end_loc)
                    projectile.start_loc = (projectile.x, projectile.y); projectile.V_start = pygame.Vector2(projectile.start_loc)

        self.rect.x, self.rect.y = self.x, self.y
