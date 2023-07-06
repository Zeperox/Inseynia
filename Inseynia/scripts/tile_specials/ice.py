import pygame

from scripts.loadingDL.files import files

_Tile = files["tiles"].Tile

class Tile(_Tile):
	def __init__(self, x, y, tile_img, collision, main_map):
		super().__init__(x, y, tile_img, collision, main_map)
		self.frictions = {}

	def special(self, entity):
		if entity.rect.colliderect(self.main_rect):
			self.frictions[entity] = entity.friction
			entity.friction = 0.05
		elif entity in self.frictions:
			entity.friction = self.frictions[entity]
			del self.frictions[entity]