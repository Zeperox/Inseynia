import os, importlib, sys, pygame
from .json_functions import load_json

loaded_mods = load_json(["mods", "loaded_mods.json"])

paths = []
def load_paths(main_path):
	for root, _, files in os.walk(main_path):
		for file in files:
			if file.endswith(".py") and not file[:-3].endswith("DL") and not "DL" in root:
				path = root
				if "\\" in path:
					path += f"\\{file}"
					x = "\\"
				elif "/" in path:
					path += f"/{file}"
					x = "/"

				paths.append(path.split(x))
load_paths("scripts")
if loaded_mods[1]:
	load_paths(os.path.join("mods", loaded_mods[1]))
mods = []
for mod in loaded_mods[2]:
	load_paths(os.path.join("mods", mod))
	mods.append(mod)

for path in paths[:]:
	if path[1] == loaded_mods[1]:
		for _path in paths:
			if _path[-1] == path[-1]:
				paths.remove(_path)
				break


files = {}
failed_paths = []
extra_failed_paths = []
x = 0
while len(files) != len(paths):
	if len(failed_paths) == 0:
		path = paths[x]
	else:
		path = failed_paths[-1]
		del failed_paths[-1]

	while True:
		location = ".".join(path)[:-3]
		try:
			file = importlib.import_module(location)

			if path[1] in mods:
				files[f"{path[1]}.{path[-1][:-3]}"] = file
			else:
				files[path[-1][:-3]] = file
		except KeyError as e:
			if path in failed_paths:
				for i, path in enumerate(failed_paths):
					failed_paths[i] = "/".join(path)
				print("Import Error: Circular import in the following files:\n\n"+"\n".join(failed_paths))
				pygame.quit(); sys.exit()
			else:
				failed_paths.append(path)
			for _path in paths:
				if f"'{_path[-1][:-3]}'" == str(e).split(".")[-1]:
					path = _path
					break
		else:
			break
		
	if path == paths[x]:
		x += 1

