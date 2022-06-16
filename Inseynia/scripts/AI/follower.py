import time

from .ai import MainAI
from scripts.logic.projectiles import Projectile

class AI(MainAI):
    def __init__(self, x: int, y: int, animation_dirs: list[str], animation_pause: int, stats):
        super().__init__(x, y, animation_dirs, animation_pause, stats)

    def attack(self, target, projs):
        if time.time()-self.proj_cooldown >= 1:
            projs.append(Projectile(self.rect.center, target.rect.center, self.stats["AP"], {"img": "Arrow", "speed": 6, "type": "normal", "duration": 1, "knockback": 10, "pierces": 0, "end stick": True, "wall stick": True}, self))
            self.proj_cooldown = time.time()
        return projs