import pygame
from pygame._sdl2 import video

class Renderer:
	def __init__(self):
		self.win = video.Window.from_display_module()
		self.main_renderer = video.Renderer.from_window(self.win)

	def blit(self, texture: video.Texture | pygame.Surface, loc: tuple[int, int], flipx: bool=None, flipy: bool=None, angle: int=0):
		if type(texture) == pygame.Surface:
			texture = self.convert_to_texture(texture)
		texture.draw(None, loc, angle, None, flipx, flipy)
	
	def convert_to_texture(self, img: str | pygame.Surface, scale: tuple[int, int]=None, flipx: bool=False, flipy: bool=False, convert: bool=False, convert_alpha: bool=False):
		if type(img) == str:
			img = pygame.image.load(img)
			if convert:
				img = img.convert()
			elif convert_alpha:
				img = img.convert_alpha()
		if scale:
			img = pygame.transform.scale(img, scale)
		if flipx or flipy:
			img = pygame.transform.flip(img, flipx, flipy)
		return video.Texture.from_surface(self.main_renderer, img)

	def surface(self, size: tuple[int, int], convert: bool=False):
		surf = pygame.Surface(size)
		if convert:
			surf = self.convert_to_texture(surf)
		return surf

	def fill(self, color: tuple[int, int, int]):
		color = list(color)
		if len(color) == 3:
			color.append(255)
		self.main_renderer.draw_color = color
		self.main_renderer.fill_rect(pygame.Rect(0, 0, 640, 360))

	def clear(self):
		self.main_renderer.clear()

	def update(self):
		self.main_renderer.present()

	def draw_circle(self, color, size, loc, width=0):
		if size <= 0.5:
			size = 0.5
		surf = pygame.Surface((size*2, size*2))
		surf.set_colorkey((0, 0, 0))
		pygame.draw.circle(surf, color, (size*0.5, size*0.5), size, width)
		self.blit(surf, (loc[0]-size*0.5, loc[1]-size*0.5))

	def draw_poly(self, color, points, width=0):
		points0 = [point[0] for point in points]
		points1 = [point[1] for point in points]
		surf = pygame.Surface((max(points0)-min(points0)+1, max(points1)-min(points1)+1))
		surf.set_colorkey((0, 0, 0))
		pygame.draw.polygon(surf, color, [(point[0]-min(points0), point[1]-min(points1)) for point in points], width)
		self.blit(surf, (min(points0), min(points1)))

	def draw_rect(self, color, rect, width=0):
		color = list(color)
		if len(color) == 3:
			color.append(255)
		self.main_renderer.draw_color = color
		if width:
			for w in range(width):
				self.main_renderer.draw_rect(pygame.Rect(rect[0]+w, rect[1]+w, rect[2]-w*2, rect[3]-w*2))
		else:
			self.main_renderer.fill_rect(pygame.Rect(rect[0], rect[1], rect[2], rect[3]))
