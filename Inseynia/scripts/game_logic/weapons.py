'''from typing import List
import pygame, os, time
from scripts.data.json_functions import *
from .projectiles import Projectiles

class Weapon:
    def __init__(self, x, y, width, height, stats, eclass=None):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, width, height)

        self.stats = stats
        self.eclass = eclass

        self.cooldown = 0

    def use(self, affected_entities, mouse_pos=None, scroll=[0, 0], attack_modifier=1):
        if time.time() - self.cooldown >= self.stats["Cooldown"]:
            if self.stats["Class"] == "Swordsman" or self.eclass == "Melee":
                for entity in affected_entities:
                    if self.rect.colliderect(entity.rect):
                        entity["Health"] -= self.stats["Attack"]*attack_modifier
            elif (self.stats["Class"] == "Archer" or self.stats["Class"] == "Mage") or self.eclass == "Ranged":
                Projectiles(self.x, self.y+arrow_img.get_height()*0.5, self.stats["Attack"]*attack_modifier, self.stats["Speed"], (mouse_pos[0]-scroll[0], mouse_pos[1]-scroll[1]), arrow_img)
            self.cooldown = time.time()

weapons = {
    "Wooden Sword": Weapon(0, 0, 1, 1, load_json(["scripts", "data", "equipment.json"])[0]["Wooden Sword"]),
    "Rusty Dagger": Weapon(0, 0, 1, 1, load_json(["scripts", "data", "equipment.json"])[0]["Rusty Dagger"]),
    "Rusty Sword": Weapon(0, 0, 1, 1, load_json(["scripts", "data", "equipment.json"])[0]["Rusty Sword"]),
    "Spear": Weapon(0, 0, 1, 1, load_json(["scripts", "data", "equipment.json"])[0]["Spear"]),
    "Steel Scimitar": Weapon(0, 0, 1, 1, load_json(["scripts", "data", "equipment.json"])[0]["Steel Scimitar"]),
    
    "Wooden Halfbow": Weapon(0, 0, 1, 1, load_json(["scripts", "data", "equipment.json"])[0]["Wooden Halfbow"]),
    "Wooden Bow": Weapon(0, 0, 1, 1, load_json(["scripts", "data", "equipment.json"])[0]["Wooden Bow"]),
    "Steel Halfbow": Weapon(0, 0, 1, 1, load_json(["scripts", "data", "equipment.json"])[0]["Steel Halfbow"]),
    "Crossbow": Weapon(0, 0, 1, 1, load_json(["scripts", "data", "equipment.json"])[0]["Crossbow"]),
    
    "Walking Staff": Weapon(0, 0, 1, 1, load_json(["scripts", "data", "equipment.json"])[0]["Walking Staff"]),
    "Amateur Staff": Weapon(0, 0, 1, 1, load_json(["scripts", "data", "equipment.json"])[0]["Amateur Staff"]),
    "Advanced Staff": Weapon(0, 0, 1, 1, load_json(["scripts", "data", "equipment.json"])[0]["Advanced Staff"]),
    "Book of Arcs": Weapon(0, 0, 1, 1, load_json(["scripts", "data", "equipment.json"])[0]["Book of Arcs"]),
    "Lightning Charges": Weapon(0, 0, 1, 1, load_json(["scripts", "data", "equipment.json"])[0]["Lightning Charges"]),
}'''