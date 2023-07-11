import time, math

from scripts.loadingDL.files import files

Projectile = files["projectiles"].Projectile

class NormalProj(Projectile):
	def __init__(self, sloc: tuple[int, int], eloc: tuple[int, int], attack: float, data: dict, shooter):
		super().__init__(sloc, eloc, attack, data, shooter)

	def move_code(self, game_map, dt, scroll, mouse_pos, entities, player):
		return self.end_drop(game_map), True

class Arc(Projectile):
	def __init__(self, sloc: tuple[int, int], eloc: tuple[int, int], attack: float, data: dict, shooter):
		super().__init__(sloc, eloc, attack, data, shooter)
		self.ang = math.degrees(math.atan2(self.sloc.y-self.eloc.y, self.eloc.x-self.sloc.x))-30
		self.start_ang = math.degrees(math.atan2(self.sloc.y-self.eloc.y, self.eloc.x-self.sloc.x))-30
		self.damaged = False

	def move_code(self, game_map, dt, scroll, mouse_pos, entities, player):
		if self.ang-self.start_ang < 60:
			x = self.sloc.x + 28 * math.cos(math.radians(self.ang))
			y = self.sloc.y - 28 * math.sin(math.radians(self.ang))
			self.ang += self.data["speed"]
			
			self.movement = [x-self.x, y-self.y]
		else:
			if self in game_map.full_projs:
				game_map.full_projs.remove(self)

		return self.end_del(game_map, tile_collide=False), True

	def damage(self, game_map, entities, actually_dmg=True):
		if not self.damaged:
			status, entity = super().damage(game_map, entities, actually_dmg)
			if status:
				self.damaged = True
			return status, entity
		return False, None

weapon_name = "Wooden Bow"
class Weapon:
	player_class = "Archer"
	attack_power = 9
	cooldown = 0.3
	special_cooldown = 1
	auto_fire = True
	proj_data = {
		"img": "arrow",
		"speed": 6,
		"knockback": 10,
		"duration": 1,
		"pierces": 0
	}
	def __init__(self):
		self.cooldown_time = 0
		self.specialed = False

	def attack(self, player, mouse_pos, enemies, projs, weaker=False):
		if (time.time()-self.cooldown_time >= self.cooldown and not self.specialed) or (time.time()-self.cooldown_time >= self.special_cooldown and self.specialed):
			self.specialed = False
			if not weaker:
				projs.append(NormalProj(player.rect.center, mouse_pos, self.attack_power, self.proj_data, player))
			else:
				proj_data = {
					"img": weapon_name.lower().replace(" ", "_"),
					"speed": 1,
					"knockback": 5,
					"duration": 0.22,
					"pierces": 999
				}
				projs.append(Arc(player.rect.center, mouse_pos, 2, proj_data, player))

			self.cooldown_time = time.time()
			return True

	def special(self, player, mouse_pos, enemies, projs):
		for i in range(8):
			rad = math.radians(i*360/8)
			projs.append(NormalProj(player.rect.center, (player.rect.centerx+100*math.cos(rad), player.rect.centery+100*math.sin(rad)), self.attack_power, self.proj_data, player))
		self.cooldown_time = time.time()
		self.specialed = True
		return True
