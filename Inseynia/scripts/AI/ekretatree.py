import time, random, math

from .ai import MainAI
from scripts.logic.projectiles import Projectile

class NormalProj(Projectile):
	def __init__(self, sloc: tuple[int, int], eloc: tuple[int, int], attack: float, data: dict, shooter):
		super().__init__(sloc, eloc, attack, data, shooter)

	def move_code(self, game_map, dt, scroll, mouse_pos, entities, player, proj_list):
		return self.end_drop(game_map, proj_list), True

class AI(MainAI):
	def __init__(self, x: int, y: int, animation_dirs: str, stats, _):
		super().__init__(x, y, animation_dirs, stats, "Ekreta Tree", "enemy")
		self.shot_time = 0
		self.proj_data = {"img": "Thorn", "speed": 4, "duration": 1000, "knockback": 10, "pierces": 0}

		self.offset = 0

	def ai(self, game_map, target, projs, dt: float):
		self.ai_action = "alert"
		super().ai(game_map, target, projs, dt)
		
	def attack(self, target, projs, game_map):
		if random.randint(0, 100) == 0:
			for _ in range(3):
				for rad in range(4):
					rad = math.radians(rad*360/4)+self.offset
					projs.append(NormalProj(self.rect.center, (self.rect.centerx+100*math.cos(rad), self.rect.centery+100*math.sin(rad)), self.stats["AP"], self.proj_data, self))
				self.proj_cooldown = time.time()
				self.offset += 0.1
		