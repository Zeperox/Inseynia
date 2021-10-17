from .entity import Entity
import pygame, math
from pygame.locals import *
from scripts.assets.sprites import images
from scripts.custom_collisions.obb import OBB

class Projectiles(Entity):
    def __init__(self, x, y, attack, proj_data, end_loc):
        self.start_loc = (x, y)
        self.end_loc = end_loc

        self.rotation = math.atan2(self.start_loc[1]-self.end_loc[1], self.end_loc[0]-self.start_loc[0]); self.rotation = math.degrees(self.rotation)

        self.img = pygame.transform.rotate(images[proj_data["Proj Obj"]], self.rotation)

        super().__init__(x, y, self.img)
        self.proj_data = proj_data
        self.attack = attack
        self.boom_return = False
        self.changed_loc = False

        self.V_start = pygame.Vector2(self.start_loc)
        self.V_end = pygame.Vector2(self.end_loc)

        #self.rect = pygame.Rect(x, y, self.img.get_width(), self.img.get_height())
        self.obb = OBB((self.x+self.img.get_width()*0.5, self.y+self.img.get_height()*0.5), self.img.get_size(), self.rotation)

    def move(self, tiles, dt, shooter, scroll=[0, 0], mouse_pos=(0, 0), entities=[], proj_list=[]):
        '''if math.degrees(math.atan2(self.start_loc[1]-self.end_loc[1], self.end_loc[0]-self.start_loc[0])) != self.rotation:
            self.rotation = math.degrees(math.atan2(self.start_loc[1]-self.end_loc[1], self.end_loc[0]-self.start_loc[0]))
            self.img = pygame.transform.rotate(self.img, self.rotation)'''

        self.movement = [0, 0]
        if self.end_loc == (mouse_pos[0]+scroll[0], mouse_pos[1]+scroll[1]):
            self.end_loc = (mouse_pos[0]+scroll[0]-self.obb.width*0.5, mouse_pos[1]+scroll[1]-self.obb.height*0.5)
        if math.dist(self.start_loc, (self.x, self.y)) < self.proj_data["Range"] and not self.boom_return and self.proj_data["Proj Type"] != "drop":
            if self.proj_data["Proj Type"] == "normal":
                vel = (self.V_end - self.V_start).normalize()*self.proj_data["Speed"]
                self.movement[0] += vel.x*dt; self.movement[1] += vel.y*dt
                
            elif self.proj_data["Proj Type"] == "mouse follow":
                vel = (pygame.Vector2(mouse_pos[0]+scroll[0], mouse_pos[1]+scroll[1]) - pygame.Vector2(self.x, self.y)).normalize()*self.proj_data["Speed"]
                self.start_loc, self.end_loc = (self.x, self.y), (mouse_pos[0]+scroll[0], mouse_pos[1]+scroll[1])
                self.movement[0] += vel.x*dt; self.movement[1] += vel.y*dt

            elif self.proj_data["Proj Type"] == "nearest follow":
                if len(entities) > 0:
                    entity_dist = []
                    for entity in entities:
                        entity_dist.append(math.dist([self.x, self.y], [entity.x, entity.y]))
                    i = entity_dist.index(min(entity_dist))
                    vel = (pygame.Vector2(entities[i].x, entities[i].y) - pygame.Vector2(self.x, self.y)).normalize()*self.proj_data["Speed"]
                    #self.start_loc, self.end_loc = (self.x, self.y), (entities[i].x, entities[i].y)
                    self.movement[0] += vel.x*dt; self.movement[1] += vel.y*dt
                else:
                    vel = (self.V_end - self.V_start).normalize()*self.proj_data["Speed"]
                    self.movement[0] += vel.x*dt; self.movement[1] += vel.y*dt
        
            elif self.proj_data["Proj Type"] == "boomerang":
                vel = (self.V_end - self.V_start).normalize()*self.proj_data["Speed"]
                self.movement[0] += vel.x*dt; self.movement[1] += vel.y*dt
        
        elif self.proj_data["Proj Type"] == "drop":
            if not self.drop_set:
                self.y = -self.obb.height
                self.x = self.end_loc[0]
                self.drop_set = True
                self.collide = False
            
            if self.end_loc[1] - self.y > 2:
                self.movement[1] += self.proj_data["Speed"]*dt
            else:
                if self.proj_data["End Destroy"]:
                    proj_list.remove(self)
                    return proj_list
                else:
                    self.collide = True

        elif self.boom_return:
            self.proj_data["Speed"] += .075
            vel = (pygame.Vector2(shooter.x, shooter.y) - pygame.Vector2(self.x, self.y)).normalize()*self.proj_data["Speed"]
            self.start_loc, self.end_loc = (self.x, self.y), (shooter.x, shooter.y)
            self.movement[0] += vel.x*dt; self.movement[1] += vel.y*dt
            if self.obb.colliderect(shooter.rect):
                proj_list.remove(self)
                return proj_list
        
        else:
            if self.proj_data["End Destroy"] and self.proj_data["Proj Type"] != "boomerang":
                proj_list.remove(self)
                return proj_list
            else:
                if self.proj_data["Proj Type"] != "boomerang":
                    self.collide = False
                else:
                    self.boom_return = True

        self.x += self.movement[0]; self.y += self.movement[1]
        self.obb.center.x, self.obb.center.y = self.x+self.img.get_width()*0.5, self.y+self.img.get_height()*0.5
        
        self.movement_collision(tiles, False, False)

        return proj_list

    def damage(self, entities, projectiles):
        for entity in entities:
            if self.obb.colliderect(entity.rect):
                entities = entity.lose_hp(self.attack, entities)

                if self.proj_data["Collision Destroy"]: projectiles.remove(self)
        return entities, projectiles
                
    def offmap(self, game_map, projectiles):
        if self.x < game_map.x-self.obb.width or self.y < game_map.y-self.obb.height or self.x > game_map.w or self.y > game_map.h:
            projectiles.remove(self)
        
        return projectiles
    