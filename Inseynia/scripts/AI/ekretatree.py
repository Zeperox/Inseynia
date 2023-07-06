import time, random, math

from scripts.loadingDL.files import files

MainAI = files["ai"].MainAI
Projectile = files["projectiles"].Projectile

class NormalProj(Projectile):
	def __init__(self, sloc: tuple[int, int], eloc: tuple[int, int], attack: float, data: dict, shooter):
		super().__init__(sloc, eloc, attack, data, shooter)

	def move_code(self, game_map, dt, scroll, mouse_pos, entities, player):
		return self.end_drop(game_map), True

class AI(MainAI):
	def __init__(self, x: int, y: int, animation_dirs: str, stats, _):
		super().__init__(x, y, animation_dirs, stats, "Ekreta Tree", "enemy")
		self.shot_time = 0
		self.proj_data = {"img": "thorn", "speed": 4, "duration": 1000, "knockback": 10, "pierces": 0}

		self.offset = 0

	def ai(self, game_map, target, dt: float, difficulty):
		self.ai_action = "alert"
		super().ai(game_map, target, dt, difficulty)
		
	def attack(self, target, game_map, difficulty):
		if random.randint(0, 100) == 0:
			for _ in range(3):
				for rad in range(4):
					rad = math.radians(rad*360/4)+self.offset
					game_map.full_projs.append(NormalProj(self.rect.center, (self.rect.centerx+100*math.cos(rad), self.rect.centery+100*math.sin(rad)), self.stats["AP"], self.proj_data, self))
				self.proj_cooldown = time.time()
				self.offset += 0.1
		