import pygame, random, os, time
from .projectiles import *
from scripts.data.json_functions import load_json
from scripts.assets.sprites import sprites_Proj

class Player(Entity):
    gender = random.choice(["male", "female"])
    Pclass = ["", None]
    difficulty = ""
    name = ""
    inventory = [[], [], [], [], [], [], [], [], [], []]
    equipment = ["Fist", "No Shield"]
    stats = {
        "Health": 10,
        "Max Health": 10,
        "Attack": [1, None],
        "Defense": 2,
        "Extra Stats": [10, None],
        "Max Extra Stats": [10, None],
        "Money": 100,
        "XP": 0,
        "Level": 1,
        "Speed": 5
    }
    location = None
    xp = 0
    max_xp = 3
    directions = {
        "Up": None,
        "Down": None,
        "Right": None,
        "Left": None
    }
    
    def __init__(self, x, y, direction):
        super().__init__(x, y, pygame.Surface((1, 1)))
        self.img = self.directions[direction]

        self.saved_health = [self.stats["Health"], self.stats["Max Health"]]
        self.saved_exrta = [[self.stats["Extra Stats"][0], self.stats["Max Extra Stats"][0]], [self.stats["Extra Stats"][1], self.stats["Max Extra Stats"][1]]]
        self.direction = "Down"

        self.vel = [0, 0]
        self.friction = 0.2

        # Combat
        self.strong_wind = 0
        self.strong_charging = False
        self.strong_charged = False
        self.attack_cooldown = [0, 0]

        self.projectiles = []

        #self.rect = pygame.Rect(self.x, self.y, self.get_width(), self.get_height())
        self.rect = pygame.Rect(self.x, self.y, 38, 40)

        self.bars_surf = pygame.Surface((205, 108)).convert()
        self.bars_surf.set_colorkey((0,0,0))
        self.generate_bars()
    
    def generate_bars(self):
        bar_font = pygame.font.Font(os.path.join("assets", "Fonts", "DefaultFont.TTF"), int(25*0.5))
        health_label = bar_font.render(f"{self.stats['Health']}/{self.stats['Max Health']}", 1, (255,255,255))

        chealth = (0,175,0)
        cstats = []
        labels = []
        for x in range(2):
            if self.Pclass[x]:
                if self.Pclass[x] == "Swordsman":
                    labels.append(bar_font.render(f"{self.stats['Extra Stats'][x]}/{self.stats['Max Extra Stats'][x]}", 1, (255,255,255)))
                    cstats.append((175,175,0))
                elif self.Pclass[x] == "Archer":
                    labels.append(bar_font.render(f"{self.stats['Extra Stats'][x]}/{self.stats['Max Extra Stats'][x]}", 1, (255,255,255)))
                    cstats.append((175,88,0))
                elif self.Pclass[x] == "Mage":
                    labels.append(bar_font.render(f"{self.stats['Extra Stats'][x]}/{self.stats['Max Extra Stats'][x]}", 1, (255,255,255)))
                    cstats.append((0,0,175))

        pygame.draw.rect(self.bars_surf, (175,0,0), (3, 3, 200, 25))
        pygame.draw.rect(self.bars_surf, chealth, (3, 3, 200 * (self.stats["Health"]/self.stats["Max Health"]), 25))
        pygame.draw.rect(self.bars_surf, (200,200,200), (1, 1, 203, 27), 3)
        pygame.draw.rect(self.bars_surf, (1,1,1), (0, 0, 205, 29), 1)
        self.bars_surf.blit(health_label, (((200*0.5)-(health_label.get_width()*0.5))+(0), ((25*0.5)-(health_label.get_height()*0.5))+0))

        for x in range(2):
            if self.Pclass[x]:
                pygame.draw.rect(self.bars_surf, (175,0,0), (3, 38+(39*x), 200, 25))
                pygame.draw.rect(self.bars_surf, cstats[x], (3, 38+(39*x), 200 * (self.stats["Extra Stats"][x]/self.stats["Max Extra Stats"][x]), 25))
                pygame.draw.rect(self.bars_surf, (200,200,200), (1, 36+(39*x), 203, 27), 3)
                pygame.draw.rect(self.bars_surf, (1,1,1), (0, 35+(39*x), 205, 29), 1)
                self.bars_surf.blit(labels[x], (((200*0.5)-(labels[x].get_width()*0.5))+(0), ((25*0.5)-(labels[x].get_height()*0.5))+35+(39*x)))

    def draw(self, window, screen_size, scroll=[0, 0]):
        #super().draw(window, scroll)
        pygame.draw.rect(window, (255,255,255), (self.x-scroll[0], self.y-scroll[1], 38, 40))
        pygame.draw.rect(window, (0,0,0), (self.x-2-scroll[0], self.y-2-scroll[1], 42, 44), 2)

        for projectile in self.projectiles:
            projectile.draw(window, scroll, self.rect)
        
        self.bars(window, screen_size[0])

    def bars(self, window, Width):
        if self.saved_health != [self.stats["Health"], self.stats["Max Health"]]:
            self.generate_bars()
            self.saved_health = self.stats["Health"]
        window.blit(self.bars_surf, (Width-210, 10))
               
    def update(self):
        if self.saved_health != [self.stats["Health"], self.stats["Max Health"]] or self.saved_exrta != [[self.stats["Extra Stats"][0], self.stats["Max Extra Stats"][0]], [self.stats["Extra Stats"][1], self.stats["Max Extra Stats"][1]]]:
            self.generate_bars()
            self.saved_health = [self.stats["Health"], self.stats["Max Health"]]
            self.saved_exrta = [[self.stats["Extra Stats"][0], self.stats["Max Extra Stats"][0]], [self.stats["Extra Stats"][1], self.stats["Max Extra Stats"][1]]]
        if self.Pclass[1]:
            if len(self.equipment) < 3:
                self.equipment.insert(1, "Fist")
                
    def move(self, tiles, dt, keys, enemies):
        self.movement = [0, 0]
        pressed_keys = pygame.key.get_pressed()

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

        if pressed_keys[keys["Up"]]:
            if self.vel[1] > -self.stats["Speed"]:
                self.vel[1] -= 0.5*dt
                self.direction = "Up"
        if pressed_keys[keys["Down"]]:
            if self.vel[1] < self.stats["Speed"]:
                self.vel[1] += 0.5*dt
                self.direction = "Down"
        if pressed_keys[keys["Left"]]:
            if self.vel[0] > -self.stats["Speed"]:
                self.vel[0] -= 0.5*dt
                self.direction = "Left"
        if pressed_keys[keys["Right"]]:
            if self.vel[0] < self.stats["Speed"]:
                self.vel[0] += 0.5*dt
                self.direction = "Right"

        self.movement[1] += round(self.vel[1]*dt)
        self.movement[0] += round(self.vel[0]*dt)
            
        for projectile in self.projectiles:
            projectile.move(tiles, dt, pygame.mouse.get_pos(), enemies)
        
        return self.movement_collision(tiles)

    def scroll(self, scroll, map, screen_size):
        if map.x == 0: scroll[0] = self.x-((screen_size[0]*0.5)-(self.rect.width*0.5))
        if map.y == 0: scroll[1] = self.y-((screen_size[1]*0.5)-(self.rect.height*0.5))

        if scroll[0] <= map.x and map.x == 0:
            scroll[0] = map.x
        elif scroll[0] >= map.map_w-screen_size[0] and map.x == 0:
            scroll[0] = map.map_w-screen_size[0]
            
        if scroll[1] <= map.y and map.y == 0:
            scroll[1] = map.y
        elif scroll[1] >= map.map_h-screen_size[1] and map.y == 0:
            scroll[1] = map.map_h-screen_size[1]

        return scroll

    def attack(self, enemies, button, mouse_pos, screen_size, window, scroll):
        if button == 1: button = 0
        elif button == 3: button = 1
        else: return

        if self.Pclass[button]:
            weapon_stats = load_json(["scripts", "data", "equipment.json"])
            if time.time() - self.attack_cooldown[button] >= weapon_stats[0][self.equipment[button]]["Cooldown"]:
                if self.Pclass[button] == "Swordsman" or self.equipment[button] == "Fist":
                    for i in range(4):
                        if i == 0:
                            p1, p2 = (0, 0), (screen_size[0], 0)
                        elif i == 1:
                            p1, p2 = (screen_size[0], 0), (screen_size[0], screen_size[1])
                        elif i == 2:
                            p1, p2 = (0, screen_size[1]), (screen_size[0], screen_size[1])
                        elif i == 3:
                            p1, p2 = (0, 0), (0, screen_size[1])
                            
                        mainA = abs((p1[0]-self.rect.centerx)*(p2[1]-self.rect.centery) - (p2[0]-self.rect.centerx)*(p1[1]-self.rect.centery))

                        a1 = abs((self.rect.centerx-mouse_pos[0])*(p1[1]-mouse_pos[1]) - (p1[0]-mouse_pos[0])*(self.rect.centery-mouse_pos[1]))
                        a2 = abs((p1[0]-mouse_pos[0])*(p2[1]-mouse_pos[1]) - (p2[0]-mouse_pos[0])*(p1[1]-mouse_pos[1]))
                        a3 = abs((p2[0]-mouse_pos[0])*(self.rect.centery-mouse_pos[1]) - (self.rect.centerx-mouse_pos[0])*(p2[1]-mouse_pos[1]))

                        if a1 + a2 + a3 == mainA:
                            if i == 0:
                                attack_rect = pygame.Rect(self.x-self.rect.width*0.5, self.y-self.rect.height*1.5, self.rect.width*2, self.rect.height*1.5)
                            elif i == 1:
                                attack_rect = pygame.Rect(self.x+self.rect.width, self.y-self.rect.height*0.5, self.rect.width*1.5, self.rect.height*2)
                            elif i == 2:
                                attack_rect = pygame.Rect(self.x-self.rect.width*0.5, self.y+self.rect.height, self.rect.width*2, self.rect.height*1.5)
                            elif i == 3:
                                attack_rect = pygame.Rect(self.x-self.rect.width*1.5, self.y-self.rect.height*0.5, self.rect.width*1.5, self.rect.height*2)
                            break
                        
                    pygame.draw.rect(window, (128,128,128), (attack_rect.x-scroll[0], attack_rect.y-scroll[1], attack_rect.width, attack_rect.height))

                    for enemy in enemies:
                        if attack_rect.colliderect(enemy.rect):
                            if self.strong_charged: enemy.lose_hp(self.stats["Attack"][button]*1.5); self.stats["Extra Stats"][button] -= 1
                            else: enemy.lose_hp(self.stats["Attack"][button])

                if self.Pclass[button] == "Archer" or self.Pclass[button] == "Mage":
                    if self.equipment[button] != "Fist":
                        if self.strong_charged: self.projectiles.append(Arrow(self.rect.centerx-(sprites_Proj["Arrow"].get_width()*0.5), self.rect.centery-(sprites_Proj["Arrow"].get_height()*0.5), self.stats["Attack"][button]*1.5, weapon_stats[0][self.equipment[0]]["Proj Type"], weapon_stats[0][self.equipment[0]]["Speed"], (mouse_pos[0]+scroll[0], mouse_pos[1]+scroll[1]))); self.stats["Extra Stats"][button] -= 2
                        else: self.projectiles.append(Arrow(self.rect.centerx-(sprites_Proj["Arrow"].get_width()*0.5), self.rect.centery-(sprites_Proj["Arrow"].get_height()*0.5), self.stats["Attack"][button], weapon_stats[0][self.equipment[0]]["Proj Type"], weapon_stats[0][self.equipment[0]]["Speed"], (mouse_pos[0]+scroll[0], mouse_pos[1]+scroll[1]))); self.stats["Extra Stats"][button] -= 1
                self.attack_cooldown[button] = time.time()

    def lose_hp(self, hp):
        if time.time() - self.i_frame_time >= self.i_frame_length:
            self.stats["Health"] -= hp
            self.i_frame_time = time.time()
