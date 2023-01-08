import math, pygame, time, random, os, copy

from scripts.logic.entity import Entity
from scripts.logic.view import View
from scripts.visuals.text import Text

class MainAI(Entity):
	def __init__(self, x: int, y: int, animation_dirs: str | pygame.Surface, stats, name, _type):
		super().__init__(x, y, animation_dirs)
		self.name = name
		self.type = _type
		stats = copy.deepcopy(stats)
		try:
			if type(stats["health"]) == int:
				stats["health"] = [stats["health"], stats["health"]]
			self.stats = {
				"HP": stats["health"],
				"AP": stats["attack"],
				"DP": stats["defense"],
				"SP": stats["speed"],
				"V": stats["view"],
				"SV": stats["suspicious view"],
				"XP": stats["XP"]
			}
		except:
			self.stats = stats
		self.knockback_resist = stats["knockback resistence"]
		self.speed_affect = 1


		self.spawn_point = [x, y]
		self.target = None

		self.view = View(list(self.rect.center), self.stats["V"][0], self.stats["V"][1], 180)
		self.sus_view = View(list(self.rect.center), self.stats["SV"][0], self.stats["SV"][1], 180) # please kill me

		self.ai_action = "wander"
		self._move = True
		
		self.target_loc = [x, y]
		self.target_view_off = 180
		self.en_ta_angle = 0

		self.proj_cooldown = 0

		# wander
		self.target_change_timer = 0

		# suspicious
		self.sus_time = [0, False] # kill me

		# lookout
		self.stop_lookout = True
		self.last_known = []

		self.damage_counters = []

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

	def ai(self, game_map, target: Entity, projs: list[Entity], dt: float, ai=True):
		self.sus_view.update_lines(self.rect.center)
		self.view.update_lines(self.rect.center)
		self.view.lines[1][1] = list(target.rect.center)
		self.sus_view.lines[1][1] = list(target.rect.center)
		self.sus_view.offset = self.view.offset

		self.en_ta_angle = math.atan2(self.target_loc[1] - self.rect.centery, self.target_loc[0] - self.rect.centerx)
		if self.movement != [0, 0]:
			self.view.offset = [math.degrees(self.en_ta_angle), self.en_ta_angle]

		if not self.disable_friction:
			acc = self.friction
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

		self.movement = [0, 0]

		if self.stats["HP"][0] < self.stats["HP"][1] or self.ai_action == "alert":
			self.view.length = self.sus_view.length*1.5

		self.alert(target, projs, game_map) if self.ai_action == "alert" else self.lookout(target, game_map) if self.ai_action == "lookout" else self.suspicious(target, game_map) if self.ai_action == "suspicious" else self.wander(game_map)
		
		if self.view.lines[1][2] < -math.pi/2 or self.view.lines[1][2] >= math.pi/2:
			self.flip = True
		else:
			self.flip = False

		if (self.sus_time[1] and time.time()-self.sus_time[0] >= (math.dist(self.rect.center, target.rect.center))*0.1) or self.view.collision(game_map.tile_rects, target.rect):
			self.ai_action = "alert"
			self.sus_time[1] = False

		elif self.sus_view.collision(game_map.tile_rects, target.rect):
			if self.ai_action != "alert":
				self.ai_action = "suspicious"
				if not self.sus_time[1]:
					self.sus_time = [time.time(), True]

		else:
			if self.ai_action == "alert":
				self.ai_action = "lookout"
				self.stop_lookout = False
				self.last_known = []
			else:
				if self.stop_lookout:
					self.ai_action = "wander"
					self.spawn_point = [self.x, self.y]

			self.sus_time[1] = False

		if self._move:
			if math.dist(self.target_loc, self.rect.center) >= 5:
				if -self.stats["SP"]*self.speed_affect < self.vel.x < self.stats["SP"]*self.speed_affect:
					self.vel.x += math.cos(self.en_ta_angle)*self.acceleration
				if -self.stats["SP"]*self.speed_affect < self.vel.y < self.stats["SP"]*self.speed_affect:
					self.vel.y += math.sin(self.en_ta_angle)*self.acceleration
			else:
				if self.ai_action == "lookout":
					self.stop_lookout = True

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

		if self.disable_friction:
			if self.movement[0] == 0:
				self.vel.x = 0
			if self.movement[1] == 0:
				self.vel.y = 0
		self.movement_collision(game_map.tile_rects)
		if self.ai_action == "wander" and True in self.collisions.values():
			self.target_loc = list(self.rect.center)

	def wander(self, game_map):
		self.speed_affect = 0.75
		if time.time()-self.target_change_timer >= 5:
			if random.randint(0, 1) == 0:
				self.target_loc = [random.uniform(self.spawn_point[0]-300, self.spawn_point[0]+300), random.uniform(self.spawn_point[1]-300, self.spawn_point[1]+300)]
			elif self.movement == [0, 0]:
				self.view.offset[0] = random.uniform(0, 360)
				self.view.offset[1] = math.radians(self.view.offset[0])

			self.target_change_timer = time.time()
		
	def suspicious(self, target: Entity, game_map):
		self.target_loc = target.rect.center
		self.view.offset = [math.degrees(self.en_ta_angle), self.en_ta_angle]
		self.speed_affect = 0.5

	def alert(self, target: Entity, projs: list[Entity], game_map):
		self.target_loc = target.rect.center
		self.view.offset = [math.degrees(self.en_ta_angle), self.en_ta_angle]
		self.speed_affect = 1

		self.attack(target, projs, game_map)

	def lookout(self, target: Entity, game_map):
		if self.last_known == []:
			self.last_known = target.rect.center

		self.target_loc = self.last_known
		self.speed_affect = 1.5

	def attack(self, target: Entity, projs: list[Entity], game_map):
		pass

	def damage(self, dmg, proj):
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

				self.view.offset = [180-proj.rotation, math.pi-math.radians(proj.rotation)]

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

	def proj_move(self, proj_list, game_map, dt):
		pass

	def proj_dmg(self, proj_list, entities):
		pass

	def draw_UI(self, win, scroll):
		for dmg_counter in self.damage_counters:
			dmg_counter[0].render(win, (dmg_counter[1][0][0], dmg_counter[1][0][1]), scroll)
