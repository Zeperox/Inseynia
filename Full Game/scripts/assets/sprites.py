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

#button overlays
sprites_Button_Overlays = dict()
sprites_Button_Overlays['Button Female Overlay'] = load_image_asset(['assets', 'Button Overlays', 'Female Symbol.png'])
sprites_Button_Overlays['Button Male Overlay'] = load_image_asset(['assets', 'Button Overlays', 'Male Symbol.png'])

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
sprites_Misc["Quit NotOver"] = load_image_asset(['assets', 'Sprites', 'Misc', 'QuitNOver.png'])
sprites_Misc["Quit Over"] = load_image_asset(['assets', 'Sprites', 'Misc', 'QuitOver.png'])
sprites_Misc["Settings NotOver"] = load_image_asset(['assets', 'Sprites', 'Misc', 'SettingsNOver.png'])
sprites_Misc["Settings Over"] = load_image_asset(['assets', 'Sprites', 'Misc', 'SettingsOver.png'])
sprites_Misc["Resume NotOver"] = load_image_asset(['assets', 'Sprites', 'Misc', 'ResumeNOver.png'])
sprites_Misc["Resume Over"] = load_image_asset(['assets', 'Sprites', 'Misc', 'ResumeOver.png'])
sprites_Misc["Resol Next"] = load_image_asset(["assets", "Button Overlays", "Next Resol.png"], Convert=True)
sprites_Misc["Resol Previous"] = load_image_asset(["assets", "Button Overlays", "Previous Resol.png"], Convert=True)

#test enemy
sprites_Enemies = dict()
sprites_Enemies["Test Enemy"] = load_image_asset(["assets", "Sprites", "Enemies", "Test Enemy.png"])

#devroom
sprites_DevRoom = dict()
sprites_DevRoom["Room 1"] = load_image_asset(["assets", "Sprites", "Dev Room", "Room1.png"], Convert=True)
