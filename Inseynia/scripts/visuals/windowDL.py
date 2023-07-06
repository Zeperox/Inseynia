import pygame, os, json, random, sys

try:
	from scripts.loadingDL.json_functions import load_json, dump_json
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
	settings = load_json(["scripts", "dataDL", "settings.json"])
except FileNotFoundError:
	settings = {
		"FPS": 60,
		"fullscreen": True,
		"vsync": 1,
		"keys": {
			"up": pygame.K_w,
			"down": pygame.K_s,
			"left": pygame.K_a,
			"right": pygame.K_d,
			"dash": pygame.K_SPACE,
			"sneak": pygame.K_LSHIFT,
			"sleep": pygame.K_f,
			"interact": pygame.K_r,
			"inventory": pygame.K_TAB,
			"pause": pygame.K_ESCAPE,
			"primary": 1,
			"secondary": 3,
			"pspecial": pygame.K_q,
			"sspecial": pygame.K_e
		},
		"cons": {
			"up": pygame.CONTROLLER_BUTTON_DPAD_UP,
			"down": pygame.CONTROLLER_BUTTON_DPAD_DOWN,
			"left": pygame.CONTROLLER_BUTTON_DPAD_LEFT,
			"right": pygame.CONTROLLER_BUTTON_DPAD_RIGHT,
			"dash": pygame.CONTROLLER_BUTTON_A,
			"sneak": pygame.CONTROLLER_BUTTON_LEFTSTICK,
			"sleep": pygame.CONTROLLER_BUTTON_Y,
			"interact": pygame.CONTROLLER_BUTTON_X,
			"inventory": pygame.CONTROLLER_BUTTON_BACK,
			"pause": pygame.CONTROLLER_BUTTON_START,
			"primary": 16,
			"secondary": 15,
			"pspecial": pygame.CONTROLLER_BUTTON_RIGHTSHOULDER,
			"sspecial": pygame.CONTROLLER_BUTTON_LEFTSHOULDER
		},
		"sticks invert": False,
		"brightness": 0,
		"permadeath": False,
		"volumes": {
			"music": 1,
			"SFX": 1
		},
		"lang": "english"
	}

	dump_json(["scripts", "dataDL", "settings.json"], settings)

Width, Height = 640, 360
win = pygame.display.set_mode((Width, Height), pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.SCALED, vsync=settings["vsync"])
if settings["fullscreen"]:
	pygame.display.toggle_fullscreen()
	

if random.randint(0, 1000) == 1:
	with open("Crash Report.txt", "w", encoding="utf-8") as f:
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
	[load_json(["scripts", "dataDL", "captions.json"]), "captions.json"],
	[load_json(["scripts", "dataDL", "enemies.json"]), "enemies.json"],
	[load_json(["scripts", "dataDL", "equipment.json"]), "equipment.json"],
	[load_json(["scripts", "dataDL", "items.json"]), "items.json"],
	[load_json(["scripts", "dataDL", "rooms.json"]), "rooms.json"],
	[load_json(["scripts", "dataDL", "sprite data.json"]), "sprite data.json"]
]
for mod in os.scandir(os.path.join("mods")):
	if mod.is_dir():
		try:
			for i, file in enumerate(os.scandir(os.path.join("mods", mod.name, "scripts", "dataDL"))):
				if file.is_file() and file.name.endswith(".json"):
					if i not in [0, 2]:
						jsons[i][0].update(load_json(["mods", mod.name, "scripts", "dataDL", jsons[i][1]]))
					elif i == 0:
						jsons[i][0] += load_json(["mods", mod.name, "scripts", "dataDL", jsons[i][1]])
		except:
			continue
for json_file in jsons:
	dump_json(["scripts", "cacheDL", json_file[1]], json_file[0])

captions = load_json(["scripts", "cacheDL", "captions.json"])
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
			if event.type == pygame.QUIT:
				quit()
