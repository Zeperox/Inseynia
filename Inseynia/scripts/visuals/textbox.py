import pygame, time
from pygame.locals import *

from .text import Text

class Textbox:
	def __init__(self, x, y, width, height, color=None, pre_text="", text_color=(255,255,255), text_pos="left",
		outline=None, outline_thickness=2, font_path: str=None, font_size: int=None, change_width: bool = True, clear_text_when_click=False, numeric=False, alpha=False, alnum=False
	):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self._color = color

		self.width = width
		self.width_init = width
		self.change_width = change_width

		font_size = self.height*0.5//7 if not font_size else font_size
		self.text = Text(font_path, pre_text, font_size, text_color)
		self.text_pos = text_pos

		self.clear_text_when_click = clear_text_when_click
		self.clicked = False

		self.numeric = numeric
		self.alpha = alpha
		self.alnum = alnum

		self.surf = pygame.Surface((width+1, height+1), SRCALPHA)
		self._outline = outline
		self._outline_thickness = outline_thickness

		self.selected = False
		self.blink_timer = time.time()

		self.update_surf()
		
	def draw(self, win: pygame.Surface, scroll: list[int, int]=[0, 0]):
		win.blit(self.surf, (self.x-scroll[0], self.y-scroll[1]))
		if self.selected:
			if self.text_pos == "left":
				text_x = self.x + 10
			elif self.text_pos == "center" or self.text_pos == "middle":
				text_x = self.x + (self.width*0.5 - self.text.width*0.5)
			elif self.text_pos == "right":
				text_x = (self.x+self.width)-(self.text.width-15)


			if time.time() - self.blink_timer >= 0.75:
				pygame.draw.line(win, (255,255,255), (text_x+self.text.width+5, self.y+15), (text_x+self.text.width+5, self.y+(self.height-15)))
			if time.time() - self.blink_timer >= 1:
				self.blink_timer = time.time()

	def update_surf(self):
		if self.change_width:
			if self.text.width > self.width_init:
				self.width = self.text.width
			else:
				self.width = self.width_init

		self.surf = pygame.Surface((self.width+1, self.height+1), SRCALPHA)
		if self._color:
			self.surf.fill(self._color)
		if self._outline:
			pygame.draw.rect(self.surf, self._outline, (0, 0, self.width, self.height), self._outline_thickness)

		if self.text_pos == "left":
			text_x = 10
		elif self.text_pos == "center" or self.text_pos == "middle":
			text_x = self.width*0.5 - self.text.width*0.5
		elif self.text_pos == "right":
			text_x = self.text.width-15
		self.text.render(self.surf, (text_x, self.height*0.5 - self.text.height*0.5))

		self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

	def is_over(self, pos):
		self.selected = self.rect.collidepoint(pos)

		if self.selected and self.clear_text_when_click and not self.clicked:
			self.text.content = ""
			self.clicked = True
			self.update_surf()

	def update_text(self, event):
		capslock = pygame.key.get_mods() & pygame.KMOD_CAPS
		shift = pygame.key.get_mods() & pygame.KMOD_SHIFT

		if self.selected:
			if event.type == KEYDOWN:
				key = pygame.key.name(event.key)
				if (capslock and not shift) or (not capslock and shift):
					key = key.capitalize()
				if event.key == K_BACKSPACE:
					self.text.content = self.text.content[:-1]
				else:
					if self.alnum or (self.numeric and self.alpha):
						if event.unicode.isalnum():
							self.text.content += key
					elif self.numeric:
						if event.unicode.isnumeric():
							if self.text.content == "0":
								self.text.content = ""
							self.text.content += key
					elif self.alpha:
						if event.unicode.isalpha():
							self.text.content += key
					else:
						self.text.content += key

				if self.text.content == "" and self.numeric:
					self.text.content = "0"
			
				self.update_surf()


	@property
	def color(self):
		return self._color

	@color.setter
	def color(self, color):
		self._color = color if color != "None" else None
		self.update_surf()

	@property
	def outline(self):
		return self._outline

	@outline.setter
	def outline(self, outline_color):
		self._outline = outline_color if outline_color != "None" else None
		self.update_surf()

if __name__ == "__main__":
	win = pygame.display.set_mode((800, 600))
	pygame.init()
	textbox = Textbox((0, 0, 0), 200, 200, 400, 200, "pre-text", (255,255,255), "center", True)
	
	while True:
		win.fill((0, 0, 0))
		textbox.draw(win, (255,255,255))
		mpos = pygame.mouse.get_pos()

		for event in pygame.event.get():
			if event.type == QUIT:
				quit()
			
			if event.type == KEYDOWN:
				textbox.update_text(event)

			if event.type == MOUSEBUTTONDOWN:
				textbox.is_over(mpos)

		pygame.display.flip()
		