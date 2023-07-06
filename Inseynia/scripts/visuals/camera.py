import pygame

class Camera:
	def __init__(self, true_scroll, target, immediate=False):
		self.main_display = pygame.Surface((640, 360))
		self.display = self.main_display.copy()
		self.zoom = 0

		self.true_scroll = true_scroll
		self.scroll = pygame.Rect(true_scroll[0], true_scroll[1], 640, 360)
		self.target = target

		self.forced_loc = None
		self.ignore_map = False
		self.immediate = immediate

	def update(self, screen_size, dt, game_map):
		if not self.forced_loc and not self.ignore_map:
			if not self.immediate:
				if game_map.x == 0: self.true_scroll[0] += (self.target.x-self.true_scroll[0]-(screen_size[0]*0.5-self.target.rect.width*0.5))/20*dt
				else: self.true_scroll[0] += -self.true_scroll[0]/20*dt
				
				if game_map.y == 0: self.true_scroll[1] += (self.target.y-self.true_scroll[1]-(screen_size[1]*0.5-self.target.rect.height*0.5))/20*dt
				else: self.true_scroll[1] += -self.true_scroll[1]/20*dt
				
				self.scroll.x, self.scroll.y = self.true_scroll

				if self.scroll.x <= game_map.x and game_map.x == 0:
					self.scroll.x = game_map.x
				elif self.scroll.x >= game_map.data["size"][0]-screen_size[0] and game_map.x == 0:
					self.scroll.x = game_map.data["size"][0]-screen_size[0]
					
				if self.scroll.y <= game_map.y and game_map.y == 0:
					self.scroll.y = game_map.y
				elif self.scroll.y >= game_map.data["size"][1]-screen_size[1] and game_map.y == 0:
					self.scroll.y = game_map.data["size"][1]-screen_size[1]
			else:
				if game_map.x == 0: self.true_scroll[0] = self.target.x-((screen_size[0]*0.5)-(self.target.rect.width*0.5))
				else: self.true_scroll[0] = 0
				if game_map.y == 0: self.true_scroll[1] = self.target.y-((screen_size[1]*0.5)-(self.target.rect.height*0.5))
				else: self.true_scroll[1] = 0

				self.scroll.x, self.scroll.y = self.true_scroll
				if self.scroll.x <= game_map.x and game_map.x == 0:
					self.scroll.x = game_map.x
				elif self.scroll.x >= game_map.data["size"][0]-screen_size[0] and game_map.x == 0:
					self.scroll.x = game_map.data["size"][0]-screen_size[0]
					
				if self.scroll.y <= game_map.y and game_map.y == 0:
					self.scroll.y = game_map.y
				elif self.scroll.y >= game_map.data["size"][1]-screen_size[1] and game_map.y == 0:
					self.scroll.y = game_map.data["size"][1]-screen_size[1]
		elif self.forced_loc and not self.ignore_map:
			if not self.immediate:
				if game_map.x == 0: self.true_scroll[0] += (self.forced_loc[0]-self.true_scroll[0]-screen_size[0]*0.5)/20*dt
				else: self.true_scroll[0] += -self.true_scroll[0]/20*dt
				
				if game_map.y == 0: self.true_scroll[1] += (self.forced_loc[1]-self.true_scroll[1]-screen_size[1]*0.5)/20*dt
				else: self.true_scroll[1] += -self.true_scroll[1]/20*dt
				
				self.scroll.x, self.scroll.y = self.true_scroll

				if self.scroll.x <= game_map.x and game_map.x == 0:
					self.scroll.x = game_map.x
				elif self.scroll.x >= game_map.data["size"][0]-screen_size[0] and game_map.x == 0:
					self.scroll.x = game_map.data["size"][0]-screen_size[0]
					
				if self.scroll.y <= game_map.y and game_map.y == 0:
					self.scroll.y = game_map.y
				elif self.scroll.y >= game_map.data["size"][1]-screen_size[1] and game_map.y == 0:
					self.scroll.y = game_map.data["size"][1]-screen_size[1]
			else:
				if game_map.x == 0: self.true_scroll[0] = self.forced_loc[0]-((screen_size[0]*0.5))
				else: self.true_scroll[0] = 0
				if game_map.y == 0: self.true_scroll[1] = self.forced_loc[1]-((screen_size[1]*0.5))
				else: self.true_scroll[1] = 0

				self.scroll.x, self.scroll.y = self.true_scroll
				if self.scroll.x <= game_map.x and game_map.x == 0:
					self.scroll.x = game_map.x
				elif self.scroll.x >= game_map.data["size"][0]-screen_size[0] and game_map.x == 0:
					self.scroll.x = game_map.data["size"][0]-screen_size[0]
					
				if self.scroll.y <= game_map.y and game_map.y == 0:
					self.scroll.y = game_map.y
				elif self.scroll.y >= game_map.data["size"][1]-screen_size[1] and game_map.y == 0:
					self.scroll.y = game_map.data["size"][1]-screen_size[1]
		elif not self.forced_loc and self.ignore_map:
			if not self.immediate:
				self.true_scroll[0] += (self.target.x-self.true_scroll[0]-(screen_size[0]*0.5-self.target.rect.width*0.5))/20*dt
				self.true_scroll[1] += (self.target.y-self.true_scroll[1]-(screen_size[1]*0.5-self.target.rect.height*0.5))/20*dt
				self.scroll.x, self.scroll.y = self.true_scroll
			else:
				self.true_scroll = [self.target.x-((screen_size[0]*0.5)-(self.target.rect.width*0.5)), self.target.y-((screen_size[1]*0.5)-(self.target.rect.height*0.5))]
				self.scroll.x, self.scroll.y = self.true_scroll
		else:
			if not self.immediate:
				self.true_scroll[0] += (self.forced_loc[0]-self.true_scroll[0]-screen_size[0]*0.5)/20*dt
				self.true_scroll[1] += (self.forced_loc[1]-self.true_scroll[1]-screen_size[1]*0.5)/20*dt
				self.scroll.x, self.scroll.y = self.true_scroll
			else:
				self.true_scroll = [self.forced_loc[0]-screen_size[0]*0.5, self.forced_loc[1]-screen_size[1]*0.5]
				self.scroll.x, self.scroll.y = self.true_scroll

		if self.zoom != 0:
			self.display = pygame.transform.scale(self.main_display.subsurface(self.zoom, self.zoom, 640-self.zoom*2, 360-self.zoom*2), (640, 360))
			self.scrollxy = [self.scroll.x-self.zoom, self.scroll.y-self.zoom]
		else:
			self.display = self.main_display
