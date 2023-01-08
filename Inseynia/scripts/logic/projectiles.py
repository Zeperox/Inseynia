import pygame, math, time, copy

from scripts.logic.drops import ProjDrop

from .entity import Entity
from scripts.loading.sprites import sprites
from scripts.loading.json_functions import load_json

class Projectile(Entity):
	def __init__(self, sloc: tuple[int, int], eloc: tuple[int, int], attack: float, data: dict, shooter: Entity):
		super().__init__(sloc[0], sloc[1], sprites[data["img"]])
		self.name = data["img"]

		self.sloc = pygame.Vector2(sloc)
		self.eloc = pygame.Vector2(eloc)
		self.data = copy.deepcopy(data)
		self.data["attack"] = attack
		self.shooter = shooter

		self.rotation = math.degrees(math.atan2(self.sloc.y-self.eloc.y, self.eloc.x-self.sloc.x))
		self.img = pygame.transform.rotate(self.orig_img, self.rotation)

		self._move = True
		self.ricochet = 0

		self.shot_time = time.time()
		self.pre_pause_time = 0
		self.pre_pause_ricochet = 0
		self.pierces = []

		#self.rect = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())

	def move(self, game_map, dt: float, scroll: list[int, int], mouse_pos: tuple[int, int], entities: list[Entity], player: Entity, proj_list: list[Entity]):
		if self._move:
			self.movement = [0, 0]
			self.pre_pause_time = time.time()
			self.pre_pause_ricochet = time.time()

			if self.rotation != math.degrees(math.atan2(self.sloc.y-self.eloc.y, self.eloc.x-self.sloc.x)):
				self.rotation = math.degrees(math.atan2(self.sloc.y-self.eloc.y, self.eloc.x-self.sloc.x))
				self.img = pygame.transform.rotate(self.orig_img, self.rotation)

			proj_list, default_movement = self.move_code(game_map, dt, scroll, mouse_pos, entities, player, proj_list)

			if default_movement:
				vel = (self.eloc - self.sloc).normalize()*self.data["speed"]
				self.movement[0] += vel.x*dt; self.movement[1] += vel.y*dt
			self.movement_collision(game_map.tile_rects, False)

	def move_code(game_map, dt, scroll, mouse_pos, entities, player, proj_list):
		pass

	def end_drop(self, game_map, proj_list, time_requirement=True):
		if not time_requirement:
			self.shot_time = 999999999999999999
		if time.time()-self.shot_time >= self.data["duration"]:
			game_map.full_drops.append([self.name, ProjDrop(self.x, self.y, self.orig_img, self.shooter, self.rotation), 0, time.time()])
			if self in proj_list:
				proj_list.remove(self)
		if True in self.collisions.values():
			game_map.full_drops.append([self.name, ProjDrop(self.x, self.y, self.orig_img, self.shooter, self.rotation), 0, time.time()])
			if self in proj_list:
				proj_list.remove(self)

	def end_del(self, proj_list, time_requirement=True):
		if not time_requirement:
			self.shot_time = 999999999999999999
		if time.time()-self.shot_time >= self.data["duration"]:
			if self in proj_list:
				proj_list.remove(self)
		if True in self.collisions.values():
			if self in proj_list:
				proj_list.remove(self)

	def damage(self, entities: list[Entity], proj_list: list[Entity], actually_dmg=True):
		damaged_entity = None
		status = False
		if self._move:
			if self.shooter in entities:
				entities.remove(self.shooter)
			for entity in entities:
				if self.entity_collision(entity):
					if actually_dmg:
						try:
							equipment = load_json(["scripts", "cache", "equipment.json"])
							shield = equipment[1][entities[-1].equipment[1]]

							if entities[-1].shielded[0] and entities[-1].shielded[0].colliderect(self.rect) and shield["ricochet"]:
								if time.time()-entities[-1].shielded[1] < 0.5:
									self.shot_time = time.time()
									if time.time()-self.ricochet >= 0.2:
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
						status, hit, critical = entity.damage(self.data["attack"], self)
						if entity not in self.pierces and hit:
							self.pierces.append(entity)
							entity.knockback = True

							if critical:
								kb_data = self.data["knockback"]*1.5
							else:
								kb_data = self.data["knockback"]

							entity.knockback_speed = (kb_data-((abs(kb_data)*entity.knockback_resist)*0.01))*0.5
							entity.knockback_dir = math.atan2(self.eloc.y-self.sloc.y, self.eloc.x-self.sloc.x)
						else:
							entity.stats["HP"] = pre_hp

						if self in proj_list and len(self.pierces) > self.data["pierces"]:
							proj_list.remove(self)
						damaged_entity = entity
						break
					else:
						return True

		if not actually_dmg:
			return False
		return status, damaged_entity

	def despawn(self, game_map, proj_list: list[Entity]):
		if self.x < game_map.x-self.rect.width or self.y < game_map.y-self.rect.height or self.x > game_map.w or self.y > game_map.h:
			if self in proj_list:
				proj_list.remove(self)
