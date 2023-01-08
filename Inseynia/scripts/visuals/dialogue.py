import pygame, os, time
from .text import Text
from scripts.loading.json_functions import load_json

texts = load_json(["scripts", "data", "text.json"])
text_ids = list(texts.keys())
text_str = list(texts.values())

class Dialogue:
	def __init__(self, id):
		self.id = id
		self.triggered = False

		for text_id in text_ids:
			if text_id.startswith(id):
				i1 = text_ids.index(text_id)
				break
		text_ids.reverse()
		for text_id in text_ids:
			if text_id.startswith(id):
				i2 = -text_ids.index(text_id)
				break
		text_ids.reverse()

		if i2:
			_texts_str = text_str[i1:i2]
		else:
			_texts_str = text_str[i1:]

		self.texts = {lang: [] for lang in load_json(["scripts", "data", "langs.json"])}
		for text in _texts_str:
			for lang_i, lang in enumerate(self.texts.keys()):
				try:
					self.texts[lang].append([Text(os.path.join("assets", "fontsDL", "font.png"), list(text.keys())[lang_i], 3, (255, 255, 255), lang), Text(os.path.join("assets", "fontsDL", "font.png"), "", 2, (255, 255, 255), lang), list(text.values())[lang_i]])
				except:
					self.texts[lang].append([Text(os.path.join("assets", "fontsDL", "font.png"), list(text.keys())[0], 3, (255, 255, 255), lang), Text(os.path.join("assets", "fontsDL", "font.png"), "", 2, (255, 255, 255), "english"), list(text.values())[0]])
		self.text_index = 0
		self.text_portion = 0
		self.text_portion_time = 0

		self.surf = pygame.Surface((600, 100))
		self.surf.fill((255, 255, 255))
		self.surf.fill((0, 0, 0), (2, 2, self.surf.get_width()-4, self.surf.get_height()-4))
		pygame.draw.line(self.surf, (255, 255, 255), (100, 0), (100, 100), 2)

	def render(self, win, lang="english"):
		win.blit(self.surf, (640*0.5-300, 250))
		if lang != "arabic":
			self.texts[lang][self.text_index][0].render(win, (640*0.5-195, 255))
			self.texts[lang][self.text_index][1].render(win, (640*0.5-195, 255+self.texts[lang][self.text_index][0].height))
			
			if self.text_portion >= len(self.texts[lang][self.text_index][2]):
				pygame.draw.polygon(win, (255, 255, 255), (
					((640*0.5-190)+(self.texts[lang][self.text_index][1].surfs[-1].get_width())*2, 255+(self.texts[lang][self.text_index][0].height+self.texts[lang][self.text_index][1].height-self.texts[lang][self.text_index][1].surfs[-1].get_height())-self.texts[lang][self.text_index][1].surfs[-1].get_height()*2),
					((640*0.5-190)+(self.texts[lang][self.text_index][1].surfs[-1].get_width()+self.texts[lang][self.text_index][1].surfs[-1].get_height())*2, 255+(self.texts[lang][self.text_index][0].height+self.texts[lang][self.text_index][1].height-self.texts[lang][self.text_index][1].surfs[-1].get_height()*0.5)-self.texts[lang][self.text_index][1].surfs[-1].get_height()*1.5),
					((640*0.5-190)+(self.texts[lang][self.text_index][1].surfs[-1].get_width())*2, 255+(self.texts[lang][self.text_index][0].height+self.texts[lang][self.text_index][1].height)-self.texts[lang][self.text_index][1].surfs[-1].get_height())))
		else:
			self.texts[lang][self.text_index][0].render(win, (640*0.5+295-self.texts[lang][self.text_index][0].width, 255))
			self.texts[lang][self.text_index][1].render(win, (640*0.5+295-self.texts[lang][self.text_index][1].width, 255+self.texts[lang][self.text_index][0].height))

			if self.text_portion >= len(self.texts[lang][self.text_index][2]):
				pygame.draw.polygon(win, (255, 255, 255), (
					((640*0.5+290-self.texts[lang][self.text_index][1].width), 255+(self.texts[lang][self.text_index][0].height+self.texts[lang][self.text_index][1].height-self.texts[lang][self.text_index][1].surfs[-1].get_height())-self.texts[lang][self.text_index][1].surfs[-1].get_height()*2),
					((640*0.5+290-self.texts[lang][self.text_index][1].width)-(self.texts[lang][self.text_index][1].surfs[-1].get_height())*2, 255+(self.texts[lang][self.text_index][0].height+self.texts[lang][self.text_index][1].height-self.texts[lang][self.text_index][1].surfs[-1].get_height()*0.5)-self.texts[lang][self.text_index][1].surfs[-1].get_height()*1.5),
					((640*0.5+290-self.texts[lang][self.text_index][1].width), 255+(self.texts[lang][self.text_index][0].height+self.texts[lang][self.text_index][1].height)-self.texts[lang][self.text_index][1].surfs[-1].get_height())))

		if time.time()-self.text_portion_time >= 0.05:
			self.text_portion += 1
			self.texts[lang][self.text_index][1].content = self.texts[lang][self.text_index][2][:self.text_portion]
			self.text_portion_time = time.time()
