import time, random, math

from .ai import MainAI
from scripts.logic.projectiles import Projectile

class AI(MainAI):
    def __init__(self, x: int, y: int, animation_dirs: list[str], animation_pause: int, stats):
        super().__init__(x, y, animation_dirs, animation_pause, stats)
        self.shot_time = 0
        self.proj_data = {"img": "Thorn", "speed": 6, "type": "normal", "duration": 1000, "knockback": 10, "pierces": 0, "end stick": True, "wall stick": True}

        self.offset = 0

    def ai(self, tiles, target, projs, dt: float):
        self.ai_action = "alert"
        super().ai(tiles, target, projs, dt)
        

    def attack(self, target, projs):
        if time.time()-self.shot_time < random.uniform(2, 3):
            self._move = False
            if time.time()-self.proj_cooldown >= .25:
                for rad in range(8):
                    rad = math.radians(rad*360/8)+self.offset
                    projs.append(Projectile(self.rect.center, (self.rect.centerx+100*math.cos(rad), self.rect.centery+100*math.sin(rad)), self.stats["AP"], self.proj_data, self))
                    self.proj_cooldown = time.time()
                self.offset += 0.1
        else:
            if random.randint(0, 50) == 0:
                self.shot_time = time.time()
        return projs