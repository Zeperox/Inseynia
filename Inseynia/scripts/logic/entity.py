import pygame, os, math, time, gif_pygame

from scripts.loadingDL.files import files

AngleRect = files["angle"].AngleRect

from typing import Union, Tuple, Iterable

class Entity:
	def __init__(self, x: int, y: int, animation_dirs: Union[str, pygame.Surface], animation_action: str = "idle") -> None:
		self.x = x
		self.y = y

		self.collisions = {"top": False, "bottom": False, "left": False, "right": False}
		
		self.img_type = type(animation_dirs)
		if self.img_type == str:
			self.animations: dict[str, gif_pygame.PygameGIF] = {}
			self.action = animation_action
			for img in os.listdir(animation_dirs):
				if not img.endswith(".gif"):
					continue

				self.animations[img[:-4]] = gif_pygame.load(os.path.join(animation_dirs, img))
		else:
			self.orig_img = animation_dirs.copy()
			self.img = animation_dirs.copy()

		self.flip = False

		self.movement = [0, 0]
		self.vel = pygame.Vector2()
		self.friction = 0.3
		self.acceleration = 0.5
		self.disable_friction = False

		self.effects = []

		self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
		if self.rect.height > 9:
			self.rect = self.rect.inflate(0, -14)
		if self.img_type == str:
			self.mask = pygame.mask.from_surface(self.animations[self.action].get_surface(0))
		else:
			self.mask = pygame.mask.from_surface(self.img)

		self.active = True
		self.collidable = True
		self.draw_img = True
		self.tile_collide = True

		self.i_frame = 0
		self.i_time = 0.1

		self.knockback = False
		self.knockback_dir = 0
		self.knockback_speed = 0
		self.knockback_resist = 0
		self.still_in_knockback = False

	@property
	def width(self) -> int:
		if self.img_type == str:
			return self.animations[self.action].get_width()
		else:
			return self.img.get_width()

	@property
	def height(self) -> int:
		if self.img_type == str:
			return self.animations[self.action].get_height()
		else:
			return self.img.get_height()

	def draw(self, win: pygame.Surface, scroll: Tuple[int, int]) -> None:
		if self.active and self.draw_img:
			img = self.animations[self.action].blit_ready() if self.img_type == str else self.img
			return (pygame.transform.flip(img, self.flip, False), (self.x-scroll.x, self.y-scroll.y))
   
	def tile_collision(self, tiles: dict, premove_rect: pygame.Rect=None, return_rects=False, directions=False) -> pygame.Rect:
		tile_pos = [(self.rect.centerx//32)-1, (self.rect.centery//32)-1]

		collidable_tiles = [tiles.get(f"{tile_pos[0]+x}:{tile_pos[1]+y}") for y in range(3) for x in range(3)]
		
		if return_rects:
			return collidable_tiles

		if premove_rect:
			rect = premove_rect.union(self.rect)
		else:
			rect = self.rect

		# 0: TL, 1: TM, 2: TR, 3: ML, 4: MM, 5: MR, 6: BL, 7: BM, 8: BR
		for tile in collidable_tiles:
			if tile == None:
				continue

			if rect.colliderect(tile.main_rect):
				return tile

	def movement_collision(self, tiles: dict, collide: bool=True) -> None:
		self.collisions = {"top": False, "bottom": False, "left": False, "right": False}

		premove_rect = self.rect.copy()

		# tiles
		self.x += self.movement[0]
		self.rect.x = self.x
		tile = self.tile_collision(tiles, premove_rect, directions=True)
		if tile and self.tile_collide:
			tile = tile.rect
			if self.movement[0] > 0:
				if collide:
					if isinstance(tile, AngleRect):
						ratio = tile.rect.width/tile.rect.height
						rel_y = (self.rect.y-tile.rect.y)*ratio

						if (rel_y <= 0 and tile.angle == 3) or (rel_y >= tile.rect.height-self.rect.height and tile.angle == 0) or (tile.angle in [1, 2] and self.rect.x < tile.rect.left):
							tile = tile.rect
						elif tile.angle == 0:
							new_x = tile.rect.x-rel_y+tile.rect.width-(self.rect.width*2)-3
							if self.x >= new_x:
								self.x = new_x
						elif tile.angle == 3:
							new_x = tile.rect.x+rel_y-self.rect.width
							if self.x >= new_x:
								self.x = new_x
					if isinstance(tile, pygame.Rect):
						self.x = tile.left-self.width
				self.collisions["right"] = True

			elif self.movement[0] < 0:
				if collide:
					if isinstance(tile, AngleRect):
						ratio = tile.rect.width/tile.rect.height
						rel_y = (self.rect.y-tile.rect.y)*ratio

						if (rel_y <= 0 and tile.angle == 2) or (rel_y >= tile.rect.height-self.rect.height and tile.angle == 1) or (tile.angle in [0, 3] and self.rect.x >= tile.rect.right-3):
							tile = tile.rect
						elif tile.angle == 1:
							new_x = tile.rect.x+rel_y+self.rect.height
							if self.x <= new_x:
								self.x = new_x
						elif tile.angle == 2:
							new_x = tile.rect.x-rel_y+tile.rect.width
							if self.x <= new_x:
								self.x = new_x
					if isinstance(tile, pygame.Rect):
						self.x = tile.right
				self.collisions["left"] = True
		self.rect.x = self.x

		self.y += self.movement[1]
		self.rect.y = self.y+7
		tile = self.tile_collision(tiles, premove_rect, directions=True)
		if tile and self.tile_collide:
			tile = tile.rect
			if self.movement[1] > 0:
				if collide:
					if isinstance(tile, AngleRect):
						ratio = tile.rect.height/tile.rect.width
						rel_x = (self.rect.x-tile.rect.x)*ratio

						if (rel_x <= 0 and tile.angle == 1) or (rel_x >= tile.rect.width-self.rect.width and tile.angle == 0) or (tile.angle in [2, 3] and self.rect.y < tile.rect.top):
							tile = tile.rect
						elif tile.angle == 0:
							new_y = tile.rect.y-rel_x+tile.rect.height-(self.rect.height*2)-6
							if self.y >= new_y:
								self.y = new_y
						elif tile.angle == 1:
							new_y = tile.rect.y+rel_x-self.rect.height-7
							if self.y >= new_y:
								self.y = new_y
					if isinstance(tile, pygame.Rect):
						self.y = tile.top-self.height+7
				self.collisions["bottom"] = True
			
			elif self.movement[1] < 0:
				if collide:
					if isinstance(tile, AngleRect):
						ratio = tile.rect.height/tile.rect.width
						rel_x = (self.rect.x-tile.rect.x)*ratio
						if (rel_x <= 0 and tile.angle == 2) or (rel_x > tile.rect.width-self.rect.width and tile.angle == 3) or (tile.angle in [0, 1] and self.rect.y >= tile.rect.bottom-3):
							tile = tile.rect
						elif tile.angle == 2:
							new_y = tile.rect.y-rel_x+tile.rect.height-7
							if self.y <= new_y:
								self.y = new_y
						elif tile.angle == 3:
							new_y = tile.rect.y+rel_x+self.rect.width-7
							if self.y <= new_y:
								self.y = new_y
					if isinstance(tile, pygame.Rect):
						self.y = tile.bottom-7
				self.collisions["top"] = True
		self.rect.y = self.y+7

	def change_anim(self, anim: str) -> None:
		if self.action != anim:
			self.animations[self.action].reset()
			self.action = anim

	def pause_anim(self) -> None:
		if self.img_type == str and not self.animations[self.action].paused:
			self.animations[self.action].pause()

	def unpause_anim(self) -> None:
		if self.img_type == str and self.animations[self.action].paused:
			self.animations[self.action].unpause()

	def entity_collision(self, entity, rect_only: bool=False) -> bool:
		if rect_only:
			return self.rect.colliderect(entity.rect)
		elif self.rect.colliderect(entity.rect):
			offset_x = entity.x - self.x
			offset_y = entity.y - self.y
			return self.mask.overlap(entity.mask, (offset_x, offset_y)) != None
		return False
