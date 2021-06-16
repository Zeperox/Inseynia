import pygame, os

pygame.mixer.init()

def load_sound(location_list):
    location = location_list[0]
    for location_entry in location_list[1:]:
        location = os.path.join(location, location_entry)
    return pygame.mixer.Sound(location)

# SFX
SFX_list = []

Ping = load_sound(["assets", "SFX", "test ping sound.wav"])
SFX_list.append(Ping)