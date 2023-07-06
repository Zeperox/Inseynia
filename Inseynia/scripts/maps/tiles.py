import pygame, os, shutil, time

if __name__ == "__main__":
	import json

	with open(os.path.join("scripts", "cacheDL", "IDs.json"), "r") as f:
		IDs = json.load(f)
	room = input("Enter the name of the desired map: ")
	with open(os.path.join("scripts", "maps", f"{room}.json"), "r") as f:
		map_data = json.load(f)

	bg_surf = pygame.Surface((map_data["size"][0]*32, map_data["size"][1]*32))
	main_surf = bg_surf.copy()
	
	for y in range(map_data["size"][1]+1):
		for x in range(map_data["size"][0]+1):
			if f"{x}:{y}" in map_data["main tiles"]:
				tile = map_data["main tiles"][f"{x}:{y}"]
				if tile >= 0:
					main_surf.blit(pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "SPRITES", "tiles", f"{IDs['Tiles'][room][tile][0]}.png"))), (x*32, y*32))

			if f"{x}:{y}" in map_data["bg img tiles"]:
				tile = map_data["bg img tiles"][f"{x}:{y}"]
				if tile >= 0:
					bg_surf.blit(pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "SPRITES", "tiles", f"{IDs['Tiles'][room][tile][0]}.png"))), (x*32, y*32))

	pygame.image.save(bg_surf, os.path.join("assets", "IMAGES", "maps", f"{room} bg.png"))
	pygame.image.save(main_surf, os.path.join("assets", "IMAGES", "maps", f"{room} main.png"))

			

	quit()
else:
	from scripts.loadingDL.files import files
	from scripts.loadingDL.json_functions import load_json
	from scripts.loadingDL.sprites import sprite

	Drop = files["drops"].Drop; ProjDrop = files["drops"].ProjDrop
	Cutscene = files["cutscene"].Cutscene
	Dialogue = files["dialogue"].Dialogue
	NPC = files["npc"].NPC
	AngleRect = files["angle"].AngleRect


if "maps" not in os.listdir(os.path.join("scripts", "cacheDL")):
	os.mkdir(os.path.join("scripts", "cacheDL", "maps"))

ai_list = {}
for file in os.scandir(os.path.join("scripts", "AI")):
	if file.is_file():
		ai_list[file.name[:-3]] = files[file.name[:-3]]
for dir in os.scandir(os.path.join("scripts", "maps")):
	if dir.is_dir() and dir.name != "__pycache__":
		if dir.name in os.listdir(os.path.join("scripts", "cacheDL", "maps")):
			shutil.rmtree(os.path.join("scripts", "cacheDL", "maps", dir.name))
		shutil.copytree(dir.path, os.path.join("scripts", "cacheDL", "maps", dir.name))


IDs = load_json(["scripts", "cacheDL", "IDs.json"])
enemies_data: dict = load_json(["scripts", "cacheDL", "enemies.json"])

enemy_list = {}
for enemy_name, enemy_data in enemies_data.items():
	ai = ai_list.get(enemy_data["AI"].lower())
	if ai:
		enemy_list[enemy_name] = {"AI": ai, "Anim": os.path.join("assets", "ANIMATIONSDL", enemy_name)}
del ai_list

tiles = IDs["Tiles"]

blank_tile = pygame.Surface((32, 32))
blank_tile.set_colorkey((0, 0, 0))

class Tile:
	def __init__(self, x, y, tile_img, collision, main_map, render=True):
		self.x = x
		self.y = y
		self.img = tile_img
		self.main_map = main_map
		self.render = render

		self.main_rect = self.img.get_rect(x=x+collision[1], y=y+collision[2])
		self.proj_collide = collision[3]
		if collision[0] == "angle":
			self.rect = AngleRect(x, y, self.width, self.height, collision[4])
		else:
			self.rect = self.main_rect.copy()

	def draw(self, win, scroll):
		if self.render:
			return (self.img, (self.x-scroll.x, self.y-scroll.y))

	def special(self, entity):
		pass

	@property
	def width(self):
		return self.img.get_width()
	
	@property
	def height(self):
		return self.img.get_height()

