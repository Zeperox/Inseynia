import time

from scripts.loadingDL.files import files

Projectile = files["projectiles"].Projectile

class NormalProj(Projectile):
	def __init__(self, sloc: tuple[int, int], eloc: tuple[int, int], attack: float, data: dict, shooter):
		super().__init__(sloc, eloc, attack, data, shooter)

	def move_code(self, game_map, dt, scroll, mouse_pos, entities, player):
		return self.end_drop(game_map), True

weapon_name = "Crossbow"
class Weapon:
	player_class = "Archer"
	attack_power = 6
	cooldown = 1
	special_cooldown = 3
	auto_fire = False
	proj_data = {
		"img": "arrow",
		"speed": 12,
		"knockback": 15,
		"duration": 5,
		"pierces": 1
	}
	def __init__(self):
		self.cooldown_time = 0
		self.specialed = False

	def attack(self, player, mouse_pos, enemies, projs):
		if time.time()-self.cooldown_time >= self.cooldown:
			projs.append(NormalProj(player.rect.center, mouse_pos, self.attack_power, self.proj_data, player))
			self.cooldown_time = time.time()

			return True
