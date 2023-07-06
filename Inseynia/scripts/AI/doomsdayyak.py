import time, random, math, os, pygame

from scripts.loadingDL.files import files

MainAI = files["ai"].MainAI
Projectile = files["projectiles"].Projectile
Text = files["text"].Text

class NormalProj(Projectile):
	def __init__(self, sloc: tuple[int, int], eloc: tuple[int, int], attack: float, data: dict, shooter):
		super().__init__(sloc, eloc, attack, data, shooter)

	def move_code(self, game_map, dt, scroll, mouse_pos, entities, player):
		return self.end_drop(game_map), True

class HalfCProj(Projectile):
	def __init__(self, sloc: tuple[int, int], eloc: tuple[int, int], attack: float, data: dict, shooter, ang: int):
		super().__init__(sloc, eloc, attack, data, shooter)
		self.ang = ang
		self.start_ang = ang

	def move_code(self, game_map, dt, scroll, mouse_pos, entities, player):
		if self.ang-self.start_ang < 180:
			x = self.sloc.x + 100 * math.cos(math.radians(self.ang))
			y = self.sloc.y - 100 * math.sin(math.radians(self.ang))
			self.ang += 1
			
			self.movement = [x-self.x, y-self.y]

			return self.end_drop(game_map), False
		return self.end_drop(game_map), True

class CircleProj2(Projectile):
	def __init__(self, sloc: tuple[int, int], eloc: tuple[int, int], attack: float, data: dict, shooter, ang: int):
		super().__init__(sloc, eloc, attack, data, shooter)
		self.ang = ang
		self.start_ang = ang
		self.tile_collide = False
		self.reset = False
		self.speed = self.data["speed"]

	def move_code(self, game_map, dt, scroll, mouse_pos, entities, player):
		if self.ang-self.start_ang < 360:
			self.eloc.x = self.sloc.x + math.cos(math.radians(self.ang))
			self.eloc.y = self.sloc.y - math.sin(math.radians(self.ang))
			self.ang += 0.75
		else:
			if self.data["speed"] > 0 and not self.reset:
				self.data["speed"] -= 0.1
			elif self.data["speed"] <= 0:
				if not self.reset:
					self.data["speed"] = self.speed
					self.reset = True
					self.sloc = pygame.Vector2(self.x, self.y)
		
		return self.end_drop(game_map), True

class CircleProj(Projectile):
	def __init__(self, sloc: tuple[int, int], eloc: tuple[int, int], attack: float, data: dict, shooter, ang: int):
		super().__init__(sloc, eloc, attack, data, shooter)
		self.ang = ang
		self.tile_collide = False

	def move_code(self, game_map, dt, scroll, mouse_pos, entities, player):
		x = self.sloc.x + 200 * math.cos(math.radians(self.ang))
		y = self.sloc.y - 200 * math.sin(math.radians(self.ang))
		self.ang += 0.75
		
		self.movement = [x-self.x, y-self.y]

		return self.end_del(game_map), False

class LineProj(Projectile):
	def __init__(self, sloc: tuple[int, int], eloc: tuple[int, int], attack: float, data: dict, shooter):
		super().__init__(sloc, eloc, attack, data, shooter)
		self.end_speed = self.data["speed"]
		self.data["speed"] = 0
		self.start_move = False

	def move_code(self, game_map, dt, scroll, mouse_pos, entities, player):
		if self.start_move and self.data["speed"] < self.end_speed:
			self.data["speed"] += 0.1*dt

		return self.end_drop(game_map), True


