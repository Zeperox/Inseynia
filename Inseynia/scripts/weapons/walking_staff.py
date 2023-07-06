import time, pygame

from scripts.loadingDL.files import files

Projectile = files["projectiles"].Projectile

class Boomerang(Projectile):
	def __init__(self, sloc, eloc, attack, data, shooter):
		super().__init__(sloc, eloc, attack, data, shooter)
		self.return_proj = False

	def move_code(self, game_map, dt, scroll, mouse_pos, entities, player):
		if self.return_proj:
			self.sloc = pygame.Vector2(self.x, self.y)
			self.eloc = pygame.Vector2(self.shooter.x, self.shooter.y)
		
		if True in self.collisions.values() or self.damage(entities, False):
			self.return_proj = True
		if self.rect.colliderect(self.shooter) and self.return_proj:
			if self in game_map.full_projs:
				game_map.full_projs.remove(self)

		return True
		

weapon_name = "Walking Staff"
class Weapon:
	player_class = "Mage"
	attack_power = 3
	cooldown = 0.3
	special_cooldown = 1
	auto_fire = False
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
			projs.append(Boomerang(player.rect.center, mouse_pos, self.attack_power, self.proj_data, player))
			self.cooldown_time = time.time()

			return True

		
