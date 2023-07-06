import pygame, os
try:
	from scripts.loadingDL.json_functions import load_json
except ModuleNotFoundError:
	from .json_functions import load_json
	
if __name__ == "__main__":
	win = pygame.display.set_mode((800, 600))

sprite_data = load_json(["scripts", "cacheDL", "sprite data.json"])
loaded_mods = load_json(["mods", "loaded_mods.json"])

paths = []
def load_paths(main_path):
	for root, _, files in os.walk(main_path):
		for file in files:
			if file.endswith(".png") and not file[:-4].endswith("DL") and not "DL" in root:
				path = root
				if "\\" in path:
					path += f"\\{file}"
					x = "\\"
				elif "/" in path:
					path += f"/{file}"
					x = "/"

				if loaded_mods[0] and path.split(x) == load_json(["mods", loaded_mods[0], "data.json"]):
					continue

				paths.append(path.split(x))
load_paths("assets")
if loaded_mods[0]:
	load_paths(os.path.join("mods", loaded_mods[0]))
mods = []
for mod in loaded_mods[2]:
	load_paths(os.path.join("mods", mod))
	mods.append(mod)

sprites = {}
for path in paths:
	location = path[0]
	for location_entry in path[1:]:
		location = os.path.join(location, location_entry)

	img = pygame.image.load(location)

	exact_dir = list(set(sprite_data.keys()).intersection(set(path)))
	if exact_dir == []:
		exact_dir = path[-1][:-4]
	else:
		exact_dir = exact_dir[0]

	if exact_dir in sprite_data:
		for key, value in sprite_data[exact_dir].items():
			if key == "flip":
				img = pygame.transform.flip(img, value[0], value[1])
			if key == "scale":
				if isinstance(value, tuple):
					img = pygame.transform.scale(img, value)
				elif isinstance(value, (int, float)):
					img = pygame.transform.scale(img, (img.get_width()*value, img.get_height()*value))
			if key == "rotate":
				img = pygame.transform.rotate(img, value)
			if key == "alpha":
				img = img.convert_alpha()
			if key == "convert":
				img.convert()
				if value:
					img.set_colorkey(tuple(value))
			if key == "scale2x":
				img = pygame.transform.scale2x(img)
		if len(sprite_data[exact_dir]) == 0:
			img = img.convert_alpha()
	else:
		img = img.convert_alpha()
	
	if path[1] in mods:
		sprites[f"{path[1]}.{path[-1][:-4]}"] = img
	else:
		sprites[path[-1][:-4]] = img

try:
	broken = pygame.image.load(os.path.join("assets" if not loaded_mods[0] else loaded_mods[0], "brokenDL.png")).convert()
except:
	broken = pygame.image.load(os.path.join("assets", "brokenDL.png")).convert()

def sprite(name):
	if name in sprites:
		return sprites[name]
	else:
		return broken


if __name__ == "__main__":
	clock = pygame.time.Clock()
	img_list = list(sprites.keys())
	x = 0
	while True:
		clock.tick(5)
		win.fill((0, 0, 0))
		img = sprites[img_list[x]]
		win.blit(img, (400-img.get_width()*0.5, 300-img.get_height()*0.5))
		if x == len(img_list)-1:
			x = -1
		x += 1

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit()

		pygame.display.flip()