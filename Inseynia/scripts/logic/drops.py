import pygame
from .entity import Entity

from scripts.loadingDL.sprites import sprite

class Drop(Entity):
	def __init__(self, x: int, y: int, img: pygame.Surface):
		super().__init__(x, y, img)
		self.rect.inflate_ip(40, 53)

class Spirit(Drop):
	def __init__(self, x: int, y: int, img: pygame.Surface):
		super().__init__(x, y, img)

		self.speed = 0
		self.spirit_taken = False

	def move(self, player: Entity, dt):
		if player.stats["EP"][player.classes.index("Mage")][0] < player.stats["EP"][player.classes.index("Mage")][1] and not self.spirit_taken:
			svec = pygame.Vector2(self.rect.center)
			pvec = pygame.Vector2(player.rect.center)
			self.speed += 0.1*dt
			
			vel = (pvec-svec).normalize()*self.speed

			self.x += vel.x; self.y += vel.y
			self.rect = pygame.Rect(self.x-20, self.y-20, self.img.get_width()+40, self.img.get_height()+40)

			if self.rect.colliderect(player.rect):
				self.spirit_taken = True
				self.img = sprite("Spirit Taken").copy()
				self.x, self.y = player.rect.centerx-self.width*0.5, player.rect.centery-self.height*0.5
				self.speed = 0
		elif player.stats["EP"][player.classes.index("Mage")][0] == player.stats["EP"][player.classes.index("Mage")][1] or self.spirit_taken:
			svec = pygame.Vector2(self.rect.center)
			pvec = pygame.Vector2(self.rect.centerx, self.rect.centery-1)
			self.speed += 0.05*dt

			vel = (pvec-svec).normalize()*self.speed

			self.x += vel.x; self.y += vel.y
			self.img.set_alpha(self.img.get_alpha()-10*dt)

			if self.img.get_alpha() <= 0:
				return True

class ProjDrop(Drop):
	def __init__(self, x: int, y: int, img: pygame.Surface, name: str, angle: int):
		img = pygame.transform.rotate(img, angle)
		super().__init__(x, y, img)
		self.name = name
		self.angle = angle