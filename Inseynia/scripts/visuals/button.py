import pygame

from .text import Text

class Button:
	def __init__(self, x: int, y: int, width: int, height: int, color: tuple[int, int, int]=(0, 0, 0), text: str="", text_lang:str = "english", text_color: tuple[int, int, int]=(255,255,255),
		outline: tuple[int, int, int]=None, outline_thickness: int=1, font_path: str=None, font_size: int=None, change_width: bool = True, text_align: str="center"
	):
		self.x = x
		self.y = y
		self.height = height
		self._color = color

		self.width = width
		self.width_init = width
		self.change_width = change_width

		self.surf = pygame.Surface((width+1, height+1), pygame.SRCALPHA)
		self._outline = outline
		self._outline_thickness = outline_thickness

		font_size = self.height*0.5//16*16 if not font_size else font_size
		if font_size == 0:
			font_size = 16
		if text:
			self.text = Text(font_path, text, font_size, text_color, text_lang)
		else:
			self.text = None
		self.text_align = text_align

		self.update_surf()
		
	def update_surf(self):
		if self.text:
			if self.change_width:
				if self.text.width > self.width_init:
					self.width = self.text.width
				else:
					self.width = self.width_init

		self.surf = pygame.Surface((self.width+1, self.height+1), pygame.SRCALPHA)
		if self._color:
			self.surf.fill(self._color)
		if self._outline:
			pygame.draw.rect(self.surf, self._outline, (0, 0, self.width, self.height), self._outline_thickness)

		if self.text:
			if self.text_align == "center":
				self.surf.blit(self.text.surf, (self.width*0.5 - self.text.width*0.5, self.height*0.5 - self.text.height*0.5))
			elif self.text_align == "left":
				self.surf.blit(self.text.surf, (5, self.height*0.5 - self.text.height*0.5))
			elif self.text_align == "right":
				self.surf.blit(self.text.surf, (self.width-self.text.width-5, self.height*0.5 - self.text.height*0.5))

		self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


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

	@property
	def text_content(self):
		return self.text.content

	@text_content.setter
	def text_content(self, text):
		self.text.content = text
		self.update_surf()

	@property
	def text_language(self):
		return self.text.language

	@text_language.setter
	def text_language(self, lang):
		self.text.language = lang
		self.update_surf()



if __name__ == "__main__":
	win = pygame.display.set_mode((800, 600))
	pygame.init()
	button = Button(200, 200, 400, 200, (0, 0, 0), "click me", (255,255,255), (255,255,255), 2, None, 32)
	while True:
		button.draw(win)
		mpos = pygame.mouse.get_pos()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit()

			if event.type == pygame.MOUSEMOTION:
				if button.rect.collidepoint(mpos):
					button.color = (255, 255, 255)
					button.text.color = (0, 0, 0)
				else:
					button.color = (0, 0, 0)
					button.text.color = (255, 255, 255)

			if event.type == pygame.MOUSEBUTTONDOWN:
				if button.rect.collidepoint(mpos):
					print("click")

		pygame.display.flip()
		