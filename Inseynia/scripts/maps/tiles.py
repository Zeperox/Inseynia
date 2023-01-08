import pygame, csv, os, importlib, shutil, time
from pygame.locals import *

from scripts.loading.json_functions import load_json
from scripts.logic.drops import Drop, ProjDrop
from scripts.logic.entity import Entity
from scripts.visuals.cutscene import Cutscene
from scripts.visuals.dialogue import Dialogue
from scripts.loading.sprites import sprites
from scripts.logic.npc import NPC
from scripts.custom_collisions.angle import AngleRect

if "maps" not in os.listdir(os.path.join("scripts", "cache")):
	os.mkdir(os.path.join("scripts", "cache", "maps"))

ai_list = {}
for file in os.scandir(os.path.join("scripts", "AI")):
	if file.is_file():
		mod = importlib.import_module(f'scripts.AI.{file.name[:-3]}')
		ai_list[mod.__name__[mod.__name__.index(".", mod.__name__.index(".")+1)+1:]] = mod
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
					mod = importlib.import_module(f'mods.{mod.name}.scripts.AI.{file.name[:-3]}')
					ai_list[mod.__name__[mod.__name__.index(".", mod.__name__.index(".")+1)+1:]] = mod
		except:
			continue

		try:
			for dir in os.scandir(os.path.join("mods", mod.name, "scripts", "maps")):
				if dir.is_dir() and dir.name != "__pycache__":
					if f"{mod.name}'s {dir.name}" in os.listdir(os.path.join("scripts", "cache", "maps")):
						shutil.rmtree(os.path.join("scripts", "cache", "maps", f"{mod.name}'s {dir.name}"))
					shutil.copytree(dir.path, os.path.join("scripts", "cache", "maps", f"{mod.name}'s {dir.name}"))

					'''for map_file in os.scandir(os.path.join("scripts", "cache", "maps", f"{mod.name}'s {dir.name}")):
						main_file = os.path.join("scripts", "cache", "maps", f"{mod.name}'s {dir.name}", map_file.name)
						tmpFile = "wa.csv"
						with open(main_file, "r+") as file, open(tmpFile, "w") as f:
							reader = csv.reader(file, delimiter=',')
							colValues = []
							for i, row in enumerate(reader):
								colValues.append([])
								for col in row:
									if col == "-1":
										colValues[-1].append("5")
									else:
										colValues[-1].append(col)
							file.write("")
							writer = csv.writer(f, delimiter=',')
							for colVal in colValues:
								writer.writerow(colVal)
						os.remove(main_file)
						os.rename(tmpFile, main_file)'''
		except:
			continue

IDs = load_json(["scripts", "cache", "IDs.json"])
enemies_data: dict = load_json(["scripts", "cache", "enemies.json"])

enemy_list = {}
for enemy_name, enemy_data in enemies_data.items():
	ai = ai_list.get(enemy_data["AI"].lower())
	if ai:
		enemy_list[enemy_name] = {"AI": ai, "Anim": os.path.join("assets", "ANIMATIONSDL", enemy_name)}
del ai_list


class Tile:
	def __init__(self, x, y, image_loc):
		self.x = x
		self.y = y
		self.image = pygame.transform.scale2x(pygame.image.load(image_loc).convert())
		self.rect = self.image.get_rect(x=x, y=y)
		self.image.set_colorkey((0,0,0))
	
	def draw(self, win, scroll):
		win.blit(self.image, (self.x-scroll[0], self.y-scroll[1]))

	@property
	def width(self):
		return self.image.get_width()
	
	@property
	def height(self):
		return self.image.get_height()
	
