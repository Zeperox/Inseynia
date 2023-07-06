import pygame, os, time, math, copy, random

from scripts.loadingDL.files import files

from scripts.loadingDL.json_functions import load_json
from scripts.loadingDL.sprites import sprite

Entity = files["entity"].Entity
OBB = files["obb"].OBB
Text = files["text"].Text
game_input = files["input"].game_input
Drop = files["drops"].Drop

weapon_stats = load_json(["scripts", "cacheDL", "equipment.json"])

weapons = {}
for file in os.scandir(os.path.join("scripts", "weapons")):
	if file.is_file():
		weapons[files[file.name[:-3]].weapon_name] = files[file.name[:-3]].Weapon


class Player(Entity):
	classes = [None, None]
	name = ""
	equipment = ["No Primary", "No Secondry", "No Backpack", "No Helmet", "No Chest", "No Leggings"]
	inventory = []
	inv_size = 5
	inv_weight = [0, None]
	inv_max_exceed_time = 0
	quests = []
	stats = {
		"HP": [999, 10], # current_HP, max_HP
		"SP": [10, 10], #current_SP, max_SP
		"AP": [1, 1], # weapon_1, weapon_2
		"DP": 0,
		"EP": [[5, 10], [7, 10]], # current_stat_1, max_stat_1 | current_stat_2, max_stat_2
		"M": 100,
		"XP": [2, 3, 1] # xp, max_xp, level
	}
	available_levels = 0
	map = None
	killed_enemies = ["Test Enemy", "Ekreta Tree", "Jlokshi", "Jlokshi", "Jlokshi", "Jlokshi"]
	
	def __init__(self, x: int, y: int):
		s = pygame.Surface((16, 32))
		s.fill((255,255,255))
		pygame.draw.rect(s, (0,0,0), (0, 0, 16, 32), 2)
		
		super().__init__(x, y, s)
		self.cached_stats = copy.deepcopy(self.stats)
		self.dirs = [1, 0]
		self.door_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.w*1.5, self.rect.h)

		self.shielded = [None, 0]
		self.regen_time = [0, 0, 0] # health, stamina, mana
		self.power_gauge = 50
		
		self.power_surf = pygame.Surface((100, 10))
		self.power_surf.fill((0, 0, 0))
		self.power_surf.fill((255, 255, 255), (1, 1, 98, 8))

		self.dash = False
		self.sneak = False
		self.pre_dash_loc = 0
		self.dash_cooldown = 0
		self.dash_dir = 0
		self.stealth = 2
		self.weight = 0

		self._move = True
		self.knockback_resist = 0

		self.main_stats_surf = pygame.Surface((100, 91))
		self.main_stats_surf.set_colorkey((0,0,0))
		self.inv_stats_surf = pygame.Surface((269.5, 325))
		self.inv_stats_surf.set_colorkey((0,0,0))


		self.held_buttons = []
		self.weapons = [[None, None], [None, None]]
		self.damage_counters = []

		self.sleep = [False, True]
		self.sleep_stamina = time.time()
		self.sleep_affect = 0

		self._generate_UI()

	def dmg_counter_log(self, dt):
		for dmg_counter in reversed(self.damage_counters):
			dmg_counter[1][1] -= dt
			
			dmg_counter[0].alpha = dmg_counter[0].alpha-7.5*dt
			if dmg_counter[0].alpha <= 5 and dmg_counter in self.damage_counters:
				self.damage_counters.remove(dmg_counter)

	def draw(self, win: pygame.Surface, scroll: list[int, int]):
		return super().draw(win, scroll)
	
	def draw_UI(self, win, game_map, scroll):
		win.fblits([(dmg_counter[0].surf, (dmg_counter[1][0]-scroll.x, dmg_counter[1][1]-scroll.y)) for dmg_counter in self.damage_counters])

		if self.cached_stats != self.stats:
			self._generate_UI()
			self.cached_stats = copy.deepcopy(self.stats)
		
		blits = [
			(self.main_stats_surf, (10, 10))
		]

		stat_names = []
		for x in range(2):
			if self.classes[x] == "Archer":
				stat_names.append("p")
			elif self.classes[x] == "Mage":
				stat_names.append("m")
			elif self.classes[x] == "Swordsman":
				stat_names.append("v")
			elif self.classes[x] == "Thief":
				stat_names.append("d")
			else:
				continue

		if self.weapons[0] != [None, None]:
			cooldown = self.weapons[0][1].special_cooldown if self.weapons[0][1].specialed else self.weapons[0][1].cooldown
			if time.time()-self.weapons[0][1].cooldown_time < cooldown:
				current_time = time.time()-self.weapons[0][1].cooldown_time
				mask = pygame.mask.from_surface(sprite(f"{stat_names[0]}f"))
				mask.invert()
				surf = mask.to_surface()
				surf.set_colorkey((255, 255, 255))
				surf.set_alpha(100)

				blits.append((surf, (10, 65+current_time/cooldown*surf.get_height()), (0, current_time/cooldown*surf.get_height(), surf.get_width(), surf.get_height()-(current_time/cooldown*surf.get_height()))))
				
		if self.weapons[1] != [None, None] and self.weapons[1][1].player_class == self.classes[1]:
			cooldown = self.weapons[1][1].special_cooldown if self.weapons[1][1].specialed else self.weapons[1][1].cooldown
			if time.time()-self.weapons[1][1].cooldown_time < cooldown:
				current_time = time.time()-self.weapons[1][1].cooldown_time
				mask = pygame.mask.from_surface(sprite(f"{stat_names[1]}f"))
				mask.invert()
				surf = mask.to_surface()
				surf.set_colorkey((255, 255, 255))
				surf.set_alpha(100)

				blits.append((surf, (10, 85+current_time/cooldown*surf.get_height()), (0, current_time/cooldown*surf.get_height(), surf.get_width(), surf.get_height()-(current_time/cooldown*surf.get_height()))))

		win.blits(blits)

		if self.inv_weight[1]:
			if self.inv_weight[0] > self.inv_weight[1] and self.inv_max_exceed_time == 0:
				self.inv_max_exceed_time = time.time()
			elif self.inv_weight[0] <= self.inv_weight[1]:
				self.inv_max_exceed_time = 0
			if time.time()-self.inv_max_exceed_time >= 30 and self.inv_max_exceed_time != 0:
				if round(time.time()-self.inv_max_exceed_time)%2 == 0 and random.randint(0, 4) == 1:
					self.equipment[2] = "No Backpack"
					for item in reversed(self.inventory):
						if item in self.inventory:
							self.inventory.remove(item)
						game_map.full_drops.append([item, Drop(random.randint(self.rect.centerx-50, self.rect.centerx+50), random.randint(self.rect.centery-50, self.rect.centery+50), sprite(item)), time.time(), time.time()])

					self.inv_max_exceed_time = 0
					self.inv_size = 5
					self.inv_weight = [0, None]
					return True

	def _generate_UI(self):
		self.power_surf.fill((100, 0, 0), (2, 2, 96, 6))
		self.power_surf.fill((150, 150, 0), (2, 2, 96*(self.power_gauge/50) if self.power_gauge <= 50 else 96, 6))

		stat_names = []
		for x in range(2):
			if self.classes[x] == "Archer":
				stat_names.append("p")
			elif self.classes[x] == "Mage":
				stat_names.append("m")
			elif self.classes[x] == "Swordsman":
				stat_names.append("v")
			elif self.classes[x] == "Thief":
				stat_names.append("d")
			else:
				continue

		hp_text = Text(os.path.join("assets", "fontsDL", "font.ttf"), f"{self.stats['HP'][0]}", 13, (255, 255, 255))
		sp_text = Text(os.path.join("assets", "fontsDL", "font.ttf"), f"{self.stats['SP'][0]}", 13, (255, 255, 255))
		es_text = [Text(os.path.join("assets", "fontsDL", "font.ttf"), f"{self.stats['EP'][0][0]}", 13, (255, 255, 255))]
		if self.stats['EP'][1] != [None, None]:
			es_text.append(Text(os.path.join("assets", "fontsDL", "font.ttf"), f"{self.stats['EP'][1][0]}", 13, (255, 255, 255)))


		stat_size = sprite("hf").get_size()
		blits = [
			(self.power_surf, (0, 0)),
			(sprite("he"), (0, 15)),
			(sprite("hf"), (0, 15+int((self.stats["HP"][1]-self.stats["HP"][0])/self.stats["HP"][1]*100/6.25)), (0, int((self.stats["HP"][1]-self.stats["HP"][0])/self.stats["HP"][1]*100/6.25), stat_size[0], stat_size[1]-(int((self.stats["HP"][1]-self.stats["HP"][0])/self.stats["HP"][1]*100/6.5)))),
			(hp_text.surf, (32-hp_text.width*0.5, 22-hp_text.height*0.5)),
			(sprite("se"), (0, 35)),
			(sprite("sf"), (0, 35+int((self.stats["SP"][1]-self.stats["SP"][0])/self.stats["SP"][1]*100/6.25)), (0, int((self.stats["SP"][1]-self.stats["SP"][0])/self.stats["SP"][1]*100/6.25), stat_size[0], stat_size[1]-(int((self.stats["SP"][1]-self.stats["SP"][0])/self.stats["SP"][1]*100/6.25)))),
			(sp_text.surf, (32-sp_text.width*0.5, 42-sp_text.height*0.5)),
			(sprite(f"{stat_names[0]}e"), (0, 55)),
			(sprite(f"{stat_names[0]}f"), (0, 55+int((self.stats["EP"][0][1]-self.stats["EP"][0][0])/self.stats["EP"][0][1]*100/6.25)), (0, int((self.stats["EP"][0][1]-self.stats["EP"][0][0])/self.stats["EP"][0][1]*100/6.25), stat_size[0], stat_size[1]-(int((self.stats["EP"][0][1]-self.stats["EP"][0][0])/self.stats["EP"][0][1]*100/6.25)))),
			(es_text[0].surf, (32-es_text[0].width*0.5, 62-es_text[0].height*0.5))
		]
		if self.stats['EP'][1] != [None, None]:
			blits.append((sprite(f"{stat_names[1]}e"), (0, 75))),
			blits.append((sprite(f"{stat_names[1]}f"), (0, 75+int((self.stats["EP"][1][1]-self.stats["EP"][1][0])/self.stats["EP"][1][1]*100/6.25)), (0, int((self.stats["EP"][1][1]-self.stats["EP"][1][0])/self.stats["EP"][1][1]*100/6.25), stat_size[0], stat_size[1]-(int((self.stats["EP"][1][1]-self.stats["EP"][1][0])/self.stats["EP"][1][1]*100/6.25))))),
			blits.append((es_text[1].surf, (32-es_text[1].width*0.5, 82-es_text[1].height*0.5)))
			
		self.main_stats_surf.blits(blits)
				
	def move(self, game_map, dt, settings, prioritize, controller):
		self.dmg_counter_log(dt)

		self._move = not self.shielded[0]
		if not self._move and (self.vel.x, self.vel.y) != (0, 0): self.vel = pygame.Vector2()
		self.collidable = not self.dash
		self.movement = [0, 0]
	  
		if self._move:
			if not self.disable_friction and not self.dash:
				acc = self.friction-((self.friction*self.weight)/100)
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
			else:
				self.vel.x, self.vel.y = 0, 0
				
			if self.dash:
				self.vel.x, self.vel.y = math.cos(self.dash_dir)*6, math.sin(self.dash_dir)*6
				if math.dist(self.pre_dash_loc, (self.rect.centerx, self.rect.centery)) >= 100 or True in self.collisions.values():
					self.dash = False
					self.dash_cooldown = time.time()
			else:
				self.collidable, self.disable_friction = True, False
							
				acc = self.acceleration-((self.acceleration*self.weight)/100)

				max_speed = 3 if not self.sneak else 1

				if settings["sticks invert"]:
					stickx = pygame.CONTROLLER_AXIS_RIGHTX
					sticky = pygame.CONTROLLER_AXIS_RIGHTY
				else:
					stickx = pygame.CONTROLLER_AXIS_LEFTX
					sticky = pygame.CONTROLLER_AXIS_LEFTY
				
					
				if self.vel.y >= -max_speed:
					if game_input.hold(settings[prioritize]["up"], prioritize, controller):
						self.vel.y -= acc*dt
						self.dirs[1] = -1
						self.door_rect = pygame.Rect(self.rect.x, self.rect.y-self.rect.h*1.5, self.rect.w*1.5, self.rect.h)
					if controller.get_axis(sticky)/32767 <= -0.1:
						self.vel.y += (controller.get_axis(sticky)/32767)*acc*dt
						self.dirs[1] = -1
						self.door_rect = pygame.Rect(self.rect.x, self.rect.y-self.rect.h*1.5, self.rect.w*1.5, self.rect.h)
				if self.vel.y <= max_speed:
					if game_input.hold(settings[prioritize]["down"], prioritize, controller):
						self.vel.y += acc*dt
						self.dirs[1] = 1
						self.door_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.w, self.rect.h*1.5)
					if controller.get_axis(sticky)/32767 >= 0.1:
						self.vel.y += (controller.get_axis(sticky)/32767)*acc*dt
						self.dirs[1] = 1
						self.door_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.w, self.rect.h*1.5)
				if self.vel.x >= -max_speed:
					if game_input.hold(settings[prioritize]["left"], prioritize, controller):
						self.vel.x -= acc*dt
						self.dirs[0] = -1
						self.door_rect = pygame.Rect(self.rect.x-self.rect.w*1.5, self.rect.y, self.rect.w*1.5, self.rect.h)
					if controller.get_axis(stickx)/32767 <= -0.1:
						self.vel.x += (controller.get_axis(stickx)/32767)*acc*dt
						self.dirs[0] = -1
						self.door_rect = pygame.Rect(self.rect.x-self.rect.w*1.5, self.rect.y, self.rect.w*1.5, self.rect.h)
				if self.vel.x <= max_speed:
					if game_input.hold(settings[prioritize]["right"], prioritize, controller):
						self.vel.x += acc*dt
						self.dirs[0] = 1
						self.door_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.w*1.5, self.rect.h)
					if controller.get_axis(stickx)/32767 >= 0.1:
						self.vel.x += (controller.get_axis(stickx)/32767)*acc*dt
						self.dirs[0] = 1
						self.door_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.w*1.5, self.rect.h)

				if self.vel.x == 0 and self.vel.y:
					self.dirs[0] = 0
				if self.vel.y == 0 and self.vel.x:
					self.dirs[1] = 0
			
				if self.y+self.height > game_map.y+game_map.data["size"][1] or self.y < game_map.y:
					if self.vel.y < 0:
						self.movement[1] = 1
					else:
						self.movement[1] = -1
					self.vel.y = 0
				if self.x+self.width > game_map.x+game_map.data["size"][0] or self.x < game_map.x:
					if self.vel.x < 0:
						self.movement[0] = 1
					else:
						self.movement[0] = -1
					self.vel.x = 0

				if self.weight <= 25:
					sroll = 1
				elif self.weight <= 50:
					sroll = 2
				else:
					sroll = 3
				
				if game_input.press(settings[prioritize]["dash"], prioritize, controller) and (time.time()-self.dash_cooldown >= 0.5 or time.time()-self.dash_cooldown <= 0.2) and self.stats["SP"][0] >= sroll:
					self.stats["SP"][0] -= sroll
					self.sleep_stamina -= sroll
					self.dash = self.disable_friction = True
					self.pre_dash_loc = self.rect.center
					self.dash_dir = math.atan2((self.y+self.dirs[1])*self.dirs[1], (self.x+self.dirs[0])*self.dirs[0])


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
		if abs(self.movement[0]) > 1 and abs(self.movement[1]) > 1:
			self.sleep_stamina -= 0.05
			self.regen_time[1] = time.time()

		if self.disable_friction:
			if self.movement[0] == 0:
				self.vel.x = 0
			if self.movement[1] == 0:
				self.vel.y = 0
		self.movement_collision(game_map.tiles)

	def attack(self, enemies, mouse_pos, settings, prioritize, controller, scroll, projs, difficulty):
		mouse_pos = (mouse_pos[0]+scroll.x, mouse_pos[1]+scroll.y)

		def initiate(special):
			if not self.shielded[0] and self.weapons[button] != [None, None]:
				if self.stats["EP"][button][0] and self.weapons[button][1].player_class == self.classes[button]:
					weaker = False
				else:
					weaker = True

				if not special:
					if not weaker:
						shot = self.weapons[button][1].attack(self, mouse_pos, enemies, projs)
					else:
						if self.weapons[button][1].player_class == "Archer":
							shot = self.weapons[button][1].attack(self, mouse_pos, enemies, projs, True)
						elif self.weapons[button][1].player_class == "Mage" and (self.stats["SP"][0] or self.stats["HP"][0] > 1):
							shot = self.weapons[button][1].attack(self, mouse_pos, enemies, projs)
						elif self.weapons[button][1].player_class == "Swordsman":
							shot = self.weapons[button][1].attack(self, mouse_pos, enemies, projs, True)
						elif self.weapons[button][1].player_class == "Thief":
							shot = self.weapons[button][1].attack(self, mouse_pos, enemies, projs)
				elif special:
					if self.power_gauge >= 50 and not weaker:
						try:
							shot = self.weapons[button][1].special(self, mouse_pos, enemies, projs)
						except:
							return
						self.power_gauge = 0
					else:
						return

				if shot:
					if weaker and self.weapons[button][1].player_class == "Mage":
						if self.stats["SP"][0]:
							self.stats["SP"][0] -= 1
						elif self.stats["HP"][0] > 1:
							self.stats["HP"][0] -= 1

					if (not special and not weaker and self.weapons[button][1].player_class != "Thief") or (special and difficulty.lower() not in ["easy", "normal"]):
						self.stats["EP"][button][0] -= 1 + (special==True)*2
							
					self.sleep_stamina -= 1
					
					if "Mage" in self.classes:
						if button == self.classes.index("Mage"):
							self.regen_time[2] = time.time()

			elif self.equipment[button] in weapon_stats[1].keys() and self.equipment[button] != "No Shield":
				offset = (pygame.Vector2(mouse_pos)-pygame.Vector2(self.rect.center)).normalize()
				shield_obb = OBB((self.rect.centerx+(offset.x*(self.rect.w*0.5+20)), self.rect.centery+(offset.y*(self.rect.h*0.5+20))), 48, -math.degrees(math.atan2(self.rect.centery-mouse_pos[1], mouse_pos[0]-self.rect.centerx)))
				self.shielded = [shield_obb, time.time()]
				self.sleep_stamina -= 1

		holds = []
		for i in range(2):
			if (self.equipment[i].startswith("No ") or self.equipment[i] not in weapon_stats[0]) and self.equipment[i] not in weapon_stats[1].keys():
				self.weapons[i] = [None, None]
				continue
			elif self.weapons[i][0] != self.equipment[i] and self.equipment[i] in weapons:
				self.weapons[i] = [self.equipment[i], weapons.get(self.equipment[i])()]
				
			if self.equipment[i] in weapon_stats[1].keys():
				holds.append(i)
			elif self.weapons[i][1].auto_fire:
				holds.append(i)

		

		if 0 in holds:
			if game_input.hold(settings[prioritize]["primary"], prioritize, controller):
				button = 0
				initiate(False)
		else:
			if game_input.press(settings[prioritize]["primary"], prioritize, controller):
				button = 0
				initiate(False)
		if 1 in holds:
			if game_input.hold(settings[prioritize]["secondary"], prioritize, controller):
				button = 1
				initiate(False)
		else:
			if game_input.press(settings[prioritize]["secondary"], prioritize, controller):
				button = 1
				initiate(False)
		'''if game_input.press(settings[prioritize]["pspecial"], prioritize, controller):
			button = 0
			initiate(True)
		if game_input.press(settings[prioritize]["sspecial"], prioritize, controller):
			button = 1
			initiate(True)'''
		
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
					s = 16
				elif dmg >= main_dmg and not critical:
					c = (244, 111, 9)
					s = 16
				elif critical:
					c = (204, 23, 0)
					s = 24
				self.damage_counters.append([Text(os.path.join("assets", "fontsDL", "font.ttf"), str(dmg), s, c, bold=True), list(self.rect.center)])

		return self.stats["HP"][0], hit, critical

	def xp(self):
		if self.stats["XP"][0] >= self.stats["XP"][1]:
			self.stats["XP"][2] += 1
			self.available_levels += 1
			self.stats["XP"][0] -= self.stats["XP"][1]
			if self.stats["XP"][0] < 0:
				self.stats["XP"][0]
			self.stats["XP"][1] = round(0.5 * (self.stats["XP"][2] ** 3) + 0.8 * (self.stats["XP"][2] ** 2) + 2 * self.stats["XP"][2])

	def check_sleep(self, enemies):
		if time.time()-self.sleep_stamina >= 1 and len(enemies) == 0:
			self.sleep[0] = True

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
		