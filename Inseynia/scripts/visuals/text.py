import pygame
from typing import Optional

from scripts.loadingDL.json_functions import load_json
from scripts.loadingDL.sprites import sprite

languages = load_json(["scripts", "dataDL", "langs.json"])

pygame.font.init()

class Text:
	def __init__(self, font: str, content: str, size: int, color: tuple[int, int, int], lang: Optional[str] = "english", bg_color: Optional[tuple[int, int, int]] = None, max_width: Optional[int] = 0, alpha: Optional[int] = 255, align=0, **kwargs):
		self.font_name = font
		self._orig_content = content
		self._content = content
		self._size = int(size)
		self._color = color
		self._bg_color = bg_color
		self._language = lang
		self.script = languages[lang]
		self._alpha = alpha
		self._max_width = abs(max_width)
		self._align = align

		self._font = pygame.Font(self.font_name, self._size)
		self._font.set_script(self.script)
		self._font.align = align
		if self.script == "Arab":
			self._font.set_direction(pygame.DIRECTION_RTL)

			nums = []
			for i_char, char in enumerate(self._content):
				if char.isnumeric():
					if i_char != 0 and self._content[i_char-1].isnumeric():
						nums[-1][0] += char
					else:
						nums.append([char, i_char])
				else:
					if i_char != 0 and self._content[i_char-1].isnumeric():
						nums[-1].append(i_char)
			
			for num in nums:
				if len(num) == 3:
					self._content = self._content[:num[1]]+num[0][::-1]+self._content[num[2]:]
				else:
					self._content = self._content[:num[1]]+num[0][::-1]

		if "bold" in kwargs.keys() and kwargs["bold"]:
			self._font.bold = True
		if "italic" in kwargs.keys() and kwargs["italic"]:
			self._font.italic = True
		if "underline" in kwargs.keys() and kwargs["underline"]:
			self._font.underline = True
		if "strikethrough" in kwargs.keys() and kwargs["strikethrough"]:
			self._font.strikethrough = True

		self._update_surf()

	def _update_surf(self):
		self._content = self._orig_content
		surfs = []
		if self._content.count("<sp:") > 0:
			for _ in range(self._content.count("<sp:")):
				i_start = self._content.index("<sp:")
				i_end = self._content.index(">", i_start)
				img = sprite(self._content[i_start+4:i_end])

				self._content = self._content.replace(self._content[i_start:i_end+1], " "*(img.get_width()//8), 1)
				c = self._content[:i_start]+" "

				surf = self._font.render(c, False, (255, 255, 255), None, abs(self._max_width))

				y = surf.get_height()-18
				if "\n" in c:
					c = c[c.rindex("\n"):].replace("\n", "")
				x = self._font.size(c[:-1])[0]
				surfs.append([img, x, y])

			surfs.append([self._font.render(self._content, False, self._color, self._bg_color, abs(self._max_width)), 0, 0])
			self.surf = pygame.Surface((max([surf[1]+surf[0].get_width() for surf in surfs]), surfs[-1][2]+surfs[-1][0].get_height()+2))

			blits = [(surf[0], (surf[1], surf[2])) for surf in surfs]
			self.surf.fblits(blits)
			self.surf.set_colorkey((0, 0, 0))
		else:
			self.surf = self._font.render(self._content, False, self._color, self._bg_color, abs(self._max_width))

		self.surf.set_alpha(self._alpha)

	
	@property
	def width(self):
		return self.surf.get_width()
	
	@property
	def height(self):
		return self.surf.get_height()
	

	@property
	def font(self):
		return self.font_name
	
	@font.setter
	def font(self, font):
		self.font_name = font
		self._font = pygame.Font(self.font_name, self._size)
		self._font.set_script(self.script)
		if self.script == "Arab":
			self._font.set_direction(pygame.DIRECTION_RTL)

		self._update_surf()

	@property
	def content(self):
		return self._orig_content
	
	@content.setter
	def content(self, content):
		self._orig_content = content
		self._content = content
		if self.script == "Arab":
			nums = []
			for i_char, char in enumerate(self._content):
				if char.isnumeric():
					if i_char != 0 and self._content[i_char-1].isnumeric():
						nums[-1][0] += char
					else:
						nums.append([char, i_char])
				else:
					if i_char != 0 and self._content[i_char-1].isnumeric():
						nums[-1].append(i_char)
			
			for num in nums:
				if len(num) == 3:
					self._content = self._content[:num[1]]+num[0][::-1]+self._content[num[2]:]
				else:
					self._content = self._content[:num[1]]+num[0][::-1]

		self._update_surf()

	@property
	def size(self):
		return self._size
	
	@size.setter
	def size(self, size):
		self._size = int(size)
		self._font = pygame.Font(self.font_name, self._size)
		self._font.set_script(self.script)
		if self.script == "Arab":
			self._font.set_direction(pygame.DIRECTION_RTL)

		self._update_surf()

	@property
	def color(self):
		return self._color
	
	@color.setter
	def color(self, color):
		self._color = color
		self._update_surf()

	@property
	def bg_color(self):
		return self._bg_color
	
	@bg_color.setter
	def bg_color(self, bg_color):
		self._bg_color = bg_color
		self._update_surf()

	@property
	def max_width(self):
		return self._max_width
	
	@max_width.setter
	def max_width(self, max_width):
		self._max_width = abs(max_width)
		self._update_surf()
	
	@property
	def language(self):
		return self._language
	
	@language.setter
	def language(self, language):
		self._language = language
		if self.script == "Arab":
			nums = []
			for i_char, char in enumerate(self._content):
				if char.isnumeric():
					if i_char != 0 and self._content[i_char-1].isnumeric():
						nums[-1][0] += char
					else:
						nums.append([char, i_char])
				else:
					if i_char != 0 and self._content[i_char-1].isnumeric():
						nums[-1].append(i_char)
			
			for num in nums:
				if len(num) == 3:
					self._content = self._content[:num[1]]+num[0][::-1]+self._content[num[2]:]
				else:
					self._content = self._content[:num[1]]+num[0][::-1]
		self.script = languages[self._language]
		self._font.set_script(self.script)
		if self.script == "Arab":
			self._font.set_direction(pygame.DIRECTION_RTL)
			nums = []
			for i_char, char in enumerate(self._content):
				if char.isnumeric():
					if i_char != 0 and self._content[i_char-1].isnumeric():
						nums[-1][0] += char
					else:
						nums.append([char, i_char])
				else:
					if i_char != 0 and self._content[i_char-1].isnumeric():
						nums[-1].append(i_char)
			
			for num in nums:
				if len(num) == 3:
					self._content = self._content[:num[1]]+num[0][::-1]+self._content[num[2]:]
				else:
					self._content = self._content[:num[1]]+num[0][::-1]
		else:
			self._font.set_direction(pygame.DIRECTION_LTR)

		self._update_surf()

	@property
	def alpha(self):
		return self._alpha
	
	@alpha.setter
	def alpha(self, alpha):
		self._alpha = alpha
		self.surf.set_alpha(self._alpha)

	@property
	def align(self):
		return self._align
	
	@align.setter
	def align(self, align):
		self._align = align
		self._font.align = align
		self._update_surf()
	


if __name__ == "__main__":
	win = pygame.display.set_mode((800, 600))

	font = Text("assets/fontsDL/font.ttf", "hello\nwo", 48, (0,0,0), lang="english", align=pygame.FONT_RIGHT, max_width=300)
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					print(font.font)
				
				if event.key == pygame.K_w:
					print(font.content)
				
				if event.key == pygame.K_e:
					print(font.size)
				
				if event.key == pygame.K_r:
					print(font.color)
				
				if event.key == pygame.K_a:
					font.language = ("english", "arabic")[font.language == "english"]
					font.content = ("hello\nwo", "بحث عن البقرة")[font.language == "arabic"]
				
				if event.key == pygame.K_s:
					font.content = ("hello\nwo", "hello\nworld")[font.content == "hello\nwo"]
				
				if event.key == pygame.K_d:
					font.size = (16, 25)[font.size == 16]
				
				if event.key == pygame.K_f:
					font.color = ((255, 255, 255), (0, 0, 0))[font.color == (255, 255, 255)]
				
		win.fill((255,255,255))
		win.blit(font.surf, (100, 100))

		pygame.display.flip()
