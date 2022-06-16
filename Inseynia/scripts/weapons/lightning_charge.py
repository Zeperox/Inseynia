import time, math
from scripts.logic.projectiles import Projectile

weapon_name = "Lightning Charge"
class Weapon:
    player_class = "Mage"
    attack_power = 25
    cooldown = 1.5
    auto_fire = True
    proj_data = {
        "img": "Arrow",
        "speed": 6,
        "knockback": 0,
        "type": "drpo",
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
