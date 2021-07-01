import pygame, os, json
from pygame.locals import *

pygame.display.init()

if not os.path.exists(os.path.join(os.getenv("localappdata"), ".inseynia", "saves", "settings.json")):
    with open (os.path.join(os.getenv("localappdata"), ".inseynia", "saves", "settings.json"), "w") as f:
        settings = {"FPS": 60, "Fullscreen": True, "Resol": None, "Keys": {"Up": K_w, "Down": K_s, "Right": K_d, "Left": K_a, "Throw": K_q, "Equip": K_e, "Switch": K_r, "Pause": K_ESCAPE}, "Brightness": 0}
        json.dump(settings, f, indent=4)
else:
    with open (os.path.join(os.getenv("localappdata"), ".inseynia", "saves", "settings.json"), "r") as f:
        settings = json.load(f)

fullscreen = settings["Fullscreen"]
resol = tuple(settings["Resol"]) if settings["Resol"] else None

# Screen
info = pygame.display.Info()
screen_w, screen_h = info.current_w, info.current_h
if not resol:
    Width, Height = screen_w, screen_h
else:
    Width, Height = resol[0], resol[1]

old_Width, old_Height = Width, Height

if fullscreen:
    win = pygame.display.set_mode((Width, Height), FULLSCREEN | DOUBLEBUF | HWSURFACE)
else:
    win = pygame.display.set_mode((Width, Height), DOUBLEBUF | HWSURFACE)
