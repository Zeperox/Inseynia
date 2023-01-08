import pygame
if __name__ != "__main__":
	from scripts.loading.json_functions import load_json

unconnected_arabic_list = "أاإآوؤءدذرزة.-،:+'!؟0123456789٠١٢٣٤٥٦٧٨٩?)(/_=\[]*\"<>; \n", ".-،:+'!؟0123456789٠١٢٣٤٥٦٧٨٩?)(/_=\[]*\"<>; \n"
arabic_letters = "أبتثجحخدذرزسشصضطظعغفقكلمنهوياإآءؤىئة"
numbers = "0123456789٠١٢٣٤٥٦٧٨٩"

'''
Letters
ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz
أبتثجحخدذرزسشصضطظعغفقكلمنهوياإآءؤىئةأاإآأاإآ،؟٠١٢٣٤٥٦٧٨٩
あいうえおかきくけこがぎぐげごさしすせそざじずぜぞたちつてとだぢづでどなにぬねのはひふへほばびぶべぼぱぴぷぺぽまみむめもやゆよらりるれろわをんゃゅょっぃ
アイウエオカキクケコガギグゲゴサシスセソザジズゼゾタチツテトダヂヅデドナニヌネノハヒフヘホバビブベボパピプペポマミムメモヤユヨラリルレロワヲンャュョッィー。、・
АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя
.-,:+'!?0123456789()/_=\[]*"<>;�
'''

