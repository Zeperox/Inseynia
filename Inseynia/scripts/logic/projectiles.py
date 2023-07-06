import pygame, math, time, copy

from scripts.loadingDL.files import files

from scripts.loadingDL.sprites import sprite
from scripts.loadingDL.json_functions import load_json

ProjDrop = files["drops"].ProjDrop
Entity = files["entity"].Entity
MainAI = files["ai"].MainAI
effects = files["effects"].effects

equipment = load_json(["scripts", "cacheDL", "equipment.json"])

class Projectile(Entity):
	def __init__(self, sloc: tuple[int, int], eloc: tuple[int, int], attack: float, data: dict, shooter: Entity, proj_class=None, effects = []):
		super().__init__(sloc[0], sloc[1], sprite("proj_"+data["img"]))
		self.name = data["img"]

		self.sloc = pygame.Vector2(sloc)
		self.eloc = pygame.Vector2(eloc)
		self.data = copy.deepcopy(data)
		self.data["attack"] = attack
		self.shooter = shooter
		self.proj_class = proj_class

		self.rotation = math.degrees(math.atan2(self.sloc.y-self.eloc.y, self.eloc.x-self.sloc.x))
		self.img = pygame.transform.rotate(self.orig_img, self.rotation)

		self._move = True
		self.ricochet = 0

		self.shot_time = time.time()
		self.pre_pause_time = 0
		self.pre_pause_ricochet = 0
		self.pierces = []

		self.effects = effects

	def tile_collision(self, tiles: dict, premove_rect: pygame.Rect=None, return_rects=False, directions=None) -> pygame.Rect:
		tile = super().tile_collision(tiles, premove_rect, return_rects, directions)
		if tile and tile.proj_collide:
			return tile
		else:
			return None

	def move(self, game_map, dt: float, scroll: list[int, int], mouse_pos: tuple[int, int], entities: list[Entity], player: Entity):
		if self._move:
			self.movement = [0, 0]
			self.pre_pause_time = time.time()
			self.pre_pause_ricochet = time.time()

			if self.rotation != math.degrees(math.atan2(self.sloc.y-self.eloc.y, self.eloc.x-self.sloc.x)):
				self.rotation = math.degrees(math.atan2(self.sloc.y-self.eloc.y, self.eloc.x-self.sloc.x))
				self.img = pygame.transform.rotate(self.orig_img, self.rotation)

			default_movement = self.move_code(game_map, dt, scroll, mouse_pos, entities, player)

			if default_movement:
				vel = (self.eloc - self.sloc).normalize()*self.data["speed"]
				self.movement[0] += vel.x*dt; self.movement[1] += vel.y*dt
			self.movement_collision(game_map.tiles, False)

	def move_code(game_map, dt, scroll, mouse_pos, entities, player):
		pass

	def end_drop(self, game_map, time_requirement=True, tile_collide=True):
		if (time.time()-self.shot_time >= self.data["duration"] and time_requirement) or (True in self.collisions.values() and tile_collide):
			game_map.full_drops.append([self.name, ProjDrop(self.x, self.y, self.orig_img, self.data["img"], self.rotation), 0, time.time()])
			if self in game_map.full_projs:
				game_map.full_projs.remove(self)

	def end_del(self, game_map, time_requirement=True, tile_collide=True):
		if (time.time()-self.shot_time >= self.data["duration"] and time_requirement) or (True in self.collisions.values() and tile_collide) and self in game_map.full_projs:
			game_map.full_projs.remove(self)

	def damage(self, game_map, entities: list[Entity], actually_dmg=True):
		from .player import Player

		damaged_entity = None
		status = False
		if self._move:
			if self.shooter in entities:
				entities.remove(self.shooter)
			for entity in entities:
				if self.entity_collision(entity) and entity.name.lower() != "sign":
					if actually_dmg:
						try:
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
									if self in game_map.full_projs:
										game_map.full_projs.remove(self)
									break
						except:
							pass

						pre_hp = entity.stats["HP"]
						if isinstance(entity, MainAI) and self.proj_class == "Thief" and entity.ai_action == "wander":
							if not isinstance(self.shooter, Player):
								self.data["attack"] *= 3
							elif isinstance(self.shooter, Player) and self.proj_class in self.shooter.classes:
								thief_index = self.shooter.classes.index(self.proj_class)
								if self.shooter.stats["EP"][thief_index][0] > 0:
									self.shooter.stats["EP"][thief_index][0] -= 1
									self.data["attack"] *= 3

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

						if len(self.pierces) > self.data["pierces"] and self in game_map.full_projs:
							game_map.full_projs.remove(self)
						damaged_entity = entity
						for effect in self.effects:
							effect = effect.split(" ")
							entity.effects.append(effects[effect[0]](entity, int(effect[1]), int(effect[2])))
						break
					else:
						return True

		if not actually_dmg:
			return False
		return status, damaged_entity

	def despawn(self, game_map):
		if self.x < game_map.x-self.rect.width or self.y < game_map.y-self.rect.height or self.x > game_map.data["size"][0]*32 or self.y > game_map.data["size"][1]*32 and self in game_map.full_projs:
			game_map.full_projs.remove(self)
