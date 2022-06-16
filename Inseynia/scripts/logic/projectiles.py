import pygame, math, time, copy

from scripts.logic.drops import Drop

from .entity import Entity
from scripts.loading.sprites import sprites
from scripts.loading.json_functions import load_json
#from scripts.custom_collisions.obb import OBB


class Projectile(Entity):
    def __init__(self, sloc: tuple[int, int], eloc: tuple[int, int], attack: float, data: dict, shooter: Entity):
        super().__init__(sloc[0], sloc[1], sprites[data["img"]])

        self.sloc = pygame.Vector2(sloc)
        self.eloc = pygame.Vector2(eloc)
        self.data = copy.deepcopy(data)
        self.data["attack"] = attack
        self.shooter = shooter

        self.rotation = math.degrees(math.atan2(self.sloc.y-self.eloc.y, self.eloc.x-self.sloc.x))
        self.img = pygame.transform.rotate(self.orig_img, self.rotation)

        self.boom_return = False
        self.changed_loc = False
        self._move = True
        self.ricochet = 0

        self.shot_time = time.time()
        self.pierces = []

        #self.rect = OBB((self.x+self.orig_img.get_width()*0.5, self.y+self.orig_img.get_height()*0.5), self.orig_img.get_size(), -self.rotation)
        self.rect = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())

    def move(self, game_map, dt: float, scroll: list[int, int] = [0, 0], mouse_pos: tuple[int, int] = (0, 0), entities: list[Entity] = [], proj_list: list[Entity] = []):
        if self._move:
            self.movement = [0, 0]

            if self.rotation != math.degrees(math.atan2(self.sloc.y-self.eloc.y, self.eloc.x-self.sloc.x)):
                self.rotation = math.degrees(math.atan2(self.sloc.y-self.eloc.y, self.eloc.x-self.sloc.x))
                self.img = pygame.transform.rotate(self.orig_img, self.rotation)

            if time.time()-self.shot_time < self.data["duration"] and not self.boom_return and self.data["type"] != "drop":
                if self.data["type"] == "mouse follow":
                    self.eloc = pygame.Vector2(mouse_pos[0]+scroll[0]-self.rect.width*0.5, mouse_pos[1]+scroll[1]-self.rect.height*0.5)
                    self.sloc = pygame.Vector2(self.x, self.y)
                
                elif self.data["type"] == "nearest follow":
                    if self.shooter in entities:
                        entities.remove(self.shooter)
                    for pierce in self.pierces:
                        if pierce in entities:
                            entities.remove(pierce)
                            
                    if len(entities) > 0:
                        entity_dist = []
                        for entity in entities:
                            entity_dist.append(math.dist([self.x, self.y], [entity.x, entity.y]))
                        i = entity_dist.index(min(entity_dist))

                        self.eloc = pygame.Vector2(entities[i].rect.center)
                        self.sloc = pygame.Vector2(self.x, self.y)

            elif self.data["type"] == "drop":
                if not self.drop_set:
                    self.y = -self.rect.height
                    self.x = self.eloc.x
                    self.drop_set = True
                    self.collide = False
                    self.sloc = pygame.Vector2(self.x, self.y)
                
                if self.eloc.y - self.y > 2:
                    self.eloc = pygame.Vector2(self.x, self.y+1)
                else:
                    if self.data["end stick"]:
                        game_map.drops.append(["arrow", Drop(self.x, self.y, self.img), 0])
                        if self in proj_list:
                            proj_list.remove(self)
                    else:
                        if self in proj_list:
                            proj_list.remove(self)

            elif self.boom_return:
                self.data["speed"] += .075
                self.eloc = pygame.Vector2(self.shooter.rect.center)
                self.sloc = pygame.Vector2(self.x, self.y)
                if self.rect.colliderect(self.shooter.rect):
                    if self in proj_list:
                        proj_list.remove(self)
                    return proj_list
            
            vel = (self.eloc - self.sloc).normalize()*self.data["speed"]
            self.movement[0] += vel.x*dt; self.movement[1] += vel.y*dt
            collision_types = self.movement_collision(game_map.tile_rects, False)

            if True in collision_types.values():
                if self.data["wall stick"]:
                    game_map.drops.append(["arrow", Drop(self.x, self.y, self.img), 0])
                    if self in proj_list:
                        proj_list.remove(self)
                elif self.data["type"] == "boomerang":
                    self.boom_return = True
                else:
                    if self in proj_list:
                        proj_list.remove(self)
            if time.time()-self.shot_time >= self.data["duration"]:
                if self.data["end stick"]:
                    game_map.drops.append(["arrow", Drop(self.x, self.y, self.img), 0])
                    if self in proj_list:
                        proj_list.remove(self)
                elif self.data["type"] == "boomerang":
                    self.boom_return = True
                else:
                    if self in proj_list:
                        proj_list.remove(self)

        return proj_list

    def damage(self, entities: list[Entity], proj_list: list[Entity], mouse_pos):
        damaged_entity = None
        status = False
        if self._move:
            if self.shooter in entities:
                entities.remove(self.shooter)
            for entity in entities:
                if self.rect.colliderect(entity.rect):
                    try:
                        equipment = load_json(["scripts", "cache", "equipment.json"])
                        shield = equipment[1][entities[-1].equipment[1]]

                        if entities[-1].shielded[0] and entities[-1].shielded[0].colliderect(self.rect) and shield["ricochet"] and self.data["type"] != "drop":
                            if time.time()-entities[-1].shielded[1] < 0.5 and self.data["type"] in ["normal", "boomerang"]:
                                self.shot_time = time.time()
                                if self.data["type"] == "boomerang":
                                    self.boom_return = True
                                elif time.time()-self.ricochet >= 0.2:
                                    old_sloc = self.sloc.copy()
                                    self.sloc = self.eloc.copy()
                                    self.eloc = old_sloc

                                    self.ricochet = time.time()
                                    self.data["speed"] = shield["rico speed"]
                                    self.data["duration"] = shield["rico dist"]
                                    self.shooter = entities[-1]
                                break
                            else:
                                if self in proj_list:
                                    proj_list.remove(self)
                                break
                    except:
                        pass

                    pre_hp = entity.stats["HP"]
                    status, hit = entity.damage(self.data["attack"], self)
                    if entity not in self.pierces and hit:
                        self.pierces.append(entity)
                        entity.knockback = True
                        rot_rad = math.atan2(self.eloc.y-self.sloc.y, self.eloc.x-self.sloc.x)
                        entity.knockback_dir = pygame.Vector2(entity.rect.centerx+(math.cos(rot_rad)*100), entity.rect.centery+(math.sin(rot_rad)*100))
                        entity.knockback_speed = self.data["knockback"]-((abs(self.data["knockback"])*entity.knockback_resist)/100)
                    else:
                        entity.stats["HP"] = pre_hp

                    if self.data["type"] != "boomerang":
                        if self in proj_list and len(self.pierces) > self.data["pierces"]:
                            proj_list.remove(self)
                    else:
                        if len(self.pierces) > self.data["pierces"]:
                            self.boom_return = True
                    damaged_entity = entity
                    break

        return status, damaged_entity, proj_list
                
    def despawn(self, game_map, proj_list: list[Entity]):
        if self.x < game_map.x-self.rect.width or self.y < game_map.y-self.rect.height or self.x > game_map.w or self.y > game_map.h and self in proj_list:
            proj_list.remove(self)
        elif len(proj_list) >= 480 and not self._move and self in proj_list:
            proj_list.remove(self)

        return proj_list
