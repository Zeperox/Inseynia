import pygame, os, time

from scripts.loadingDL.files import files
from scripts.loadingDL.json_functions import load_json

Button = files["button"].Button
Text = files["text"].Text

texts = load_json(["scripts", "dataDL", "text.json"])
langs = load_json(["scripts", "dataDL", "langs.json"])

quests = {}
for file in os.scandir(os.path.join("scripts", "quests")):
	if file.is_file():
		quests[file.name[:-3]] = files[file.name[:-3]].Quest

class Dialogue:
	def __init__(self, id):
		self.id = id
		self.triggered = False
		self.quest = False
		self.quests = {}
		self.previous_id = []

		self.text_index = 0
		self.text_portion = 0
		self.text_portion_time = 0

		self.texts = {lang: [] for lang in langs}
		self.goto_texts = {lang: {} for lang in langs}
		self.quest_text = {"start": {lang: [] for lang in langs}, "progress": {lang: [] for lang in langs}, "end": {lang: [] for lang in langs}, "fail": {lang: [] for lang in langs}}

		for text_id, text_datas in texts.items():
			if text_id.startswith(self.id):
				for text_data in text_datas:
					for lang_i, lang in enumerate(langs):
						try:
							text_data["name"][lang_i]
						except:
							lang_i = 0
						
						if lang == "arabic":
							align = pygame.FONT_RIGHT
							tri = " ◀"
						else:
							align = pygame.FONT_LEFT
							tri = " ▶"
							
						buttons = []
						space_width = (640-200*len(text_data["input"]))/(len(text_data["input"])+1) # (surf_width - button_width*button_count) / (button_count+1)
						for button_i, button in enumerate(text_data["input"]):
							try:
								button_text = button[0][lang_i]
							except:
								button_text = button[0][0]
							buttons.append([Button(space_width*(button_i+1)+200*button_i, 320, 200, 35, (0, 0, 0), button_text, lang, (255, 255, 255), (255, 255, 255), font_path=os.path.join("assets", "fontsDL", "font.ttf")), button[1]])
							if button[1].startswith("quest"):
								self.quests[" ".join(button[1].split(" ")[1:])] = quests[" ".join(button[1].split(" ")[1:])]()

						if ".quest" in text_id:
							self.quest = "start"
							self.quest_text[text_id.split("_")[-1]][lang].append([Text(os.path.join("assets", "fontsDL", "font.ttf"), text_data["name"][lang_i], 16, (255, 255, 255), lang, max_width=490, align=align, bold=True), Text(os.path.join("assets", "fontsDL", "font.ttf"), "", 16, (255, 255, 255), lang, max_width=490, align=align), text_data["text"][lang_i]+tri, text_data["extra"], buttons])
						elif "." in text_id:
							if text_id not in self.goto_texts[lang]:
								self.goto_texts[lang][text_id] = []
							self.goto_texts[lang][text_id].append([Text(os.path.join("assets", "fontsDL", "font.ttf"), text_data["name"][lang_i], 16, (255, 255, 255), lang, max_width=490, align=align, bold=True), Text(os.path.join("assets", "fontsDL", "font.ttf"), "", 16, (255, 255, 255), lang, max_width=490, align=align), text_data["text"][lang_i]+tri, text_data["extra"], buttons])
						else:
							self.texts[lang].append([Text(os.path.join("assets", "fontsDL", "font.ttf"), text_data["name"][lang_i], 16, (255, 255, 255), lang, max_width=490, align=align, bold=True), Text(os.path.join("assets", "fontsDL", "font.ttf"), "", 16, (255, 255, 255), lang, max_width=490, align=align), text_data["text"][lang_i]+tri, text_data["extra"], buttons])

					if text_data["extra"] and text_data["extra"].startswith("quest"):
						self.quests[" ".join(text_data["extra"].split(" ")[1:])] = quests[" ".join(text_data["extra"].split(" ")[1:])]()

		self.surf = pygame.Surface((600, 100))
		self.surf.fill((255, 255, 255))
		self.surf.fill((0, 0, 0), (2, 2, self.surf.get_width()-4, self.surf.get_height()-4))
		pygame.draw.line(self.surf, (255, 255, 255), (100, 0), (100, 100), 2)

	def render(self, win, lang):
		if self.quest and len(self.previous_id) == 0:
			text_data = self.quest_text[self.quest][lang][self.text_index]
		elif len(self.previous_id):
			text_data = self.goto_texts[lang][self.id][self.text_index]
		else:
			text_data = self.texts[lang][self.text_index]

		blits = [
			(self.surf, (640*0.5-300, 215)),
			(text_data[0].surf, (640*0.5-195, 220)),
			(text_data[1].surf, (640*0.5-195, 220+text_data[0].height))
		]
		for button in text_data[4]:
			blits.append((button[0].surf, (button[0].x, button[0].y)))
		win.fblits(blits)
		
		if time.time()-self.text_portion_time >= 0.025:
			self.text_portion += 1
			text_data[1].content = text_data[2][:self.text_portion]
			self.text_portion_time = time.time()

	def next_index(self, lang, player, ignore_buttons=False):
		if self.quest:
			text_data = self.quest_text[self.quest][lang][self.text_index]
		elif len(self.previous_id):
			text_data = self.goto_texts[lang][self.id][self.text_index]
		else:
			text_data = self.texts[lang][self.text_index]

		if text_data[1].content != text_data[2]:
			self.text_portion = len(text_data[2])
			text_data[1].content = text_data[2]
		elif not len(text_data[4]) or ignore_buttons:
			if text_data[3]:
				if text_data[3] == "back":
					self.id = self.previous_id[-1][0]
					self.text_index = self.previous_id[-1][1]
					self.previous_id = self.previous_id[:-1]
				elif text_data[3] == "return":
					return True
				elif text_data[3].startswith("quest"):
					player.quests.append(self.quests[" ".join(text_data[3].split(" ")[1:])])
				elif text_data[3].startswith("goto"):
					self.previous_id.append([self.id, self.text_index+1])
					text_data[3] = " ".join(text_data[3].split(" ")[1:])
					if (text_data[3].count(":") == 1 and text_data[3].startswith("trg")) or (text_data[3].count(":") == 2 and text_data[3].startswith("npc")):
						self.text_index = 0
						self.id = text_data[3]
					else:
						text_data[3] = text_data[3].split(":")
						self.text_index = int(text_data[3][-1])
						self.id = "".join(text_data[3][:-1])
				else:
					self.text_index += 1
			else:
				self.text_index += 1

			self.text_portion = 0
			self.text_portion_time = 0
		
			for _ in reversed(self.previous_id):
				text_len = len(self.goto_texts[lang][self.id])
				if self.text_index == text_len:
					self.id = self.previous_id[-1][0]
					self.text_index = self.previous_id[-1][1]
					self.previous_id = self.previous_id[:-1]
				else:
					break
			else:
				if self.quest:
					text_len = len(self.quest_text[self.quest][lang])
				else:
					text_len = len(self.texts[lang])
				if self.text_index == text_len:
					return True
				
		if self.quest == "fail":
			self.quest = "start"
					
	def button_press(self, mouse, lang, player):
		if self.quest:
			text_data = self.quest_text[self.quest][lang][self.text_index]
		elif len(self.previous_id):
			text_data = self.goto_texts[lang][self.id][self.text_index]
		else:
			text_data = self.texts[lang][self.text_index]

		quest_index = False
		for button in text_data[4]:
			if button[0].rect.collidepoint(mouse):
				if button[1] == "back":
					self.id = self.previous_id[-1][0]
					self.text_index = self.previous_id[-1][1]
					self.previous_id = self.previous_id[:-1]
				elif button[1] == "return":
					return True
				elif button[1].startswith("quest"):
					player.quests.append(self.quests[" ".join(button[1].split(" ")[1:])])
					quest_index = self.next_index(lang, player, True)
					if self.quests[" ".join(button[1].split(" ")[1:])].start(player, self):
						self.quest = "fail"
				elif button[1].startswith("goto"):
					self.previous_id.append([self.id, self.text_index+1])
					button[1] = " ".join(button[1].split(" ")[1:])
					if (button[1].count(":") == 1 and button[1].startswith("trg")) or (button[1].count(":") == 2 and button[1].startswith("npc")):
						self.text_index = 0
						self.id = button[1]
					else:
						button[1] = button[1].split(":")
						self.text_index = int(button[1][-1])
						self.id = "".join(button[1][:-1])

				self.text_portion = 0
				self.text_portion_time = 0
		return quest_index

	def get_data(self, lang):
		if self.quest:
			return self.quest_text[self.quest][lang][self.text_index]
		elif len(self.previous_id):
			return self.goto_texts[lang][self.id][self.text_index]
		else:
			return self.texts[lang][self.text_index]