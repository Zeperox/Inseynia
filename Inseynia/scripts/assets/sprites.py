import pygame, os
from pygame.locals import *

def load_image_asset(location_list, Scale=None, Flip=None, Rotate=None, Alpha=False, Convert=False):
    location = location_list[0]
    for location_entry in location_list[1:]:
        location = os.path.join(location, location_entry)
    if Scale is not None:
        return pygame.transform.scale(pygame.image.load(location), (Scale))
    if Flip is not None:
        return pygame.transform.flip(pygame.image.load(location), (Flip))
    if Rotate is not None:
        return pygame.transform.rotate(pygame.image.load(location), (Rotate))
    if Alpha:
        return pygame.image.load(location).convert_alpha()
    if Convert:
        return pygame.image.load(location).convert()
    return pygame.image.load(location)


# Images
BG = dict()
BG["Main Menu"] = load_image_asset(["assets", "BG", "Main Menu BG.png"], Convert=True)

#logo
sprites_Logo = dict()
sprites_Logo["Texaract"] = load_image_asset(["assets", "icon", "Texaract.png"])

#button overlays
sprites_Buttons = dict()
sprites_Buttons["Quit NotOver"] = load_image_asset(['assets', 'Buttons', 'QuitNOver.png'])
sprites_Buttons["Quit Over"] = load_image_asset(['assets', 'Buttons', 'QuitOver.png'])
sprites_Buttons["Return NotOver"] = load_image_asset(['assets', 'Buttons', 'ReturnNOver.png'])
sprites_Buttons["Return Over"] = load_image_asset(['assets', 'Buttons', 'ReturnOver.png'])
sprites_Buttons["Settings NotOver"] = load_image_asset(['assets', 'Buttons', 'SettingsNOver.png'])
sprites_Buttons["Settings Over"] = load_image_asset(['assets', 'Buttons', 'SettingsOver.png'])
sprites_Buttons["Resume NotOver"] = load_image_asset(['assets', 'Buttons', 'ResumeNOver.png'])
sprites_Buttons["Resume Over"] = load_image_asset(['assets', 'Buttons', 'ResumeOver.png'])
sprites_Buttons["Resol Next"] = load_image_asset(["assets", "Buttons", "Next Resol.png"], Convert=True)
sprites_Buttons["Resol Previous"] = load_image_asset(["assets", "Buttons", "Previous Resol.png"], Convert=True)

#story
sprites_Story_Photoes = dict()
sprites_Story_Photoes['S1'] = load_image_asset(['assets', 'Sprites', 'Story', 'S1.png'], Convert=True)


# Sprites
#inv
sprites_Equipment = dict()
sprites_Equipment['Wooden Sword'] = load_image_asset(['assets', 'Sprites', 'Arsenal & Tools', 'Wooden Sword.png'], (48, 48))
sprites_Equipment['No Shield'] = load_image_asset(['assets', 'Sprites', 'Arsenal & Tools', 'No Shield.png'], (48, 48))
sprites_Equipment['Crossbow'] = load_image_asset(['assets', 'Sprites', 'Arsenal & Tools', 'Crossbow.png'], (48, 48))
sprites_Equipment['Wooden Shield'] = load_image_asset(['assets', 'Sprites', 'Arsenal & Tools', 'Wooden Shield.png'], (48, 48))
sprites_Equipment['ph1'] = load_image_asset(['assets', 'Sprites', 'Arsenal & Tools', 'ph1.png'])
sprites_Equipment['ph2'] = load_image_asset(['assets', 'Sprites', 'Arsenal & Tools', 'ph2.png'])
sprites_Equipment['ph3'] = load_image_asset(['assets', 'Sprites', 'Arsenal & Tools', 'ph3.png'])
sprites_Equipment['ph4'] = load_image_asset(['assets', 'Sprites', 'Arsenal & Tools', 'ph4.png'])
sprites_Equipment['Fist'] = load_image_asset(['assets', 'Sprites', 'Arsenal & Tools', 'Fist.png'], (48, 48))

#misc
sprites_Misc = dict()
sprites_Misc['Inventory Slot'] = load_image_asset(['assets', 'Sprites', 'Misc', 'Inventory Slot.png'])

#test enemy
sprites_Enemies = dict()
sprites_Enemies["Test Enemy"] = load_image_asset(["assets", "Sprites", "Enemies", "Test Enemy.png"])
