import pygame, csv, os; from pygame.locals import *

tiles_csv = {
    "Dev Room": {
        "0": [os.path.join("assets", "Tiles", "Dev Room", "floor1.png"), False],
        "1": "Spawn",
        "2": [os.path.join("assets", "Tiles", "Dev Room", "wall1.png"), True],
        "3": [os.path.join("assets", "Tiles", "Dev Room", "wallD1.png"), True],
        "4": [os.path.join("assets", "Tiles", "Dev Room", "wallDL1.png"), True],
        "5": [os.path.join("assets", "Tiles", "Dev Room", "wallDR1.png"), True],
        "6": [os.path.join("assets", "Tiles", "Dev Room", "wallL1.png"), True],
        "7": [os.path.join("assets", "Tiles", "Dev Room", "wallR1.png"), True],
        "8": [os.path.join("assets", "Tiles", "Dev Room", "wallU1.png"), True],
        "9": [os.path.join("assets", "Tiles", "Dev Room", "wallUL1.png"), True],
        "10": [os.path.join("assets", "Tiles", "Dev Room", "wallUR1.png"), True]
    }
}

class Tile:
    def __init__(self, x, y, image_loc):
        self.x = x
        self.y = y
        self.image = pygame.transform.scale(pygame.image.load(image_loc), (50, 50)).convert()
        self.image.set_colorkey((0,0,0))
    
    def draw(self, win):
        win.blit(self.image, (self.x, self.y))


class TileMap:
    def __init__(self, filename, room, screen_size):
        self.tile_size = 50
        self.start_x, self.start_y = 0, 0
        self.room = room
        self.screen_size = screen_size
        self.tiles = self.load_tiles(filename)
        self.set_spawn(f"{filename.split('.')[0]} spawn.csv")
        self.map_surface = pygame.Surface((self.map_w, self.map_h))
        self.map_surface.set_colorkey((0,0,0))
        self.load_map()

    def draw_map(self, win, scroll=[0, 0]):
        win.blit(self.map_surface, (self.x-scroll[0], self.y-scroll[1]))

    def load_map(self):
        for tile in self.tiles:
            tile.draw(self.map_surface)

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

        self.map_w, self.map_h = len(map[0])*self.tile_size, len(map)*self.tile_size

        if self.screen_size[0] > self.map_w:
            self.x = (self.screen_size[0]*0.5)-(self.map_w*0.5)
        else:
            self.x = 0
        if self.screen_size[1] > self.map_h:
            self.y = (self.screen_size[1]*0.5)-(self.map_h*0.5)
        else:
            self.y = 0

        x, y = 0, 0
        for row in map:
            x = 0
            for tile in row:
                if tile != "-1":
                    if tiles_csv[self.room][tile] != "Spawn":
                        tiles.append(Tile(x*self.tile_size, y*self.tile_size, tiles_csv[self.room][tile][0]))
                        if tiles_csv[self.room][tile][1]:        
                            self.tile_rects.append(pygame.Rect(self.x+x*self.tile_size, self.y+y*self.tile_size, self.tile_size, self.tile_size))
                    else:
                        self.start_x, self.start_y = self.x+x*self.tile_size, self.y+y*self.tile_size
                x += 1
            y += 1

        return tiles

    def set_spawn(self, filename):
        spawn_map = self.read_csv(filename)

        x, y = 0, 0
        for row in spawn_map:
            x = 0
            for tile in row:
                if tile != "-1":
                    if tiles_csv[self.room][tile] == "Spawn":
                        self.start_x, self.start_y = self.x+x*self.tile_size, self.y+y*self.tile_size
                x += 1
            y += 1
                