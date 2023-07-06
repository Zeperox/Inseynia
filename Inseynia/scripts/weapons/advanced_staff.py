import time

from scripts.loadingDL.files import files

Projectile = files["projectiles"].Projectile

class NormalProj(Projectile):
	def __init__(self, sloc: tuple[int, int], eloc: tuple[int, int], attack: float, data: dict, shooter, proj_class):
		super().__init__(sloc, eloc, attack, data, shooter, proj_class)

	def move_code(self, game_map, dt, scroll, mouse_pos, entities, player):
		return self.end_del(game_map), True

weapon_name = "Advanced Staff"
class Weapon:
	player_class = "Mage"
	attack_power = 4
	cooldown = 0.3
	special_cooldown = 1
	auto_fire = True
	proj_data = {
		"img": "fireball",
		"speed": 6,
		"knockback": 10,
		"duration": 1,
		"pierces": 0
	}
	def __init__(self):
		self.cooldown_time = 0
		self.specialed = False

	def attack(self, player, mouse_pos, enemies, projs):
		if time.time()-self.cooldown_time >= self.cooldown:
			projs.append(NormalProj(player.rect.center, mouse_pos, self.attack_power, self.proj_data, player, self.player_class))
			self.cooldown_time = time.time()

			return True

	def special(self, player, mouse_pos, enemies, projs):
		if time.time()-self.cooldown_time >= self.cooldown:
			projs.append(NormalProj(player.rect.center, mouse_pos, self.attack_power, self.proj_data, player, self.player_class))
			self.cooldown_time = time.time()

			return True
		