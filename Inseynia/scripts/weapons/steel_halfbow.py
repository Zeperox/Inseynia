import time, math
from scripts.logic.projectiles import Projectile

weapon_name = "Steel Halfbow"
class Weapon:
    player_class = "Archer"
    attack_power = 7
    cooldown = 0.3
    auto_fire = False
    proj_data = {
        "img": "Arrow",
        "speed": 8,
        "knockback": 5,
        "type": "normal",
        "duration": 0.6,
        "pierces": 0,
        "end stick": True,
        "wall stick": True
    }
    def __init__(self):
        self.cooldown_time = 0

    def attack(self, player, mouse_pos, enemies, projs):
        shot = False
        if time.time()-self.cooldown_time >= self.cooldown:
            shot = True
            projs.append(Projectile(player.rect.center, mouse_pos, self.attack_power, self.proj_data, player))
            self.cooldown_time = time.time()

        return projs, shot
