import pygame, json, os
from pygame.locals import *
from .drops import Drop

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
        

    def draw_inventory(self, win, font_name:str=None):
        try:
            font = pygame.font.Font(font_name, 24)
            quant_font = pygame.font.Font(font_name, 12)
        except FileNotFoundError():
            font = pygame.font.SysFont(font_name, 24)
            quant_font = pygame.font.SysFont(font_name, 30)

        inv_label = font.render("Inventory", 1, (255,255,255))
        equip_label = font.render("Equipment", 1, (255,255,255))

        no = 0
        y = 10
        x = 10

        if self.inv:
            if self.resol:
                if round((self.resol[0]/self.resol[1])*100) <= 133:
                    win.blit(inv_label, (320*0.5-inv_label.get_width()*0.5, y))
                else:
                    win.blit(inv_label, (620*0.5-inv_label.get_width()*0.5, y))
            else:
                win.blit(inv_label, (620/2-inv_label.get_width()/2, y))
            for _ in range(self.inv_length):
                win.blit(self.inv_img, (x, y+inv_label.get_height()+5))
                x += 60
                no += 1
                if self.resol:
                    if round((self.resol[0]/self.resol[1])*100) <= 133 and no >= 5:
                        x = 10
                        y += 60
                        no = 0
            
            offset_x = 13
            offset_y = 18
            no = 0
            for item in self.player.inventory.keys():
                win.blit(self.equipment_imgs[item], (offset_x, inv_label.get_height()+offset_y))
                offset_x += 60
                no += 1
                if self.resol:
                    if round((self.resol[0]/self.resol[1])*100) <= 133 and no >= 5:
                        offset_x = 13
                        offset_y += 60
                        no = 0
            
            offset_x = 50
            offset_y = 48
            no = 0
            for item_quantity in self.player.inventory.values():
                if not item_quantity == 1:
                    quantity = quant_font.render(str(item_quantity), 1, (255,255,255))
                    win.blit(quantity, (offset_x-quantity.get_width()+8, inv_label.get_height()+offset_y))
                offset_x += 60
                no += 1
                if self.resol:
                    if round((self.resol[0]/self.resol[1])*100) <= 133 and no >= 5:
                        offset_x = 50
                        offset_y += 60
                        no = 0

            if self.inv_index <= 4:
                pygame.draw.rect(win, (200,200,200), (self.inv_index*60+10,10+inv_label.get_height()+5,54,54),3)
            else:
                if self.resol:
                    if round((self.resol[0]/self.resol[1])*100) <= 133:
                        pygame.draw.rect(win, (200,200,200), ((self.inv_index-5)*60+10, 10+inv_label.get_height()+65, 54, 54), 3)
                    else:
                        pygame.draw.rect(win, (200,200,200), (self.inv_index*60+10, 10+inv_label.get_height()+5, 54, 54), 3)
                else:
                    pygame.draw.rect(win, (200,200,200), (self.inv_index*60+10, 10+inv_label.get_height()+5, 54, 54), 3)

        else:
            x = 95
            win.blit(equip_label, (310*0.5-equip_label.get_width()*0.5, y))
            for _ in range(self.equip_length):
                win.blit(self.inv_img, (x, y+equip_label.get_height()+5))
                x += 60
            
            offset_x = 98
            offset_y = 8
            for item in self.player.equipment:
                win.blit(self.equipment_imgs[item], (offset_x, y+inv_label.get_height()+offset_y))
                offset_x += 60

            if self.eq_index <= 1:
                pygame.draw.rect(win, (200,200,200), (self.eq_index*60+95,10+equip_label.get_height()+5,54,54),3)

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

    def equip_item(self):
        if self.inv:
            self.inv = False

            try:
                equipment = load_json(["scripts", "data", "equipment.json"])

                l = list(self.player.inventory.keys())
                item = l[self.inv_index]

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
                            
                    if self.player.inventory[item] > 1:
                        self.player.inventory[item] -= 1
                    else:
                        del self.player.inventory[item]

                    if self.player.equipment[ind] != "Fist" and self.player.equipment[ind] != "No Shield":
                        if item in self.player.inventory.keys():
                            self.player.inventory[self.player.equipment[ind]] += 1
                        else:
                            self.player.inventory[self.player.equipment[ind]] = 1
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
            except:
                self.inv = True
        else:
            if self.player.equipment[self.eq_index] != "Fist" and self.player.equipment[self.eq_index] != "No Shield":
                if self.player.equipment[self.eq_index] in self.player.inventory.keys():
                    self.player.inventory[self.player.equipment[self.eq_index]] += 1
                else:
                    self.player.inventory[self.player.equipment[self.eq_index]] = 1

                del self.player.equipment[self.eq_index]
                if self.eq_index == 0:
                    self.player.equipment.insert(0, "Fist")
                    self.player.stats["Attack"] = 1
                else:
                    self.player.equipment.insert(1, "No Shield")
                    self.player.stats["Defense"] = 0
                    self.player.stats["Speed"] = 5
                
                self.inv = True
    
    def throw_item(self, player_loc:list):
        if self.inv:
            l = list(self.player.inventory.keys())
            try:
                item = l[self.inv_index]
            except:
                return
            
            if self.player.inventory[item] > 1:
                self.player.inventory[item] -= 1
            else:
                del self.player.inventory[item]

            return [item, Drop(player_loc[0], player_loc[1], self.equipment_imgs[item]), 3*60]
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

                return [item, Drop(player_loc[0], player_loc[1], self.equipment_imgs[item]), 3*60]

    def grab_item(self, item, quantity:int=1):
        if len(self.player.inventory) < 10:
            if not item in self.player.inventory.keys():
                self.player.inventory[item] = quantity
                return True
            else:
                items = load_json(["scripts", "data", "items.json"])
                if self.player.inventory[item] < items[item]["stack"]:
                    self.player.inventory[item] += quantity
                    return True