class Text:
	def __init__(self, font_path: str, text: str, size: int, color: list[int, int, int], language="english", alpha=255):
		color = list(color)
		self._font = self.font_name = font_path
		self._content = text
		self._size = size//1
		self._color = [1, 1, 1]
		self.spacing = 1
		self.language = language
		self._alpha = alpha
		
		if color[0] == 128:
			color[0] = 127
		elif color[0] == 255:
			color[0] = 254
		elif color[0] == 0:
			color[0] = 1

		self.font_cut = load_json([f"{self._font[:-4]}_cut.json"])
		self.font_img = pygame.image.load(self._font).convert()
		self.font_img.set_colorkey((255, 255, 255))
		
		self.space_width = self.font_cut["-"][1]-self.font_cut["-"][0]

		data = []
		x_offset = [0]
		y_offset = 0
		if language == "arabic":
			splitted_content = self._content.split("\n")
			for i, content in enumerate(splitted_content):
				if len(splitted_content) > 1 and i < len(splitted_content)-1:
					content = "\n"+content
				flipped_content = content[::-1]
				for i, char in enumerate(flipped_content):
					if char in numbers and flipped_content[i-1] not in numbers:
						numcont = ""
						for numchar in flipped_content[i:]:
							if numchar in numbers:
								numcont += numchar
							else:
								flipped_content = flipped_content.replace(numcont, numcont[::-1])
								break

				for i, char in enumerate(flipped_content):
					font_type = None
					i = len(content)-i-1
					try:
						if char in "اأإآ" and i > 0 and content[i-1] == "ل":
							if i != 1 and content[i-2] not in unconnected_arabic_list[0]:
								font_type = 5
							else:
								font_type = 4
						elif char == "ل" and i < len(content)-1 and content[i+1] in "اأإآ":
							continue

						elif i not in [len(content)-1, 0]:
							if content[i-1] in unconnected_arabic_list[0] and content[i+1] in unconnected_arabic_list[1]:
								font_type = ""
							elif content[i-1] in unconnected_arabic_list[0] and content[i+1] not in unconnected_arabic_list[1]:
								font_type = 1
							elif content[i-1] not in unconnected_arabic_list[0] and content[i+1] in unconnected_arabic_list[1]:
								font_type = 3
							
						else:
							if i-1 != -1:
								if content[i-1] in unconnected_arabic_list[0]:
									font_type = ""
								else:
									font_type = 3
							elif i-1 == -1:
								if content[i+1] in unconnected_arabic_list[1]:
									font_type = ""
								else:
									font_type = 1
					except:
						font_type = ""
					if font_type == None:
						font_type = 2
					if char not in arabic_letters:
						font_type = ""

					if f"{char}{font_type}" not in self.font_cut.keys() and char not in [" ", "\n"]:
						char = "�"

					if char == " ":
						x_offset[-1] += self.space_width+self.spacing
					elif char == "\n":
						x_offset.append(0)
						y_offset += 16+self.spacing
					else:
						data.append([f"{char}{font_type}", x_offset[-1], y_offset])
						x_offset[-1] += self.font_cut[f"{char}{font_type}"][1]-self.font_cut[f"{char}{font_type}"][0]
						if (i != 0 and content[i-1] in unconnected_arabic_list[0]) or (content[i] in unconnected_arabic_list[1]):
							x_offset[-1] += self.spacing
						if char in "اأإآ" and i > 0 and content[i-1] == "ل" and content[i-2] in unconnected_arabic_list[0]:
							x_offset[-1] += self.spacing
		else:
			for char in self._content:
				if char not in self.font_cut.keys() and char not in [" ", "\n"]:
					char = "�"

				if char == " ":
					x_offset[-1] += self.space_width+self.spacing
				elif char == "\n":
					x_offset.append(0)
					y_offset += 16+self.spacing
				else:
					data.append([char, x_offset[-1], y_offset])
					x_offset[-1] += self.font_cut[char][1]-self.font_cut[char][0]+self.spacing
		
		self.surfs = []
		for i, x_off in enumerate(x_offset):
			orig_surf = pygame.Surface((x_off, 16))
			for char in data:
				if i*17 == char[2]:
					orig_surf.blit(self.font_img, (char[1], 0), (self.font_cut[char[0]][0], 0, self.font_cut[char[0]][1]-self.font_cut[char[0]][0], 16))
				elif i*17 < char[2]:
					break

			crop_y = [0, 15]
			for i in range(2):
				for y in range(16):
					if i == 1:
						y = 15-y
					for x in range(x_off):
						if orig_surf.get_at((x, y)) != (0, 0, 0, 255):
							crop_y[i] = y
							break
						
					else:
						continue
					break

			orig_surf = orig_surf.subsurface(pygame.Rect(0, crop_y[0], x_off, crop_y[1]-crop_y[0]+1))

			self.surfs.append(orig_surf)
		
		h = 0
		for surf in self.surfs:
			h += surf.get_height()+self.space_width
		self.orig_surf = pygame.Surface((max(x_offset), h))

		y = 0
		for i, surf in enumerate(self.surfs):
			if language != "arabic":
				self.orig_surf.blit(surf, (0, y))
				y += surf.get_height()+self.space_width
			else:
				self.orig_surf.blit(surf, (self.orig_surf.get_width()-surf.get_width(), y))
				y += surf.get_height()+self.space_width
		self.orig_surf.set_colorkey((0, 0, 0))

		self.surf = pygame.transform.scale(self.orig_surf, (self.orig_surf.get_width()*self._size, self.orig_surf.get_height()*self._size))
		self.surf.set_alpha(self._alpha)
		self.color = color

	def _clip(self, surf: pygame.Surface, x: int, y: int, width: int, height: int):
		handle_surf = surf.copy()
		clip_rect = pygame.Rect(x, y, width, height)

		handle_surf.set_clip(clip_rect)
		img = surf.subsurface(handle_surf.get_clip())
		return img

	def render(self, surf: pygame.Surface, loc: tuple[int, int], scroll: list[int, int]=[0, 0]):
		surf.blit(self.surf, (loc[0]-scroll[0], loc[1]-scroll[1]))

	@property
	def width(self):
		return self.surf.get_width()
	
	@property
	def height(self):
		return self.surf.get_height()
	

	@property
	def content(self):
		return self._content

	@content.setter
	def content(self, new_text):
		if type(new_text) == tuple:
			self.language = new_text[1]
			new_text = new_text[0]

		self._content = new_text
		
		data = []
		x_offset = [0]
		y_offset = 0
		if self.language == "arabic":
			splitted_content = self._content.split("\n")
			for i, content in enumerate(splitted_content):
				if len(splitted_content) > 1 and i < len(splitted_content)-1:
					content = "\n"+content
				flipped_content = content[::-1]
				for i, char in enumerate(flipped_content):
					if char in numbers and flipped_content[i-1] not in numbers:
						numcont = ""
						for numchar in flipped_content[i:]:
							if numchar in numbers:
								numcont += numchar
							else:
								flipped_content = flipped_content.replace(numcont, numcont[::-1])
								break

				for i, char in enumerate(flipped_content):
					font_type = None
					i = len(content)-i-1
					try:
						if char in "اأإآ" and i > 0 and content[i-1] == "ل":
							if i != 1 and content[i-2] not in unconnected_arabic_list[0]:
								font_type = 5
							else:
								font_type = 4
						elif char == "ل" and i < len(content)-1 and content[i+1] in "اأإآ":
							continue

						elif i not in [len(content)-1, 0]:
							if content[i-1] in unconnected_arabic_list[0] and content[i+1] in unconnected_arabic_list[1]:
								font_type = ""
							elif content[i-1] in unconnected_arabic_list[0] and content[i+1] not in unconnected_arabic_list[1]:
								font_type = 1
							elif content[i-1] not in unconnected_arabic_list[0] and content[i+1] in unconnected_arabic_list[1]:
								font_type = 3
							
						else:
							if i-1 != -1:
								if content[i-1] in unconnected_arabic_list[0]:
									font_type = ""
								else:
									font_type = 3
							elif i-1 == -1:
								if content[i+1] in unconnected_arabic_list[1]:
									font_type = ""
								else:
									font_type = 1
					except:
						font_type = ""
					if font_type == None:
						font_type = 2
					if char not in arabic_letters:
						font_type = ""

					if f"{char}{font_type}" not in self.font_cut.keys() and char not in [" ", "\n"]:
						char = "�"

					if char == " ":
						x_offset[-1] += self.space_width+self.spacing
					elif char == "\n":
						x_offset.append(0)
						y_offset += 16+self.spacing
					else:
						data.append([f"{char}{font_type}", x_offset[-1], y_offset])
						x_offset[-1] += self.font_cut[f"{char}{font_type}"][1]-self.font_cut[f"{char}{font_type}"][0]
						if (i != 0 and content[i-1] in unconnected_arabic_list[0]) or (content[i] in unconnected_arabic_list[1]):
							x_offset[-1] += self.spacing
						if char in "اأإآ" and i > 0 and content[i-1] == "ل" and content[i-2] in unconnected_arabic_list[0]:
							x_offset[-1] += self.spacing
		else:
			for char in self._content:
				if char not in self.font_cut.keys() and char not in [" ", "\n"]:
					char = "�"

				if char == " ":
					x_offset[-1] += self.space_width+self.spacing
				elif char == "\n":
					x_offset.append(0)
					y_offset += 16+self.spacing
				else:
					data.append([char, x_offset[-1], y_offset])
					x_offset[-1] += self.font_cut[char][1]-self.font_cut[char][0]+self.spacing
		
		self.surfs = []
		for i, x_off in enumerate(x_offset):
			orig_surf = pygame.Surface((x_off, 16))
			for char in data:
				if i*17 == char[2]:
					orig_surf.blit(self.font_img, (char[1], 0), (self.font_cut[char[0]][0], 0, self.font_cut[char[0]][1]-self.font_cut[char[0]][0], 16))
				elif i*17 < char[2]:
					break

			crop_y = [0, 15]
			for i in range(2):
				for y in range(16):
					if i == 1:
						y = 15-y
					for x in range(x_off):
						if orig_surf.get_at((x, y)) != (0, 0, 0, 255):
							crop_y[i] = y
							break
						
					else:
						continue
					break

			orig_surf = orig_surf.subsurface(pygame.Rect(0, crop_y[0], x_off, crop_y[1]-crop_y[0]+1))

			self.surfs.append(orig_surf)
		
		h = 0
		for surf in self.surfs:
			h += surf.get_height()+self.space_width
		self.orig_surf = pygame.Surface((max(x_offset), h))
		
		y = 0
		for i, surf in enumerate(self.surfs):
			if self.language != "arabic":
				self.orig_surf.blit(surf, (0, y))
				y += surf.get_height()+self.space_width
			else:
				self.orig_surf.blit(surf, (self.orig_surf.get_width()-surf.get_width(), y))
				y += surf.get_height()+self.space_width
		self.orig_surf.set_colorkey((0, 0, 0))

		self.surf = pygame.transform.scale(self.orig_surf, (self.orig_surf.get_width()*self._size, self.orig_surf.get_height()*self._size))
		self.surf.set_alpha(self._alpha)

		c = self._color
		self._color = [1, 1, 1]
		self.color = c

	@property
	def size(self):
		return self._size

	@size.setter
	def size(self, new_size):
		self._size = new_size//1
		self.surf = pygame.transform.scale(self.orig_surf, (self.orig_surf.get_width()*self._size, self.orig_surf.get_height()*self._size))
		self.surf.set_alpha(self._alpha)

	@property
	def color(self):
		return self._color

	@color.setter
	def color(self, new_color):
		new_color = list(new_color)
		if new_color[0] == 128:
			new_color[0] = 127
		elif new_color[0] == 255:
			new_color[0] = 254
		elif new_color[0] == 0:
			new_color[0] = 1

		surf1 = pygame.Surface(self.surf.get_size())
		surf2 = pygame.Surface(self.surf.get_size())

		surf1.fill((self._color[0], self._color[1], abs(self._color[2]-1)))
		surf1.blit(self.surf, (0, 0))
		surf1.set_colorkey(self._color)

		surf2.fill(new_color)
		surf2.blit(surf1, (0, 0))
		surf2.set_colorkey((self._color[0], self._color[1], abs(self._color[2]-1)))
		self.surf = surf2
		self.surf.set_alpha(self._alpha)

		self._color = new_color

	@property
	def font(self):
		return self.font_name

	@font.setter
	def font(self, new_font):
		self.font_name = new_font
		self.font_cut = load_json([f"{self._font[:-4]}_cut.json"])
		self.font_img = pygame.image.load(self._font).convert()
		self.font_img.set_colorkey((255, 255, 255))
		
		self.space_width = self.font_cut["-"][1]-self.font_cut["-"][0]

		data = []
		x_offset = [0]
		y_offset = 0
		if self.language == "arabic":
			splitted_content = self._content.split("\n")
			for i, content in enumerate(splitted_content):
				if len(splitted_content) > 1 and i < len(splitted_content)-1:
					content = "\n"+content
				flipped_content = content[::-1]
				for i, char in enumerate(flipped_content):
					font_type = None
					i = len(content)-i-1
					try:
						if char in "اأإآ" and i > 0 and content[i-1] == "ل":
							if i != 1 and content[i-2] not in unconnected_arabic_list[0]:
								font_type = 5
							else:
								font_type = 4
						elif char == "ل" and i < len(content)-1 and content[i+1] in "اأإآ":
							continue

						elif i not in [len(content)-1, 0]:
							if content[i-1] in unconnected_arabic_list[0] and content[i+1] in unconnected_arabic_list[1]:
								font_type = ""
							elif content[i-1] in unconnected_arabic_list[0] and content[i+1] not in unconnected_arabic_list[1]:
								font_type = 1
							elif content[i-1] not in unconnected_arabic_list[0] and content[i+1] in unconnected_arabic_list[1]:
								font_type = 3
							
						else:
							if i-1 != -1:
								if content[i-1] in unconnected_arabic_list[0]:
									font_type = ""
								else:
									font_type = 3
							elif i-1 == -1:
								if content[i+1] in unconnected_arabic_list[1]:
									font_type = ""
								else:
									font_type = 1
					except:
						font_type = ""
					if font_type == None:
						font_type = 2
					if char not in arabic_letters:
						font_type = ""

					if f"{char}{font_type}" not in self.font_cut.keys() and char not in [" ", "\n"]:
						char = "�"

					if char == " ":
						x_offset[-1] += self.space_width+self.spacing
					elif char == "\n":
						x_offset.append(0)
						y_offset += 16+self.spacing
					else:
						data.append([f"{char}{font_type}", x_offset[-1], y_offset])
						x_offset[-1] += self.font_cut[f"{char}{font_type}"][1]-self.font_cut[f"{char}{font_type}"][0]
						if (i != 0 and content[i-1] in unconnected_arabic_list[0]) or (content[i] in unconnected_arabic_list[1]):
							x_offset[-1] += self.spacing
						if char in "اأإآ" and i > 0 and content[i-1] == "ل" and content[i-2] in unconnected_arabic_list[0]:
							x_offset[-1] += self.spacing
		else:
			for char in self._content:
				if char not in self.font_cut.keys() and char not in [" ", "\n"]:
					char = "�"

				if char == " ":
					x_offset[-1] += self.space_width+self.spacing
				elif char == "\n":
					x_offset.append(0)
					y_offset += 16+self.spacing
				else:
					data.append([char, x_offset[-1], y_offset])
					x_offset[-1] += self.font_cut[char][1]-self.font_cut[char][0]+self.spacing
		
		self.surfs = []
		for i, x_off in enumerate(x_offset):
			orig_surf = pygame.Surface((x_off, 16))
			for char in data:
				if i*17 == char[2]:
					orig_surf.blit(self.font_img, (char[1], 0), (self.font_cut[char[0]][0], 0, self.font_cut[char[0]][1]-self.font_cut[char[0]][0], 16))
				elif i*17 < char[2]:
					break

			crop_y = [0, 15]
			for i in range(2):
				for y in range(16):
					if i == 1:
						y = 15-y
					for x in range(x_off):
						if orig_surf.get_at((x, y)) != (0, 0, 0, 255):
							crop_y[i] = y
							break
						
					else:
						continue
					break

			orig_surf = orig_surf.subsurface(pygame.Rect(0, crop_y[0], x_off, crop_y[1]-crop_y[0]+1))

			self.surfs.append(orig_surf)
		
		h = 0
		for surf in self.surfs:
			h += surf.get_height()+self.space_width
		self.orig_surf = pygame.Surface((max(x_offset), h))
		
		y = 0
		for i, surf in enumerate(self.surfs):
			if self.language != "arabic":
				self.orig_surf.blit(surf, (0, y))
				y += surf.get_height()+self.space_width
			else:
				self.orig_surf.blit(surf, (self.orig_surf.get_width()-surf.get_width(), y))
				y += surf.get_height()+self.space_width
		self.orig_surf.set_colorkey((0, 0, 0))

		self.surf = pygame.transform.scale(self.orig_surf, (self.orig_surf.get_width()*self._size, self.orig_surf.get_height()*self._size))
		self.surf.set_alpha(self._alpha)
		c = self._color
		self._color = [1, 1, 1]
		self.color = c


	@property
	def alpha(self):
		return self._alpha

	@alpha.setter
	def alpha(self, new_alpha):
		self._alpha = new_alpha
		self.surf.set_alpha(self._alpha)

if __name__ == "__main__":
	win = pygame.display.set_mode((800, 600))

	font = Text("assets/fontsDL/font.png", "hello\nwo", 16, (0, 0, 0))
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
					font.font = ("assets/fontsDL/font.png", "assets/fontsDL/Font2.png")[font.font == "assets/fontsDL/font.png"]
				
				if event.key == pygame.K_s:
					font.content = ("hello\nwo", "hello\nworld")[font.content == "hello\nwo"]
				
				if event.key == pygame.K_d:
					font.size = (16, 25)[font.size == 16]
				
				if event.key == pygame.K_f:
					font.color = ((255, 255, 255), (0, 0, 0))[font.color == [254, 255, 255]]
				
		win.fill((128,128,128))
		font.render(win, (100, 100))

		pygame.display.flip()
