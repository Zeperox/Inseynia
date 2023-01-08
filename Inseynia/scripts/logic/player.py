import pygame, os, time, math, copy, importlib, random
from pygame.locals import *

from .entity import Entity
from scripts.custom_collisions.obb import OBB
from scripts.loading.json_functions import load_json
from scripts.loading.sprites import sprites
from scripts.visuals.text import Text
from .drops import Drop

weapons = {}
for file in os.scandir(os.path.join("scripts", "weapons")):
	if file.is_file():
		mod = importlib.import_module(f'scripts.weapons.{file.name[:-3]}')
		weapons[mod.weapon_name] = mod.Weapon
for mod in os.scandir(os.path.join("mods")):
	if mod.is_dir():
		try:
			for file in os.scandir(os.path.join("mods", mod.name, "scripts", "wepaons")):
				if file.is_file() and file.name.endswith(".py"):
					mod = importlib.import_module(f'mods.{mod.name}.scripts.weapons.{file.name[:-3]}')
					weapons[mod.weapon_name] = mod.Weapon
		except:
			continue


class Player(Entity):
	classes = [None, None]
	name = ""
	equipment = ["No Primary", "No Secondry", "No Armor", "No Backpack"]
	inventory = []
	inv_size = 5
	inv_weight = [0, None]
	inv_max_exceed_time = 0
	stats = {
		"HP": [999, 10], # current_HP, max_HP
		"SP": [10, 10], #current_SP, max_SP
		"AP": [1, 1], # weapon_1, weapon_2
		"DP": 0,
		"EP": [[5, 10], [7, 10]], # current_stat_1, max_stat_1 | current_stat_2, max_stat_2
		"M": 100,
		"XP": [2, 3, 1] # xp, max_xp, level
	}
	map = None
	def __init__(self, x: int, y: int):
		s = pygame.Surface((16, 32))
		s.fill((255,255,255))
		pygame.draw.rect(s, (0,0,0), (0, 0, 16, 32), 2)
		
		super().__init__(x, y, s)
		self.cached_stats = copy.deepcopy(self.stats)
		self.dirs = [1, 0]
		self.door_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.w*1.5, self.rect.h)

		self.attack_cooldown = [0, 0]
		self.shielded = [None, 0]
		self.regen_time = [0, 0, 0] # health, stamina, mana

		self.dash = False
		self.pre_dash_loc = 0
		self.dash_cooldown = 0
		self.dash_dir = 0

		self._move = True
		self.knockback_resist = 0

		self.main_stats_surf = pygame.Surface((64, 152))
		self.main_stats_surf.set_colorkey((0,0,0))
		self.inv_stats_surf = pygame.Surface((269.5, 325))
		self.inv_stats_surf.set_colorkey((0,0,0))


		self.held_buttons = []
		self.weapons = [[None, None], [None, None]]
		self.damage_counters = []

		self.sleep = [False, True]
		self.sleep_stamina = 10

		self._generate_UI(False)

	def dmg_counter_log(self, dt):
		for dmg_counter in reversed(self.damage_counters):
			if dmg_counter[1][1] > 0.1 and not dmg_counter[1][2]:
				dmg_counter[1][1] *= 0.8
			else:
				if not dmg_counter[1][2]:
					dmg_counter[1][1] = -dmg_counter[1][1]
				dmg_counter[1][2] = True
				dmg_counter[1][1] /= 0.95
			dmg_counter[1][0][1] -= dmg_counter[1][1]*dt

			if dmg_counter[1][1] < 0:
				dmg_counter[0].alpha = dmg_counter[0].alpha-7.5*dt
				if dmg_counter[0].alpha <= 5 and dmg_counter in self.damage_counters:
					self.damage_counters.remove(dmg_counter)

	def draw(self, win: pygame.Surface, scroll: list[int, int]):
		super().draw(win, scroll)
		for dmg_counter in reversed(self.damage_counters):
			dmg_counter[0].render(win, (dmg_counter[1][0][0], dmg_counter[1][0][1]), scroll)

	def _generate_UI(self, inv_open):
		stat_names = []
		for x in range(2):
			if self.classes[x] == "Archer":
				stat_names.append("p")
			elif self.classes[x] == "Mage":
				stat_names.append("m")
			else:
				continue

		if inv_open:
			self.inv_stats_surf = pygame.Surface((269.5, 325))
			self.inv_stats_surf.set_colorkey((0,0,0))
			hp_text = Text(os.path.join("assets", "fontsDL", "font.png"), f"Health: {self.stats['HP'][0]}/{self.stats['HP'][1]}", 2, (255, 255, 255))
			sp_text = Text(os.path.join("assets", "fontsDL", "font.png"), f"Stamina: {self.stats['SP'][0]}/{self.stats['SP'][1]}", 2, (255, 255, 255))
			es_text = [Text(os.path.join("assets", "fontsDL", "font.png"), f"{('Projectiles', 'Mana')[self.classes[0]=='Mage']}: {self.stats['EP'][0][0]}/{self.stats['EP'][0][1]}", 2, (255, 255, 255))]
			ap_text = [Text(os.path.join("assets", "fontsDL", "font.png"), f"{('Ranged', 'Magic')[self.classes[0]=='Mage']} Attack: {self.stats['AP'][0]}", 2, (255, 255, 255))]
			dp_text = Text(os.path.join("assets", "fontsDL", "font.png"), f"Defense: {self.stats['DP']}", 2, (255, 255, 255))
			lp_text = Text(os.path.join("assets", "fontsDL", "font.png"), f"Level: {self.stats['XP'][2]} | XP: {self.stats['XP'][0]}/{self.stats['XP'][1]}", 2, (255, 255, 255))
			mp_text = Text(os.path.join("assets", "fontsDL", "font.png"), f"Money: {self.stats['M']}", 2, (255, 255, 255))
			ip_text = Text(os.path.join("assets", "fontsDL", "font.png"), f"Inseyfication: 0%", 2, (255, 255, 255))
			cl_text = [Text(os.path.join("assets", "fontsDL", "font.png"), f"Class 1: {self.classes[0]}", 2, (255, 255, 255))]

			if self.classes[1]:
				es_text.append(Text(os.path.join("assets", "fontsDL", "font.png"), f"{('Projectiles', 'Mana')[self.classes[1]=='Mage']}: {self.stats['EP'][1][0]}/{self.stats['EP'][1][1]}", 2, (255, 255, 255)))
				ap_text.append(Text(os.path.join("assets", "fontsDL", "font.png"), f"{('Ranged', 'Magic')[self.classes[1]=='Mage']} Attack: {self.stats['AP'][1]}", 2, (255, 255, 255)))
				cl_text.append(Text(os.path.join("assets", "fontsDL", "font.png"), f"Class 2: {self.classes[1]}", 2, (255, 255, 255)))
			else:
				es_text.append(Text(os.path.join("assets", "fontsDL", "font.png"), "You don't have a second class", 2, (255, 255, 255)))
				ap_text.append(Text(os.path.join("assets", "fontsDL", "font.png"), "You don't have a second class", 2, (255, 255, 255)))
				cl_text.append(Text(os.path.join("assets", "fontsDL", "font.png"), "You don't have a second class", 2, (255, 255, 255)))
			
			self.inv_stats_surf.blit(sprites["health"], (0, 0));																			hp_text.render(self.inv_stats_surf, (25, 0))
			self.inv_stats_surf.blit(sprites["stamina"], (0, 25));																		  sp_text.render(self.inv_stats_surf, (25, 25))
			self.inv_stats_surf.blit(sprites[('projectiles', 'mana')[self.classes[0]=='Mage']], (0, 50));								   es_text[0].render(self.inv_stats_surf, (25, 50))
			self.inv_stats_surf.blit(sprites[('projectiles', 'mana')[self.classes[1]=='Mage'] if self.classes[1] else "none"], (0, 75));	es_text[1].render(self.inv_stats_surf, (25, 75))
			self.inv_stats_surf.blit(sprites[str(self.classes[0]).lower()], (0, 100));													  ap_text[0].render(self.inv_stats_surf, (25, 100))
			self.inv_stats_surf.blit(sprites[str(self.classes[1]).lower()], (0, 125));													  ap_text[1].render(self.inv_stats_surf, (25, 125))
			self.inv_stats_surf.blit(sprites["defense"], (0, 150));																		 dp_text.render(self.inv_stats_surf, (25, 150))
			self.inv_stats_surf.blit(sprites["level"], (0, 175));																		   lp_text.render(self.inv_stats_surf, (25, 175))
			self.inv_stats_surf.blit(sprites["money"], (0, 200));																		   mp_text.render(self.inv_stats_surf, (25, 200))
			self.inv_stats_surf.blit(sprites["health"], (0, 225));																		  ip_text.render(self.inv_stats_surf, (25, 225))
			self.inv_stats_surf.blit(sprites[str(self.classes[0]).lower()], (0, 250));													  cl_text[0].render(self.inv_stats_surf, (25, 250))
			self.inv_stats_surf.blit(sprites[str(self.classes[1]).lower()], (0, 275));													  cl_text[1].render(self.inv_stats_surf, (25, 275))
		else:
			self.main_stats_surf = pygame.Surface((64, 152))
			self.main_stats_surf.set_colorkey((0,0,0))
			hp_text = Text(os.path.join("assets", "fontsDL", "font.png"), f"{self.stats['HP'][0]}", 1, (255, 255, 255))
			sp_text = Text(os.path.join("assets", "fontsDL", "font.png"), f"{self.stats['SP'][0]}", 1, (255, 255, 255))
			es_text = [Text(os.path.join("assets", "fontsDL", "font.png"), f"{self.stats['EP'][0][0]}", 1, (255, 255, 255))]
			if self.stats['EP'][1] != [None, None]:
				es_text.append(Text(os.path.join("assets", "fontsDL", "font.png"), f"{self.stats['EP'][1][0]}", 1, (255, 255, 255)))


			self.main_stats_surf.blit(sprites["he"], (0, 0))
			self.main_stats_surf.blit(sprites["hf"], (0, int((self.stats["HP"][1]-self.stats["HP"][0])/self.stats["HP"][1]*100/6.25)), (0, int((self.stats["HP"][1]-self.stats["HP"][0])/self.stats["HP"][1]*100/6.25), sprites["hf"].get_width(), sprites["hf"].get_height()-(int((self.stats["HP"][1]-self.stats["HP"][0])/self.stats["HP"][1]*100/6.5))))
			hp_text.render(self.main_stats_surf, (17.5, 8-hp_text.height*0.5))
			
			self.main_stats_surf.blit(sprites["se"], (0, 20))
			self.main_stats_surf.blit(sprites["sf"], (0, 20+int((self.stats["SP"][1]-self.stats["SP"][0])/self.stats["SP"][1]*100/6.25)), (0, int((self.stats["SP"][1]-self.stats["SP"][0])/self.stats["SP"][1]*100/6.25), sprites["hf"].get_width(), sprites["hf"].get_height()-(int((self.stats["SP"][1]-self.stats["SP"][0])/self.stats["SP"][1]*100/6.25))))
			sp_text.render(self.main_stats_surf, (17.5, 20+(8-hp_text.height*0.5)))

			for x in range(2):
				if self.classes[x]:
					self.main_stats_surf.blit(sprites[f"{stat_names[x]}e"], (0, 40+20*x))
					self.main_stats_surf.blit(sprites[f"{stat_names[x]}f"], (0, 40+20*x+int((self.stats["EP"][x][1]-self.stats["EP"][x][0])/self.stats["EP"][x][1]*100/6.25)), (0, int((self.stats["EP"][x][1]-self.stats["EP"][x][0])/self.stats["EP"][x][1]*100/6.25), sprites["hf"].get_width(), sprites["hf"].get_height()-(int((self.stats["EP"][x][1]-self.stats["EP"][x][0])/self.stats["EP"][x][1]*100/6.25))))
					es_text[x].render(self.main_stats_surf, (17.5, 40+(8-hp_text.height*0.5)+20*x))
				
	def UI(self, win, inventory_on, game_map):
		if self.cached_stats != self.stats:
			self._generate_UI(inventory_on)
			self.cached_stats = copy.deepcopy(self.stats)
		
		if inventory_on:
			win.blit(self.inv_stats_surf, (win.get_width()*0.75-self.inv_stats_surf.get_width()*0.5, 30))
		else:
			win.blit(self.main_stats_surf, (10, 10))

		if self.inv_weight[1]:
			if self.inv_weight[0] > self.inv_weight[1] and self.inv_max_exceed_time == 0:
				self.inv_max_exceed_time = time.time()
			elif self.inv_weight[0] <= self.inv_weight[1]:
				self.inv_max_exceed_time = 0
			if time.time()-self.inv_max_exceed_time >= 30 and self.inv_max_exceed_time != 0:
				if round(time.time()-self.inv_max_exceed_time)%2 == 0 and random.randint(0, 4) == 1:
					self.equipment[3] = "No Backpack"
					for item in reversed(self.inventory):
						if item in self.inventory:
							self.inventory.remove(item)
						game_map.full_drops.append([item, Drop(self.x, self.y, sprites[item]), time.time(), time.time()])

					self.inv_max_exceed_time = 0
					self.inv_size = 5
					self.inv_weight = [0, None]
					return True

	def move(self, game_map, dt, keys, controller):
		self.dmg_counter_log(dt)

		self._move = not self.shielded[0]
		if not self._move and (self.vel.x, self.vel.y) != (0, 0): self.vel = pygame.Vector2()
		self.collidable = not self.dash
		self.movement = [0, 0]

		equipment = load_json(["scripts", "cache", "equipment.json"])
			  
		if self._move:
			if not self.disable_friction and not self.dash:
				acc = self.friction-((self.friction*equipment[2][self.equipment[2]]["weight"])/100)
				v = list(self.vel)
				for index in range(2):
					if v[index] > 0:
						if v[index] - acc*dt < 0:
							v[index] = 0
						else:
							v[index] -= acc*dt
					elif v[index] < 0:
						if v[index] + acc*dt > 0:
							v[index] = 0
						else:
							v[index] += acc*dt
				self.vel = pygame.Vector2(v)
			elif self.dash:
				self.vel.x, self.vel.y = 0, 0
				
			if self.dash:
				self.vel.x, self.vel.y = math.cos(self.dash_dir)*6, math.sin(self.dash_dir)*6
				if math.dist(self.pre_dash_loc, (self.rect.centerx, self.rect.centery)) >= 100 or True in self.collisions.values():
					self.dash = False
					self.dash_cooldown = time.time()
			else:
				self.collidable, self.disable_friction = True, False
							
				pressed_keys = pygame.key.get_pressed()

				acc = self.acceleration-((self.acceleration*equipment[2][self.equipment[2]]["weight"])/100)
				self.knockback_resist = equipment[2][self.equipment[2]]["knockback resistence"]

				if self.vel.y >= -3:
					if pressed_keys[keys["up"]] or controller.get_button(CONTROLLER_BUTTON_DPAD_UP):
						self.vel.y -= acc*dt
						self.dirs[1] = -1
						self.door_rect = pygame.Rect(self.rect.x, self.rect.y-self.rect.h*1.5, self.rect.w*1.5, self.rect.h)
					if controller.get_axis(CONTROLLER_AXIS_LEFTY)/32767 <= -0.1:
						self.vel.y += (controller.get_axis(CONTROLLER_AXIS_LEFTY)/32767)*acc*dt
						self.dirs[1] = -1
						self.door_rect = pygame.Rect(self.rect.x, self.rect.y-self.rect.h*1.5, self.rect.w*1.5, self.rect.h)
				if self.vel.y <= 3:
					if pressed_keys[keys["down"]] or controller.get_button(CONTROLLER_BUTTON_DPAD_DOWN):
						self.vel.y += acc*dt
						self.dirs[1] = 1
						self.door_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.w, self.rect.h*1.5)
					if controller.get_axis(CONTROLLER_AXIS_LEFTY)/32767 >= 0.1:
						self.vel.y += (controller.get_axis(CONTROLLER_AXIS_LEFTY)/32767)*acc*dt
						self.dirs[1] = 1
						self.door_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.w, self.rect.h*1.5)
				if self.vel.x >= -3:
					if pressed_keys[keys["left"]] or controller.get_button(CONTROLLER_BUTTON_DPAD_LEFT):
						self.vel.x -= acc*dt
						self.dirs[0] = -1
						self.door_rect = pygame.Rect(self.rect.x-self.rect.w*1.5, self.rect.y, self.rect.w*1.5, self.rect.h)
					if controller.get_axis(CONTROLLER_AXIS_LEFTX)/32767 <= -0.1:
						self.vel.x += (controller.get_axis(CONTROLLER_AXIS_LEFTX)/32767)*acc*dt
						self.dirs[0] = -1
						self.door_rect = pygame.Rect(self.rect.x-self.rect.w*1.5, self.rect.y, self.rect.w*1.5, self.rect.h)
				if self.vel.x <= 3:
					if pressed_keys[keys["right"]] or controller.get_button(CONTROLLER_BUTTON_DPAD_RIGHT):
						self.vel.x += acc*dt
						self.dirs[0] = 1
						self.door_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.w*1.5, self.rect.h)
					if controller.get_axis(CONTROLLER_AXIS_LEFTX)/32767 >= 0.1:
						self.vel.x += (controller.get_axis(CONTROLLER_AXIS_LEFTX)/32767)*acc*dt
						self.dirs[0] = 1
						self.door_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.w*1.5, self.rect.h)

				if self.vel.x == 0 and self.vel.y:
					self.dirs[0] = 0
				if self.vel.y == 0 and self.vel.x:
					self.dirs[1] = 0
			
				if self.y+self.height > game_map.y+game_map.h or self.y < game_map.y:
					if self.vel.y < 0:
						self.movement[1] = 1
					else:
						self.movement[1] = -1
					self.vel.y = 0
				if self.x+self.width > game_map.x+game_map.w or self.x < game_map.x:
					if self.vel.x < 0:
						self.movement[0] = 1
					else:
						self.movement[0] = -1
					self.vel.x = 0

				if equipment[2][self.equipment[2]]["weight"] <= 25:
					sroll = 1
				elif equipment[2][self.equipment[2]]["weight"] <= 50:
					sroll = 2
				else:
					sroll = 3
				
				if pressed_keys[keys["dash"]] or controller.get_button(CONTROLLER_BUTTON_A):
					if (time.time()-self.dash_cooldown >= 1 or time.time()-self.dash_cooldown <= 0.2) and self.stats["SP"][0] >= sroll and not keys["dash"] in self.held_buttons:
						self.stats["SP"][0] -= sroll
						self.sleep_stamina -= sroll/self.stats["SP"][1]*100
						self.dash = self.disable_friction = True
						self.pre_dash_loc = self.rect.center
						self.dash_dir = math.atan2((self.y+self.dirs[1])*self.dirs[1], (self.x+self.dirs[0])*self.dirs[0])

						if not keys["dash"] in self.held_buttons:
							self.held_buttons.append(keys["dash"])
				else:
					if keys["dash"] in self.held_buttons:
						self.held_buttons.remove(keys["dash"])

		if self.knockback:
			self.vel.x, self.vel.y = math.cos(self.knockback_dir)*self.knockback_speed, math.sin(self.knockback_dir)*self.knockback_speed
			self.knockback = False
			self.still_in_knockback = True
		if self.still_in_knockback:
			self.friction = 0.9
			if -3 <= self.vel.x <= 3 and -3 <= self.vel.y <= 3:
				self.still_in_knockback = False
		else:
			self.friction = 0.3

		self.movement[1] += self.vel.y*dt
		self.movement[0] += self.vel.x*dt
		if len([m for m in self.movement if m]) > 0:
			self.sleep_stamina -= 2*dt

		if self.disable_friction:
			if self.movement[0] == 0:
				self.vel.x = 0
			if self.movement[1] == 0:
				self.vel.y = 0
		self.movement_collision(game_map.tile_rects)

		if self.movement != [0, 0]:
			self.regen_time[1] = time.time()

	def attack(self, enemies, mouse_pos, controller, scroll, projs):
		buttons = pygame.mouse.get_pressed()
		if controller:
			LT = controller.get_axis(CONTROLLER_AXIS_TRIGGERRIGHT)/32767
			RT = controller.get_axis(CONTROLLER_AXIS_TRIGGERLEFT)/32767
		else:
			LT = RT = 0

		if buttons[0] or LT >= 0.5: button = 0
		elif buttons[2] or RT >= 0.5: button = 1

		mouse_pos = (mouse_pos[0]+scroll[0], mouse_pos[1]+scroll[1])
		weapon_stats = load_json(["scripts", "cache", "equipment.json"])

		if buttons[0] or buttons[2] or LT >= 0.5 or RT >= 0.5:
			if self.equipment[button].startswith("No ") or self.equipment[button] not in weapon_stats[0]:
				self.weapons[button] = [None, None]
			elif self.weapons[button][0] != self.equipment[button] and self.equipment[button] in weapons:
				self.weapons[button] = [self.equipment[button], weapons.get(self.equipment[button])()]


			if self.classes[button] and not self.shielded[0] and self.stats["EP"][button][0] > 0 and self.weapons[button] != [None, None] and button not in self.held_buttons:
				if len(projs):
					last_proj = projs[-1]
				else:
					last_proj = None
				self.weapons[button][1].attack(self, mouse_pos, 1, projs)
				if not last_proj or last_proj != projs[-1]:
					self.stats["EP"][button][0] -= 1
					self.sleep_stamina -= 10
					
					if not self.weapons[button][1].auto_fire:
						self.held_buttons.append(button)
						
					if "Mage" in self.classes:
						if button == self.classes.index("Mage"):
							self.regen_time[2] = time.time()

			elif self.equipment[button] in weapon_stats[1].keys() and self.equipment[button] != "No Shield" and button not in self.held_buttons:
				offset = (pygame.Vector2(mouse_pos)-pygame.Vector2(self.rect.center)).normalize()
				shield_obb = OBB((self.rect.centerx+(offset.x*(self.rect.w*0.5+20)), self.rect.centery+(offset.y*(self.rect.h*0.5+20))), 48, -math.degrees(math.atan2(self.rect.centery-mouse_pos[1], mouse_pos[0]-self.rect.centerx)))
				self.shielded = [shield_obb, time.time()]
				self.sleep_stamina -= 5
				self.held_buttons.append(button)
		else:
			if not buttons[0] and 0 in self.held_buttons:
				self.held_buttons.remove(0)
			if not buttons[2] and 1 in self.held_buttons:
				self.held_buttons.remove(1)

		return enemies, projs

	def damage(self, dmg, _):
		hit = False
		main_dmg = dmg
		critical = False
		if self.collidable and self.active:
			hit = True
			if time.time()-self.i_frame >= self.i_time:
				dmg *= random.uniform(0.75, 1.25)
				if random.randint(0, 10) == 0:
					dmg *= 1.75
					critical = True
				dmg = round(dmg*dmg/(dmg+self.stats["DP"]))
				if dmg == 0: dmg = 1

				self.stats["HP"][0] -= dmg
				self.i_frame = time.time()
				self.regen_time[0] = time.time()

				if dmg < main_dmg:
					c = (211, 142, 23)
					s = 2
				elif dmg >= main_dmg and not critical:
					c = (244, 111, 9)
					s = 2
				elif critical:
					c = (204, 23, 0)
					s = 3
				self.damage_counters.append([Text(os.path.join("assets", "fontsDL", "font.png"), str(dmg), s, c), [list(self.rect.center), 10, False]])

		return self.stats["HP"][0], hit, critical

	def xp(self):
		if self.stats["XP"][0] >= self.stats["XP"][1]:
			self.stats["XP"][2] += 1
			self.stats["XP"][0] -= self.stats["XP"][1]
			if self.stats["XP"][0] < 0:
				self.stats["XP"][0]
			self.stats["XP"][1] = round(0.5 * (self.stats["XP"][2] ** 3) + 0.8 * (self.stats["XP"][2] ** 2) + 2 * self.stats["XP"][2])
			
			self.stats["HP"][0] += 1
			self.stats["HP"][1] += 1
			self.stats["SP"][0] += 1
			self.stats["SP"][1] += 1
			if self.weapons[0] != [None, None]:
				self.stats["AP"][0] += 1
			if self.weapons[1] != [None, None] and self.classes[1]:
				self.stats["AP"][1] += 1
			self.stats["DP"] += 1
			try:
				mi = self.classes.index("Mage")
				self.stats["EP"][mi][0] += 1
				self.stats["EP"][mi][1] += 1
			except:
				pass

	def check_sleep(self, enemies):
		print(self.sleep_stamina)
		if self.sleep_stamina <= 0:
			radius = pygame.Rect(0, 0, 1280, 720)
			radius.center = self.rect.center
			if radius.collidelist([enemy.rect for enemy in enemies]) == -1:
				self.sleep[0] = True
				self.sleep_stamina = 18000

	def regen(self):
		if time.time()-self.regen_time[0] >= 5 and self.stats["HP"][0] < self.stats["HP"][1]:
			self.stats["HP"][0] += 1
			self.regen_time[0] = time.time()
		if time.time()-self.regen_time[1] >= 2 and self.stats["SP"][0] < self.stats["SP"][1]:
			self.stats["SP"][0] += 3
			self.regen_time[1] = time.time()
		if "Mage" in self.classes:
			i = self.classes.index("Mage")
			if time.time()-self.regen_time[2] >= 1 and self.stats["EP"][i][0] < self.stats["EP"][i][1]:
				self.stats["EP"][i][0] += 1
				self.regen_time[2] = time.time()
		
