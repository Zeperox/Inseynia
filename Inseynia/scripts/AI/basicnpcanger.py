import time

from scripts.loadingDL.files import files

MainAI = files["ai"].MainAI
Projectile = files["projectiles"].Projectile

class NormalProj(Projectile):
	def __init__(self, sloc: tuple[int, int], eloc: tuple[int, int], attack: float, data: dict, shooter):
		super().__init__(sloc, eloc, attack, data, shooter)

	def move_code(self, game_map, dt, scroll, mouse_pos, entities, player):
		return self.end_drop(game_map), True

class AI(MainAI):
	def __init__(self, x: int, y: int, animation_dirs: str, stats, name):
		super().__init__(x, y, animation_dirs, stats, name, "enemy")

	def attack(self, target, game_map, difficulty):
		if time.time()-self.proj_cooldown >= 1:
			game_map.full_projs.append(NormalProj(self.rect.center, target.rect.center, self.stats["AP"], {"img": "arrow", "speed": 6, "duration": 1, "knockback": 30, "pierces": 0}, self))
			self.proj_cooldown = time.time()
		