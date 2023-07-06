import time

from scripts.loadingDL.files import files

Projectile = files["projectiles"].Projectile

weapon_name = "Lightning Charge"
class Weapon:
	player_class = "Mage"
	attack_power = 25
	cooldown = 1.5
	special_cooldown = 5
	auto_fire = True
	proj_data = {
		"img": "arrow",
		"speed": 6,
		"knockback": 0,
		"type": "drop",
		"duration": 1,
		"pierces": 0
	}
	def __init__(self):
		self.cooldown_time = 0
		self.specialed = False

	def attack(self, player, mouse_pos, enemies, projs):
		if time.time()-self.cooldown_time >= self.cooldown:
			projs.append(Projectile(player.rect.center, mouse_pos, self.attack_power, self.proj_data, player))
			self.cooldown_time = time.time()

			return True

		
