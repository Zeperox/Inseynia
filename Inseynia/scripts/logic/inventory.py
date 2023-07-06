import pygame, time, os

from scripts.loadingDL.files import files

from scripts.loadingDL.sprites import sprite
from scripts.loadingDL.json_functions import load_json
Player = files["player"].Player; weapons = files["player"].weapons
Drop = files["drops"].Drop; Spirit = files["drops"].Spirit; ProjDrop = files["drops"].ProjDrop
Text = files["text"].Text
effects = files["effects"].effects

items = load_json(["scripts", "dataDL", "items.json"])
langs = load_json(["scripts", "dataDL", "langs.json"])
equipment: list[dict] = load_json(["scripts", "cacheDL", "equipment.json"])
items = load_json(["scripts", "cacheDL", "items.json"])


class Inventory:
	def __init__(self, player: Player):
		self.player = player
		self.rects = [[], []]
		self.index = 6
		self.select_area = "inv"
		self.weight_text = Text(os.path.join("assets", "fontsDL", "font.ttf"), "" if self.player.inv_weight[1] == None else f"Weight: {self.player.inv_weight[0]}/{self.player.inv_weight[1]}", 16, (255, 255, 255), bold=True)

		self.tooltips = {lang: {} for lang in langs}

		text_use = Text(os.path.join("assets", "fontsDL", "font.ttf"), ": Use/(Un)equip Item", 16, (255, 255, 255))
		text_throw = Text(os.path.join("assets", "fontsDL", "font.ttf"), ": Throw Item", 16, (255, 255, 255))
		#text_switch = Text(os.path.join("assets", "fontsDL", "font.ttf"), ": Switch", 16, (255, 255, 255))
		text_close = Text(os.path.join("assets", "fontsDL", "font.ttf"), ": Close Inventory", 16, (255, 255, 255))
		surf_k_use = sprite("K_space")
		surf_k_throw = sprite("K_left shift")
		surf_k_close = sprite("K_escape")

		surf_c_use = sprite("button_a")
		surf_c_throw = sprite("button_x")
		surf_c_close = sprite("button_b")

		self.inv_k_controls = pygame.Surface((640, text_use.height+10), pygame.SRCALPHA)
		self.inv_k_controls.fblits((
			(surf_k_use, (5, 5)),
			(sprite("mouse_1"), (surf_k_use.get_width()+10, 5)),
			(text_use.surf, (surf_k_use.get_width()+sprite("mouse_1").get_width()+15, 5)),
			
			(surf_k_throw, (320-(text_throw.width+sprite("mouse_3").get_width()+surf_k_throw.get_width())*0.5, 5)),
			(sprite("mouse_3"), (320-(text_throw.width+sprite("mouse_3").get_width()+surf_k_throw.get_width())*0.5+surf_k_throw.get_width()+5, 5)),
			(text_throw.surf, (320-(text_throw.width+sprite("mouse_3").get_width()+surf_k_throw.get_width())*0.5+surf_k_throw.get_width()+sprite("mouse_3").get_width()+10, 5)),
			
			(surf_k_close, (640-text_close.width-surf_k_close.get_width()-10, 5)),
			(text_close.surf, (640-text_close.width-5, 5))
		))

		self.inv_c_controls = pygame.Surface((640, text_use.height+10), pygame.SRCALPHA)
		self.inv_c_controls.fblits((
			(surf_c_use, (5, 5)),
			(text_use.surf, (surf_c_use.get_width()+10, 5)),
			
			(surf_c_throw, (320-(text_throw.width+surf_c_throw.get_width())*0.5, 5)),
			(text_throw.surf, (320-(text_throw.width+surf_c_throw.get_width())*0.5+surf_c_throw.get_width()+5, 5)),
			
			(surf_c_close, (640-text_close.width-surf_c_close.get_width()-10, 5)),
			(text_close.surf, (640-text_close.width-5, 5))
		))

	def draw(self, win: pygame.Surface, lang, input_method):
		if self.player.inv_weight[1] == None and self.weight_text.content != "": self.weight_text.content = ""
		elif f"Weight: {self.player.inv_weight[0]}/{self.player.inv_weight[1]}" != self.weight_text.content and self.player.inv_weight[1] != None: self.weight_text.content = f"Weight: {self.player.inv_weight[0]}/{self.player.inv_weight[1]}"
		win.blit(self.weight_text.surf, (560-(self.weight_text.width*0.5), 270))
		
		self.rects = [[], []]
		y = 0
		for x in range(self.player.inv_size):
			if x % 10 == 0 and x > 0:
				y += 1

			item = self.player.inventory[x] if len(self.player.inventory)-1 >= x else None
			self.rects[0].append([pygame.Rect((x-y*10)*40+40, y*40+40, 36, 36), item])
			win.blit(sprite("Inventory Slot"), ((x-y*10)*40+40, y*40+40))
			if item is not None:
				win.blit(pygame.transform.scale(sprite(item), (sprite(item).get_width()*2, sprite(item).get_height()*2)), ((x-y*10)*40+42, y*40+42))

		for i in range(6):
			if i < 3:
				x = 0
				y = i
			else:
				x = 1
				y = i-3

			self.rects[1].append([pygame.Rect(600-(2-x)*40, 150+y*40, 36, 36), self.player.equipment[i]])
			win.blit(sprite("Inventory Slot"), (600-(2-x)*40, 150+y*40))
			spr_name = self.player.equipment[i]
			win.blit(pygame.transform.scale(sprite(spr_name), (sprite(spr_name).get_width()*2, sprite(spr_name).get_height()*2)), (602-(2-x)*40, 150+y*40+2))


		mouse_pos = pygame.mouse.get_pos()
		for i, rect in enumerate(self.rects[1]):
			if rect[0].collidepoint(mouse_pos):
				self.index = i
				break
		else:
			for i, rect in enumerate(self.rects[0]):
				if rect[0].collidepoint(mouse_pos):
					self.index = i+6
					break

		if self.index < 6:
			pygame.draw.rect(win, (255, 128, 0), self.rects[1][self.index][0], 1)
		else:
			pygame.draw.rect(win, (255, 128, 0), self.rects[0][self.index-6][0], 1)

		rects = self.rects[1] + self.rects[0]
		if rects[self.index][1] is not None:
			if rects[self.index][1] not in self.tooltips[lang]:
				name = Text(os.path.join("assets", "fontsDL", "font.ttf"), items[rects[self.index][1]]["name"][list(langs.keys()).index(lang)], 16, (62, 41, 20) if rects[self.index][1] in weapons.keys() and weapons.get(rects[self.index][1]).player_class == "Archer" else (0, 58, 144) if rects[self.index][1] in weapons.keys() and weapons.get(rects[self.index][1]).player_class == "Mage" else (150, 33, 13) if rects[self.index][1] in weapons.keys() and weapons.get(rects[self.index][1]).player_class == "Swordsman" else (120, 120, 120) if rects[self.index][1] in weapons.keys() and weapons.get(rects[self.index][1]).player_class == "Thief" else (255, 255, 255), lang, bold=True)
				text = Text(os.path.join("assets", "fontsDL", "font.ttf"), items[rects[self.index][1]]["tooltip"][list(langs.keys()).index(lang)], 16, (255, 255, 255), lang)
				if max([name.width, text.width]) < 214:
					surf = pygame.Surface((max([name.width, text.width])+5, name.height+text.height+10))
				else:
					text.max_width = 214
					surf = pygame.Surface((219, name.height+text.height+10))

				if text.content == "":
					surf = surf.subsurface((0, 0, name.width+5, name.height+10))
				surf.fill((255, 255, 255))
				surf.fill((0, 0, 0), (1, 1, surf.get_width()-2, surf.get_height()-2))
				name_x = 5
				if lang == "arabic":
					text.align = pygame.FONT_RIGHT
					if name.width < text.width:
						name_x = 0
					else:
						name_x = name.width-text.width

				surf.fblits((
					(name.surf, (surf.get_width()*0.5-name.width*0.5, 5)),
					(text.surf, ((name_x, name.height+10)))
				))
				self.tooltips[lang][rects[self.index][1]] = surf

			tooltip = self.tooltips[lang][rects[self.index][1]]
			win.blit(tooltip, (rects[self.index][0].right if rects[self.index][0].right+tooltip.get_width() < 640 else rects[self.index][0].left-tooltip.get_width(), rects[self.index][0].bottom if rects[self.index][0].bottom+tooltip.get_height() < 360 else rects[self.index][0].top-tooltip.get_height()))
		if input_method == "keys":
			win.blit(self.inv_k_controls, (0, 360-self.inv_k_controls.get_height()))
		else:
			win.blit(self.inv_c_controls, (0, 360-self.inv_c_controls.get_height()))

	def pick_item(self, item: str, drop_data):
		if isinstance(drop_data, ProjDrop):
			projs = []
			if self.player.weapons[0] != [None, None]:
				projs.append(self.player.weapons[0][1].proj_data["img"])
			if self.player.weapons[1] != [None, None]:
				projs.append(self.player.weapons[1][1].proj_data["img"])

			if drop_data.name in projs:
				if "Archer" in self.player.classes and self.player.stats["EP"][self.player.classes.index("Archer")][0] < self.player.stats["EP"][self.player.classes.index("Archer")][1]:
					i = self.player.classes.index("Archer")
					self.player.stats["EP"][i][0] += 1
					if self.player.stats["EP"][i][0] > self.player.stats["EP"][i][1]:
						self.player.stats["EP"][i][0] = self.player.stats["EP"][i][1]

					return True
			else:
				return False
		elif isinstance(drop_data, Spirit):
			if "Mage" in self.player.classes and self.player.stats["EP"][self.player.classes.index("Mage")][0] < self.player.stats["EP"][self.player.classes.index("Mage")][1]:
				i = self.player.classes.index("Mage")
				self.player.stats["EP"][i][0] += 3
				if self.player.stats["EP"][i][0] > self.player.stats["EP"][i][1]:
					self.player.stats["EP"][i][0] = self.player.stats["EP"][i][1]
				
				return True
		else:
			if len(self.player.inventory) < self.player.inv_size:
				self.player.inventory.append(item)

				self.player.inv_weight[0] = 0
				for weight_item in self.player.inventory:
					self.player.inv_weight[0] += items[weight_item]["weight"]

				return True

	def equip_item(self, item: str):
		moved = False

		try:
			i = self.player.classes.index(weapons[item].player_class)
			if not self.player.equipment[i].startswith("No "):
				self.player.inventory.append(self.player.equipment[i])
			self.player.equipment[i] = item
			moved = True
		
		except:
			if item in equipment[1].keys() or item in equipment[0]:
				i = 1
			elif item in equipment[2].keys():
				i = 2
				if self.player.inv_size > equipment[2][item]["slots"]:
					return
				self.player.inv_size = equipment[2][item]["slots"]
				self.player.inv_weight[1] = equipment[2][item]["max weight"]
			elif item in equipment[3].keys():
				if equipment[3][item]["type"] == "helm":
					i = 3
				elif equipment[3][item]["type"] == "chest":
					i = 4
				elif equipment[3][item]["type"] == "legg":
					i = 5
			elif item in equipment[4].keys():
				buff = equipment[4][item].split(" ")
				self.player.effects.append(effects[buff[0]](self.player, int(buff[1]), int(buff[2])))
				self.player.effects[-1].pause()
				del self.player.inventory[self.index-6]
				
				self.player.inv_weight[0] = 0
				for weight_item in self.player.inventory:
					self.player.inv_weight[0] += items[weight_item]["weight"]

				return
			else:
				return

			if not self.player.equipment[i].startswith("No "):
				self.player.inventory.append(self.player.equipment[i])
			self.player.equipment[i] = item

			moved = True
		
		if moved:
			del self.player.inventory[self.index-6]

			if item in weapons:
				weapon = weapons.get(item)
				if weapon.player_class in self.player.classes:
					i = self.player.classes.index(weapon.player_class)
				else:
					i = 0

				self.player.stats["AP"][i] = weapon.attack_power+self.player.stats["AP"][i]
			elif item in equipment[3]:
				self.player.stats["DP"] += equipment[3][item]["defense"]+self.player.stats["DP"]
				self.player.weight += equipment[3][item]["weight"]
				self.player.knockback_resist += equipment[3][item]["knockback resistence"]
			
			self.player.inv_weight[0] = 0
			for weight_item in self.player.inventory:
				self.player.inv_weight[0] += items[weight_item]["weight"]

	def unequip_item(self, item: str):
		if len(self.player.inventory) < self.player.inv_size:
			if not item.startswith("No "):
				i = self.player.equipment.index(item)

				if i < 2:
					if self.player.classes[i] == "Archer":
						empty_equip = "No AWeapon"
					elif self.player.classes[i] == "Mage":
						empty_equip = "No MWeapon"
					elif self.player.classes[i] == "Swordsman":
						empty_equip = "No SWeapon"
					elif self.player.classes[i] == "Thief":
						empty_equip = "No TWeapon"

				if i == 0:
					self.player.equipment[i] = empty_equip
				elif i == 1:
					if self.player.classes[i] == None:
						self.player.equipment[i] = "No Shield"
					else:
						self.player.equipment[i] = empty_equip
				elif i == 2:
					if len(self.player.inventory) >= 5:
						return
					self.player.equipment[i] = "No Backpack"
					self.player.inv_size = 5
					self.player.inv_weight[1] = None
				elif i == 3:
					self.player.equipment[i] = "No Helmet"
				elif i == 4:
					self.player.equipment[i] = "No Chest"
				elif i == 5:
					self.player.equipment[i] = "No Leggings"
				
				self.player.inventory.append(item)
				if item in weapons:
					weapon = weapons.get(item)
					if weapon.player_class in self.player.classes:
						i = self.player.classes.index(weapon.player_class)
					else:
						i = 0

					self.player.stats["AP"][i] -= weapon.attack_power
				elif item in equipment[3]:
					self.player.stats["DP"] -= equipment[3][item]["defense"]
					self.player.weight -= equipment[3][item]["weight"]
					self.player.knockback_resist -= equipment[3][item]["knockback resistence"]
				
				self.player.inv_weight[0] = 0
				for weight_item in self.player.inventory:
					self.player.inv_weight[0] += items[weight_item]["weight"]

	def throw_inv_item(self, item: str):
		del self.player.inventory[self.index-6]

		self.player.inv_weight[0] = 0
		for weight_item in self.player.inventory:
			self.player.inv_weight[0] += items[weight_item]["weight"]

		return [item, Drop(self.player.x, self.player.y, sprite(item)), time.time(), time.time()]

	def throw_eq_item(self, item: str):
		if not item.startswith("No "):
			i = self.player.equipment.index(item)

			if i < 2:
				if self.player.classes[i] == "Archer":
					empty_equip = "No AWeapon"
				elif self.player.classes[i] == "Mage":
					empty_equip = "No MWeapon"
				elif self.player.classes[i] == "Swordsman":
					empty_equip = "No SWeapon"
				elif self.player.classes[i] == "Thief":
					empty_equip = "No TWeapon"

			if i == 0:
				self.player.equipment[i] = empty_equip
			elif i == 1:
				if self.player.classes[i] == None:
					self.player.equipment[i] = "No Shield"
				else:
					self.player.equipment[i] = empty_equip
			elif i == 2:
				if len(self.player.inventory) >= 5:
					return
				self.player.equipment[i] = "No Backpack"
				self.player.inv_size = 5
				self.player.inv_weight[1] = None
			elif i == 3:
				self.player.equipment[i] = "No Helmet"
			elif i == 4:
				self.player.equipment[i] = "No Chest"
			elif i == 5:
				self.player.equipment[i] = "No Leggings"

			if item in weapons:
				weapon = weapons.get(item)
				if weapon.player_class in self.player.classes:
					i = self.player.classes.index(weapon.player_class)
				else:
					i = 0

				self.player.stats["AP"][i] -=  weapon.attack_power
			elif item in equipment[3]:
				self.player.stats["DP"] -= equipment[3][item]["defense"]
				self.player.weight -= equipment[3][item]["weight"]
				self.player.knockback_resist -= equipment[3][item]["knockback resistence"]
			
			return [item, Drop(self.player.x, self.player.y, sprite(item)), time.time(), time.time()]

	def select_slot(self, button: int):
		if button == 0.1:
			self.select_area = "inv"
			self.index = 6
		elif button == 0.2:
			self.select_area = "eq"
			self.index = 0

		if self.select_area == "inv":
			self.index -= 6

			inv_rows = len(self.rects[0]) // 10
			last_row = len(self.rects[0]) % 10
			ind_row = self.index // 10
			ind_col = self.index % 10
			ind_row_length = 10 if ind_row < inv_rows else last_row

			if button == pygame.CONTROLLER_BUTTON_DPAD_LEFT:
				if ind_col > 0:
					self.index -= 1
				else:
					self.index = ind_row*10+ind_row_length-1
			if button == pygame.CONTROLLER_BUTTON_DPAD_RIGHT:
				if ind_col < ind_row_length-1:
					self.index += 1
				else:
					self.index = ind_row*10
			if button == pygame.CONTROLLER_BUTTON_DPAD_UP:
				if ind_row > 0:
					self.index -= 10
				else:
					if ind_col < last_row:
						self.index = (inv_rows)*10+ind_col
					else:
						self.index = (inv_rows-1)*10+ind_col
			if button == pygame.CONTROLLER_BUTTON_DPAD_DOWN:
				if (ind_col < last_row and ind_row >= inv_rows) or (ind_col > last_row-1 and ind_row >= inv_rows-1):
					self.index = ind_col
				else:
					self.index += 10

			self.index += 6
		else:
			if button in [pygame.CONTROLLER_BUTTON_DPAD_LEFT, pygame.CONTROLLER_BUTTON_DPAD_RIGHT]:
				if 0 <= self.index <= 2:
					self.index += 3
				else:
					self.index -= 3
			if button == pygame.CONTROLLER_BUTTON_DPAD_UP:
				if 0 <= self.index <= 2:
					if self.index > 0:
						self.index -= 1
					else:
						self.index = 2
				else:
					if self.index > 3:
						self.index -= 1
					else:
						self.index = 5
			if button == pygame.CONTROLLER_BUTTON_DPAD_DOWN:
				if 0 <= self.index <= 2:
					if self.index < 2:
						self.index += 1
					else:
						self.index = 0
				else:
					if self.index < 5:
						self.index += 1
					else:
						self.index = 3
