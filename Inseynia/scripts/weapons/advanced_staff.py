import time, math
from scripts.logic.projectiles import Projectile

weapon_name = "Advanced Staff"
class Weapon:
    player_class = "Mage"
    attack_power = 4
    cooldown = 0.3
    auto_fire = True
    proj_data = {
        "img": "Fireball",
        "speed": 6,
        "knockback": 10,
        "type": "normal",
        "duration": 1,
        "pierces": 0,
        "end stick": False,
        "wall stick": False
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
