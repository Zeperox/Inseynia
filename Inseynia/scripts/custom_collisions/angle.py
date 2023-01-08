import pygame

class AngleRect():
	def __init__(self, x, y, w, h, angle):
		self.rect = pygame.Rect(x, y, w, h)
		self.angle = angle

	def colliderect(self, rect):
		return self.rect.colliderect(rect)
