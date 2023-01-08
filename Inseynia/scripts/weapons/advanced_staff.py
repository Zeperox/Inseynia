import time
from scripts.logic.projectiles import Projectile

class NormalProj(Projectile):
	def __init__(self, sloc: tuple[int, int], eloc: tuple[int, int], attack: float, data: dict, shooter):
		super().__init__(sloc, eloc, attack, data, shooter)

	def move_code(self, game_map, dt, scroll, mouse_pos, entities, player, proj_list):
		return self.end_del(proj_list), True

weapon_name = "Advanced Staff"
class Weapon:
	player_class = "Mage"
	attack_power = 4
	cooldown = 0.3
	auto_fire = True
	proj_data = {
		"img": "Fireball",
		"speed": 6,
		"knockback": 10,
		"duration": 1,
		"pierces": 0
	}
	def __init__(self):
		self.cooldown_time = 0

	def attack(self, player, mouse_pos, enemies, projs):
		if time.time()-self.cooldown_time >= self.cooldown:
			projs.append(NormalProj(player.rect.center, mouse_pos, self.attack_power, self.proj_data, player))
			self.cooldown_time = time.time()
		