import time, math
from scripts.logic.projectiles import Projectile

weapon_name = "Wooden Bow"
class Weapon:
    player_class = "Archer"
    attack_power = 9
    cooldown = 0.3
    auto_fire = False
    proj_data = {
        "img": "Arrow",
        "speed": 6,
        "knockback": 10,
        "type": "normal",
        "duration": 1,
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
            offset = math.atan2(mouse_pos[1]-player.rect.centery, mouse_pos[0]-player.rect.centerx)
            for ang in range(5):
                ang = ang-5//2
                if ang < 0:
                    rad = offset-math.radians(abs(ang)*12.5/5)
                elif ang > 0:
                    rad = offset+math.radians(ang*12.5/5)
                else:
                    rad = offset

                projs.append(Projectile(player.rect.center, (player.rect.centerx+math.cos(rad)*100,player.rect.centery+ math.sin(rad)*100), self.attack_power, self.proj_data, player))

            self.cooldown_time = time.time()

        return projs, shot
