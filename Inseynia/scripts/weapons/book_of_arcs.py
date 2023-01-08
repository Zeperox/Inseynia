import time, pygame
from scripts.logic.projectiles import Projectile

class Boomerang(Projectile):
	def __init__(self, sloc, eloc, attack, data, shooter):
		super().__init__(sloc, eloc, attack, data, shooter)
		self.return_proj = False

	def move_code(self, game_map, dt, scroll, mouse_pos, entities, player, proj_list):
		if self.return_proj:
			self.sloc = pygame.Vector2(self.x, self.y)
			self.eloc = pygame.Vector2(self.shooter.x, self.shooter.y)
		
		if True in self.collisions.values() or self.damage(entities, proj_list, False):
			self.return_proj = True
		if self.rect.colliderect(self.shooter) and self.return_proj:
			if self in proj_list:
				proj_list.remove(self)
		
		return proj_list, True
		

weapon_name = "Book of Arcs"
class Weapon:
	player_class = "Mage"
	attack_power = 13
	cooldown = 0.3
	auto_fire = True
	proj_data = {
		"img": "Arrow",
		"speed": 4,
		"knockback": 10,
		"duration": 1,
		"pierces": 3
	}
	def __init__(self):
		self.cooldown_time = 0

	def attack(self, player, mouse_pos, enemies, projs):
		if time.time()-self.cooldown_time >= self.cooldown:
			projs.append(Boomerang(player.rect.center, mouse_pos, self.attack_power, self.proj_data, player))
			self.cooldown_time = time.time()

		
