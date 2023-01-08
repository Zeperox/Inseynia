import pygame

class Particles:
	def __init__(self):
		self.particles = []

	def emit(self, win, scroll):
		for particle in self.particles:
			particle[0][0] += particle[1][0]; particle[0][1] += particle[1][1]
			if particle[6] == "smaller":
				particle[4] -= particle[5]
			if type(particle[2]) == str:
				if not particle[7]:
					pygame.draw.circle(win, particle[3], (particle[0][0]-scroll[0], particle[0][1]-scroll[1]), particle[4])
				else:
					pygame.draw.circle(win, particle[3], (particle[0][0], particle[0][1]), particle[4])
			else:
				if not particle[7]:
					win.blit(particle[2], (particle[0][0]-scroll[0], particle[0][1]-scroll[1]))
				else:
					win.blit(particle[2], (particle[0][0], particle[0][1]))

			self.remove(particle)

	def add(self, loc, dir, type="circle", color=(0, 0, 0), size=0, size_sub_speed = 0.2, remove="offscreen", angle=0, ignore_scroll=False):
		self.particles.append([loc, dir, type, color, size, size_sub_speed, remove, ignore_scroll])

	def remove(self, particle, screen_size, scroll):
		if particle[6] == "offscreen":
			if not particle[7]:
				if particle[0][0]-scroll[0] < 0 or particle[0][0]-scroll[0] > screen_size[0] or particle[0][1]-scroll[1] < 0 or particle[0][1]-scroll[1] > screen_size[1]:
					self.particles.remove(particle)
			else:
				if particle[0][0] < 0 or particle[0][0] > screen_size[0] or particle[0][1] < 0 or particle[0][1] > screen_size[1]:
					self.particles.remove(particle)
		elif particle[6] == "smaller":
			if particle[4] < 0:
				self.particles.remove(particle)
