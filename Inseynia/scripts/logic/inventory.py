import pygame, time

from scripts.loading.sprites import sprites
from scripts.loading.json_functions import load_json
from .player import Player, weapons
from .drops import Drop

class Inventory:
    def __init__(self, player):
        self.player = player
        self.rects = [[], []]
        self.update_surf()

    def update_surf(self):
        self.surf = pygame.Surface((5*80, 5*80+144), pygame.SRCALPHA)
        self.rects = [[], []]
        for y in range(5):
            for x in range(5):
                self.surf.blit(sprites["Inventory Slot"], (x*80, y*80+144))
        
        for index, item in enumerate(self.player.inventory):
            self.rects[0].append([pygame.Rect((1280*0.25-196)+(index%5)*80, (720*0.5-196)+(index//5)*80, 72, 72), item])
            self.surf.blit(pygame.transform.scale(sprites[item], (sprites[item].get_width()*2, sprites[item].get_height()*2)), ((index%5)*80+2, (index//5)*80+2+144))


        s = self.surf.get_width()*0.5-116

        for x in range(3):
            self.rects[1].append([pygame.Rect(s+x*80+1280*0.25-self.surf.get_width()*0.5, 20, 72, 72), self.player.equipment[x]])
            self.surf.blit(sprites["Inventory Slot"], (s+x*80, 0))
            if self.player.equipment[x].startswith("No "):
                if x < 2:
                    if self.player.classes[x] == "Archer":
                        spr_name = "No AWeapon"
                    elif self.player.classes[x] == "Mage":
                        spr_name = "No MWeapon"
                    else:
                        spr_name = "No Shield"
                else:
                    spr_name = "No Armor"
            else:
                spr_name = self.player.equipment[x]
            self.surf.blit(pygame.transform.scale(sprites[spr_name], (sprites[spr_name].get_width()*2, sprites[spr_name].get_height()*2)), (s+x*80+2, 2))

    def draw(self, win: pygame.Surface, screen_size: list[int, int]):
        win.blit(self.surf, (screen_size[0]*0.25-196, 20))

    def pick_item(self, item: str):
        if len(self.player.inventory) < 25:
            if item == "arrow":
                if "Archer" in self.player.classes and self.player.stats["EP"][self.player.classes.index("Archer")][0] < self.player.stats["EP"][self.player.classes.index("Archer")][1]:
                    i = self.player.classes.index("Archer")
                    self.player.stats["EP"][i][0] += 1
                    if self.player.stats["EP"][i][0] > self.player.stats["EP"][i][1]:
                        self.player.stats["EP"][i][0] = self.player.stats["EP"][i][1]

                    return True
            elif item == "spirit":
                if "Mage" in self.player.classes and self.player.stats["EP"][self.player.classes.index("Mage")][0] < self.player.stats["EP"][self.player.classes.index("Mage")][1]:
                    i = self.player.classes.index("Mage")
                    self.player.stats["EP"][i][0] += 3
                    if self.player.stats["EP"][i][0] > self.player.stats["EP"][i][1]:
                        self.player.stats["EP"][i][0] = self.player.stats["EP"][i][1]
                    
                    return True
            else:
                self.player.inventory.append(item)
                self.update_surf()
                return True

    def equip_item(self, item: str, player: Player):
        equipment: list[dict] = load_json(["scripts", "cache", "equipment.json"])
        moved = False

        try:
            i = player.classes.index(weapons[item].player_class)
            if player.classes[0] == player.classes[1] and not player.equipment[0].startswith("No ") and player.equipment[1].startswith("No "):
                i = 1
            if not player.equipment[i].startswith("No "):
                player.inventory.append(player.equipment[i])
            player.equipment[i] = item
            moved = True
        
        except:
            if item in equipment[1].keys():
                i = 1
            elif item in equipment[2].keys():
                i = 2
            else:
                return

            if not player.equipment[i].startswith("No "):
                player.inventory.append(player.equipment[i])
            player.equipment[i] = item
            moved = True
        
        if moved:
            if item in player.inventory:
                player.inventory.remove(item)

            if item in weapons:
                weapon = weapons.get(item)
                if weapon.player_class in player.classes:
                    i = player.classes.index(weapon.player_class)
                else:
                    i = 0

                player.stats["AP"][i] = weapon.attack_power
            elif item in equipment[2]:
                player.stats["DP"] = equipment[2][item]["dp"]

            self.update_surf()

    def unequip_item(self, item: str, player: Player):
        if len(player.inventory) < 25:
            if not item.startswith("No "):
                player.inventory.append(item)
                i = player.equipment.index(item)
                player.equipment[i] = f"No Primary" if i == 0 else "No Shield" if i == 1 and not player.classes[1] else "No Secondry" if i == 1 else "No Armor"
                
                equipment: list[dict] = load_json(["scripts", "cache", "equipment.json"])
                if item in weapons:
                    weapon = weapons.get(item)
                    if weapon.player_class in player.classes:
                        i = player.classes.index(weapon.player_class)
                    else:
                        i = 0

                    player.stats["AP"][i] = 0
                elif item in equipment[2]:
                    player.stats["DP"] = 0
                
                self.update_surf()

    def throw_inv_item(self, item: str, player: Player):
        if item in player.inventory:
            player.inventory.remove(item)

        self.update_surf()
        return [item, Drop(player.x, player.y, sprites[item]), time.time()]

    def throw_eq_item(self, item: str, player: Player):
        if not item.startswith("No "):
            i = player.equipment.index(item)
            player.equipment[i] = f"No Primary" if i == 0 else "No Shield" if i == 1 and not player.classes[1] else "No Secondry" if i == 1 else "No Armor"
            
            equipment: list[dict] = load_json(["scripts", "cache", "equipment.json"])
            if item in weapons:
                weapon = weapons.get(item)
                if weapon.player_class in player.classes:
                    i = player.classes.index(weapon.player_class)
                else:
                    i = 0

                player.stats["AP"][i] = 0
            elif item in equipment[2]:
                player.stats["DP"] = 0
            
            self.update_surf()
            return [item, Drop(player.x, player.y, sprites[item]), time.time()]