class TileMap:
	def __init__(self, room, save=None):
		self.tile_size = 32
		self.room = room

		self.data = load_json(["scripts", "maps", f"{room}.json"])
		self.data["size"][0] *= 32; self.data["size"][1] *= 32
		
		if 640 > self.data["size"][0]:
			self.x = 320-(self.data["size"][0]*0.5)
		else:
			self.x = 0
		if 360 > self.data["size"][1]:
			self.y = 180-(self.data["size"][1]*0.5)
		else:
			self.y = 0

		self.bg_surf = sprite(f"{room} bg")
		self.main_surf = sprite(f"{room} main")

		self.tiles = {}
		self.bgs = {}
		self.connectors = []

		self.full_enemies = []
		self.full_drops = []
		self.full_npcs = []
		self.full_projs = []
		self.trg_rects = []
		self.cut_rects = []

		self.enemies = []
		self.drops = []
		self.npcs = []
		self.projs = []
		self.cutscene_entities = []

		self.initial_load(save)

	def initial_load(self, save):
		# connectors
		for loc, data in self.data["connectors"].items():
			loc = [int(_loc) for _loc in loc.split(":")]
			self.connectors.append([pygame.Rect(self.x+loc[0]*(self.tile_size), self.y+loc[1]*(self.tile_size), (self.tile_size), (self.tile_size)), data[0], data[1]*self.tile_size, data[2]*self.tile_size])

		if save and self.room in save["enemies"]:
			# enemies
			for enemy in save["enemies"][self.room]:
				self.full_enemies.append(enemy_list[enemy[2]]["AI"].AI(enemy[0], enemy[1], enemy_list[enemy[2]]["Anim"], enemy[3], enemy[2]))
				if self.full_enemies[-1].type == "boss":
					self.full_enemies[-1].active = False

			# drops
			for drop in save["drops"][self.room]:
				if drop[3] == "normal":
					self.full_drops.append([drop[2], Drop(drop[0], drop[1], sprite(drop[2])), 0, time.time()])
				else:
					self.full_drops.append([drop[2], ProjDrop(drop[0], drop[1], sprite(f"proj_{drop[2]}"), drop[4], drop[5]), 0, time.time()])
			
			# npcs
			for npc in save["dialogues"][self.room]["npc"]:
				self.full_npcs.append(NPC(npc[0], npc[1], npc[2], npc[2].split(":")[1] in enemy_list.keys(), npc[2].split(":")[1], enemies_data.get(npc[2].split(":")[1]), Dialogue(npc[2])))
		
			# trgs
			for trg in save["dialogues"][self.room]["trg"]:
				self.trg_rects.append([pygame.Rect(trg[0][0], trg[0][1], trg[0][2], trg[0][3]), Dialogue(trg[1])])

			# cuts
			for cut in save["dialogues"][self.room]["cut"]:
				self.cut_rects.append([pygame.Rect(cut[0][0], cut[0][1], cut[0][2], cut[0][3]), Cutscene(cut[1])])
		else:
			# enemies
			for ID, data in self.data["enemies"].items():
				enemy_name = IDs["Enemies"][int(ID)]
				self.full_enemies.append(enemy_list[enemy_name]["AI"].AI(data[0]*self.tile_size+self.x, data[1]*self.tile_size+self.y, enemy_list[enemy_name]["Anim"], enemies_data[enemy_name], enemy_name))
				if self.full_enemies[-1].type == "boss":
					self.full_enemies[-1].active = False

			# drops
			for ID, data in self.data["drops"].items():
				self.full_drops.append([IDs["Items"][int(ID)], Drop(data[0]*self.tile_size+self.x, data[1]*self.tile_size+self.y, sprite(IDs["Items"][int(ID)])), 0, time.time()])

			# npcs
			if "NPC" in self.data["dialogues"]:
				for ID, data in self.data["dialogues"]["NPC"].items():
					self.full_npcs.append(NPC(data[0]*self.tile_size+self.x, data[1]*self.tile_size+self.y, ID, ID.split(":")[1] in enemy_list.keys(), ID.split(":")[1], enemies_data.get(ID.split(":")[1]), Dialogue(ID)))

			# trgs
			if "TRG" in self.data["dialogues"]:
				for ID, data in self.data["dialogues"]["TRG"].items():
					self.trg_rects.append([pygame.Rect(data[0]*32, data[1]*32, data[2]*32, data[3]*32), Dialogue(ID)])

			# cuts
			if "CUT" in self.data["dialogues"]:
				for ID, data in self.data["dialogues"]["CUT"].items():
					self.cut_rects.append([pygame.Rect(data[0]*32, data[1]*32, data[2]*32, data[3]*32), Cutscene(ID)])

	def draw_map(self, win, player, scroll):
		blits = [(self.bg_surf, (self.x-scroll.x, self.y-scroll.y))]

		for drop in self.drops:
			surf = drop[1].draw(win, scroll)
			if surf:
				blits.append(surf)
		
		blits.append((self.main_surf, (self.x-scroll.x, self.y-scroll.y)))

		objs = list(self.tiles.values())+self.enemies+self.npcs+[entity[0] for entity in self.cutscene_entities]+self.projs+[player]
		objs = sorted(objs, key=lambda obj: obj.y)
		for obj in objs:
			if obj in self.full_enemies:
				self.enemies.append(obj)
			elif obj in self.full_npcs:
				self.npcs.append(obj)

			if not isinstance(obj, pygame.Rect):
				surf = obj.draw(win, scroll)
				if surf:
					blits.append(surf)

		win.blits(blits)
		
	def load_tiles(self, scroll, player):
		self.tiles = {}
		self.bgs = {}
		if len(self.projs+self.enemies+[player]) <= 300:
			for entity in self.projs+self.enemies+[player]:
				entity_x, entity_y = (entity.rect.centerx//32)-1, (entity.rect.centery//32)-1
				for y in range(3):
					for x in range(3):
						loc = f"{entity_x+x}:{entity_y+y}"
						if loc in self.data["main tiles"]:
							tile = self.data["main tiles"][loc]
							if tiles[self.room][self.data["main tiles"][loc]][2] in files.keys():
								self.tiles[loc] = files[tiles[self.room][self.data["main tiles"][loc]][2]].Tile((entity_x+x)*self.tile_size, (entity_y+y)*self.tile_size, sprite(tiles[self.room][self.data["main tiles"][loc]][0]), tiles[self.room][self.data["main tiles"][loc]][1], True)
							elif tile >= 0:
								self.tiles[loc] = Tile((entity_x+x)*self.tile_size, (entity_y+y)*self.tile_size, sprite(tiles[self.room][self.data["main tiles"][loc]][0]), tiles[self.room][self.data["main tiles"][loc]][1], True)
							else:
								if tile == -1:
									collision = ["rect", 0, 0, False]
								elif tile == -2:
									collision = ["angle", 0, 0, False, 0]
								elif tile == -3:
									collision = ["angle", 0, 0, False, 1]
								elif tile == -4:
									collision = ["angle", 0, 0, False, 2]
								elif tile == -5:
									collision = ["angle", 0, 0, False, 3]
								
								self.tiles[loc] = Tile((entity_x+x)*self.tile_size, (entity_y+y)*self.tile_size, blank_tile, collision, True)

						if loc in self.data["bg tiles"]:
							tile = self.data["bg tiles"][loc]
							if tiles[self.room][self.data["bg tiles"][loc]][2] in files.keys():
								self.bgs[loc] = files[tiles[self.room][self.data["bg tiles"][loc]][2]].Tile((entity_x+x)*self.tile_size, (entity_y+y)*self.tile_size, sprite(tiles[self.room][self.data["bg tiles"][loc]][0]), tiles[self.room][self.data["bg tiles"][loc]][1], False)
							else:
								self.bgs[loc] = Tile((entity_x+x)*self.tile_size, (entity_y+y)*self.tile_size, sprite(tiles[self.room][self.data["bg tiles"][loc]][0]), tiles[self.room][self.data["bg tiles"][loc]][1], False)
		else:
			scroll_x = scroll.x//32
			scroll_y = scroll.y//32
			self.tiles = {f"{scroll_x+x}:{scroll_y+y}": Tile(self.x+(scroll_x+x)*self.tile_size, self.y+(scroll_y+y)*self.tile_size, sprite(tiles[self.room][self.data["main tiles"][f"{scroll_x+x}:{scroll_y+y}"]][0]), tiles[self.room][self.data["main tiles"][f"{scroll_x+x}:{scroll_y+y}"]][1], True) if self.data["main tiles"][f"{scroll_x+x}:{scroll_y+y}"] != -2 and tiles[self.room][self.data["main tiles"][f"{scroll_x+x}:{scroll_y+y}"]][2] not in files.keys() else files[tiles[self.room][self.data["main tiles"][f"{scroll_x+x}:{scroll_y+y}"]][2]].Tile(self.x+(scroll_x+x)*self.tile_size, self.y+(scroll_y+y)*self.tile_size, sprite(tiles[self.room][self.data["main tiles"][f"{scroll_x+x}:{scroll_y+y}"]][0]), tiles[self.room][self.data["main tiles"][f"{scroll_x+x}:{scroll_y+y}"]][1], True) if self.data["main tiles"][f"{scroll_x+x}:{scroll_y+y}"] != -2 else Tile(self.x+(scroll_x+x)*self.tile_size, self.y+(scroll_y+y)*self.tile_size, blank_tile, tiles[self.room][self.data["main tiles"][f"{scroll_x+x}:{scroll_y+y}"]][1], True) for x in range(21) for y in range(13) if f"{scroll_x+x}:{scroll_y+y}" in self.data["main tiles"]}
			self.bgs = {f"{scroll_x+x}:{scroll_y+y}": Tile(self.x+(scroll_x+x)*self.tile_size, self.y+(scroll_y+y)*self.tile_size, sprite(tiles[self.room][self.data["bg tiles"][f"{scroll_x+x}:{scroll_y+y}"]][0]), tiles[self.room][self.data["bg tiles"][f"{scroll_x+x}:{scroll_y+y}"]][1], False) if tiles[self.room][self.data["bg tiles"][f"{scroll_x+x}:{scroll_y+y}"]][2] not in files.keys() else files[tiles[self.room][self.data["bg tiles"][f"{scroll_x+x}:{scroll_y+y}"]][2]].Tile(self.x+(scroll_x+x)*self.tile_size, self.y+(scroll_y+y)*self.tile_size, sprite(tiles[self.room][self.data["bg tiles"][f"{scroll_x+x}:{scroll_y+y}"]][0]), tiles[self.room][self.data["bg tiles"][f"{scroll_x+x}:{scroll_y+y}"]][1], False) for x in range(21) for y in range(13) if f"{scroll_x+x}:{scroll_y+y}" in self.data["bg tiles"]}
