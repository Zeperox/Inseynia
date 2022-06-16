import pygame, os, time, math, copy, importlib
from pygame.locals import *

from .entity import Entity
from scripts.custom_collisions.obb import OBB
from scripts.loading.json_functions import load_json
from scripts.loading.sprites import sprites
from scripts.UI.text import Text

weapons = {}
for file in os.scandir(os.path.join("scripts", "weapons")):
    if file.is_file():
        mod = importlib.import_module(f'scripts.weapons.{file.name[:-3]}')
        weapons[mod.weapon_name] = mod.Weapon
for mod in os.scandir(os.path.join("mods")):
    if mod.is_dir():
        try:
            for file in os.scandir(os.path.join("mods", mod.name, "scripts", "wepaons")):
                if file.is_file() and file.name.endswith(".py"):
                    mod = importlib.import_module(f'mods.{mod}.scripts.weapons.{file.name[:-3]}')
                    weapons[mod.weapon_name] = mod.Weapon
        except:
            continue


class Player(Entity):
    classes = ["Archer", None]
    name = ""
    equipment = ["No Primary", "No Secondry", "No Armor"]
    inventory = []
    stats = {
        "HP": [999, 10], # current_HP, max_HP
        "SP": [10, 10], #current_SP, max_SP
        "AP": [1, 1], # weapon_1, weapon_2
        "DP": 0,
        "EP": [[5, 10], [7, 10]], # current_stat_1, max_stat_1 | current_stat_2, max_stat_2
        "M": 100,
        "XP": [2, 3, 1] # xp, max_xp, level
    }
    location = None
    def __init__(self, x: int, y: int):
        s = pygame.Surface((32, 64))
        s.fill((255,255,255))
        pygame.draw.rect(s, (0,0,0), (0, 0, 32, 64), 2)
        
        super().__init__(x, y, s)
        self.cached_stats = copy.deepcopy(self.stats)

        self.vel = pygame.Vector2()
        self.friction = 0.2
        self.disable_friction = False

        self.strong_charged = False
        self.attack_cooldown = [0, 0]
        self.shielded = [None, 0]

        self.dash = False
        self.dash_timer = 0
        self.dash_cooldown = 0
        self.dash_dir = pygame.Vector2()

        self._move = True
        self.knockback_resist = 0

        self.main_stats_surf = pygame.Surface((64, 152))
        self.main_stats_surf.set_colorkey((0,0,0))
        self.inv_stats_surf = pygame.Surface((514, 131))
        self.inv_stats_surf.set_colorkey((0,0,0))

        self.map_text = Text(os.path.join("assets", "fontsDL", "Font.png"), "Map coming soon :)", 30, (255, 255, 255))

        self.held_buttons = []
        self.weapons = [[None, None], [None, None]]

        self._generate_bars()

    def _generate_bars(self):
        hp_text = Text(os.path.join("assets", "fontsDL", "Font.png"), f"{self.stats['HP'][0]}", 20, (255, 255, 255))
        st_text = Text(os.path.join("assets", "fontsDL", "Font.png"), f"{self.stats['SP'][0]}", 20, (255, 255, 255))
        es_text = [Text(os.path.join("assets", "fontsDL", "Font.png"), f"{self.stats['EP'][0][0]}", 20, (255, 255, 255))]
        if self.stats['EP'][1] != [None, None]:
            es_text.append(Text(os.path.join("assets", "fontsDL", "Font.png"), f"{self.stats['EP'][1][0]}", 20, (255, 255, 255)))
        dp_text =  Text(os.path.join("assets", "fontsDL", "Font.png"), f"{self.stats['DP']}", 30, (255, 255, 255))
        ap_text =  Text(os.path.join("assets", "fontsDL", "Font.png"), f"{self.stats['AP'][0]}", 30, (255, 255, 255))
        if self.stats["AP"][1] is not None:
            ap_text.content = f"{self.stats['AP'][0]}/{self.stats['AP'][1]}"
        lv_text =  Text(os.path.join("assets", "fontsDL", "Font.png"), f"{self.stats['XP'][2]}", 30, (255, 255, 255))
        m_text =  Text(os.path.join("assets", "fontsDL", "Font.png"), f"{self.stats['M']}", 30, (255, 255, 255))

        imgs = []
        for x in range(2):
            if self.classes[x] == "Archer":
                imgs.append("p")
            elif self.classes[x] == "Mage":
                imgs.append("m")
            else:
                continue

        self.main_stats_surf.blit(sprites["he"], (0, 0))
        self.main_stats_surf.blit(sprites["hf"], (0, int((self.stats["HP"][1]-self.stats["HP"][0])/self.stats["HP"][1]*100/6.25)*2), (0, int((self.stats["HP"][1]-self.stats["HP"][0])/self.stats["HP"][1]*100/6.25)*2, sprites["hf"].get_width(), sprites["hf"].get_height()-(int((self.stats["HP"][1]-self.stats["HP"][0])/self.stats["HP"][1]*100/6.25)*2)))
        hp_text.render(self.main_stats_surf, (35, 16-hp_text.height*0.5))
        

        self.main_stats_surf.blit(sprites["se"], (0, 40))
        self.main_stats_surf.blit(sprites["sf"], (0, 40+int((self.stats["SP"][1]-self.stats["SP"][0])/self.stats["SP"][1]*100/6.25)*2), (0, int((self.stats["SP"][1]-self.stats["SP"][0])/self.stats["SP"][1]*100/6.25)*2, sprites["hf"].get_width(), sprites["hf"].get_height()-(int((self.stats["SP"][1]-self.stats["SP"][0])/self.stats["SP"][1]*100/6.25)*2)))
        st_text.render(self.main_stats_surf, (35, 40+(16-hp_text.height*0.5)))

        for x in range(2):
            if self.classes[x]:
                self.main_stats_surf.blit(sprites[f"{imgs[x]}e"], (0, 80+40*x))
                self.main_stats_surf.blit(sprites[f"{imgs[x]}f"], (0, 80+40*x+int((self.stats["EP"][x][1]-self.stats["EP"][x][0])/self.stats["EP"][x][1]*100/6.25)*2), (0, int((self.stats["EP"][x][1]-self.stats["EP"][x][0])/self.stats["EP"][x][1]*100/6.25)*2, sprites["hf"].get_width(), sprites["hf"].get_height()-(int((self.stats["EP"][x][1]-self.stats["EP"][x][0])/self.stats["EP"][x][1]*100/6.25)*2)))
                es_text[x].render(self.main_stats_surf, (35, 80+(16-hp_text.height*0.5)+40*x))
            

        img_size = pygame.transform.scale(sprites["he"], (sprites["he"].get_width()*0.5*3, sprites["he"].get_height()*0.5*3)).get_size()
        hp_text.size = 30
        self.inv_stats_surf.blit(pygame.transform.scale(sprites["he"], img_size), (0, 0))
        self.inv_stats_surf.blit(pygame.transform.scale(sprites["hf"], img_size), (0, int((self.stats["HP"][1]-self.stats["HP"][0])/self.stats["HP"][1]*100/6.25)*3), (0, int((self.stats["HP"][1]-self.stats["HP"][0])/self.stats["HP"][1]*100/6.25)*3, img_size[0], img_size[1]-(int((self.stats["HP"][1]-self.stats["HP"][0])/self.stats["HP"][1]*100/6.25)*3)))
        hp_text.render(self.inv_stats_surf, (53, 26-hp_text.height*0.5))
        
        st_text.size = 30
        self.inv_stats_surf.blit(pygame.transform.scale(sprites["se"], img_size), (125, 0))
        self.inv_stats_surf.blit(pygame.transform.scale(sprites["sf"], img_size), (125, int((self.stats["SP"][1]-self.stats["SP"][0])/self.stats["SP"][1]*100/6.25)*3), (0, int((self.stats["SP"][1]-self.stats["SP"][0])/self.stats["SP"][1]*100/6.25)*3, img_size[0], img_size[1]-(int((self.stats["SP"][1]-self.stats["SP"][0])/self.stats["SP"][1]*100/6.25)*3)))
        st_text.render(self.inv_stats_surf, (178, 26-st_text.height*0.5))

        for x in range(2):
            if self.classes[x]:
                es_text[x].size = 30
                self.inv_stats_surf.blit(pygame.transform.scale(sprites[f"{imgs[x]}e"], img_size), (250+125*x, 0))
                self.inv_stats_surf.blit(pygame.transform.scale(sprites[f"{imgs[x]}f"], img_size), (250+125*x, int((self.stats["EP"][x][1]-self.stats["EP"][x][0])/self.stats["EP"][x][1]*100/6.25)*3), (0, int((self.stats["EP"][x][1]-self.stats["EP"][x][0])/self.stats["EP"][x][1]*100/6.25)*3, img_size[0], img_size[1]-(int((self.stats["EP"][x][1]-self.stats["EP"][x][0])/self.stats["EP"][x][1]*100/6.25)*3)))
                es_text[x].render(self.inv_stats_surf, (303+125*x, 26-es_text[x].height*0.5))

        self.inv_stats_surf.blit(pygame.transform.scale(sprites["dp"], img_size), (0, 73))
        dp_text.render(self.inv_stats_surf, (53, 26-dp_text.height*0.5+73))

        self.inv_stats_surf.blit(pygame.transform.scale(sprites["ap"], img_size), (125, 73))
        ap_text.render(self.inv_stats_surf, (178, 26-ap_text.height*0.5+73))

        self.inv_stats_surf.blit(pygame.transform.scale(sprites["le"], img_size), (250, 73))
        self.inv_stats_surf.blit(pygame.transform.scale(sprites["lf"], img_size), (250, int((self.stats["XP"][1]-self.stats["XP"][0])/self.stats["XP"][1]*100/6.25)*3+73), (0, int((self.stats["XP"][1]-self.stats["XP"][0])/self.stats["XP"][1]*100/6.25)*3, img_size[0], img_size[1]-(int((self.stats["XP"][1]-self.stats["XP"][0])/self.stats["XP"][1]*100/6.25)*3)))
        lv_text.render(self.inv_stats_surf, (303, 26-lv_text.height*0.5+73))

        self.inv_stats_surf.blit(pygame.transform.scale(sprites["money"], img_size), (375, 73))
        m_text.render(self.inv_stats_surf, (428, 26-m_text.height*0.5+73))

    def UI(self, win, inventory_on):
        if self.cached_stats != self.stats:
            self._generate_bars()
            self.cached_stats = copy.deepcopy(self.stats)
        
        if inventory_on:
            win.blit(self.inv_stats_surf, (win.get_width()*0.75-self.inv_stats_surf.get_width()*0.5, 10))
            self.map_text.render(win, (win.get_width()*0.75-self.map_text.width*0.5, win.get_height()*0.5-self.map_text.height*0.5))
        else:
            win.blit(self.main_stats_surf, (10, 10))

    def move(self, tiles, dt, keys, mouse_pos):
        self._move = not self.shielded[0]
        self.collidable = not self.dash
        self.movement = [0, 0]
              
        if self._move:
            equiped_armor = load_json(["scripts", "cache", "equipment.json"])[2][self.equipment[2]]

            if self.knockback:
                self.vel = (self.knockback_dir-pygame.Vector2(self.rect.center)).normalize()*self.knockback_speed

                self.knockback_speed *= 0.9
                if self.knockback_speed <= 0.5:
                    self.knockback = False
                
            elif self.dash:
                speed = 10
                secs = .4

                try:
                    pvec = pygame.Vector2(self.rect.center)
                    vel = (self.dash_dir - pvec).normalize()*speed
                    self.vel.x, self.vel.y = vel.x, vel.y
                except ValueError:
                    self.vel.x = speed

                if time.time() - self.dash_timer >= secs:
                    self.dash = False
                    self.dash_cooldown = time.time()

            else:
                
                if not self.disable_friction:
                    acc = 0.3-((0.3*equiped_armor["weight"])/100)
                    v = list(self.vel)
                    for index in range(2):
                        if v[index] > 0:
                            if v[index] - acc*dt < 0:
                                v[index] = 0
                            else:
                                v[index] -= acc*dt
                        elif v[index] < 0:
                            if v[index] + acc*dt > 0:
                                v[index] = 0
                            else:
                                v[index] += acc*dt
                    self.vel = pygame.Vector2(v)
                else:
                    self.vel.x, self.vel.y = 0, 0
                
                self.collidable, self.disable_friction = True, False
                            
                pressed_keys = pygame.key.get_pressed()

                acc = 0.5-((0.5*equiped_armor["weight"])/100)
                self.knockback_resist = equiped_armor["knockback resistence"]

                if pressed_keys[keys["Up"]]:
                    if self.vel.y > -5:
                        self.vel.y -= acc*dt
                if pressed_keys[keys["Down"]]:
                    if self.vel.y < 5:
                        self.vel.y += acc*dt
                if pressed_keys[keys["Left"]]:
                    if self.vel.x > -5:
                        self.vel.x -= acc*dt
                if pressed_keys[keys["Right"]]:
                    if self.vel.x < 5:
                        self.vel.x += acc*dt
            
                if equiped_armor["weight"] <= 37:
                    sroll = 1
                else:
                    sroll = 2
                
                if pressed_keys[keys["Dash"]]:
                    if (time.time()-self.dash_cooldown >= 1 or time.time()-self.dash_cooldown <= 0.2) and self.stats["SP"][0] > sroll-1 and not keys["Dash"] in self.held_buttons:
                        self.stats["SP"][0] -= sroll
                        self.dash = self.disable_friction = True
                        self.dash_timer = time.time()
                        self.dash_dir = pygame.Vector2(mouse_pos)

                        if not keys["Dash"] in self.held_buttons:
                            self.held_buttons.append(keys["Dash"])
                else:
                    if keys["Dash"] in self.held_buttons:
                        self.held_buttons.remove(keys["Dash"])

            self.movement[1] += self.vel.y*dt
            self.movement[0] += self.vel.x*dt

        return self.movement_collision(tiles)

    def attack(self, enemies, mouse_pos, scroll, projs):
        buttons = pygame.mouse.get_pressed()

        if buttons[0]: button = 0
        elif buttons[2]: button = 1

        mouse_pos = (mouse_pos[0]+scroll[0], mouse_pos[1]+scroll[1])
        weapon_stats = load_json(["scripts", "cache", "equipment.json"])

        if buttons[0] or buttons[2]:
            if self.equipment[button].startswith("No "):
                self.weapons[button] = [None, None]
            elif self.weapons[button][0] != self.equipment[button] and self.equipment[button] in weapons:
                self.weapons[button] = [self.equipment[button], weapons.get(self.equipment[button])()]

            if self.classes[button] and not self.shielded[0] and self.stats["EP"][button][0] > 0 and self.weapons[button] != [None, None] and button not in self.held_buttons:
                if self.weapons[button][1].attack(self, mouse_pos, 1, projs)[1]:
                    self.stats["EP"][button][0] -= 1
                    
                    if not self.weapons[button][1].auto_fire:
                        self.held_buttons.append(button)
                '''if time.time() - self.attack_cooldown[button] >= weapon_stats[0][self.equipment[button]]["cooldown"]:
                    if self.stats["EP"][button][0] > 0 and button not in self.held_buttons:
                        if not weapon_stats[0][self.equipment[button]]["autofire"]:
                            self.held_buttons.append(button)
                        projs.append(Projectile(self.rect.center, mouse_pos, self.stats["AP"][button], weapon_stats[0][self.equipment[button]]["proj data"], self))
                        self.stats["EP"][button][0] -= 1
                        self.attack_cooldown[button] = time.time()'''
                        
            elif self.equipment[button] in weapon_stats[1].keys() and self.equipment[button] != "No Shield":
                offset = (pygame.Vector2(mouse_pos)-pygame.Vector2(self.rect.center)).normalize()
                attack_obb = OBB((self.rect.centerx+(offset.x*(self.rect.w*0.5+20)), self.rect.centery+(offset.y*(self.rect.h*0.5+20))), 48, -math.degrees(math.atan2(self.rect.centery-mouse_pos[1], mouse_pos[0]-self.rect.centerx)))
                self.shielded = [attack_obb, time.time()]
        else:
            if not buttons[0] and 0 in self.held_buttons:
                self.held_buttons.remove(0)
            if not buttons[2] and 1 in self.held_buttons:
                self.held_buttons.remove(1)

        return enemies, projs

    def damage(self, dmg, _):
        hit = False
        if time.time() - self.i_frame >= 0.5 and self.collidable and self.active:
            hit = True
            dmg = round(dmg*dmg/(dmg+self.stats["DP"]))
            if dmg == 0: dmg = 1

            self.stats["HP"][0] -= dmg
            self.i_frame = time.time()

        return self.stats["HP"][0], hit
