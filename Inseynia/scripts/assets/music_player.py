import pygame, os

def play_music(location_list: list, loop=0):
    location = location_list[0]
    for location_entry in location_list[1:]:
        location = os.path.join(location, location_entry)
    pygame.mixer.music.load(location)
    return pygame.mixer.music.play(loop)