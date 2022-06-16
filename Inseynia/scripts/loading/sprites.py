import pygame, os, json
try:
    from scripts.loading.json_functions import *
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

if __name__ == "__main__":
    win = pygame.display.set_mode((800, 600))

sprite_data = load_json(["scripts", "cache", "sprite data.json"])

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

                paths.append(path.split(x))
load_paths("assets")
for mod in os.scandir(os.path.join("mods")):
    if mod.is_dir():
        try:
            load_paths(os.path.join("mods", mod.name, "assets"))
        except:
            continue

sprites = {}
for path in paths:
    location = path[0]
    for location_entry in path[1:]:
        location = os.path.join(location, location_entry)

    img = pygame.image.load(location)

    if path[-1][:-4] in sprite_data:
        for key, value in sprite_data[path[-1][:-4]].items():
            if key == "flip":
                img = pygame.transform.flip(img, value[0], value[1])
            if key == "scale":
                if type(value) == tuple:
                    img = pygame.transform.scale(img, value)
                elif type(value) == int or type(value) == float:
                    img = pygame.transform.scale(img, (img.get_width()*value, img.get_height()*value))
            if key == "rotate":
                img = pygame.transform.rotate(img, value)
            if key == "alpha":
                img.convert_alpha()
            if key == "convert":
                img.convert()
                if value:
                    img.set_colorkey(tuple(value))
    
    sprites[path[-1][:-4]] = img

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