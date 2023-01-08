import pygame, time, os

from scripts.loading.sprites import sprites
from scripts.loading.json_functions import load_json
from .player import Player, weapons
from .drops import Drop, Spirit, ProjDrop
from scripts.visuals.text import Text

class Inventory:
	def __init__(self, player: Player):
		self.player = player
		self.rects = [[], []]
		self.index = 4
		self.update_surf()

	def update_surf(self):
		weight_text = Text(os.path.join("assets", "fontsDL", "font.png"), f"Weight: {self.player.inv_weight[0]}/{self.player.inv_weight[1]}", 2, (255, 255, 255))
		if self.player.inv_weight[1] == None:
			weight_text.content = ""

		self.surf = pygame.Surface((5*40, (5-self.player.inv_size%5)*40+weight_text.height+82))
		self.surf.set_colorkey((0, 0, 0))

		weight_text.render(self.surf, (self.surf.get_width()*0.5-weight_text.width*0.5, 0))

		self.rects = [[], []]
		for y in range(self.player.inv_size//5):
			for x in range(5-self.player.inv_size%5):
				self.surf.blit(sprites["Inventory Slot"], (x*40, y*40+weight_text.height+62))
		
		for index, item in enumerate(self.player.inventory):
			self.rects[0].append([pygame.Rect((640*0.25-98)+(index%5)*40, (360*0.5-118)+(index//5)*40+weight_text.height+10, 36, 36), item])
			self.surf.blit(pygame.transform.scale(sprites[item], (sprites[item].get_width()*2, sprites[item].get_height()*2)), ((index%5)*40+2, (index//5)*40+weight_text.height+64))


		s = self.surf.get_width()*0.5-77

		for x in range(4):
			self.rects[1].append([pygame.Rect(s+x*40+650*0.25-self.surf.get_width()*0.5, weight_text.height+20, 36, 36), self.player.equipment[x]])
			self.surf.blit(sprites["Inventory Slot"], (s+x*40, weight_text.height+10))
			spr_name = self.player.equipment[x]
			self.surf.blit(pygame.transform.scale(sprites[spr_name], (sprites[spr_name].get_width()*2, sprites[spr_name].get_height()*2)), (s+x*40+2, weight_text.height+12))

	def draw(self, win: pygame.Surface, screen_size: list[int, int]):
		win.blit(self.surf, (screen_size[0]*0.25-98, 10))

		mouse_pos = pygame.mouse.get_pos()
		select = False
		for i, rect in enumerate(self.rects[1]):
			if rect[0].collidepoint(mouse_pos):
				self.index = i
				select = True
				break

		if not select:
			for i, rect in enumerate(self.rects[0]):
				if rect[0].collidepoint(mouse_pos):
					self.index = i+4
					break

		if len(self.rects[0]) == 0:
			self.index = 3
		if self.index < 4:
			pygame.draw.rect(win, (255, 255, 255), self.rects[1][self.index][0], 3)
		else:
			pygame.draw.rect(win, (255, 255, 255), self.rects[0][self.index-4][0], 3)

	def pick_item(self, item: str, drop_data):
		if len(self.player.inventory) < self.player.inv_size:
			if type(drop_data) == ProjDrop:
				if drop_data.shooter == self.player:
					if "Archer" in self.player.classes and self.player.stats["EP"][self.player.classes.index("Archer")][0] < self.player.stats["EP"][self.player.classes.index("Archer")][1]:
						i = self.player.classes.index("Archer")
						self.player.stats["EP"][i][0] += 1
						if self.player.stats["EP"][i][0] > self.player.stats["EP"][i][1]:
							self.player.stats["EP"][i][0] = self.player.stats["EP"][i][1]

						return True
				else:
					return False
			elif type(drop_data) == Spirit:
				if "Mage" in self.player.classes and self.player.stats["EP"][self.player.classes.index("Mage")][0] < self.player.stats["EP"][self.player.classes.index("Mage")][1]:
					i = self.player.classes.index("Mage")
					self.player.stats["EP"][i][0] += 3
					if self.player.stats["EP"][i][0] > self.player.stats["EP"][i][1]:
						self.player.stats["EP"][i][0] = self.player.stats["EP"][i][1]
					
					return True
			else:
				self.player.inventory.append(item)
				items = load_json(["scripts", "cache", "items.json"])

				self.player.inv_weight[0] = 0
				for weight_item in self.player.inventory:
					self.player.inv_weight[0] += items[weight_item]["weight"]

				self.update_surf()
				return True

	def equip_item(self, item: str):
		equipment: list[dict] = load_json(["scripts", "cache", "equipment.json"])
		items = load_json(["scripts", "cache", "items.json"])
		moved = False

		try:
			i = self.player.classes.index(weapons[item].player_class)
			if self.player.classes[0] == self.player.classes[1] and not self.player.equipment[0].startswith("No ") and self.player.equipment[1].startswith("No "):
				i = 1
			if not self.player.equipment[i].startswith("No "):
				self.player.inventory.append(self.player.equipment[i])
			self.player.equipment[i] = item
			moved = True
		
		except:
			if item in equipment[1].keys():
				i = 1
			elif item in equipment[2].keys():
				i = 2
			elif item in equipment[3].keys():
				i = 3
				if self.player.inv_size > equipment[3][item]["slots"]:
					return
				self.player.inv_size = equipment[3][item]["slots"]
				self.player.inv_weight[1] = equipment[3][item]["max weight"]
			elif item in equipment[4].keys():
				for buff in equipment[4][item][0]:
					if "HP+" in buff:
						if buff[-1] == "+":
							self.player.stats["HP"][0] = self.player.stats["HP"][1]
						else:
							self.player.stats["HP"][0] += int(buff[-1])
							if self.player.stats["HP"][0] > self.player.stats["HP"][1]:
								self.player.stats["HP"][0] = self.player.stats["HP"][1]
					elif "SP+" in buff:
						if buff[-1] == "+":
							self.player.stats["SP"][0] = self.player.stats["SP"][1]
						else:
							self.player.stats["SP"][0] += int(buff[-1])
							if self.player.stats["SP"][0] > self.player.stats["SP"][1]:
								self.player.stats["SP"][0] = self.player.stats["SP"][1]
					elif "MP+" in buff:
						if "Mage" in self.player.classes:
							ind = self.player.classes.index("Mage")
							if buff[-1] == "+":
								self.player.stats["EP"][ind][0] = self.player.stats["EP"][ind][1]
							else:
								self.player.stats["EP"][ind][0] += int(buff[-1])
								if self.player.stats["EP"][ind][0] > self.player.stats["EP"][ind][1]:
									self.player.stats["EP"][ind][0] = self.player.stats["EP"][ind][1]
					elif "QP+" in buff:
						if "Archer" in self.player.classes:
							ind = self.player.classes.index("Archer")
							if buff[-1] == "+":
								self.player.stats["EP"][ind][0] = self.player.stats["EP"][ind][1]
							else:
								self.player.stats["EP"][ind][0] += int(buff[-1])
								if self.player.stats["EP"][ind][0] > self.player.stats["EP"][ind][1]:
									self.player.stats["EP"][ind][0] = self.player.stats["EP"][ind][1]

				del self.player.inventory[self.index-4]
				
				self.player.inv_weight[0] = 0
				for weight_item in self.player.inventory:
					self.player.inv_weight[0] += items[weight_item]["weight"]

				self.update_surf()
				self.player._generate_UI(True)
				return
			else:
				return

			if not self.player.equipment[i].startswith("No "):
				self.player.inventory.append(self.player.equipment[i])
			self.player.equipment[i] = item

			moved = True
		
		if moved:
			del self.player.inventory[self.index-4]

			if item in weapons:
				weapon = weapons.get(item)
				if weapon.player_class in self.player.classes:
					i = self.player.classes.index(weapon.player_class)
				else:
					i = 0

				self.player.stats["AP"][i] = weapon.attack_power+self.player.stats["XP"][2]-1
			elif item in equipment[2]:
				self.player.stats["DP"] = equipment[2][item]["defense"]+self.player.stats["XP"][2]-1
			
			self.player.inv_weight[0] = 0
			for weight_item in self.player.inventory:
				self.player.inv_weight[0] += items[weight_item]["weight"]

			self.update_surf()

	def unequip_item(self, item: str):
		if len(self.player.inventory) < self.player.inv_size:
			if not item.startswith("No "):
				i = self.player.equipment.index(item)
				if i == 0:
					self.player.equipment[i] = ("No AWeapon", "No MWeapon")[self.player.classes[i] == "Mage"]
				elif i == 1:
					if self.player.classes[i] == None:
						self.player.equipment[i] = "No Shield"
					else:
						self.player.equipment[i] = ("No AWeapon", "No MWeapon")[self.player.classes[i] == "Mage"]
				elif i == 2:
					self.player.equipment[i] = "No Armor"
				else:
					if len(self.player.inventory) >= 5:
						return
					self.player.equipment[i] = "No Backpack"
					self.player.inv_size = 5
					self.player.inv_weight[1] = None
				
				self.player.inventory.append(item)
				items = load_json(["scripts", "cache", "items.json"])

				equipment: list[dict] = load_json(["scripts", "cache", "equipment.json"])
				if item in weapons:
					weapon = weapons.get(item)
					if weapon.player_class in self.player.classes:
						i = self.player.classes.index(weapon.player_class)
					else:
						i = 0

					self.player.stats["AP"][i] = 0
				elif item in equipment[2]:
					self.player.stats["DP"] = self.player.stats["XP"][2]-1
				
				self.player.inv_weight[0] = 0
				for weight_item in self.player.inventory:
					self.player.inv_weight[0] += items[weight_item]["weight"]

				self.update_surf()

	def throw_inv_item(self, item: str):
		del self.player.inventory[self.index-4]
		items = load_json(["scripts", "cache", "items.json"])

		self.player.inv_weight[0] = 0
		for weight_item in self.player.inventory:
			self.player.inv_weight[0] += items[weight_item]["weight"]

		self.update_surf()
		return [item, Drop(self.player.x, self.player.y, sprites[item]), time.time(), time.time()]

	def throw_eq_item(self, item: str):
		if not item.startswith("No "):
			i = self.player.equipment.index(item)
			if i == 0:
				self.player.equipment[i] = ("No AWeapon", "No MWeapon")[self.player.classes[i] == "Mage"]
			elif i == 1:
				if self.player.classes[i] == None:
					self.player.equipment[i] = "No Shield"
				else:
					self.player.equipment[i] = ("No AWeapon", "No MWeapon")[self.player.classes[i] == "Mage"]
			elif i == 2:
				self.player.equipment[i] = "No Armor"
			else:
				if len(self.player.inventory) > 5:
					return
				self.player.equipment[i] = "No Backpack"
				self.player.inv_size = 5
				self.player.inv_weight[1] = None

			equipment: list[dict] = load_json(["scripts", "cache", "equipment.json"])
			if item in weapons:
				weapon = weapons.get(item)
				if weapon.player_class in self.player.classes:
					i = self.player.classes.index(weapon.player_class)
				else:
					i = 0

				self.player.stats["AP"][i] = 0
			elif item in equipment[2]:
				self.player.stats["DP"] = self.player.stats["XP"][2]-1
			
			self.update_surf()
			return [item, Drop(self.player.x, self.player.y, sprites[item]), time.time(), time.time()]

	def select_slot(self, button: int):
		if button == pygame.CONTROLLER_BUTTON_DPAD_LEFT:
			if self.index > 0:
				self.index -= 1
			else:
				self.index = len(self.player.equipment+self.player.inventory)-1
		if button == pygame.CONTROLLER_BUTTON_DPAD_RIGHT:
			if self.index < len(self.player.equipment+self.player.inventory)-1:
				self.index += 1
			else:
				self.index = 0
		if button == pygame.CONTROLLER_BUTTON_DPAD_UP:
			if self.index > 4:
				self.index -= 5
			elif self.index == 4:
				self.index = 0
			else:
				self.index = len(self.player.equipment+self.player.inventory)-self.index-1
		if button == pygame.CONTROLLER_BUTTON_DPAD_DOWN:
			if self.index < len(self.player.equipment+self.player.inventory)-5:
				self.index += 5
			elif self.index == len(self.player.equipment+self.player.inventory)-5:
				self.index = 0
			elif self.index == len(self.player.equipment+self.player.inventory)-4:
				self.index = 1
			elif self.index == len(self.player.equipment+self.player.inventory)-3:
				self.index = 2
			elif self.index in [len(self.player.equipment+self.player.inventory)-2, len(self.player.equipment+self.player.inventory)-1]:
				self.index = 3
