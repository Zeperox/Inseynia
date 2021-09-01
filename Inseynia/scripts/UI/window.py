import pygame, os, json, platform
from pygame.locals import *
from scripts.data.json_functions import *

pygame.display.init()

try:
    settings = load_json(["scripts", "data", "settings.json"])
except FileNotFoundError:
    settings = {
        "FPS": 60,
        "Fullscreen": True,
        "Resol": None,
        "Keys": {
            "Up": 119,
            "Down": 115,
            "Right": 100,
            "Left": 97,
            "Throw": 113,
            "Equip": 101,
            "Switch": 114,
            "Pause": 27
        },
        "Brightness": 0,
        "Permadeath Enabled": False,
        "Volumes": {
            "Music": 1,
            "SFX": 1
        }
    }

    dump_json(["scripts", "data", "settings.json"], settings)

fullscreen = settings["Fullscreen"]
resol = tuple(settings["Resol"]) if settings["Resol"] else None
if not "Volumes" in settings.keys():
    settings["Volumes"] = {"Music": 1, "SFX": 1}
    dump_json(["scripts", "data", "settings.json"], settings)

# Screen
info = pygame.display.Info()
screen_w, screen_h = info.current_w, info.current_h
if not resol:
    Width, Height = screen_w, screen_h
else:
    Width, Height = resol[0], resol[1]

old_Width, old_Height = Width, Height

if fullscreen and platform.system() == "Windows":
    win = pygame.display.set_mode((Width, Height), FULLSCREEN | DOUBLEBUF | HWSURFACE | SCALED)
else:
    win = pygame.display.set_mode((Width, Height), DOUBLEBUF | HWSURFACE | SCALED)