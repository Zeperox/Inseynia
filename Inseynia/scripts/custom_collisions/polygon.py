import pygame
from pygame.constants import QUIT

class Polygon:
	def __init__(self, vertices):
		self.vertices = vertices

	def collidepoint(self, point):
		collide = False

		next = 0
		for current in range(len(self.vertices)):
			next = current+1
			if next == len(self.vertices): next = 0

			vc = self.vertices[current]
			vn = self.vertices[next]
			
			if (((vc[1] >= point[1] and vn[1] < point[1]) or (vc[1] < point[1] and vn[1] >= point[1])) and (point[0] < (vn[0]-vc[0])*(point[1]-vc[1]) / (vn[1]-vc[1])+vc[0])):
				collide = not collide

		return collide

	def colliderect(self, rect):
		def colliderect_line(line, rect: pygame.Rect):
			def collideline_line(line1: list[list[int, int], list[int, int]], line2: list[list[int, int], list[int, int]]):
				uA = ((line2[1][0]-line2[0][0])*(line1[0][1]-line2[0][1]) - (line2[1][1]-line2[0][1])*(line1[0][0]-line2[0][0])) / (((line2[1][1]-line2[0][1])*(line1[1][0]-line1[0][0]) - (line2[1][0]-line2[0][0])*(line1[1][1]-line1[0][1]))+1)
				uB = ((line1[1][0]-line1[0][0])*(line1[0][1]-line2[0][1]) - (line1[1][1]-line1[0][1])*(line1[0][0]-line2[0][0])) / (((line2[1][1]-line2[0][1])*(line1[1][0]-line1[0][0]) - (line2[1][0]-line2[0][0])*(line1[1][1]-line1[0][1]))+1)
				return uA >= 0 and uA <= 1 and uB >= 0 and uB <= 1
			
			l = collideline_line(line, (rect.topleft, rect.bottomleft))
			r = collideline_line(line, (rect.topright, rect.bottomright))
			t = collideline_line(line, (rect.topleft, rect.topright))
			b = collideline_line(line, (rect.bottomleft, rect.bottomright))
			return l or r or t or b

		next = 0
		for current in range(len(self.vertices)):
			next = current+1
			if next == len(self.vertices): next = 0

			vc = self.vertices[current]
			vn = self.vertices[next]

			if colliderect_line((vc, vn), rect): return True
		return self.collidepoint((rect.x, rect.y))

	def draw_poly(self, win, color, scroll=[0, 0]):
		points = []
		for v in self.vertices:
			points.append((v[0]-scroll[0], v[1]-scroll[1]))

		pygame.draw.polygon(win, color, points, 1)

if __name__ == "__main__":
	c = (0, 0, 0)
	poly = Polygon([(100, 100), (300, 100), (150, 300)])
	rect = pygame.Rect(20, 20, 20, 20)
	win = pygame.display.set_mode((500, 500))
	while True:
		win.fill((255,255,255))
		poly.draw_poly(win, c)
		pygame.draw.rect(win, (255,0,0), rect)

		for event in pygame.event.get():
			if event.type == QUIT: quit()

		rect.center = pygame.mouse.get_pos()

		if poly.colliderect(rect):
			c = (255, 0, 0)
		else:
			c = (0, 0, 0)
		pygame.display.update()