class AI(MainAI):
	def __init__(self, x: int, y: int, animation_dirs: str, stats, _):
		super().__init__(x, y, animation_dirs, stats, "Jlokshi", "boss")
		self.text_name = Text(os.path.join("assets", "fontsDL", "font.ttf"), "Jlokshi", 16, (255, 255, 255))
		self.health_bar = pygame.Surface((600, self.text_name.height+10))
		self.health_bar.fill((0, 0, 0)); self.health_bar.fill((255, 255, 255), (1, 1, self.health_bar.get_width()-2, self.health_bar.get_height()-2)); self.health_bar.fill((127, 0, 0), (3, 3, self.health_bar.get_width()-6, self.health_bar.get_height()-6)); 
		self.health_bar.fill((0, 127, 0), (3, 3, (self.health_bar.get_width()-6)*(self.stats["HP"][0]/self.stats["HP"][1]), self.health_bar.get_height()-6))
		self.health_bar.blit(self.text_name.surf, (300-self.text_name.width*0.5, self.health_bar.get_height()*0.5-self.text_name.height*0.5))
		self.health_bar.set_alpha(200)

		self.music = "assets/SOUND/music/Into Jahanam.ogg"

		self.shot_time = 0
		self.proj_data = {"img": "thorn", "speed": 4, "duration": 1000, "knockback": 10, "pierces": 0}

		self.attack_num = -1
		self.start_attack = False
		self.attack_end = False
		self.attack_cooldown = 0
		self.attack_time = 0
		self.offset = 0
		self.camera = True

		# attack 0
		self.target_lastknown_loc = []
		self.attack_turns = 0

		# attack 4
		self.offset2 = 0

		# attack 6
		self.illusion_locs = []
		self.proj_cooldown2 = 0

		# attack 7
		self.att7_shapes = [
			[
				(0, 0),
				(-120, -150),
				(40, -150),
				(-80, 0),
				(-40, -200),
				(0, 0)
			],
			[
				(0, 0),
				(-200, 0),
				(-200, -200),
				(0, -200),
				(0, 0),
				(-200, -200),
				(-200, 0),
				(0, -200),
				(0, 0)
			],
			[
				(0, 0),
				(-100, 0),
				(-100, -200),
				(-200, 0),
				(0, 0),
				(-100, -200),
				(-100, 0),
				(0, 0)
			]
		]
		self.chosen_shape = [0, 0]
		self.first_loc = (0, 0)

	def draw(self, win: pygame.Surface, scroll: list[int, int]):
		win.fblits([(self.animations[self.action].blit_ready(), (loc[0]-scroll.x, loc[1]-scroll.y)) for loc in self.illusion_locs])

		return super().draw(win, scroll)
		
	def draw_UI(self, win, scroll, target=False):
		super().draw_UI(win, scroll)
		if target:
			win.blit(self.health_bar, (20, 330-self.text_name.height))

	def ai(self, game_map, target, dt: float, difficulty):
		self.ai_action = "alert"
		super().ai(game_map, target, dt, difficulty)
		
	def alert(self, target, game_map, difficulty):
		self.camera = True
		self.draw_img = True
		self.collidable = True
		self.illusion_locs = []

		if not self.start_attack:
			self.target_loc = target.rect.center
			self.speed_affect = 1

		elif self.attack_num == 0:
			self.target_loc = self.target_lastknown_loc
			self.speed_affect = 5

		elif self.attack_num in [1, 2, 3, 4, 5]:
			self.target_loc = self.rect.center

		elif self.attack_num == 6:
			self.target_loc = self.rect.center
			self.camera = False
			self.draw_img = False
			self.collidable = False

			for i in range(5):
				rad = math.radians(i*360/5)+math.radians(self.offset)
				self.illusion_locs.append((target.rect.centerx+200*math.cos(rad)-self.rect.width*0.5, target.rect.centery+200*math.sin(rad)-self.rect.height*0.5))
			self.offset += 0.5

		elif self.attack_num == 7:
			self.target_loc = self.target_lastknown_loc
			self.speed_affect = 4

		self.attack(target, game_map, difficulty)

	def attack(self, target, game_map, difficulty):
		if self.attack_num == -1 and self.attack_cooldown == 0:
			self._move = False
			self.attack_cooldown = time.time()-4
			self.attack_end = True

		if time.time()-self.attack_cooldown >= 5:
			if self.attack_end:
				self._move = True

				self.start_attack = True
				self.attack_num = random.randint(0, 7)
				self.attack_time = time.time()
				self.offset = 0

				if self.attack_num == 0:
					self.target_lastknown_loc = target.rect.center
				elif self.attack_num == 7:
					self.chosen_shape = [random.randint(0, 2), 0]
					self.first_loc = self.rect.center
					self.target_lastknown_loc = (self.first_loc[0]+self.att7_shapes[self.chosen_shape[0]][self.chosen_shape[1]][0], self.first_loc[1]+self.att7_shapes[self.chosen_shape[0]][self.chosen_shape[1]][1])

				self.attack_end = False
				
			if self.start_attack:
				if self.attack_num == 0:
					if difficulty == "Easy":
						attack_turn_num = 2
					elif difficulty == "Normal":
						attack_turn_num = 3
					else:
						attack_turn_num = 5
					if self.attack_turns < attack_turn_num:
						if math.dist(self.rect.center, self.target_lastknown_loc) >= 10:
							if time.time()-self.proj_cooldown >= 0.25:
								for i in range(4):
									if (i+1)%2 == 0:
										rad = math.radians(i*360/4)+self.en_ta_angle

										game_map.full_projs.append(NormalProj(self.rect.center, (self.rect.centerx+100*math.cos(rad), self.rect.centery+100*math.sin(rad)), self.stats["AP"], self.proj_data, self))
								self.proj_cooldown = time.time()
						else:
							for i in range(24):
								rad = math.radians(i*360/24)
								game_map.full_projs.append(NormalProj(self.rect.center, (self.rect.centerx+100*math.cos(rad), self.rect.centery+100*math.sin(rad)), self.stats["AP"], self.proj_data, self))
							self.attack_turns += 1
		
							self.target_lastknown_loc = target.rect.center
					else:
						self.attack_cooldown = time.time()
						self.attack_end = True

				elif self.attack_num == 1:
					if time.time()-self.attack_time <= 10:
						if time.time()-self.proj_cooldown >= 0.25:
							max_num = 16 if difficulty == "Easy" else 24 if difficulty == "Normal" else 32
							num = max_num/2 if self.attack_turns < 3 else max_num
							for i in range(int(num)):
								rad = math.radians(i*360/num)+self.offset
								game_map.full_projs.append(NormalProj(self.rect.center, (self.rect.centerx+100*math.cos(rad), self.rect.centery+100*math.sin(rad)), self.stats["AP"], self.proj_data, self))
							self.offset += math.radians(5.625)
							self.attack_turns += 1
							if num == max_num:
								self.attack_turns = 0
								self.offset += math.radians(360/32)
							self.proj_cooldown = time.time()
					else:
						self.attack_cooldown = time.time()
						self.attack_end = True
					
				elif self.attack_num == 2:
					if time.time()-self.attack_time <= 10:
						if time.time()-self.proj_cooldown >= 0.25:
							for i in range(4):
								rad = math.radians(i*360/4)+self.offset
								game_map.full_projs.append(NormalProj(self.rect.center, (self.rect.centerx+100*math.cos(rad+0.4), self.rect.centery+100*math.sin(rad+0.5)), self.stats["AP"], {"img": "thorn", "speed": 6, "duration": 1000, "knockback": 10, "pierces": 0}, self))
								game_map.full_projs.append(NormalProj(self.rect.center, (self.rect.centerx+100*math.cos(rad+0.4), self.rect.centery+100*math.sin(rad+0.4)), self.stats["AP"], {"img": "thorn", "speed": 5, "duration": 1000, "knockback": 10, "pierces": 0}, self))
								game_map.full_projs.append(NormalProj(self.rect.center, (self.rect.centerx+100*math.cos(rad+0.4), self.rect.centery+100*math.sin(rad+0.3)), self.stats["AP"], {"img": "thorn", "speed": 4, "duration": 1000, "knockback": 10, "pierces": 0}, self))
								game_map.full_projs.append(NormalProj(self.rect.center, (self.rect.centerx+100*math.cos(rad+0.4), self.rect.centery+100*math.sin(rad+0.2)), self.stats["AP"], {"img": "thorn", "speed": 3, "duration": 1000, "knockback": 10, "pierces": 0}, self))
								game_map.full_projs.append(NormalProj(self.rect.center, (self.rect.centerx+100*math.cos(rad+0.2), self.rect.centery+100*math.sin(rad+0.1)), self.stats["AP"], {"img": "thorn", "speed": 2, "duration": 1000, "knockback": 10, "pierces": 0}, self))
								game_map.full_projs.append(NormalProj(self.rect.center, (self.rect.centerx+100*math.cos(rad), self.rect.centery+100*math.sin(rad)), self.stats["AP"], {"img": "thorn", "speed": 1, "duration": 1000, "knockback": 10, "pierces": 0}, self))
							self.offset += 0.1
							self.proj_cooldown = time.time()
					else:
						self.attack_cooldown = time.time()
						self.attack_end = True

				elif self.attack_num == 3:
					if time.time()-self.attack_time <= 10:
						if time.time()-self.proj_cooldown >= 0.25:
							for i in range(8):
								rad = math.radians(i*360/8)+self.offset
								if i%2 == 0:
									game_map.full_projs.append(HalfCProj(self.rect.center, (self.rect.centerx+100*math.cos(rad), self.rect.centery+100*math.sin(rad)), self.stats["AP"], {"img": "thorn", "speed": 3, "duration": 1000, "knockback": 10, "pierces": 0}, self, i*360/8))
								else:
									game_map.full_projs.append(HalfCProj(self.rect.center, (self.rect.centerx+100*math.sin(rad), self.rect.centery+100*math.cos(rad)), self.stats["AP"], {"img": "thorn", "speed": 3, "duration": 1000, "knockback": 10, "pierces": 0}, self, i*360/8))
							self.offset += 0.1
							self.proj_cooldown = time.time()
					else:
						self.attack_cooldown = time.time()
						self.attack_end = True

				elif self.attack_num == 4:
					if time.time()-self.attack_time <= 10:
						if time.time()-self.proj_cooldown >= 0.25:
							for i in range(12):
								rad = math.radians(i*360/12)
								game_map.full_projs.append(CircleProj2(self.rect.center, (self.rect.centerx+100*math.cos(rad), self.rect.centery+100*math.sin(rad)), self.stats["AP"], {"img": "thorn", "speed": 3, "duration": 1000, "knockback": 10, "pierces": 0}, self, i*360/8))
							self.offset += 5.625
							self.proj_cooldown = time.time()
					else:
						self.attack_cooldown = time.time()
						self.attack_end = True

				elif self.attack_num == 5:
					if time.time()-self.attack_time <= 10:
						if time.time()-self.proj_cooldown >= 0.25:
							for i in range(8):
								rad = math.radians(i*360/8)+self.offset
								game_map.full_projs.append(NormalProj(self.rect.center, (self.rect.centerx+100*math.cos(rad+math.radians(120*2)), self.rect.centery+100*math.sin(rad+math.radians(120*2))), self.stats["AP"], {"img": "thorn", "speed": i/8*4+1, "duration": 1000, "knockback": 10, "pierces": 0}, self))
								game_map.full_projs.append(NormalProj(self.rect.center, (self.rect.centerx+100*math.cos(rad+math.radians(120)), self.rect.centery+100*math.sin(rad+math.radians(120))), self.stats["AP"], {"img": "thorn", "speed": i/8*4+1, "duration": 1000, "knockback": 10, "pierces": 0}, self))
								game_map.full_projs.append(NormalProj(self.rect.center, (self.rect.centerx+100*math.cos(rad), self.rect.centery+100*math.sin(rad)), self.stats["AP"], {"img": "thorn", "speed": i/8*4+1, "duration": 1000, "knockback": 10, "pierces": 0}, self))
							self.offset += 0.1
							self.proj_cooldown = time.time()
					else:
						self.attack_cooldown = time.time()
						self.attack_end = True
			
				elif self.attack_num == 6:
					if time.time()-self.attack_time <= 10:
						if time.time()-self.proj_cooldown >= 0.25:
							for ill, loc in enumerate(self.illusion_locs):
								game_map.full_projs.append(CircleProj(target.rect.center, self.rect.center, self.stats["AP"], {"img": "thorn", "speed": 4, "duration": 2, "knockback": 10, "pierces": 0}, self, ill*360/5+self.offset))
							self.proj_cooldown = time.time()
						if time.time()-self.proj_cooldown2 >= 0.3:
							for ill, loc in enumerate(self.illusion_locs):
								game_map.full_projs.append(NormalProj(loc, target.rect.center, self.stats["AP"], {"img": "thorn", "speed": 1, "duration": 5, "knockback": 10, "pierces": 0}, self))								
							self.proj_cooldown2 = time.time()
					else:
						self.attack_cooldown = time.time()
						self.attack_end = True

				elif self.attack_num == 7:
					if self.chosen_shape[1] < len(self.att7_shapes[self.chosen_shape[0]]):
						if math.dist(self.rect.center, self.target_lastknown_loc) >= 10:
							if time.time()-self.proj_cooldown >= 0.05:
								for i in range(4):
									if (i+1)%2 == 0:
										rad = math.radians(i*360/4)+self.en_ta_angle
										game_map.full_projs.append(LineProj(self.rect.center, (self.rect.centerx+100*math.cos(rad), self.rect.centery+100*math.sin(rad)), self.stats["AP"], {"img": "thorn", "speed": 10, "duration": 1000, "knockback": 10, "pierces": 1}, self))
								self.proj_cooldown = time.time()
						else:
							for i in range(16):
								rad = math.radians(i*360/16)
								game_map.full_projs.append(NormalProj(self.rect.center, (self.rect.centerx+100*math.cos(rad), self.rect.centery+100*math.sin(rad)), self.stats["AP"], self.proj_data, self))
							
							self.chosen_shape[1] += 1
							try:
								self.target_lastknown_loc = (self.first_loc[0]+self.att7_shapes[self.chosen_shape[0]][self.chosen_shape[1]][0], self.first_loc[1]+self.att7_shapes[self.chosen_shape[0]][self.chosen_shape[1]][1])
							except:
								pass
					else:
						for proj in game_map.full_projs:
							if isinstance(proj, LineProj):
								proj.start_move = True
						self.attack_cooldown = time.time()
						self.attack_end = True

		else:
			self.start_attack = False

	def damage(self, dmg, proj):
		self.health_bar.fill((0, 0, 0)); self.health_bar.fill((255, 255, 255), (1, 1, self.health_bar.get_width()-2, self.health_bar.get_height()-2)); self.health_bar.fill((127, 0, 0), (3, 3, self.health_bar.get_width()-6, self.health_bar.get_height()-6)); 
		self.health_bar.fill((0, 127, 0), (3, 3, (self.health_bar.get_width()-6)*(self.stats["HP"][0]/self.stats["HP"][1]), self.health_bar.get_height()-6))
		self.health_bar.blit(self.text_name.surf, (300-self.text_name.width*0.5, self.health_bar.get_height()*0.5-self.text_name.height*0.5))
		return super().damage(dmg, proj)
