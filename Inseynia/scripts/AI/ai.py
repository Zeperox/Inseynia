import math, pygame, time, random

from scripts.logic.entity import Entity
from scripts.logic.view import View

class MainAI(Entity):
    def __init__(self, x: int, y: int, animation_dirs: list[str], animation_pause: int, stats):
        super().__init__(x, y, animation_dirs, animation_pause)
        self.stats = {
            "HP": [stats["health"], stats["health"]],
            "AP": stats["attack"],
            "DP": stats["defense"],
            "SP": stats["speed"],
            "V": stats["view"],
            "SV": stats["suspicious view"]
        }
        self.speed_affect = 1
        self.knockback_resist = stats["knockback resistence"]

        self.spawn_point = [x, y]
        self.target = None

        self.view = View(list(self.rect.center), self.stats["V"][0], self.stats["V"][1], 180)
        self.sus_view = View(list(self.rect.center), self.stats["SV"][0], self.stats["SV"][1], 180) # please kill me

        self.ai_action = "wander"
        self._move = True
        
        self.target_loc = [x, y]
        self.target_view_off = 180
        self.en_ta_angle = 0

        self.proj_cooldown = 0

        # wander
        self.target_change_timer = 0

        # suspicious
        self.sus_time = [0, False] # kill me

        # lookout
        self.stop_lookout = True
        self.last_known = []

    def ai(self, tiles: list[pygame.Rect], target: Entity, projs: list[Entity], dt: float):
        self.sus_view.update_lines(self.rect.center)
        self.view.update_lines(self.rect.center)
        self.view.lines[1][1] = list(target.rect.center)
        self.sus_view.lines[1][1] = list(target.rect.center)
        self.sus_view.offset = self.view.offset

        self.en_ta_angle = math.atan2(self.target_loc[1] - self.rect.centery, self.target_loc[0] - self.rect.centerx)
        if self.movement != [0, 0]:
            self.view.offset = [math.degrees(self.en_ta_angle), self.en_ta_angle]

        self.movement = [0, 0]
        dx = dy = 0

        if self.stats["HP"][0] < self.stats["HP"][1] or self.ai_action == "alert":
            self.view.length = self.sus_view.length*1.5

        self.alert(target, projs) if self.ai_action == "alert" else self.lookout(target) if self.ai_action == "lookout" else self.suspicious(target) if self.ai_action == "suspicious" else self.wander()
        
        if self.view.lines[1][2] < -math.pi/2 or self.view.lines[1][2] >= math.pi/2:
            self.flip = True
        else:
            self.flip = False

        if (self.sus_time[1] and time.time()-self.sus_time[0] >= (math.dist(self.rect.center, target.rect.center))*0.1) or self.view.collision(tiles, target.rect):
            self.ai_action = "alert"
            self.sus_time[1] = False

        elif self.sus_view.collision(tiles, target.rect):
            if self.ai_action != "alert":
                self.ai_action = "suspicious"
                if not self.sus_time[1]:
                    self.sus_time = [time.time(), True]

        else:
            if self.ai_action == "alert":
                self.ai_action = "lookout"
                self.stop_lookout = False
                self.last_known = []
            else:
                if self.stop_lookout:
                    self.ai_action = "wander"
                    self.spawn_point = [self.x, self.y]

            self.sus_time[1] = False

        if math.dist(self.target_loc, self.rect.center) >= 20:
            dx = math.cos(self.en_ta_angle)*self.stats["SP"]*dt*self.speed_affect
            dy = math.sin(self.en_ta_angle)*self.stats["SP"]*dt*self.speed_affect
        else:
            if self.ai_action == "lookout":
                self.stop_lookout = True

        if self._move:
            if not self.knockback:
                self.movement[1] += dy
                self.movement[0] += dx
            else:
                vel = (self.knockback_dir-pygame.Vector2(self.rect.center)).normalize()*self.knockback_speed
                self.movement[1] += vel.y*dt
                self.movement[0] += vel.x*dt

                self.knockback_speed *= 0.9
                if self.knockback_speed <= 0.5:
                    self.knockback = False

        collision_types = self.movement_collision(tiles)
        if self.ai_action == "wander" and True in collision_types.values():
            self.target_loc = list(self.rect.center)

        return collision_types

    def wander(self):
        self.speed_affect = 0.75
        if time.time()-self.target_change_timer >= 5:
            if random.randint(0, 1) == 0:
                self.target_loc = [random.uniform(self.spawn_point[0]-300, self.spawn_point[0]+300), random.uniform(self.spawn_point[1]-300, self.spawn_point[1]+300)]
            elif self.movement == [0, 0]:
                self.view.offset[0] = random.uniform(0, 360)
                self.view.offset[1] = math.radians(self.view.offset[0])

            self.target_change_timer = time.time()
        
    def suspicious(self, target: Entity):
        self.target_loc = target.rect.center
        self.view.offset = [math.degrees(self.en_ta_angle), self.en_ta_angle]
        self.speed_affect = 0.5

    def alert(self, target: Entity, projs: list[Entity]):
        self.target_loc = target.rect.center
        self.view.offset = [math.degrees(self.en_ta_angle), self.en_ta_angle]
        self.speed_affect = 1

        self.attack(target, projs)

    def lookout(self, target: Entity):
        if self.last_known == []:
            self.last_known = target.rect.center

        self.target_loc = self.last_known
        self.speed_affect = 1.5

    def attack(self, target: Entity, projs: list[Entity]):
        return projs

    def damage(self, dmg, proj):
        hit = False
        if self.collidable and self.active:
            hit = True
            if time.time()-self.i_frame >= 0.5:
                dmg = round(dmg*dmg/(dmg+self.stats["DP"]))
                if dmg == 0: dmg = 1

                self.stats["HP"][0] -= dmg
                self.i_frame = time.time()

                self.view.offset = [180-proj.rotation, math.pi-math.radians(proj.rotation)]

        return self.stats["HP"][0], hit
