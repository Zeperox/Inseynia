import pygame, os, json, random, sys

from pygame.locals import *

try:
	from scripts.loading.json_functions import load_json, dump_json
except ModuleNotFoundError:
	def load_json(location_list):
		location = location_list[0]
		for location_entry in location_list[1:]:
			location = os.path.join(location, location_entry)

		with open(location, "r") as f:
			return json.load(f)

	def dump_json(location_list, var):
		location = location_list[0]
		for location_entry in location_list[1:]:
			location = os.path.join(location, location_entry)

		with open(location, "w") as f:
			json.dump(var, f, indent=4)

pygame.display.init()

try:
	settings = load_json(["scripts", "data", "settings.json"])
except FileNotFoundError:
	settings = {
		"FPS": 60,
		"fullscreen": True,
		"keys": {
			"up": K_w,
			"down": K_s,
			"left": K_a,
			"right": K_d,
			"dash": K_SPACE,
			"sleep": K_f,
			"interact": K_e,
			"inventory": K_TAB,
			"pause": K_ESCAPE
		},
		"brightness": 0,
		"permadeath": False,
		"volumes": {
			"music": 1,
			"SFX": 1
		},
		"lang": "english"
	}

	dump_json(["scripts", "data", "settings.json"], settings)

info = pygame.display.Info()
Width, Height = 640, 360

if settings["fullscreen"]:
	win = pygame.display.set_mode((Width, Height), DOUBLEBUF | HWSURFACE | SCALED | FULLSCREEN)
else:
	win = pygame.display.set_mode((Width, Height), DOUBLEBUF | HWSURFACE | SCALED)

if random.randint(0, 1000) == 1:
	with open("Crash Report.txt", "w") as f:
		text = random.choice([
			"The game crashed",
			"It do be crashin' doe",
			"Have you tried reopening the game?",
			"Exited with code 0",
			"Crash Report\n\nReason of crash: idk ¯\_(ツ)_/¯",
			"You were too beautiful that the game got so shy and jealous that it crashed... sorry",
			"'|, |, :|° '|, '\\' ^¯---_° ¯__- has caused it",
			"Uhhh... What happened?",
			"Delete System32 to grant access to the game",
			"This crash has a chance of 0.1% chance of happening, do I consider you lucky or unlucky?"
		])
		f.write(text)
		pygame.quit()
		sys.exit()

jsons = [
	[load_json(["scripts", "data", "captions.json"]), "captions.json"],
	[load_json(["scripts", "data", "enemies.json"]), "enemies.json"],
	[load_json(["scripts", "data", "equipment.json"]), "equipment.json"],
	[load_json(["scripts", "data", "items.json"]), "items.json"],
	[load_json(["scripts", "data", "rooms.json"]), "rooms.json"],
	[load_json(["scripts", "data", "sprite data.json"]), "sprite data.json"]
]
for mod in os.scandir(os.path.join("mods")):
	if mod.is_dir():
		try:
			for i, file in enumerate(os.scandir(os.path.join("mods", mod.name, "scripts", "data"))):
				if file.is_file() and file.name.endswith(".json"):
					if i not in [0, 2]:
						jsons[i][0].update(load_json(["mods", mod.name, "scripts", "data", jsons[i][1]]))
					elif i == 0:
						jsons[i][0] += load_json(["mods", mod.name, "scripts", "data", jsons[i][1]])
		except:
			continue
for json_file in jsons:
	dump_json(["scripts", "cache", json_file[1]], json_file[0])

captions = load_json(["scripts", "cache", "captions.json"])
try:
	i = captions.remove("This caption will never appear, isn't that weird?")
	captions.append("This caption will never appear, isn't that weird?")
except:
	pass

randcaption = random.choice(captions[:-1])

if randcaption == "騙你":
	pygame.display.set_caption(f"印西尼亞: {randcaption}") # yinxi ni ya
elif randcaption == "Welcome, ":
	randcaption += os.getlogin()
	pygame.display.set_caption(f"Inseynia: {randcaption}")
elif randcaption == "Opposite of Inseynia":
	pygame.display.set_caption(f"Calmia: {randcaption}")
elif randcaption == "نَاْوْ إِنْ أَرَبِكْ":
	pygame.display.set_caption(f"إنسينيا: {randcaption}")
elif randcaption == "なお イン じゃぱねせ":
	pygame.display.set_caption(f"いんせいにあ: {randcaption}")
elif randcaption in ["¯\_(ツ)_/¯", "( ͡° ͜ʖ ͡°)"]:
	pygame.display.set_caption(randcaption)
elif randcaption == "flip":
	pygame.display.set_caption(f"Inseynia | ainyesnI")
else:
	pygame.display.set_caption(f"Inseynia: {randcaption}")

icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)


if __name__ == "__main__":
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				quit()
