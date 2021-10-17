import pygame, os
from scripts.data.json_functions import *

sprite_data = load_json(["scripts", "data", "sprite data.json"])

paths = []
def get_files(dir):
    for root, _, files in os.walk(dir):
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

images = {}
def load_image():
    global images
    for path in paths:
        location = path[0]
        for location_entry in path[1:]:
            location = os.path.join(location, location_entry)

        img = pygame.image.load(location)

        for key, value in sprite_data[path[-1][:-4]].items():
            if key == "flip":
                img = pygame.transform.flip(img, value[0], value[1])
            elif key == "scale":
                if type(value) == tuple:
                    img = pygame.transform.scale(img, value)
                elif type(value) == int or type(value) == float:
                    img = pygame.transform.scale(img, (img.get_width()*value, img.get_height()*value))
            elif key == "rotate":
                img = pygame.transform.rotate(img, value)
            elif key == "alpha":
                img.convert_alpha()
            elif key == "convert":
                img.convert()
                if value:
                    img.set_colorkey(tuple(value))
        
        images[path[-1][:-4]] = img

get_files("assets")
load_image()