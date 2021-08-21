import pygame, json, os
from pygame.locals import *

from .drops import Drop
from scripts.UI.text import Text

def load_json(location_list:list):
    location = location_list[0]
    for location_entry in location_list[1:]:
        location = os.path.join(location, location_entry)

    with open(location, "r") as f:
        return json.load(f)

class Inventory:
    inv_length = 10
    equip_length = 2
    inv = True
    eq = False
    inv_index = 0
    eq_index = 0
        
    def __init__(self, resol, player, inv_img, equipment_imgs):
        self.resol = resol
        self.player = player
        self.inv_img = inv_img
        self.equipment_imgs = equipment_imgs

        #self.inv_text = Text(0, 0, "Inventory", os.path.join("assets", "Fonts", "DefaultFont.TTF"), 24, (255,255,255))
        #self.eq_text = Text(0, 0, "Equipment", os.path.join("assets", "Fonts", "DefaultFont.TTF"), 24, (255,255,255))
        self.quant_texts = [Text(0, 0, "0", os.path.join("assets", "Fonts", "DefaultFont.TTF"), 16, (255,255,255)) for _ in range(self.inv_length)]
        #self.quant_texts = [Text(0, 0, "0", os.path.join("assets", "Fonts", "Font.png"), (255,255,255)) for _ in range(self.inv_length)]
        
        if self.resol:
            if round((self.resol[0]/self.resol[1])*100) <= 133:
                self.inv_surf = pygame.Surface((53*5+40, 53*2+10), SRCALPHA)
            else:
                self.inv_surf = pygame.Surface((53*10+90, 53), SRCALPHA)
        else:
            self.inv_surf = pygame.Surface((53*10+90, 53), SRCALPHA)
        self.eq_surf = pygame.Surface((53*2+10, 53), SRCALPHA)

        #self.inv_surf.set_colorkey((0,0,0))
        #self.eq_surf.set_colorkey((0,0,0))

        y = 0
        x = 0
        no = 0
        for _ in self.player.inventory:
            self.inv_surf.blit(self.inv_img, (x, y))
            x += 60
            no += 1
            if self.resol:
                if round((self.resol[0]/self.resol[1])*100) <= 133 and no >= 5:
                    x = 0
                    y += 60
                    no = 0

        x = 0
        for _ in self.player.equipment:
            self.eq_surf.blit(self.inv_img, (x, 0))
            x += 60


        '''if self.resol:
            if round((self.resol[0]/self.resol[1])*100) <= 133:
                self.inv_text.x = 320*0.5-self.inv_text.get_width()*0.5; self.inv_text.y = 10
                self.eq_text.x = 620*0.5-self.eq_text.get_width()*0.5; self.eq_text.y = 10
            else:
                self.inv_text.x = 620*0.5-self.inv_text.get_width()*0.5; self.inv_text.y = 10
                self.eq_text.x = 620*0.5-self.eq_text.get_width()*0.5; self.eq_text.y = 10
        else:
            self.inv_text.x = 620*0.5-self.inv_text.get_width()*0.5; self.inv_text.y = 10
            self.eq_text.x = 620*0.5-self.eq_text.get_width()*0.5; self.eq_text.y = 10'''

    def draw_inventory(self, win):
        no = 0
        y = 10
        x = 10
        item_x = 13
        item_y =  13
        quant_x = 58
        quant_y = 48
        text_i = 0

        if self.inv:
            win.blit(self.inv_surf, (x, y))
            for i in self.player.inventory:
                if len(i) > 0:
                    win.blit(self.equipment_imgs[i[0]], (item_x, item_y))
                    if i[1] != 1:
                        self.quant_texts[text_i].text = str(i[1])
                        self.quant_texts[text_i].x = quant_x-self.quant_texts[text_i].get_width()
                        self.quant_texts[text_i].y = 10+quant_y-self.quant_texts[text_i].get_height()

                        self.quant_texts[text_i].render(win)

                item_x += 60
                quant_x += 60
                x += 60
                no += 1
                text_i += 1

                if self.resol:
                    if round((self.resol[0]/self.resol[1])*100) <= 133 and no >= 5:
                        x = 10
                        y += 60
                        item_x = 13
                        item_y += 60
                        quant_x = 58
                        quant_y += 60
                        no = 0

            if self.inv_index <= 4:
                pygame.draw.rect(win, (200,200,200), (self.inv_index*60+10, 10, 54, 54),3)
            else:
                if self.resol:
                    if round((self.resol[0]/self.resol[1])*100) <= 133:
                        pygame.draw.rect(win, (200,200,200), ((self.inv_index-5)*60+10, 610, 54, 54), 3)
                    else:
                        pygame.draw.rect(win, (200,200,200), (self.inv_index*60+10, 10, 54, 54), 3)
                else:
                    pygame.draw.rect(win, (200,200,200), (self.inv_index*60+10, 10, 54, 54), 3)

        else:
            for item in self.player.equipment:
                win.blit(self.eq_surf, (x+95, y))
                win.blit(self.equipment_imgs[item], (item_x+95, item_y))
                
                item_x += 60
                x += 60

            if self.eq_index <= 1:
                pygame.draw.rect(win, (200,200,200), (self.eq_index*60+105, 10, 54, 54),3)

    def select_item(self, event):
        if self.inv:
            if event.type == KEYDOWN:
                if event.key >= K_0 and event.key <= K_9:
                    self.inv_index = event.key - K_1
                    if event.key == K_0:
                        self.inv_index = 9
                
                if event.key >= K_KP_1 and event.key <= K_KP_0:
                    self.inv_index = event.key - K_KP_1

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 4:
                    if not self.inv_index <= 0:
                        self.inv_index -= 1
                    else:
                        self.inv_index = 9
                if event.button == 5:
                    if not self.inv_index >= 9:
                        self.inv_index += 1
                    else:
                        self.inv_index = 0
        else:
            if event.type == KEYDOWN:
                if event.key >= K_1 and event.key <= K_2:
                    self.eq_index = event.key - K_1
                
                if event.key >= K_KP_1 and event.key <= K_KP_2:
                    self.eq_index = event.key - K_KP_1

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 4:
                    if not self.eq_index <= 0:
                        self.eq_index -= 1
                    else:
                        self.eq_index = 1
                if event.button == 5:
                    if not self.eq_index >= 1:
                        self.eq_index += 1
                    else:
                        self.eq_index = 0

    def equip_item(self, player_loc):
        if self.inv:
            self.inv = False

            equipment = load_json(["scripts", "data", "equipment.json"])

            item = self.player.inventory[self.inv_index][0]

            if item in equipment[0].keys():
                ind = 0
            elif item in equipment[1].keys():
                ind = 1
            else:
                self.inv = True
                return

            l = list(equipment[ind].keys())

            if not item in self.player.equipment:
                if ind == 0:
                    if equipment[0][item]["Class"] != self.player.Pclass:
                        self.inv = True
                        return
                        
                if self.player.inventory[self.inv_index][1] > 1:
                    self.player.inventory[self.inv_index][1] -= 1
                else:
                    self.player.inventory[self.inv_index] = []

                if self.player.equipment[ind] != "Fist" and self.player.equipment[ind] != "No Shield":
                    if self.player.inventory[self.inv_index][0] == item:
                        self.player.inventory[self.inv_index][1] += 1
                    else:
                        self.player.inventory[self.inv_index] = [self.player.equipment[ind], 1]
                del self.player.equipment[ind]
                self.player.equipment.insert(ind, item)

                if ind == 0:
                    self.player.stats["Attack"] = equipment[0][item]["AP"]
                else:
                    self.player.stats["Defense"] = equipment[1][item]["DP"]
                    self.player.stats["Speed"] = self.player.stats["Speed"]-((self.player.stats["Speed"]*equipment[1][item]["Speed"])/100)
            else:
                self.inv = True
                return
        else:
            d = None
            if self.player.equipment[self.eq_index] != "Fist" and self.player.equipment[self.eq_index] != "No Shield":
                x = False
                for i, item in enumerate(self.player.inventory):
                    if len(item) > 0 and self.player.equipment[self.eq_index] == item[0]:
                        self.player.inventory[i][1] += 1
                        x = True
                        break
                if not x:
                    for i, slot in enumerate(self.player.inventory):
                        if slot == []:
                            self.player.inventory[i] = [self.player.equipment[self.eq_index], 1]
                            x = True
                            break
                    if not x:
                        d = [item, Drop(player_loc[0], player_loc[1], self.equipment_imgs[item]), 3*60]

                del self.player.equipment[self.eq_index]
                if self.eq_index == 0:
                    self.player.equipment.insert(0, "Fist")
                    self.player.stats["Attack"] = 1
                else:
                    self.player.equipment.insert(1, "No Shield")
                    self.player.stats["Defense"] = 0
                    self.player.stats["Speed"] = 5
                
                self.inv = True
            return d
    
    def throw_item(self, player_loc:list):
        item = None
        if self.inv:
            item = self.player.inventory[self.inv_index]
            
            if item[1] > 1:
                self.player.inventory[self.inv_index][1] -= 1
            else:
                self.player.inventory[self.inv_index] = []

        else:
            if self.player.equipment[self.eq_index] != "Fist" and self.player.equipment[self.eq_index] != "No Shield":
                item = self.player.equipment[self.eq_index]
                del self.player.equipment[self.eq_index]
                if self.eq_index == 0:
                    self.player.equipment.insert(0, "Fist")
                    self.player.stats["Attack"] = 1
                else:
                    self.player.equipment.insert(1, "No Shield")
                    self.player.stats["Defense"] = 0
                    self.player.stats["Speed"] = 5

        if item: return [item[0], Drop(player_loc[0], player_loc[1], self.equipment_imgs[item[0]]), 3*60]

    def grab_item(self, item, quantity:int=1):
        for i, slot in enumerate(self.player.inventory):
            if len(slot) == 0:
                self.player.inventory[i] = [item, quantity]
                return True
            else:
                if slot[0] == item:
                    items = load_json(["scripts", "data", "items.json"])
                    if self.player.inventory[i][1] < items[item]["stack"]:
                        self.player.inventory[i][1] += quantity
                        return True
