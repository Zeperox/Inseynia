import pygame, os, math, time
from scripts.custom_collisions.angle import AngleRect
from scripts.loading.json_functions import load_json

def _clip(surf: pygame.Surface, x: int, y: int, width: int, height: int):
	handle_surf = surf.copy()
	clip_rect = pygame.Rect(x, y, width, height)

	handle_surf.set_clip(clip_rect)
	img = surf.subsurface(handle_surf.get_clip())
	return img

class Entity:
	def __init__(self, x: int, y: int, animation_dirs: str | pygame.Surface, animation_action: str = "idle"):
		self.x = x
		self.y = y
		self.collisions = {"top": False, "bottom": False, "left": False, "right": False}
		
		self.img_type = type(animation_dirs)
		if type(animation_dirs) == str:
			timing_data = load_json([animation_dirs, "timing.json"])

			self.animations = {}
			self.action = animation_action
			for img in os.listdir(animation_dirs):
				if not img.endswith(".png"):
					continue

				frames = []
				_img = pygame.image.load(os.path.join(animation_dirs, img))
				cur_width = 0
				img_count = 0
				for x in range(_img.get_width()):
					if _img.get_at((x, 0)) == (0, 0, 0, 128):
						frames.append([_clip(_img, x-cur_width, 0, cur_width, _img.get_height()), timing_data[img[:-4]][img_count]])
						cur_width = 0
						img_count += 1
					else:
						cur_width += 1
				self.animations[img[:-4]] = frames

			self.frame = 0
			self.frame_time = 0
			self.paused_time = 0
			self.paused = False
			
		else:
			self.orig_img = animation_dirs.copy()
			self.img = animation_dirs.copy()

		self.flip = False

		self.movement = [0, 0]
		self.vel = pygame.Vector2()
		self.friction = 0.3
		self.acceleration = 0.5
		self.disable_friction = False

		self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
		self.rect = self.rect.inflate(0, -14)
		if self.img_type == str:
			self.mask = pygame.mask.from_surface(self.animations[self.action][0][0])
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
	def width(self):
		if self.img_type == str:
			return self.animations[self.action][self.frame][0].get_width()
		else:
			return self.img.get_width()

	@property
	def height(self):
		if self.img_type == str:
			return self.animations[self.action][self.frame][0].get_height()
		else:
			return self.img.get_height()

	def draw(self, win: pygame.Surface, scroll: list[int, int]):
		if self.active and self.draw_img:
			if self.img_type == str:
				if self.frame_time == 0:
					self.frame_time = time.time()
					
				win.blit(pygame.transform.flip(self.animations[self.action][self.frame][0], self.flip, False), (self.x-scroll[0], self.y-scroll[1]))
				if time.time()-self.frame_time >= self.animations[self.action][self.frame][1] and not self.paused:
					self.frame = self.frame + 1 if self.frame < len(self.animations[self.action])-1 else 0
					self.frame_time = time.time()
			else:
				win.blit(pygame.transform.flip(self.img, self.flip, False), (self.x-scroll[0], self.y-scroll[1]))
   
	def tile_collision(self, tiles: list[pygame.Rect]):
		tile_pos = [math.floor(self.rect.centerx / 32), math.floor(self.rect.centery / 32)]
		collidable_tiles = [tiles[tile_pos[1] + y][tile_pos[0] + x] for x in range(3) for y in range(3)]

		for orig_tile in collidable_tiles:
			if orig_tile == None:
				continue

			try:
				orig_tile.center
				tile = orig_tile
			except:
				tile = orig_tile.rect
			if self.rect.colliderect(tile):
				return orig_tile

	def movement_collision(self, tiles: list[pygame.Rect], collide=True, move_angle=True):
		self.collisions = {"top": False, "bottom": False, "left": False, "right": False}

		# tiles
		self.x += self.movement[0]
		self.rect.x = self.x
		tile = self.tile_collision(tiles)
		if tile and self.tile_collide:
			if self.movement[0] > 0:
				if collide:
					if type(tile) == AngleRect:
						ratio = tile.rect.width/tile.rect.height
						rel_y = (self.rect.y-tile.rect.y)*ratio
						if rel_y < -self.rect.height or rel_y > tile.rect.height:
							tile = tile.rect
						else:
							if tile.angle in [1, 2]:
								if self.rect.x <= tile.rect.left+1:
									tile = tile.rect
							elif tile.angle == 0:
								new_x = tile.rect.x-rel_y+tile.rect.width-(self.rect.width*2)
								if self.x >= new_x:
									self.x = new_x
							elif tile.angle == 3:
								new_x = tile.rect.x+rel_y-self.rect.width
								if self.x >= new_x:
									self.x = new_x
					if type(tile) == pygame.Rect:
						self.x = tile.left-self.width
				self.collisions["right"] = True

			elif self.movement[0] < 0:
				if collide:
					if type(tile) == AngleRect:
						ratio = tile.rect.width/tile.rect.height
						rel_y = (self.rect.y-tile.rect.y)*ratio
						if rel_y < -self.rect.height or rel_y > tile.rect.height:
							tile = tile.rect
						else:
							if tile.angle in [0, 3]:
								if self.rect.x >= tile.rect.right-1:
									tile = tile.rect
							elif tile.angle == 1:
								new_x = tile.rect.x+rel_y+self.rect.height
								if self.x <= new_x:
									self.x = new_x
							elif tile.angle == 2:
								new_x = tile.rect.x-rel_y+tile.rect.width
								if self.x <= new_x:
									self.x = new_x
					if type(tile) == pygame.Rect:
						self.x = tile.right
				self.collisions["left"] = True
		self.rect.x = self.x

		self.y += self.movement[1]
		self.rect.y = self.y+7
		tile = self.tile_collision(tiles)
		if tile and self.tile_collide:
			if self.movement[1] > 0:
				if collide:
					if type(tile) == AngleRect:
						ratio = tile.rect.height/tile.rect.width
						rel_x = (self.rect.x-tile.rect.x)*ratio
						if rel_x < -self.rect.width or rel_x > tile.rect.width:
							tile = tile.rect
						else:
							if tile.angle in [2, 3]:
								if self.rect.y <= tile.rect.top+1:
									tile = tile.rect
							elif tile.angle == 0:
								new_y = tile.rect.y-rel_x+tile.rect.height-(self.rect.height*2)-7
								if self.y >= new_y:
									self.y = new_y
							elif tile.angle == 1:
								new_y = tile.rect.y+rel_x-self.rect.height-7
								if self.y >= new_y:
									self.y = new_y
					if type(tile) == pygame.Rect:
						self.y = tile.top-self.height+7
				self.collisions["bottom"] = True
			
			elif self.movement[1] < 0:
				if collide:
					if type(tile) == AngleRect:
						ratio = tile.rect.height/tile.rect.width
						rel_x = (self.rect.x-tile.rect.x)*ratio
						if rel_x < -self.rect.width or rel_x > tile.rect.width:
							tile = tile.rect
						else:
							if tile.angle in [0, 1]:
								if self.rect.y >= tile.rect.bottom-1:
									tile = tile.rect
							elif tile.angle == 2:
								new_y = tile.rect.y-rel_x+tile.rect.height-7
								if self.y <= new_y:
									self.y = new_y
							elif tile.angle == 3:
								new_y = tile.rect.y+rel_x+self.rect.width-7
								if self.y <= new_y:
									self.y = new_y
					if type(tile) == pygame.Rect:
						self.y = tile.bottom-7
				self.collisions["top"] = True
		self.rect.y = self.y+7

	def change_anim(self, anim):
		if self.action != anim:
			self.action = anim
			self.frame = 0
			self.frame_time = 0

	def pause_anim(self):
		if not self.paused:
			self.paused_time = self.frame_time
		self.paused = True

	def unpause_anim(self):
		if self.paused:
			self.frame_time = time.time()-(time.time()-self.paused_time)
		self.paused = False

	def entity_collision(self, entity, rect_only=False):
		if rect_only:
			return self.rect.colliderect(entity.rect)

		if self.rect.colliderect(entity.rect):
			offset_x = entity.x - self.x
			offset_y = entity.y - self.y
			return self.mask.overlap(entity.mask, (offset_x, offset_y)) != None
		return False