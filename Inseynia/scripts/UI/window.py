import pygame, os, json, platform
from pygame.locals import *

pygame.display.init()

with open (os.path.join("scripts", "data", "settings.json"), "r") as f:
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

if fullscreen and platform.system() == "Windows":
    win = pygame.display.set_mode((Width, Height), FULLSCREEN | DOUBLEBUF | HWSURFACE | SCALED)
else:
    win = pygame.display.set_mode((Width, Height), DOUBLEBUF | HWSURFACE | SCALED)