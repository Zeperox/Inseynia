import pygame, random, os, time

from .projectiles import *
from scripts.custom_collisions.polygon import Polygon
from scripts.data.json_functions import load_json
from scripts.assets.sprites import images

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
        "Stamina": 10,
        "Max Stamina": 10,
        "Extra Stats": [10, None],
        "Max Extra Stats": [10, None],
        "Money": 100,
        "XP": 0,
        "Level": 1
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
        surf = pygame.Surface((42, 44))
        pygame.draw.rect(surf, (255,255,255), (2, 2, 38, 40))
        pygame.draw.rect(surf, (0,0,0), (0, 0, 42, 44), 2)

        super().__init__(x, y, surf)
        #self.img = self.directions[direction]

        self.saved_stats = self.stats.copy()

        self.directions = [True, False, False, False] # Up, Down, Left, Right

        self.vel = [0, 0]
        self.friction = 0.2
        self.disable_friction = False

        # Combat
        self.strong_wind = 0
        self.strong_charging = False
        self.strong_charged = False
        self.attack_cooldown = [0, 0]

        self.melee_dir_poly = []

        self.projectiles = []

        # Evade
        self.roll = False
        self.dash = None if not "Swordsman" in self.Pclass else False

        self.evade_timer = 0
        self.evade_cooldown = 0
        self.evade_choice_timer = None

        #self.rect = pygame.Rect(self.x, self.y, self.get_width(), self.get_height())
        self.rect = pygame.Rect(self.x, self.y, 38, 40)

        self.bars_surf = pygame.Surface((450, 112)).convert()
        self.bars_surf.set_colorkey((0,0,0))
        self.generate_bars()
    
    def generate_bars(self):
        self.bars_surf.blit(images["Player Data"], (0, 0))
        bar_font = pygame.font.Font(os.path.join("assets", "fonts", "DefaultFont.TTF"), int(25*0.5))
        health_label = bar_font.render(f"{self.stats['Health']}/{self.stats['Max Health']}", False, (255,255,255))
        stamina_label = bar_font.render(f"{self.stats['Stamina']}/{self.stats['Max Stamina']}", False, (255,255,255))
        attack_label = bar_font.render(f"{self.stats['Attack'][0]} | {self.stats['Attack'][1]}", False, (255,255,255)) if self.stats["Attack"][1] else bar_font.render(str(self.stats["Attack"][0]), False, (255,255,255))
        defense_label = bar_font.render(str(self.stats["Defense"]), False, (255,255,255))
        money_label = bar_font.render(str(self.stats["Money"]), False, (255,255,255))
        level_label = bar_font.render(str(self.stats["Level"]), False, (255,255,255))
        

        chealth = (0, 175, 0)
        cstamina = (175, 175, 0)
        cstats = []
        labels = []
        imgs = []
        for x in range(2):
            if self.Pclass[x]:
                if self.Pclass[x] == "Swordsman":
                    labels.append(bar_font.render(f"{self.stats['Extra Stats'][x]}/{self.stats['Max Extra Stats'][x]}", False, (255,255,255)))
                    cstats.append((175,175,0))
                    imgs.append("Stamina")
                elif self.Pclass[x] == "Archer":
                    labels.append(bar_font.render(f"{self.stats['Extra Stats'][x]}/{self.stats['Max Extra Stats'][x]}", False, (255,255,255)))
                    cstats.append((175,88,0))
                    imgs.append("Projectile")
                elif self.Pclass[x] == "Mage":
                    labels.append(bar_font.render(f"{self.stats['Extra Stats'][x]}/{self.stats['Max Extra Stats'][x]}", False, (255,255,255)))
                    cstats.append((0,88,175))
                    imgs.append("Mana")

        pygame.draw.rect(self.bars_surf, (175,0,0), (29, 10, 200, 25))
        pygame.draw.rect(self.bars_surf, chealth, (29, 10, 200 * (self.stats["Health"]/self.stats["Max Health"]), 25))
        pygame.draw.rect(self.bars_surf, (200,200,200), (27, 8, 203, 27), 3)
        pygame.draw.rect(self.bars_surf, (1,1,1), (26, 7, 205, 29), 1)
        self.bars_surf.blit(health_label, (((200*0.5)-(health_label.get_width()*0.5)), ((25*0.5)-(health_label.get_height()*0.5))+7))
        self.bars_surf.blit(images["Heart"], (7, 10))

        pygame.draw.rect(self.bars_surf, (175,0,0), (29, 45, 200, 25))
        pygame.draw.rect(self.bars_surf, cstamina, (29, 45, 200 * (self.stats["Stamina"]/self.stats["Max Stamina"]), 25))
        pygame.draw.rect(self.bars_surf, (200,200,200), (27, 43, 203, 27), 3)
        pygame.draw.rect(self.bars_surf, (1,1,1), (26, 42, 205, 29), 1)
        self.bars_surf.blit(stamina_label, (((200*0.5)-(stamina_label.get_width()*0.5)), ((25*0.5)-(stamina_label.get_height()*0.5))+42))
        self.bars_surf.blit(images["Stamina"], (7, 45))

        for x in range(2):
            if self.Pclass[x]:
                pygame.draw.rect(self.bars_surf, (175,0,0), (29+(165*x), 80, 140, 25))
                pygame.draw.rect(self.bars_surf, cstats[x], (29+(165*x), 80, 140 * (self.stats["Extra Stats"][x]/self.stats["Max Extra Stats"][x]), 25))
                pygame.draw.rect(self.bars_surf, (200,200,200), (27+(165*x), 78, 143, 27), 3)
                pygame.draw.rect(self.bars_surf, (1,1,1), (26+(165*x), 77, 145, 29), 1)
                self.bars_surf.blit(images[imgs[x]], (7+(165*x), 80))
                self.bars_surf.blit(labels[x], (26+(165*x+((140*0.5)-(labels[x].get_width()*0.5))), ((25*0.5)-(labels[x].get_height()*0.5))+77)) # ((200*0.5)-(labels[x].get_width()*0.5))+(0), ((25*0.5)-(labels[x].get_height()*0.5))+35+(39*x+39))

        self.bars_surf.blit(images["Attack"], (254, 10))
        self.bars_surf.blit(attack_label, (275, 10))
        self.bars_surf.blit(images["Defense"], (334, 10))
        self.bars_surf.blit(defense_label, (355, 10))
        self.bars_surf.blit(images["Money"], (254, 45))
        self.bars_surf.blit(money_label, (275, 45))
        self.bars_surf.blit(images["Level"], (334, 45))
        self.bars_surf.blit(level_label, (355, 45))

    def draw(self, window, scroll=[0, 0]):
        super().draw(window, scroll)
        self.bars(window)

    def bars(self, window):
        self.update()
        window.blit(self.bars_surf, (10, 10))
               
    def update(self):
        if self.saved_stats != self.stats:
            self.generate_bars()
            self.saved_stats = self.stats.copy()
        if self.Pclass[1]:
            if len(self.equipment) < 3:
                self.equipment.insert(1, "Fist")
                
    def move(self, tiles, dt, keys, enemies):
        self.movement = [0, 0]

        equiped_armor = load_json(["scripts", "data", "equipment.json"])[1][self.equipment[len(self.equipment)-1]]

        if not self.roll and not self.dash:
            if not self.disable_friction:
                acc = 0.3-((0.3*equiped_armor["Weight"])/100)
                for index in range(2):
                    if self.vel[index] > 0:
                        if self.vel[index] - acc*dt < 0:
                            self.vel[index] = 0
                        else:
                            self.vel[index] -= acc*dt
                    elif self.vel[index] < 0:
                        if self.vel[index] + acc*dt > 0:
                            self.vel[index] = 0
                        else:
                            self.vel[index] += acc*dt
            else:
                self.vel = [0, 0]
            
            self.collide, self.disable_friction = True, False
                        
            pressed_keys = pygame.key.get_pressed()

            acc = 0.5-((0.5*equiped_armor["Weight"])/100)

            if pressed_keys[keys["Up"]]:
                if self.vel[1] > -5:
                    self.vel[1] -= acc*dt
            if pressed_keys[keys["Down"]]:
                if self.vel[1] < 5:
                    self.vel[1] += acc*dt
            if pressed_keys[keys["Left"]]:
                if self.vel[0] > -5:
                    self.vel[0] -= acc*dt
            if pressed_keys[keys["Right"]]:
                if self.vel[0] < 5:
                    self.vel[0] += acc*dt

            if pressed_keys[keys["Up"]]:
                self.directions[0] = True
                self.directions[1] = False
                if pressed_keys[keys["Left"]]:
                    self.directions[2] = True
                elif pressed_keys[keys["Right"]]:
                    self.directions[3] = True
                else:
                    self.directions[2], self.directions[3] = False, False
            elif pressed_keys[keys["Down"]]:
                self.directions[1] = True
                self.directions[0] = False
                if pressed_keys[keys["Left"]]:
                    self.directions[2] = True
                elif pressed_keys[keys["Right"]]:
                    self.directions[3] = True
                else:
                    self.directions[2], self.directions[3] = False, False
            if pressed_keys[keys["Left"]]:
                self.directions[2] = True
                self.directions[3] = False
                if pressed_keys[keys["Up"]]:
                    self.directions[0] = True
                elif pressed_keys[keys["Down"]]:
                    self.directions[1] = True
                else:
                    self.directions[0], self.directions[1] = False, False
            elif pressed_keys[keys["Right"]]:
                self.directions[3] = True
                self.directions[2] = False
                if pressed_keys[keys["Up"]]:
                    self.directions[0] = True
                elif pressed_keys[keys["Down"]]:
                    self.directions[1] = True
                else:
                    self.directions[0], self.directions[1] = False, False


            if equiped_armor["Weight"] <= 37:
                sroll = 1
                sdash = 2
            else:
                sroll = 2
                sdash = 3

            if pressed_keys[keys["Roll"]] and time.time() - self.evade_cooldown >= .5 and self.stats["Stamina"] > sroll-1:
                self.roll = True
                self.collide, self.disable_friction = False, True
                self.evade_timer = time.time()
                self.stats["Stamina"] -= sroll
            if pressed_keys[keys["Dash"]] and time.time() - self.evade_cooldown >= .5 and self.stats["Stamina"] > sdash-1 and "Swordsman" in self.Pclass:
                self.dash = True
                self.collide, self.disable_friction = False, True
                self.evade_timer = time.time()
                self.stats["Stamina"] -= sdash
        else:
            if self.dash:
                speed = 15
                secs = .34
            elif self.roll:
                speed = 10
                secs = .4

            if self.directions[0]:
                if self.dash:
                    self.vel[1] = -speed
                else:
                    self.vel[1] = -speed
            elif self.directions[1]:
                if self.dash:
                    self.vel[1] = speed
                else:
                    self.vel[1] = speed
            if self.directions[2]:
                if self.dash:
                    self.vel[0] = -speed
                else:
                    self.vel[0] = -speed
            elif self.directions[3]:
                if self.dash:
                    self.vel[0] = speed
                else:
                    self.vel[0] = speed

            if time.time() - self.evade_timer >= secs:
                self.roll = False; self.dash = False
                self.evade_cooldown = time.time()

        #self.movement = list(map(round, list(map(*dt, self.vel))))
        self.movement[1] += round(self.vel[1]*dt)
        self.movement[0] += round(self.vel[0]*dt)

        return self.movement_collision(tiles)

    def attack(self, enemies, button, mouse_pos, screen_size, window, scroll):
        if button == 1: button = 0
        elif button == 3: button = 1
        else: return enemies

        if self.Pclass[button]:
            weapon_stats = load_json(["scripts", "data", "equipment.json"])
            if time.time() - self.attack_cooldown[button] >= weapon_stats[0][self.equipment[button]]["Cooldown"]:
                if self.Pclass[button] == "Swordsman" or self.equipment[button] == "Fist":
                    self.melee_dir_poly = [
                        Polygon(((scroll[0], scroll[1]), (screen_size[0]+scroll[0], scroll[1]), self.rect.center)),
                        Polygon(((screen_size[0]+scroll[0], scroll[1]), (screen_size[0]+scroll[0], screen_size[1]+scroll[1]), self.rect.center)),
                        Polygon(((scroll[0], screen_size[1]+scroll[1]), (screen_size[0]+scroll[0], screen_size[1]+scroll[1]), self.rect.center)),
                        Polygon(((scroll[0], scroll[1]), (scroll[0], screen_size[1]+scroll[1]), self.rect.center))
                    ]
                    for i, tri in enumerate(self.melee_dir_poly):
                        if tri.collidepoint((mouse_pos[0]+scroll[0], mouse_pos[1]+scroll[1])):
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
                            if self.strong_charged: enemy.lose_hp(self.stats["Attack"][button]*1.5, enemies); self.stats["Extra Stats"][button] -= 1
                            else: enemies = enemy.lose_hp(self.stats["Attack"][button], enemies)

                if self.Pclass[button] == "Archer" or self.Pclass[button] == "Mage":
                    if self.equipment[button] != "Fist":
                        if self.strong_charged: self.projectiles.append(Projectiles(self.rect.centerx-(images["Arrow"].get_width()*0.5), self.rect.centery-(images["Arrow"].get_height()*0.5), self.stats["Attack"][button]*1.5, weapon_stats[0][self.equipment[button]]["Proj Data"], (mouse_pos[0]+scroll[0], mouse_pos[1]+scroll[1]))); self.stats["Extra Stats"][button] -= 2
                        else: self.projectiles.append(Projectiles(self.rect.centerx-(images["Arrow"].get_width()*0.5), self.rect.centery-(images["Arrow"].get_height()*0.5), self.stats["Attack"][button], weapon_stats[0][self.equipment[button]]["Proj Data"], (mouse_pos[0]+scroll[0], mouse_pos[1]+scroll[1]))); self.stats["Extra Stats"][button] -= 1
                self.attack_cooldown[button] = time.time()
                self.generate_bars()
        return enemies

    def lose_hp(self, hp, _=None):
        if time.time() - self.i_frame_time >= self.i_frame_length and self.collide:
            dmg = round(hp*hp/(hp+self.stats["Defense"]))
            if dmg == 0: dmg = 1

            self.stats["Health"] -= dmg
            self.i_frame_time = time.time()
        return [self]