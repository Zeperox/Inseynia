import time, pygame

from scripts.loadingDL.files import files

Projectile = files["projectiles"].Projectile

class MouseProj(Projectile):
	def __init__(self, sloc: tuple[int, int], eloc: tuple[int, int], attack: float, data: dict, shooter):
		super().__init__(sloc, eloc, attack, data, shooter)

	def move_code(self, game_map, dt, scroll, mouse_pos, entities, player):
		self.sloc = pygame.Vector2(self.x, self.y)
		self.eloc = pygame.Vector2(mouse_pos[0]+scroll.x, mouse_pos[1]+scroll.y)

		return self.end_del(game_map), True

weapon_name = "Amateur Staff"
class Weapon:
	player_class = "Mage"
	attack_power = 6
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
			projs.append(MouseProj(player.rect.center, mouse_pos, self.attack_power, self.proj_data, player))
			self.cooldown_time = time.time()

			return True

		
