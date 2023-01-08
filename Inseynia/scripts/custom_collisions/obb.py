import pygame
from typing import Iterator


class OBB:
	def __init__(self, center, size, angle):
		self.center = pygame.Vector2(center)
		self.size = pygame.Vector2(size)
		self.angle = angle

		# utility vectors for calculating corner of bounding box
		self._tl = pygame.Vector2(-self.size.x / 2, self.size.y / 2)
		self._tr = pygame.Vector2(self.size.x / 2, self.size.y / 2)
		self._bl = pygame.Vector2(-self.size.x / 2, -self.size.y / 2)
		self._br = pygame.Vector2(self.size.x / 2, -self.size.y / 2)

	@classmethod
	def from_rect(cls, rect:pygame.Rect):
		center = pygame.Vector2(rect.center)
		size = pygame.Vector2(rect.size)
		return cls(center, size, 0)

	@property
	def orientation(self) -> pygame.Vector2:
		o = pygame.Vector2()
		o.from_polar((1, self.angle))
		return o

	@property
	def width(self) -> float:
		return self.size[0]

	@width.setter
	def width(self, w: float) -> None:
		self.size[0] = w

	@property
	def height(self) -> float:
		return self.size[1]

	@height.setter
	def height(self, h: float) -> None:
		self.size[1] = h

	@property
	def topleft(self) -> pygame.Vector2:
		return self.center + self._tl.rotate(self.angle)

	@property
	def topright(self) -> pygame.Vector2:
		return self.center + self._tr.rotate(self.angle)

	@property
	def bottomleft(self) -> pygame.Vector2:
		return self.center + self._bl.rotate(self.angle)

	@property
	def bottomright(self) -> pygame.Vector2:
		return self.center + self._br.rotate(self.angle)

	def corners(self) -> Iterator[pygame.Vector2]:
		return iter((self.topleft, self.topright,
					 self.bottomright, self.bottomleft))

	def collideobb(self, obb) -> bool:
		# Using SAT algorithm
		axes = iter((self.orientation, self.orientation.rotate(90),
					 obb.orientation, obb.orientation.rotate(90)))
		for ax in axes:
			min_along1, max_along1 = 1E10, -1E10
			min_along2, max_along2 = 1E10, -1E10
			for corner in self.corners():
				p = ax.dot(corner)
				if p > max_along1:
					max_along1 = p
				if p < min_along1:
					min_along1 = p
			for corner in obb.corners():
				p = ax.dot(corner)
				if p > max_along2:
					max_along2 = p
				if p < min_along2:
					min_along2 = p
			if min_along1 <= max_along2 and max_along1 >= min_along2:
				continue
			return False
		return True

	def colliderect(self, rect) -> bool:
		return self.collideobb(OBB.from_rect(rect))

	def draw_obb(self, display, color, scroll):
		pygame.draw.lines(display, color, True, [self.topleft-scroll, self.topright-scroll, self.bottomright-scroll, self.bottomleft-scroll])

if __name__ == "__main__":
	pygame.init()
	screen = pygame.display.set_mode((500, 500))
	clock = pygame.time.Clock()


	running = True
	sq1 = OBB([150, 250], [160, 160], 45)
	sq2 = OBB([350, 250], [160, 160], 45)
	sq1_rot_vel = 2
	sq2_rot_vel = 2
	col = pygame.Color("black")
	pause = False
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					pause = not pause

		if pause:
			continue

		sq1.angle += sq1_rot_vel
		sq2.angle += sq2_rot_vel
		collided = sq1.collideobb(sq2)
		if collided:
			col = pygame.Color("red")
		else:
			col = pygame.Color("black")

		screen.fill(pygame.Color("white"))
		sq1.draw_obb(screen, col, [0, 0])
		sq2.draw_obb(screen, col, [0, 0])
		pygame.display.flip()
		clock.tick(60)