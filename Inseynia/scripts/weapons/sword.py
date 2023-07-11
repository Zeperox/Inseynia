import time, math

from scripts.loadingDL.files import files

Projectile = files["projectiles"].Projectile

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

weapon_name = "Sword"
class Weapon:
	player_class = "Swordsman"
	attack_power = 20
	cooldown = 0.3
	special_cooldown = 1
	auto_fire = False
	proj_data = {
		"img": "sword",
		"speed": 1,
		"knockback": 5,
		"duration": 0.22,
		"pierces": 999
	}
	def __init__(self):
		self.cooldown_time = 0
		self.specialed = False

	def attack(self, player, mouse_pos, enemies, projs, weaken=False):
		if time.time()-self.cooldown_time >= self.cooldown:
			if not weaken:
				projs.append(Arc(player.rect.center, mouse_pos, self.attack_power, self.proj_data, player))
			else:
				proj_data = self.proj_data.copy()
				proj_data["duration"] *= 1.5
				proj_data["speed"] *= 0.5
				proj_data["knockback"] *= 0.75
				projs.append(Arc(player.rect.center, mouse_pos, self.attack_power*0.75, proj_data, player))
			self.cooldown_time = time.time()

			return True
