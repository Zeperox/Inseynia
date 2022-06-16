import pygame, csv, os, importlib, shutil
from pygame.locals import *

from scripts.loading.json_functions import load_json
from scripts.logic.drops import Drop
from scripts.logic.entity import Entity
from scripts.loading.sprites import sprites

if "maps" not in os.listdir(os.path.join("scripts", "cache")):
    os.mkdir(os.path.join("scripts", "cache", "maps"))

enemy_list = {}
for file in os.scandir(os.path.join("scripts", "AI")):
    if file.is_file():
        mod = importlib.import_module(f'scripts.AI.{file.name[:-3]}')
        enemy_list[mod.__name__[mod.__name__.index(".", mod.__name__.index(".")+1)+1:]] = mod
for dir in os.scandir(os.path.join("scripts", "maps")):
    if dir.is_dir() and dir.name != "__pycache__":
        if dir.name in os.listdir(os.path.join("scripts", "cache", "maps")):
            shutil.rmtree(os.path.join("scripts", "cache", "maps", dir.name))
        shutil.copytree(dir.path, os.path.join("scripts", "cache", "maps", dir.name))

for mod in os.scandir(os.path.join("mods")):
    if mod.is_dir():
        try:
            for file in os.scandir(os.path.join("mods", mod.name, "scripts", "AI")):
                if file.is_file() and file.name.endswith(".py"):
                    mod = importlib.import_module(f'mods.{mod}.scripts.AI.{file.name[:-3]}')
                    enemy_list[mod.__name__[mod.__name__.index(".", mod.__name__.index(".")+1)+1:]] = mod
        except:
            continue
        try:
            for dir in os.scandir(os.path.join("mods", mod.name, "scripts", "maps")):
                if dir.is_dir() and dir.name != "__pycache__":
                    if dir.name in os.listdir(os.path.join("scripts", "cache", "maps")):
                        shutil.rmtree(os.path.join("scripts", "cache", "maps", dir.name))
                    shutil.copytree(dir.path, os.path.join("scripts", "cache", "maps", dir.name))
        except:
            continue

IDs = load_json(["scripts", "cache", "IDs.json"])
enemy_data = load_json(["scripts", "cache", "enemies.json"])

animations = {}
enemy_names = []
for index, enemy_ID in enumerate(IDs["Enemies"]):
    IDs["Enemies"][index] = enemy_list.get(enemy_data[enemy_ID]["AI"].lower())
    if IDs["Enemies"][index]:
        animations[enemy_ID] = [os.path.join("assets", "ANIMATIONSDL", enemy_ID, animation) for animation in enemy_data[enemy_ID]["animations"]]
        enemy_names.append(enemy_ID)


class Tile:
    def __init__(self, x, y, image_loc):
        self.x = x
        self.y = y
        self.image = pygame.transform.scale2x(pygame.image.load(image_loc)).convert()
        self.image.set_colorkey((0,0,0))
    
    def draw(self, win, scroll):
        win.blit(self.image, (self.x-scroll[0], self.y-scroll[1]))

class TileMap:
    def __init__(self, filename, room, screen_size):
        self.tile_size = 50
        self.start_x, self.start_y = 0, 0
        self.room = room
        self.screen_size = screen_size
        self.tiles, self.drops, self.enemies = self.load_tiles(filename); self.tiles: list[pygame.Surface]; self.drops: list[Drop]; self.enemies: list[Entity]
        self.map_surface = pygame.Surface((self.w, self.h))
        self.map_surface.set_colorkey((0,0,0))
        self.load_map()

    def draw_map(self, win, player, projs, dt, scroll=[0, 0]):
        win.blit(self.map_surface, (self.x-scroll[0], self.y-scroll[1]))

        for drop in self.drops:
            drop[1].draw(win, scroll)

        objs: list[Tile | Entity] = self.tiles+self.enemies+projs+[player]
        objs = sorted(objs, key=lambda obj: obj.y)
        for obj in objs:
            if type(obj) == Tile:
                obj.draw(win, scroll)
            else:
                obj.draw(win, scroll, dt)
        

    def load_map(self):
        for i, tile in enumerate(self.tiles):
            if tile[1] == False:
                tile[0].draw(self.map_surface, [0, 0])
            else:
                self.tiles[i] = tile[0]

        self.tiles = [tile for tile in self.tiles if type(tile) == Tile]


    def read_csv(self, filename):
        map = []
        with open(os.path.join(filename)) as data:
            data = csv.reader(data, delimiter=",")
            for row in data:
                map.append(list(row))
        return map

    def load_tiles(self, filename):
        tiles = []
        self.tile_rects = []
        map = self.read_csv(filename)

        filename = filename.split(".")
        drops = []
        drop_map = self.read_csv(filename[0]+" drops.csv")
        enemies = []
        enemy_map = self.read_csv(filename[0]+" enemies.csv")
        spawn_map = self.read_csv(filename[0]+" spawn.csv")
        

        self.w, self.h = len(map[0])*(self.tile_size), len(map)*(self.tile_size)

        if self.screen_size[0] > self.w:
            self.x = (self.screen_size[0]*0.5)-(self.w*0.5)
        else:
            self.x = 0
        if self.screen_size[1] > self.h:
            self.y = (self.screen_size[1]*0.5)-(self.h*0.5)
        else:
            self.y = 0

        for y, row in enumerate(map):
            for x, tile in enumerate(row):
                tile = int(tile)
                if tile != -1:
                    tiles.append([Tile(x*self.tile_size, y*self.tile_size, IDs["Tiles"][self.room][tile][0]), IDs["Tiles"][self.room][tile][1]])
                    if IDs["Tiles"][self.room][tile][1]:
                        rect = pygame.Rect(self.x+x*(self.tile_size), self.y+y*(self.tile_size), (self.tile_size), (self.tile_size))
                        tile_rect = rect.inflate(0, -10)
                        tile_rect.center = rect.center
                        self.tile_rects.append(tile_rect)

        for y, row in enumerate(spawn_map):
            for x, tile in enumerate(row):
                tile = int(tile)
                if tile == 0:
                    self.start_x, self.start_y = self.x+x*(self.tile_size), self.y+y*(self.tile_size)

        for y, row in enumerate(drop_map):
            for x, drop in enumerate(row):
                drop = int(drop)
                if drop != -1:
                    drops.append([IDs["Items"][drop], Drop(x*self.tile_size+self.x, y*self.tile_size+self.y, sprites[IDs["Items"][drop]]), 0])

        for y, row in enumerate(enemy_map):
            for x, enemy in enumerate(row):
                enemy = int(enemy)
                if enemy != -1:
                    enemies.append(IDs["Enemies"][enemy].AI(x*self.tile_size+self.x, y*self.tile_size+self.y, animations[enemy_names[enemy]], 5, enemy_data[enemy_names[enemy]]))

        return tiles, drops, enemies