class TileMap:
	def __init__(self, filename, room, screen_size, load_from_files=True, save=1):
		self.tile_size = 32
		self.room = room
		self.screen_size = screen_size

		self.full_tiles: list[Tile] = [[], []]
		self.full_drops: list[str, Drop, int] = []
		self.full_enemies: list[Entity] = []
		self.full_npcs: list[NPC] = []
		self.tiles: list[Tile] = []
		self.drops: list[str, Drop, int] = []
		self.enemies: list[Entity] = []
		self.npcs: list[NPC] = []
		self.cutscene_entities: list[Entity] = []
		self.tile_rects: list[pygame.Rect] = []
		self.dlg_trg_rects: list[pygame.Rect] = []
		self.cut_rects: list[pygame.Rect] = []
		self.connectors: list[list[pygame.Rect, int, int, int]] = []

		for file in os.listdir(filename):
			if file.endswith(".csv") and " " not in file:
				filename = os.path.join(filename, file)
		if not filename.endswith(".csv"):
			raise NameError("Invalid Path")
		self.load_tiles(filename, load_from_files, save)

		self.map_surface = pygame.Surface((self.w, self.h))
		self.load_map()

	def draw_map(self, win, player, projs, scroll):
		self.tiles = []
		self.drops = []
		self.enemies = []
		self.npcs = []

		win.blit(self.map_surface, (self.x-scroll.x, self.y-scroll.y))

		for drop in self.full_drops:
			if drop[1].rect.colliderect(scroll):
				self.drops.append(drop)
				drop[1].draw(win, scroll)

		objs: list[Tile | Entity | pygame.Rect] = self.full_tiles+self.full_enemies+self.full_npcs+[entity[0] for entity in self.cutscene_entities]+projs+[player]
		objs = sorted(objs, key=lambda obj: obj.y)
		for obj in objs:
			if obj.rect.colliderect(scroll):
				if obj in self.full_tiles:
					self.tiles.append(obj)
				elif obj in self.full_enemies:
					self.enemies.append(obj)
				elif obj in self.full_npcs:
					self.npcs.append(obj)

				if not type(obj) == pygame.Rect:
					obj.draw(win, scroll)
			elif obj in self.full_enemies and obj.type == "boss":
				obj.draw(win, scroll)
			
	def load_map(self):
		for tile in self.full_tiles[1]:
			tile.draw(self.map_surface, (0, 0))

		self.full_tiles = self.full_tiles[0]

	def read_csv(self, filename):
		map = []
		with open(os.path.join(filename)) as data:
			data = csv.reader(data, delimiter=",")
			for row in data:
				map.append(list(row))
		return map

	def load_tiles(self, filename, load_from_files, save):
		tile_map = self.read_csv(filename)

		filename = filename.split(".")
		bg_map = self.read_csv(filename[0]+" bg.csv")
		connector_map = self.read_csv(filename[0]+" connectors.csv")
		dlg_map = self.read_csv(filename[0]+" dialogue.csv")
		drop_map = self.read_csv(filename[0]+" drops.csv")
		enemy_map = self.read_csv(filename[0]+" enemies.csv")
		
		self.w, self.h = len(tile_map[0])*(self.tile_size), len(tile_map)*(self.tile_size)

		if self.screen_size[0] > self.w:
			self.x = (self.screen_size[0]*0.5)-(self.w*0.5)
		else:
			self.x = 0
		if self.screen_size[1] > self.h:
			self.y = (self.screen_size[1]*0.5)-(self.h*0.5)
		else:
			self.y = 0

		self.tile_rects.append([])
		for y, row in enumerate(tile_map):
			if len(self.tile_rects) > 1:
				self.tile_rects[-1].append(None)
			self.tile_rects.append([None])
			for x, tile in enumerate(row):
				tile = int(tile)
				if tile != -1:
					if tile != -2:
						self.full_tiles[0].append(Tile(self.x+x*self.tile_size, self.y+y*self.tile_size, IDs["Tiles"][self.room][tile]["tile"]))
					if "rect" in IDs["Tiles"][self.room][tile].keys():
						tile_rect = pygame.Rect(self.x+x*(self.tile_size)+IDs["Tiles"][self.room][tile]["rect"][0]*2, self.y+y*(self.tile_size)+IDs["Tiles"][self.room][tile]["rect"][1]*2, IDs["Tiles"][self.room][tile]["rect"][2]*2, IDs["Tiles"][self.room][tile]["rect"][3]*2)
					elif "angle" in IDs["Tiles"][self.room][tile].keys():
						tile_rect = AngleRect(self.x+x*(self.tile_size)+IDs["Tiles"][self.room][tile]["angle"][0]*2, self.y+y*(self.tile_size)+IDs["Tiles"][self.room][tile]["angle"][1]*2, IDs["Tiles"][self.room][tile]["angle"][2]*2, IDs["Tiles"][self.room][tile]["angle"][3]*2, IDs["Tiles"][self.room][tile]["angle"][4])
					self.tile_rects[y+1].append(tile_rect)
				else:
					self.tile_rects[y+1].append(None)
		self.tile_rects[0] = [None for _ in range(len(self.tile_rects[1]))]+[None, None]
		self.tile_rects.append([None for _ in range(len(self.tile_rects[1]))]+[None, None])

		for y, row in enumerate(bg_map):
			for x, tile in enumerate(row):
				tile = int(tile)
				if tile != -1:
					self.full_tiles[1].append(Tile(self.x+x*self.tile_size, self.y+y*self.tile_size, IDs["Tiles"][self.room][tile]["tile"]))

		for y, row in enumerate(connector_map):
			for x, tile in enumerate(row):
				if tile != "-1":
					tile = tile.split(":")
					tile = [tile[0]]+[int(t) for t in tile[1:]]
					self.connectors.append([pygame.Rect(self.x+x*(self.tile_size), self.y+y*(self.tile_size), (self.tile_size), (self.tile_size)), tile[0], tile[1]*self.tile_size, tile[2]*self.tile_size])

		if load_from_files:
			for y, row in enumerate(drop_map):
				for x, drop in enumerate(row):
					drop = int(drop)
					if drop != -1:
						self.full_drops.append([IDs["Items"][drop], Drop(x*self.tile_size+self.x, y*self.tile_size+self.y, sprites[IDs["Items"][drop]]), 0, time.time()])

			for y, row in enumerate(enemy_map):
				for x, enemy in enumerate(row):
					enemy = int(enemy)
					if enemy != -1:
						enemy_name = IDs["Enemies"][enemy]
						self.full_enemies.append(enemy_list[enemy_name]["AI"].AI(x*self.tile_size+self.x, y*self.tile_size+self.y, enemy_list[enemy_name]["Anim"], enemies_data[enemy_name], enemy_name))
						if self.full_enemies[-1].type == "boss":
							self.full_enemies[-1].active = False

			inputted_triggers = {}
			for y, row in enumerate(dlg_map):
				for x, dlg in enumerate(row):
					if dlg.startswith("cut"):
						if dlg not in inputted_triggers.keys():
							inputted_triggers[dlg] = Cutscene(dlg)

						rect = pygame.Rect(self.x+x*(self.tile_size)-1, self.y+y*(self.tile_size)-1, (self.tile_size)+2, (self.tile_size)+2)
						for trg_rect in self.cut_rects:
							if rect.colliderect(trg_rect[0]) and trg_rect[1] == inputted_triggers[dlg]:
								trg_rect[0] = trg_rect[0].union(rect)
								break
						else:
							self.cut_rects.append([rect, inputted_triggers[dlg]])
					elif dlg.startswith("trg"):
						if dlg not in inputted_triggers.keys():
							inputted_triggers[dlg] = Dialogue(dlg)

						rect = pygame.Rect(self.x+x*(self.tile_size)-1, self.y+y*(self.tile_size)-1, (self.tile_size)+2, (self.tile_size)+2)
						for trg_rect in self.dlg_trg_rects:
							if rect.colliderect(trg_rect[0]) and trg_rect[1] == inputted_triggers[dlg]:
								trg_rect[0] = trg_rect[0].union(rect)
								break
						else:
							self.dlg_trg_rects.append([rect, inputted_triggers[dlg]])
					elif dlg.startswith("npc"):
						self.full_npcs.append(NPC(x*self.tile_size+self.x, y*self.tile_size+self.y, dlg, dlg.split(":")[-2] in enemy_list.keys(), dlg.split(":")[-2], enemies_data.get(dlg.split(":")[-2]), Dialogue(dlg)))
		else:
			save = load_json(["scripts", "saves", f"save{save}.json"])
			for enemy in save["enemies"][self.room]:
				self.full_enemies.append(enemy_list[enemy[2]]["AI"].AI(enemy[0], enemy[1], enemy_list[enemy[2]]["Anim"], enemy[3], enemy[2]))
				if self.full_enemies[-1].type == "boss":
					self.full_enemies[-1].active = False
			
			for drop in save["drops"][self.room]:
				if drop[3] == "proj":
					self.full_drops.append([drop[2], ProjDrop(drop[0], drop[1], sprites[drop[2]], drop[4], drop[5]), 0, time.time()])
				else:
					self.full_drops.append([drop[2], Drop(drop[0], drop[1], sprites[drop[2]]), 0, time.time()])
			
			for npc in save["dialogues"][self.room]["npc"]:
				self.full_npcs.append(NPC(npc[0], npc[1], npc[2], npc[2].split(":")[-2] in enemy_list.keys(), npc[2].split(":")[-2], enemies_data.get(npc[2].split(":")[-2]), Dialogue(npc[2])))
			for dlg in save["dialogues"][self.room]["dlg"]:
				self.dlg_trg_rects.append([pygame.Rect(dlg[0][0], dlg[0][1], dlg[0][2], dlg[0][3]), Dialogue(dlg[1])])
			for cut in save["dialogues"][self.room]["cut"]:
				self.cut_rects.append([pygame.Rect(cut[0][0], cut[0][1], cut[0][2], cut[0][3]), Cutscene(cut[1])])


	@property
	def width(self):
		return self.map_surface.get_width()
	
	@property
	def height(self):
		return self.map_surface.get_height()
