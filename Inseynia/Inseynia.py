# Import modules
import pygame, os, sys, random, time, platform, warnings

from pygame.locals import *
from pygame._sdl2.video import Window
from pypresence import Presence

# Import game scripts
from scripts.UI.window import *
from scripts.UI.brightness import *
from scripts.UI.button import *
from scripts.UI.slider import *
from scripts.UI.textbox import *
from scripts.UI.text import *

from scripts.assets.sprites import images
from scripts.assets.SFX import *
from scripts.assets.music_player import *

from scripts.tiles.tiles import *

from scripts.game_logic.drops import *
from scripts.game_logic.inventory import *
from scripts.game_logic.enemy import *
from scripts.game_logic.player import *
from scripts.game_logic.boss import *
from scripts.game_logic.camera import *

from scripts.data.json_functions import *

from scripts.custom_collisions.obb import *
from scripts.custom_collisions.polygon import *


pygame.event.set_allowed([KEYDOWN, MOUSEBUTTONDOWN, MOUSEMOTION, MOUSEBUTTONUP, QUIT])

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.set_num_channels(128)


# Window
window = Window.from_display_module()
window.position = ((screen_w*0.5)-(Width*0.5), (screen_h*0.5)-(Height*0.5))

if random.randint(0, 1000) == 1:
    with open("Crash Report.txt", "w") as f:
        text = random.choice([
            "The game crashed",
            "It do be crashin' doe",
            "Have you tried reopening the game?",
            "Exited with code 0",
            "Crash Report\n\nReason of crash: idk ¯\_(ツ)_/¯",
            "You were too beautiful that the game got so shy and jealous that it crashed... sorry",
            "----•-••••••-•-••-• has caused it",
            "Uhhh... What happened?",
            "Delete System32 to grant access to the game",
            "Crash Report\n\nReason of crash: you probably like amogus memes",
            "This crash has a chance of 0.1% chance of happening, do I consider you lucky or unlucky?"
        ])
        f.write(text)
        pygame.quit()
        sys.exit()

caption_list = [
    "The evil is growing",
    "Try Minceraft",
    "Try Lanterner",
    "Maybe Inseynia is True?",
    "Inseyniaer is coming!",
    "Babushka",
    "Check out Indian Panini",
    "This was a bad idea...",
    "Tunak Tunak Tun",
    "The first of us",
    "Dolphin gun soon... maybe... idk... developer lost hope",
    "The Morgan horse is the best!",
    "Subscribe to PewDiePie and unsubscribe to T-Series and Cocomelon",
    "Ogres like Onions!",
    "Meme man is angery",
    "*Bonk*",
    "I was born at a very young age",
    "It's time to go",
    "騙你",
    "Now in XBOX 180!",
    "Quarter Life Steve",
    '"SMASH DAT LIKE BUTTON CAN WE GET 1M LIKES THAT WE BE DOPE!" - Some random youtuber',
    "Based on a true story",
    "(In a parallel universe) Now on geegle store for only $9.99!",
    "Here's Johnny!",
    "It's what it's",
    "Made in North Korea",
    "Made in the Soviet Union",
    "Made in China",
    "Breath of the Mild",
    "Welcome, ",
    "Opposite of Inseynia",
    "ناو إن أرابيك",
    "Wishlist Karlson now, GAMER",
    "Made with pygame & python",
    "Full of lore",
    "なお　イン　じゃぱねせ",
    "Wasted",
    "¯\_(ツ)_/¯",
    "Totally not a rip-off, wdym",
    'Therapis: "All dreams have meanings" | My Dreams:',
    "jEHyIAuH YI jxu huqB lyBBqyD",
    "...yPRGDyAR yLB JMAIGLE GR BCCN GL y AyTC...",
    '"Game of the year" -Inseynia',
    "flip",
    "Zelenor was the greatest leader of all time, but he made a mistake...",
    "...mereljepeja jeu fhhse jepe b ebxh ibsle islero ujbhjesle xjememebjahsn..."
    "This caption will never appear, isn't that weird?"
]

randcaption = random.choice(caption_list[:-1])

if randcaption == "騙你":
    pygame.display.set_caption(f"印西尼亞: {randcaption}") # yinxi ni ya
elif randcaption == "Welcome, ":
    randcaption += os.getlogin()
    pygame.display.set_caption(f"Inseynia: {randcaption}")
elif randcaption == "Opposite of Inseynia":
    pygame.display.set_caption(f"Calmia: {randcaption}")
elif randcaption == "ناو إن أرابيك":
    pygame.display.set_caption(f"إنسينيا: {randcaption}")
elif randcaption == "なお　イン　じゃぱねせ":
    pygame.display.set_caption(f"いんせいにあ: {randcaption}")
elif randcaption == "¯\_(ツ)_/¯":
    pygame.display.set_caption(randcaption)
elif randcaption == "flip":
    pygame.display.set_caption(f"Inseynia|aiyesnI")
else:
    pygame.display.set_caption(f"Inseynia: {randcaption}")

icon = pygame.image.load("Inseynia Icon.ico")
pygame.display.set_icon(icon)

# Classes
class Story:
    def __init__(self, text_list):
        self.texts = text_list
        self.str = []

    def render(self, window, img=None):
        for x, str_ in enumerate(self.str):
            text = Text(0, 30*x+400, str_, os.path.join("assets", "fonts", "DefaultFont.TTF"), 16, (255,255,255))
            #text = Text(0, 30*x+400, str_, os.path.join("assets", "fonts", "Font.png"), (255,255,255))
            text.x = Width*0.5-text.get_width()*0.5
            text.render(win)
        if img:
            window.blit(img, (Width*0.5-img.get_width()*0.5, 75))

    def update_text(self, func):
        global debug_menu
        last_call = time.time()
        for str_, text in enumerate(self.texts):
            self.str.append("")
            for x in range(1, len(text)+1):
                while self.str[str_] != text[:x]:
                    if time.time() - last_call >= 1/30:
                        self.str[str_] = text[:x]
                        func()
                        for event in pygame.event.get():
                            if event.type == QUIT:
                                pygame.quit()
                                sys.exit()
                            if event.type == KEYDOWN:
                                if event.key == K_F11:
                                    F11()
                                elif event.key == K_F3:
                                    debug_menu = not debug_menu
                                elif event.key == K_SPACE:
                                    self.str = self.texts
                                    func()
                                    pygame.display.flip()
                                    return
                                else:
                                    return True
                        pygame.display.flip()
                        last_call = time.time()

# Vars

clock = pygame.time.Clock()
FPS = settings["FPS"]
fullscreen = settings["Fullscreen"]
resol = tuple(settings["Resol"]) if settings["Resol"] else None
keys = settings["Keys"]
set_brightness = settings["Brightness"]
volumes = settings["Volumes"]

for music in musics.values():
    music.set_volume(volumes["Music"], True)

true_scroll = [0, 0]; scroll = [0, 0]
brightness_overlay = Brightness((0, 0), (Width, Height), set_brightness)

images["Main Menu BG"] = pygame.transform.scale(images["Main Menu BG"], (Width, Height))

#debug menu
debug_menu = False
show_hitboxes = False
show_mid = False

#discord rich presence
start_time = time.time()
async def start_rpc():
    try:
        rpc = Presence("871701732349079592")
        rpc.connect()

        await update_rpc()
    except:
        pass

async def update_rpc(rpc: Presence):
    if Player.location:
        rpc.update(
            state=f"Region: {Player.location}",
            large_image="inseynia",
            large_text="Inseynia",
            start=start_time
        )
    else:
        rpc.update(
            large_image="inseynia",
            large_text="Inseynia",
            start=start_time
        )
warnings.filterwarnings("ignore")
start_rpc()
warnings.filterwarnings("default")


# Program Functions
def FPS_ind(last_time):
    return (time.time() - last_time) * 60

def F11(fullscreen_param=None):
    if platform.system() == "Windows":
        global fullscreen, Width, Height, info
        if fullscreen_param != None:
            fullscreen = fullscreen_param
            if fullscreen:
                pygame.display.set_mode((Width, Height), FULLSCREEN | DOUBLEBUF | HWSURFACE | SCALED)
            else:
                pygame.display.set_mode((Width, Height), DOUBLEBUF | HWSURFACE | SCALED)
        else:
            fullscreen = not fullscreen
            pygame.display.toggle_fullscreen()

        save_settings()

def change_resol(new_resol):
    global Width, Height, resol, info
    resol = new_resol
    if not resol:
        Width, Height = info.current_w, info.current_h
    else:
        Width, Height = resol[0], resol[1]

    if fullscreen and platform.system() == "Windows":
        pygame.display.set_mode((Width, Height), FULLSCREEN | DOUBLEBUF | HWSURFACE | SCALED)
    else:
        os.environ['SDL_VIDEO_CENTERED'] = '1'

        screen_w, screen_h = info.current_w, info.current_h
        x, y = (screen_w*0.5)-(Width*0.5), (screen_h*0.5)-(Height*0.5)
        os.environ['SDL_VIDEO_WINDOW_POS'] = '%d,%d' % (x,y)
        pygame.display.set_mode((Width, Height), DOUBLEBUF | HWSURFACE | SCALED)

    brightness_overlay.reconfigure(size=(Width, Height))
    images["Main Menu BG"] = pygame.transform.scale(images["Main Menu BG"], (Width, Height))

def save_settings():
    settings = load_json(["scripts", "data", "settings.json"])

    settings["FPS"] = FPS
    settings["Fullscreen"] = fullscreen
    settings["Resol"] = list(resol) if resol else None
    settings["Keys"] = keys
    settings["Brightness"] = set_brightness
    settings["Volumes"] = volumes

    dump_json(["scripts", "data", "settings.json"], settings)

def debug(last_call, player=None, enemies=[], rect_list=[], scroll=[0, 0]):
    fps = str(int(1/(time.time()-last_call)))
    # ticks = (time.time() - last_call)*dt

    if player:
        pos = f"{int(player.x)}X, {int(player.y)}Y"
        pos = pos.strip("'")
    else:
        pos = "Nonexistent"

    fps_text = Text(3, 3, f"FPS: {fps}", os.path.join("assets", "fonts", "DefaultFont.TTF"), 24, (255,255,255))
    #ticks_text = Text(3, 3, f"Ticks: {ticks}", os.path.join("assets", "fonts", "DefaultFont.TTF"), 24, (255,255,255))
    pos_text = Text(3, 3, f"Pos: {pos}", os.path.join("assets", "fonts", "DefaultFont.TTF"), 24, (255,255,255))
    room_text = Text(3, 3, f"Room: {Player.location}", os.path.join("assets", "fonts", "DefaultFont.TTF"), 24, (255,255,255))
    #fps_text = Text(3, 3, f"FPS: {fps}", os.path.join("assets", "fonts", "Font.png"), (255,255,255))
    #ticks_text = Text(3, 3, f"Ticks: {ticks}", os.path.join("assets", "fonts", "Font.png"), (255,255,255))
    #pos_text = Text(3, 3, f"Pos: {pos}", os.path.join("assets", "fonts", "Font.png"), (255,255,255))
    #room_text = Text(3, 3, f"Room: {Player.location}", os.path.join("assets", "fonts", "Font.png"), (255,255,255))
    

    def show_fps():
        surf = pygame.Surface((fps_text.get_width()+6, fps_text.get_height()+6))
        surf.fill((100,100,100))
        surf.set_alpha(200)
        fps_text.render(surf)
        win.blit(surf, (10, Height-fps_text.get_height()-75))
    '''def show_ticks():
        surf = pygame.Surface((ticks_text.get_width()+6, ticks_text.get_height()+6))
        surf.fill((100,100,100))
        surf.set_alpha(200)
        ticks_text.render(surf)
        win.blit(surf, (10, Height-ticks_text.get_height()-75))'''
    def player_pos():
        surf = pygame.Surface((pos_text.get_width()+6, pos_text.get_height()+6))
        surf.fill((100,100,100))
        surf.set_alpha(200)
        pos_text.render(surf)
        win.blit(surf, (10, Height-pos_text.get_height()-45))
    def room_name():
        surf = pygame.Surface((room_text.get_width()+6, room_text.get_height()+6))
        surf.fill((100,100,100))
        surf.set_alpha(200)
        room_text.render(surf)
        win.blit(surf, (10, Height-room_text.get_height()-15))
    def show_hitbox():
        def draw(_list):
            for rect in _list:
                if type(rect) == pygame.Rect:
                    pygame.draw.rect(win, (0, 255, 0), (rect.x-scroll[0], rect.y-scroll[1], rect.width, rect.height), 1)
                elif type(rect) == Polygon:
                    draw_poly(win, (0, 255, 0), rect, scroll)
                elif type(rect) == Projectiles:
                    draw_obb(win, (0, 255, 0), rect.obb, scroll)
                elif type(rect) == list:
                    draw(rect)
                else:
                    pygame.draw.rect(win, (0, 255, 0), (rect.rect.x-scroll[0], rect.rect.y-scroll[1], rect.rect.width, rect.rect.height), 1)
        if player:
            pygame.draw.rect(win, (0, 255, 0), (player.x-scroll[0], player.y-scroll[1], player.rect.width, player.rect.height), 1)
        for rects in rect_list:
            draw(rects)
        for enemy in enemies:
            pygame.draw.rect(win, (255,0,0), (enemy.view_rect.x-scroll[0], enemy.view_rect.y-scroll[1], enemy.view_rect.width, enemy.view_rect.height), 2)
    def show_middle():
        pygame.draw.line(win, (128,128,128), (0, Height*0.5), (Width, Height*0.5))
        pygame.draw.line(win, (128,128,128), (Width*0.5, 0), (Width*0.5, Height))

    show_fps()
    #show_ticks()
    player_pos()
    room_name()
    if show_hitboxes:
        show_hitbox()
    if show_mid:
        show_middle()

def save_game(pick_ups):
    data = {
        "gender": Player.gender,
        "class": Player.Pclass,
        "difficulty": Player.difficulty,
        "name": Player.name,
        "inventory": Player.inventory,
        "equipment": Player.equipment,
        "stats": Player.stats,
        "location": Player.location,
    }
    dump_json(["scripts", "data", "save.json"], data)
    if pick_ups:
        dump_json(["scripts", "data", "pick ups.json"], pick_ups)

def load_new_game():
    Player.location = "House 1"

    pick_ups = load_json(["scripts", "data", "pick ups.json"])

    for room, items in pick_ups.items():
        for item in items.keys():
            pick_ups[room][item] = False

    save_game(pick_ups)
    main_game("House 1")

def fade_in(func, speed=1):
    fade = pygame.Surface((Width, Height))
    fade.fill((0,0,0))
    opacity = 300
    for _ in range(0, int(300/speed)):
        opacity -= speed
        fade.set_alpha(opacity)
        func()
        win.blit(fade, (0,0))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        if opacity <= set_brightness:
            break
        pygame.display.flip()

def fade_out(func, speed=1):
    fade = pygame.Surface((Width, Height))
    fade.fill((0,0,0))
    opacity = set_brightness
    for _ in range(0, int(300/speed)):
        opacity += speed
        fade.set_alpha(opacity)
        func()
        win.blit(fade, (0,0))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        if opacity >= 300:
            break
        pygame.display.flip()

# Game Functions
def pause(func, pick_ups):
    global Width, Height
    set_button_over = False
    strt_button_over = False
    return_button_over = False
    returned = False

    brightness_foreground = Brightness((0, 0), (Width, Height), brightness=200, color=-1)

    w1 = 400-(50*3)
    w2 = w1*0.25

    button_set = Button(((Width*0.5)-(400*0.5))+w2, Height*0.5+20, 50, 50, (0,0,0))
    button_strt = Button(((Width*0.5)-(400*0.5))+37.5+(w2*2), Height*0.5-5, 75, 75, (0,0,0))
    button_return = Button(((Width*0.5)-(400*0.5))+(50*2)+(w2*3), Height*0.5+20, 50, 50, (0,0,0))

    pause_text = Text(0, 0, "Paused Game", os.path.join("assets", "fonts", "DefaultFont.TTF"), 28, (255,255,255))
    #pause_text = Text(0, 0, "Paused Game", os.path.join("assets", "fonts", "Font.png"), (255,255,255))

    last_call = time.time()
    def redraw():
        func()

        display_size = pygame.display.get_surface().get_size()
        Width, Height = display_size

        brightness_foreground.draw(win)

        try:
            loc = Player.location.split(" ")
        except AttributeError:
            loc = [None]

        if loc[0] == "House":
            pygame.draw.rect(win, (216, 201, 86), ((Width*0.5)-(400*0.5), (Height*0.5)-(200*0.5), 400, 200))
        else:
            pygame.draw.rect(win, (0, 0, 0), ((Width*0.5)-(400*0.5), (Height*0.5)-(200*0.5), 400, 200))
        pygame.draw.rect(win, (255,255,255), ((Width*0.5)-(400*0.5)-1, (Height*0.5)-(200*0.5)-1, 401, 201), 3)

        button_set.x, button_set.y = ((Width*0.5)-(400*0.5))+w2, Height*0.5+20; button_set.rect.x, button_set.rect.y = button_set.x, button_set.y
        button_strt.x, button_strt.y = ((Width*0.5)-(400*0.5))+37.5+(w2*2), Height*0.5-5; button_strt.rect.x, button_strt.rect.y = button_strt.x, button_strt.y
        button_return.x, button_return.y = ((Width*0.5)-(400*0.5))+(50*2)+(w2*3), Height*0.5+20; button_return.rect.x, button_return.rect.y = button_return.x, button_return.y
        pause_text.x, pause_text.y = (Width*0.5)-(pause_text.get_width()*0.5), (Height*0.5)-(200*0.5)+20

        if not set_button_over:
            win.blit(images["SettingsNOver"], (button_set.x, button_set.y))
        else:
            win.blit(images["SettingsOver"], (button_set.x, button_set.y))
        if not strt_button_over:
            win.blit(images["ResumeNOver"], (button_strt.x, button_strt.y))
        else:
            win.blit(images["ResumeOver"], (button_strt.x, button_strt.y))
        if not return_button_over:
            win.blit(images["ReturnNOver"], (button_return.x, button_return.y))
        else:
            win.blit(images["ReturnOver"], (button_return.x, button_return.y))

        pause_text.render(win)

        brightness_overlay.draw(win)

    while 1:
        if time.time() - last_call >= 1/FPS:
            if returned:
                return
            redraw()

            for event in pygame.event.get():
                mx, my = pygame.mouse.get_pos()
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN and event.key == keys["Pause"]:
                    return

                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if button_set.isOver([mx, my]):
                            settings_menu()
                        if button_strt.isOver([mx, my]):
                            return
                        if button_return.isOver([mx, my]):
                            returned = True
                            save_game(pick_ups)
                            main_menu()

                if event.type == MOUSEMOTION:
                    if button_set.isOver([mx, my]):
                        set_button_over = True
                    else:
                        set_button_over = False
                    if button_strt.isOver([mx, my]):
                        strt_button_over = True
                    else:
                        strt_button_over = False
                    if button_return.isOver([mx, my]):
                        return_button_over = True
                    else:
                        return_button_over = False
                    
            pygame.display.flip()
            last_call = time.time()

def popup():
    txts = [
        Text(0, 0, "To experience the full 1.5 update, please do the following", "comicsans", 64, (255,255,255)),
        Text(0, 0, "You can copy the " + '"1.5 save.json" (but first rename it to "save.json", this is important) and move it to ".\\scripts\\data\\"', "comicsans", 32, (255,255,255)),
        Text(0, 0, "Press any button to continue", "comicsans", 28, (255,255,255))
    ]
    for i, txt in enumerate(txts):
        txt.x = Width*0.5-txt.get_width()*0.5
        txt.y = Height*0.5-txt.get_height()*0.5 + i*60

    last_call = time.time()

    def redraw():
        win.fill((0, 0, 0))
        for txt in txts:
            txt.render(win)
    
    while 1:
        if time.time() - last_call >= 1/FPS:
            redraw()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit(); sys.exit()
                
                if event.type == KEYDOWN:
                    return

            pygame.display.flip()


def main_menu():
    global debug_menu
    set_button_over = False
    exit_button_over = False

    button_new = Button((Width*0.5)-(400*0.5), (Height*0.5)-(70*0.5), 400, 70, (0,0,0), "New Game", outline=(255,255,255), font_path=os.path.join("assets", "fonts", "DefaultFont.TTF"))
    if os.path.isfile(os.path.join("scripts", "data", "save.json")):
        button_load = Button((Width*0.5)-(400*0.5), (Height*0.5)-(70*0.5)+100, 400, 70, (0,0,0), "Load Game", outline=(255,255,255), font_path=os.path.join("assets", "fonts", "DefaultFont.TTF"))
    else:
        button_load = Button((Width*0.5)-(400*0.5), (Height*0.5)-(70*0.5)+100, 400, 70, (0,0,0), "Load Game", (128,128,128), (128,128,128), font_path=os.path.join("assets", "fonts", "DefaultFont.TTF"))

    button_tutor = Button((Width*0.5)-(400*0.5), (Height*0.5)-(70*0.5)+200, 400, 70, (0,0,0), "Tutorial", outline=(255,255,255), font_path=os.path.join("assets", "fonts", "DefaultFont.TTF"))
    button_set = Button(25, Height-75, 50, 50, (0,0,0))
    button_exit = Button(Width-75, Height-75, 50, 50, (0,0,0))

    musics["Music Main"].start()

    text = Text(0, 100, "Inseynia", os.path.join("assets", "fonts", "DefaultFont.TTF"), 72, (255,255,255))
    version_text = Text(0, 0, "Version Indev 1.5", os.path.join("assets", "fonts", "DefaultFont.TTF"), 18, (50, 50, 50))
    #text = Text(0, 100, "Inseynia", os.path.join("assets", "fonts", "Font.png"), (255,255,255))

    last_call = time.time()
    def redraw():
        win.fill((0,0,0))
        display_size = pygame.display.get_surface().get_size()
        Width, Height = display_size
        
        win.blit(images["Main Menu BG"], (0,0))

        text.x = (Width*0.5)-(text.get_width()*0.5)
        text.render(win)

        version_text.x, version_text.y = (Width*0.5)-(version_text.get_width()*0.5), Height-version_text.get_height()-20
        version_text.render(win)

        button_new.x, button_new.y = (Width*0.5)-(400*0.5), (Height*0.5)-(70*0.5); button_new.rect.x, button_new.rect.y = button_new.x, button_new.y
        button_tutor.x, button_tutor.y = (Width*0.5)-(400*0.5), (Height*0.5)-(70*0.5)+200; button_tutor.rect.x, button_tutor.rect.y = button_tutor.x, button_tutor.y
        button_load.x, button_load.y = (Width*0.5)-(400*0.5), (Height*0.5)-(70*0.5)+100; button_load.rect.x, button_load.rect.y = button_load.x, button_load.y
        button_set.x, button_set.y = 25, Height-75; button_set.rect.x, button_set.rect.y = button_set.x, button_set.y
        button_exit.x, button_exit.y = Width-75, Height-75; button_exit.rect.x, button_exit.rect.y = button_exit.x, button_exit.y

        button_new.draw(win)
        button_tutor.draw(win)
        button_load.draw(win)

        if set_button_over:
            win.blit(images["SettingsOver"], (button_set.x, button_set.y))
        else:
            win.blit(images["SettingsNOver"], (button_set.x, button_set.y))
        
        if exit_button_over:
            win.blit(images["QuitOver"], (button_exit.x, button_exit.y))
        else:
            win.blit(images["QuitNOver"], (button_exit.x, button_exit.y))

        if debug_menu:
            debug(last_call)

        brightness_overlay.draw(win)

    while 1:
        if time.time() - last_call >= 1/FPS:
            redraw()
            
            for event in pygame.event.get():
                mx, my = pygame.mouse.get_pos()
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    if event.key == K_F11:
                        F11()
                    if event.key == K_F3:
                        debug_menu = not debug_menu
                    if event.key == K_c:
                        credits()

                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if button_new.isOver([mx, my]):
                            story()

                        if button_tutor.isOver([mx, my]):
                            pass
                        
                        if button_set.isOver([mx, my]):
                            settings_menu()
                        
                        if button_exit.isOver([mx, my]):
                            pygame.quit()
                            sys.exit()
                
                if event.type == MOUSEBUTTONUP:
                    if event.button == 1:
                        if button_load.isOver([mx, my]):
                                return True

                if event.type == MOUSEMOTION:
                    if button_new.isOver([mx, my]):
                        button_new.change_color((0, 128, 0))
                    else:
                        button_new.change_color((0, 0, 0))

                    if button_tutor.isOver([mx, my]):
                        button_tutor.change_color((128, 0, 128))
                    else:
                        button_tutor.change_color((0,0,0))

                    if os.path.isfile(os.path.join("scripts", "data", "save.json")):
                        if button_load.isOver([mx, my]):
                            button_load.change_color((0, 0, 128))
                        else:
                            button_load.change_color((0,0,0))

                    if button_set.isOver([mx, my]):
                        set_button_over = True
                    else:
                        set_button_over = False
                    
                    if button_exit.isOver([mx, my]):
                        exit_button_over = True
                    else:
                        exit_button_over = False

            pygame.display.flip()
            last_call = time.time()

def settings_menu():
    global FPS
    def global_redraw():
        win.fill((0,0,0))
        win.blit(images["Main Menu BG"], (0,0))

    def debugg(last_call):
        if debug_menu:
            debug(last_call)


    def main():
        global debug_menu, last_call

        button_video = Button((Width*0.5)-(400*0.5), (Height*0.5)-(70*0.5), 400, 70, (0,0,0), "Video", outline=(255,255,255), font_path=os.path.join("assets", "fonts", "DefaultFont.TTF"))
        button_volume = Button((Width*0.5)-(400*0.5), (Height*0.5)-(70*0.5)+100, 400, 70, (0,0,0), "Volume", outline=(255,255,255), font_path=os.path.join("assets", "fonts", "DefaultFont.TTF"))
        button_controls = Button((Width*0.5)-(400*0.5), (Height*0.5)-(70*0.5)+200, 400, 70, (0,0,0), "Controls", outline=(255,255,255), font_path=os.path.join("assets", "fonts", "DefaultFont.TTF"))
        button_back = Button((Width*0.5)-(200*0.5), (Height*0.5)-(35*0.5)+275, 200, 35, (0,0,0), "Back", outline=(255,255,255), font_path=os.path.join("assets", "fonts", "DefaultFont.TTF"))

        text = Text(0, 100, "Settings", os.path.join("assets", "fonts", "DefaultFont.TTF"), 72, (255,255,255))
        #text = Text(0, 100, "Settings", os.path.join("assets", "fonts", "Font.png"), (255,255,255))

        last_call = time.time()
        def redraw():
            global_redraw()

            display_size = pygame.display.get_surface().get_size()
            Width, Height = display_size

            text.x = (Width*0.5)-(text.get_width()*0.5)
            text.render(win)

            button_video.x, button_video.y = (Width*0.5)-(400*0.5), (Height*0.5)-(70*0.5); button_video.rect.x, button_video.rect.y = button_video.x, button_video.y
            button_volume.x, button_volume.y = (Width*0.5)-(400*0.5), (Height*0.5)-(70*0.5)+100; button_volume.rect.x, button_volume.rect.y = button_volume.x, button_volume.y
            button_controls.x, button_controls.y = (Width*0.5)-(400*0.5), (Height*0.5)-(70*0.5)+200; button_controls.rect.x, button_controls.rect.y = button_controls.x, button_controls.y
            button_back.x, button_back.y = (Width*0.5)-(200*0.5), (Height*0.5)-(35*0.5)+275; button_back.rect.x, button_back.rect.y = button_back.x, button_back.y

            button_video.draw(win)
            button_volume.draw(win)
            button_controls.draw(win)
            button_back.draw(win)

            debugg(last_call)
            brightness_overlay.draw(win)

        while 1:
            if time.time() - last_call >= 1/FPS:
                redraw()
                for event in pygame.event.get():
                    mx, my = pygame.mouse.get_pos()
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == KEYDOWN:
                        if event.key == K_F11:
                            F11()
                        if event.key == K_F3:
                            debug_menu = not debug_menu

                    if event.type == MOUSEBUTTONDOWN:
                        if event.button == 1:
                            if button_video.isOver([mx, my]):
                                video_settings()

                            if button_volume.isOver([mx, my]):
                                volume_settings()
                            
                            if button_controls.isOver([mx, my]):
                                controls()
                            
                            if button_back.isOver([mx, my]):
                                return
                            
                    if event.type == MOUSEMOTION:
                        if button_video.isOver([mx, my]):
                            button_video.change_color((0, 128, 0))
                        else:
                            button_video.change_color((0,0,0))

                        if button_volume.isOver([mx, my]):
                            button_volume.change_color((128, 0, 128))
                        else:
                            button_volume.change_color((0,0,0))

                        if button_controls.isOver([mx, my]):
                            button_controls.change_color((0, 0, 128))
                        else:
                            button_controls.change_color((0,0,0))

                        if button_back.isOver([mx, my]):
                            button_back.change_color((128, 0, 0))
                        else:
                            button_back.change_color((0, 0, 0))

                pygame.display.flip()

                last_call = time.time()

    def video_settings():
        global fullscreen, resol, FPS, set_brightness, debug_menu, last_call
        fullscreen_init = fullscreen
        resol_init = resol
        FPS_init = FPS
        brightness_init = set_brightness
        
        resolutions = [
            None,
            (1920, 1080),
            (1600, 900),
            (1280, 720),
            (1024, 768),
            (960, 720),
            (800, 600)
        ]
        resol_index = resolutions.index(resol)

        resol_rect = pygame.Rect((Width*0.5)-(400*0.5), (Height*0.5)-(70*0.5)-75, 400, 70)
        resol_front = Button((Width*0.5)-(400*0.5)+425, (Height*0.5)-(70*0.5)-75, 100, 70, (128,128,128))
        resol_back = Button((Width*0.5)-(400*0.5)-125, (Height*0.5)-(70*0.5)-75, 100, 70, (128,128,128))

        button_fullscreen = Button((Width*0.5)-(500*0.5), (Height*0.5)-(70*0.5), 500, 70, (0,0,0), "Fullscreen", outline=(255,255,255), font_path=os.path.join("assets", "fonts", "DefaultFont.TTF"))
        button_back = Button((Width*0.5)-(200*0.5)-175, (Height*0.5)-(35*0.5)+275, 200, 35, (0,0,0), "Back", outline=(255,255,255), font_path=os.path.join("assets", "fonts", "DefaultFont.TTF"))
        button_apply = Button((Width*0.5)-(200*0.5)+175, (Height*0.5)-(35*0.5)+275, 200, 35, (0,0,0), "Apply", outline=(255,255,255), font_path=os.path.join("assets", "fonts", "DefaultFont.TTF"))

        button_yes = Button((Width*0.5)-(400*0.5)+50, (Height*0.5)-(250*0.5)+170, 75, 35, (0,128,0), "Yes", outline=(255,255,255), font_path=os.path.join("assets", "fonts", "DefaultFont.TTF"))
        button_no = Button((Width*0.5)-(400*0.5)+275, (Height*0.5)-(250*0.5)+170, 75, 35, (128,0,0), "No", outline=(255,255,255), font_path=os.path.join("assets", "fonts", "DefaultFont.TTF"))
        AYS = False
        AYS_text = Text(0, 0, "Are You Sure?",  os.path.join("assets", "fonts", "DefaultFont.TTF"), 28, (255,255,255))
        #AYS_text = Text(0, 0, "Are You Sure?",  os.path.join("assets", "fonts", "Font.png"), (255,255,255))
        ASYI_texts = [
            Text(0, 0, "The game was not optimized for",  os.path.join("assets", "fonts", "DefaultFont.TTF"), 11, (255,255,255)),
            Text(0, 0, "resolutions over 1080p, so a lot",  os.path.join("assets", "fonts", "DefaultFont.TTF"), 11, (255,255,255)),
            Text(0, 0, "of bugs might appear.",  os.path.join("assets", "fonts", "DefaultFont.TTF"), 11, (255,255,255)),
            Text(0, 0, "Are you willing to continue?",  os.path.join("assets", "fonts", "DefaultFont.TTF"), 16, (255,255,255)),
            #Text(0, 0, "The game was not optimized for",  os.path.join("assets", "fonts", "Font.png"), (255,255,255)),
            #Text(0, 0, "resolutions over 1080p, so a lot",  os.path.join("assets", "fonts", "Font.png"), (255,255,255)),
            #Text(0, 0, "of bugs might appear.",  os.path.join("assets", "fonts", "Font.png"), (255,255,255)),
            #Text(0, 0, "Are you willing to continue?",  os.path.join("assets", "fonts", "Font.png"), (255,255,255))
        ]

        if FPS_init == 10:
            slider_FPS = SliderX((Width*0.5)-(500*0.5), (Height*0.5)-(70*0.5)+100, 500, 70, (0,0,0), 40, (99, 155, 255), "FPS")
        elif FPS_init == 2147483647:
            slider_FPS = SliderX((Width*0.5)-(500*0.5), (Height*0.5)-(70*0.5)+100, 500, 70, (0,0,0), 500, (99, 155, 255), "FPS")
        else:
            slider_FPS = SliderX((Width*0.5)-(500*0.5), (Height*0.5)-(70*0.5)+100, 500, 70, (0,0,0), int(FPS_init*2), (99, 155, 255), "FPS")

        slider_brightness = SliderX((Width*0.5)-(500*0.5), (Height*0.5)-(70*0.5)+200, 500, 70, (0,0,0), 0, (128, 0, 0), "brightness")
        slider_brightness.width2 = int((((brightness_init + 200) / 2.5) / 100) * (slider_brightness.width-40)+40)

        slider_FPS_slide = False
        slider_brightness_slide = False
        
        video_text = Text(0, 50, "Video Settings", os.path.join("assets", "fonts", "DefaultFont.TTF"), 48, (255,255,255))
        resol_text = Text(0, 0, "", os.path.join("assets", "fonts", "DefaultFont.TTF"), 32, (255,255,255))
        #video_text = Text(0, 50, "Video Settings", os.path.join("assets", "fonts", "Font.png"), (255,255,255))
        #resol_text = Text(0, 0, "", os.path.join("assets", "fonts", "Font.png"), (255,255,255))

        brightness_slider = Brightness((slider_brightness.x-2, slider_brightness.y-2), (slider_brightness.width+5, slider_brightness.height+5), abs(brightness_init), brightness_init)
        brightness_foreground = Brightness((0, 0), (Width, Height), brightness=200, color=-1)

        last_call = time.time()
        def redraw():
            global_redraw()

            if fullscreen_init:
                button_fullscreen.change_text("Fullscreen On")
            elif not fullscreen_init:
                button_fullscreen.change_text("Fullscreen Off")

            display_size = pygame.display.get_surface().get_size()
            Width, Height = display_size

            video_text.x = (Width*0.5)-(video_text.get_width()*0.5)
            video_text.render(win)

            button_fullscreen.x, button_fullscreen.y = (Width*0.5)-(500*0.5), (Height*0.5)-(70*0.5); button_fullscreen.rect.x, button_fullscreen.rect.y = button_fullscreen.x, button_fullscreen.y
            button_back.x, button_back.y = (Width*0.5)-(200*0.5)-175, (Height*0.5)-(35*0.5)+275; button_back.rect.x, button_back.rect.y = button_back.x, button_back.y
            button_apply.x, button_apply.y = (Width*0.5)-(200*0.5)+175, (Height*0.5)-(35*0.5)+275; button_apply.rect.x, button_apply.rect.y = button_apply.x, button_apply.y

            resol_front.x, resol_front.y = (Width*0.5)-(400*0.5)+425, (Height*0.5)-(70*0.5)-100; resol_front.rect.x, resol_front.rect.y = resol_front.x, resol_front.y
            resol_back.x, resol_back.y = (Width*0.5)-(400*0.5)-125, (Height*0.5)-(70*0.5)-100; resol_back.rect.x, resol_back.rect.y = resol_back.x, resol_back.y
            resol_rect.x, resol_rect.y = (Width*0.5)-(400*0.5), (Height*0.5)-(70*0.5)-100

            slider_FPS.x, slider_FPS.y = (Width*0.5)-(500*0.5), (Height*0.5)-(70*0.5)+100; slider_FPS.rect.x, slider_FPS.rect.y = slider_FPS.x, slider_FPS.y
            slider_brightness.x, slider_brightness.y = (Width*0.5)-(500*0.5), (Height*0.5)-(70*0.5)+200; slider_brightness.rect.x, slider_brightness.rect.y = slider_brightness.x, slider_brightness.y
            
            button_yes.x, button_yes.y = (Width*0.5)-(400*0.5)+50, (Height*0.5)-(250*0.5)+170; button_yes.rect.x, button_yes.rect.y = button_yes.x, button_yes.y
            button_no.x, button_no.y = (Width*0.5)-(400*0.5)+275, (Height*0.5)-(250*0.5)+170; button_no.rect.x, button_no.rect.y = button_no.x, button_no.y
            
            if not FPS_init == 2147483647:
                slider_FPS.text = f"{FPS_init} FPS"
            else:
                slider_FPS.text = "Unlimited FPS"

            slider_brightness.text = f"Brightness {int(((slider_brightness.width2-40)/(slider_brightness.width-40))*100)}%"

            win.blit(images["Next Resol"], (resol_front.x, resol_front.y))
            win.blit(images["Previous Resol"], (resol_back.x, resol_back.y))
            pygame.draw.rect(win, (255,255,255), resol_rect, 3)
            if not resol_init:
                resol_text.text = "Current"
            else:
               resol_text.text = f"{resol_init[0]}x{resol_init[1]}"
            resol_text.x, resol_text.y = (Width*0.5)-(resol_text.get_width()*0.5), (Height*0.5)-(resol_text.get_height()*0.5)-100
            resol_text.render(win)

            if platform.system() == "Windows": button_fullscreen.draw(win)
            button_back.draw(win)
            button_apply.draw(win)

            slider_FPS.draw(win, (255,255,255), font_name=os.path.join("assets", "fonts", "DefaultFont.TTF"))
            
            if not AYS:
                debugg(last_call)
                brightness_overlay.draw(win)
            
            slider_brightness.draw(win, (255,255,255), font_name=os.path.join("assets", "fonts", "DefaultFont.TTF"))

            brightness_slider.draw(win)

            if AYS:
                brightness_foreground.draw(win)
                pygame.draw.rect(win, (0, 0, 0), ((Width*0.5)-(400*0.5), (Height*0.5)-(250*0.5), 400, 250))
                pygame.draw.rect(win, (255,255,255), ((Width*0.5)-(400*0.5)-1, (Height*0.5)-(250*0.5)-1, 401, 251), 3)

                AYS_text.x, AYS_text.y = (Width*0.5)-(AYS_text.get_width()*0.5), (Height*0.5)-(250*0.5)+20
                x = 80
                for AYSI_text in ASYI_texts:
                    AYSI_text.x, AYSI_text.y = (Width*0.5)-(AYSI_text.get_width()*0.5), (Height*0.5)-(250*0.5)+x
                    AYSI_text.render(win)
                    x += 15
                

                button_yes.draw(win)
                button_no.draw(win)
                AYS_text.render(win)
                
                debugg(last_call)
                brightness_overlay.draw(win)
        while 1:
            if time.time() - last_call >= 1/FPS:
                if not brightness_init:
                    brightness_init = 1
                redraw()

                mx, my = pygame.mouse.get_pos()

                if slider_FPS.width2 > slider_FPS.width:
                    slider_FPS.width2 = slider_FPS.width
                if slider_brightness.width2 > slider_brightness.width:
                    slider_brightness.width2 = slider_brightness.width
                
                if slider_FPS_slide:
                    slider_FPS.move([mx, my])
                if slider_FPS.width2 <= 40:
                    FPS_init = 10
                elif slider_FPS.width2 >= slider_FPS.width:
                    FPS_init = 2147483647
                else:
                    FPS_init = int(slider_FPS.width2*0.5)
                
                if slider_brightness_slide:
                    slider_brightness.move([mx, my])
                    brightness_slider.reconfigure(brightness=abs(brightness_init), color=brightness_init)
                if slider_brightness.width2 <= 40:
                    brightness_init = -200
                elif slider_brightness.width2 >= slider_brightness.width:
                    brightness_init = 50
                else:
                    brightness_init = int(2.5*((slider_brightness.width2-40)/(slider_brightness.width-40)*100)-200)

                brightness_overlay.reconfigure(brightness=set_brightness)

                for event in pygame.event.get():
                    mx, my = pygame.mouse.get_pos()
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == KEYDOWN:
                        if event.key == K_F11:
                            F11()
                            fullscreen_init = fullscreen
                        if event.key == K_F3:
                            debug_menu = not debug_menu
                        if event.key == K_RETURN:
                            F11(fullscreen_param=fullscreen_init)
                            change_resol(resol_init)
                            brightness_foreground.reconfigure(size=(Width, Height))

                            FPS = FPS_init
                            resol = resol_init
                            fullscreen = fullscreen_init
                            set_brightness = brightness_init
                            save_settings()

                    if event.type == MOUSEBUTTONDOWN:
                        if event.button == 1 and not AYS:
                            if button_fullscreen.isOver([mx, my]) and platform.system() == "Windows":
                                fullscreen_init = not fullscreen_init

                            if resol_front.isOver([mx, my]):
                                resol_index += 1
                                try:
                                    resol_init = resolutions[resol_index]
                                except IndexError:
                                    resol_index = 0
                                    resol_init = resolutions[resol_index]
                            
                            if resol_back.isOver([mx, my]):
                                resol_index -= 1
                                try:
                                    resol_init = resolutions[resol_index]
                                except IndexError:
                                    resol_index = len(resolutions)-1
                                    resol_init = resolutions[resol_index]
                            
                            if slider_FPS.isOver([mx, my]):
                                slider_FPS_slide = True

                            if slider_brightness.isOver([mx, my]):
                                slider_brightness_slide = True

                            if button_back.isOver([mx, my]):
                                return

                            if button_apply.isOver([mx, my]):
                                if not resol_init:
                                    AYS = True
                                    button_apply.change_color((0,0,0))
                                else:
                                    F11(fullscreen_param=fullscreen_init)
                                    change_resol(resol_init)
                                    brightness_foreground.reconfigure(size=(Width, Height))

                                    FPS = FPS_init
                                    resol = resol_init
                                    fullscreen = fullscreen_init
                                    set_brightness = brightness_init
                                    save_settings()
                            
                        if (event.button == 4 and not AYS) or (event.button == 5 and not AYS):
                            if slider_FPS.isOver([mx, my]):
                                slider_FPS.scroll(event.button, 4)
                            
                            if slider_brightness.isOver([mx, my]):
                                slider_brightness.scroll(event.button, 4)

                        if event.button == 1 and AYS:
                            if button_yes.isOver([mx, my]):
                                F11(fullscreen_param=fullscreen_init)
                                change_resol(resol_init)
                                FPS = FPS_init
                                resol = resol_init
                                fullscreen = fullscreen_init
                                set_brightness = brightness_init
                                save_settings()
                                AYS = False
                            if button_no.isOver([mx, my]):
                                AYS = False

                    if event.type == MOUSEBUTTONUP:
                        if event.button == 1 and not AYS:
                            slider_FPS_slide = False
                            slider_brightness_slide = False

                    if event.type == MOUSEMOTION:
                        if not AYS:
                            if button_fullscreen.isOver([mx, my]):
                                button_fullscreen.change_color((0, 128, 128))
                            else:
                                button_fullscreen.change_color((0,0,0))

                            if button_back.isOver([mx, my]):
                                button_back.change_color((128, 0, 0))
                            else:
                                button_back.change_color((0, 0, 0))

                            if button_apply.isOver([mx, my]):
                                button_apply.change_color((0, 128, 0))
                            else:
                                button_apply.change_color((0, 0, 0))

                pygame.display.flip()

                last_call = time.time()

    def volume_settings():
        global debug_menu, last_call

        #slider_master = SliderX((0,0,0), (Width*0.5)-(700*0.5), (Height*0.5)-(100*0.5)-25, 700, 100, (128,128,0), 700*0.5, "Master Volume")
        slider_music = SliderX((Width*0.5)-650*0.5, (Height*0.5)-(70*0.5), 650, 70, (0,0,0), 0, (0,128,0), "Music")
        slider_music.width2 = musics["Music Main"].volume*(slider_music.width-40)+40
        slider_sfx = SliderX((Width*0.5)-650*0.5, (Height*0.5)-(70*0.5)+100, 650, 70, (0,0,0), 325*0.5, (0,128,128), "SFX")

        slider_music_slide = False
        slider_sfx_slide = False

        button_back = Button((Width*0.5)-(200*0.5), (Height*0.5)-(35*0.5)+275, 200, 35, (0,0,0), "Back", outline=(255,255,255), font_path=os.path.join("assets", "fonts", "DefaultFont.TTF"))

        text = Text(0, 100, "Volume Settings", os.path.join("assets", "fonts", "DefaultFont.TTF"), 48, (255,255,255))
        text.x = Width*0.5-text.get_width()*0.5
        #text = Text(0, 100, "Volume Settings", os.path.join("assets", "fonts", "Font.png"), (255,255,255))

        last_call = time.time()
        def redraw():
            global_redraw()

            text.render(win)

            slider_music.text = f"Music: {int(musics['Music Main'].volume*100)}%"

            slider_music.draw(win, (255,255,255), font_name=os.path.join("assets", "fonts", "DefaultFont.TTF"))
            slider_sfx.draw(win, (255,255,255), font_name=os.path.join("assets", "fonts", "DefaultFont.TTF"))

            button_back.draw(win)
        
            debugg(last_call)
            brightness_overlay.draw(win)
        
        while 1:
            if time.time() - last_call >= 1/FPS:
                redraw()

                mx, my = pygame.mouse.get_pos()

                if slider_music_slide:
                    slider_music.move([mx, my])
                if slider_music.width2 <= 40:
                    volumes["Music"] = 0
                elif slider_music.width2 >= slider_music.width:
                    volumes["Music"] = 1
                else:
                    volumes["Music"] = (slider_music.width2-40)/(slider_music.width-40)

                for music in musics.values():
                    music.set_volume(volumes["Music"], True)
                
                if slider_sfx_slide:
                    slider_sfx.move([mx, my])

                for event in pygame.event.get():
                    mx, my = pygame.mouse.get_pos()
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == KEYDOWN:
                        if event.key == K_F11:
                            F11()
                        if event.key == K_F3:
                            debug_menu = not debug_menu

                    if event.type == MOUSEBUTTONDOWN:
                        if event.button == 1:
                            if slider_music.isOver([mx, my]):
                                slider_music_slide = True
                            
                            if slider_sfx.isOver([mx, my]):
                                slider_sfx_slide = True

                            if button_back.isOver([mx, my]):
                                return

                        if event.button == 4 or event.button == 5:
                            if slider_music.isOver([mx, my]):
                                slider_music.scroll(event.button, 4)
                            
                            if slider_sfx.isOver([mx, my]):
                                slider_sfx.scroll(event.button, 4)

                    if event.type == MOUSEBUTTONUP:
                        if event.button == 1:
                            if slider_music.isOver([mx, my]):
                                slider_music_slide = False
                            
                            if slider_sfx.isOver([mx, my]):
                                slider_sfx_slide = False

                    if event.type == MOUSEMOTION:
                        if button_back.isOver([mx, my]):
                            button_back.change_color((128, 0, 0))
                        else:
                            button_back.change_color((0, 0, 0))

                pygame.display.flip()

                last_call = time.time()
                save_settings()

    def controls():
        global debug_menu, last_call

        change = None

        new_key = None
        old_key = None
        
        buttons = {
            "Up": Button((Width*0.5)-(450*0.5), (Height*0.5)-160, 450, 35, (0,0,0), f"Up: {pygame.key.name(keys['Up'])}", outline=(255,255,255), font_path=os.path.join("assets", "fonts", "DefaultFont.TTF")),
            "Down": Button((Width*0.5)-(450*0.5), (Height*0.5)-115, 450, 35, (0,0,0), f"Down: {pygame.key.name(keys['Down'])}", outline=(255,255,255), font_path=os.path.join("assets", "fonts", "DefaultFont.TTF")),
            "Left": Button((Width*0.5)-(450*0.5), (Height*0.5)-25, 450, 35, (0,0,0), f"Left: {pygame.key.name(keys['Left'])}", outline=(255,255,255), font_path=os.path.join("assets", "fonts", "DefaultFont.TTF")),
            "Right": Button((Width*0.5)-(450*0.5), (Height*0.5)-70, 450, 35, (0,0,0), f"Right: {pygame.key.name(keys['Right'])}", outline=(255,255,255), font_path=os.path.join("assets", "fonts", "DefaultFont.TTF")),
            "Roll": Button((Width*0.5)-(450*0.5), (Height*0.5)-(35*0.5), 450, 35, (0,0,0), f"Roll: {pygame.key.name(keys['Roll'])}", outline=(255,255,255), font_path=os.path.join("assets", "fonts", "DefaultFont.TTF")),
            "Throw": Button((Width*0.5)-(450*0.5), (Height*0.5)+20, 450, 35, (0,0,0), f"Throw Item: {pygame.key.name(keys['Throw'])}", outline=(255,255,255), font_path=os.path.join("assets", "fonts", "DefaultFont.TTF")),
            "Equip": Button((Width*0.5)-(450*0.5), (Height*0.5)+65, 450, 35, (0,0,0), f"Equip/Unequip Item: {pygame.key.name(keys['Equip'])}", outline=(255,255,255), font_path=os.path.join("assets", "fonts", "DefaultFont.TTF")),
            "Switch": Button((Width*0.5)-(450*0.5), (Height*0.5)+110, 450, 35, (0,0,0), f"View Equipment/Inventory: {pygame.key.name(keys['Switch'])}", outline=(255,255,255), font_path=os.path.join("assets", "fonts", "DefaultFont.TTF")),
            "Pause": Button((Width*0.5)-(450*0.5), (Height*0.5)+155, 450, 35, (0,0,0), f"Pause Gme: {pygame.key.name(keys['Pause'])}", outline=(255,255,255), font_path=os.path.join("assets", "fonts", "DefaultFont.TTF"))
        }
        
        button_back = Button((Width*0.5)-(200*0.5), (Height*0.5)-(35*0.5)+275, 200, 35, (0,0,0), "Back", outline=(255,255,255), font_path=os.path.join("assets", "fonts", "DefaultFont.TTF"))

        text = Text(0, 50, "Controls", os.path.join("assets", "fonts", "DefaultFont.TTF"), 48, (255,255,255))
        #text = Text(0, 50, "Controls", os.path.join("assets", "fonts", "Font.png"), (255,255,255))

        last_call = time.time()
        def redraw():
            global_redraw()

            text.x = (Width*0.5)-(text.get_width()*0.5)
            text.render(win)

            if not change:
                for name in buttons.keys():
                    buttons[name].change_text(f"{name.capitalize()}: {pygame.key.name(keys[name]).capitalize()}")
            else:
                for name, button in buttons.items():
                    if name == change:
                        buttons[name].change_text("--Please Select A Key--")
                        break

            for button in buttons.values():
                button.draw(win)
            
            button_back.draw(win)
        
            debugg(last_call)
            brightness_overlay.draw(win)
        while 1:
            if time.time() - last_call >= 1/FPS:
                redraw()

                if change:
                    if new_key:
                        old_key = keys[change]
                        for name, key in keys.items():
                            if new_key == key and name != change:
                                keys[name] = old_key
                                old_key = None
                                break
                        keys[change] = new_key
                        change = None
                    save_settings()
                new_key = None

                for event in pygame.event.get():
                    mx, my = pygame.mouse.get_pos()
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == KEYDOWN:
                        if event.key == K_F11:
                            F11()
                        if event.key == K_F3:
                            debug_menu = not debug_menu
                        new_key = event.key

                    if event.type == MOUSEBUTTONDOWN:
                        if event.button == 1:
                            for name, button in buttons.items():
                                if button.isOver([mx, my]):
                                    change = name

                            if button_back.isOver([mx, my]):
                                return

                    if event.type == MOUSEMOTION:
                        if button_back.isOver([mx, my]):
                            button_back.change_color((128, 0, 0))
                        else:
                            button_back.change_color((0, 0, 0))

                pygame.display.flip()

                last_call = time.time()

    main()
    return

def new_game_creator():
    global debug_menu
    chosen_class = random.choice(["Swordsman", "Archer", "Mage"])
    chosen_difficulty = random.choice(["easy", "normal", "hard"])
    chosen_name = random.choice(["Akesta", "Jonea", "John Cena", "Elat", "Inora"])

    classes = [
        [Button((Width*0.5-144*0.5)-(144+92), 50, 144, 144, text="Swordsman"), pygame.transform.scale(images['Wooden Sword'], (144, 144))],
        [Button(Width*0.5-144*0.5, 50, 144, 144, text="Archer"), pygame.transform.scale(images["Crossbow"], (144, 144))],
        [Button((Width*0.5-144*0.5)+144+92, 50, 144, 144, text="Mage"), pygame.transform.scale(images['Wooden Shield'], (144, 144))]
    ]
    '''if settings["Permadeath Enabled"]:
        difficulties = [
            Button((Width*0.5)-360, 300, 150, 50, (0, 128, 0), "Easy"),
            Button((Width*0.5)-170, 300, 150, 50, (128, 64, 0), "Normal"),
            Button((Width*0.5)+20, 300, 150, 50, (128, 0, 0), "Hard"),
            Button((Width*0.5)+210, 300, 150, 50, (64, 0, 0), "Permadeath")
        ]
    else:
        difficulties = [
            Button((Width*0.5-150*0.5)-190, 300, 150, 50, (0, 128, 0), "Easy"),
            Button(Width*0.5-150*0.5, 300, 150, 50, (128, 64, 0), "Normal"),
            Button((Width*0.5-150*0.5)+190, 300, 150, 50, (128, 0, 0), "Hard")
        ]
    '''
    slider_difficulty = SliderX(Width*0.5-450*0.5, 300, 450, 50, color2=(0,128,0), text=f"Difficulty: {chosen_difficulty.capitalize()}")
    slider_difficulty_move = False

    name = TextBox((0,0,0), Width*0.5-250, 400, 500, 100, "Enter your username", clear_text_when_click=True)
    button_cancel = Button((Width*0.5)-(200*0.5)-175, (Height*0.5)-(35*0.5)+275, 200, 35, (0,0,0), "Cancel", outline=(255,255,255), font_path=os.path.join("assets", "fonts", "DefaultFont.TTF"))
    button_apply = Button((Width*0.5)-(200*0.5)+175, (Height*0.5)-(35*0.5)+275, 200, 35, (0,0,0), "Apply", outline=(255,255,255), font_path=os.path.join("assets", "fonts", "DefaultFont.TTF"))

    def redraw():
        win.fill((0,0,0))
        win.blit(images["Main Menu BG"], (0,0))

        for _class in classes:
            win.blit(_class[1], (_class[0].x, _class[0].y))
        '''for difficulty in difficulties:
            difficulty.draw(win, (255,255,255))
        '''
        slider_difficulty.text = f"Difficulty: {chosen_difficulty.capitalize()}"
        slider_difficulty.draw(win, (255,255,255))

        button_cancel.draw(win)
        button_apply.draw(win)

        #pygame.draw.line(win, (255,255,255), (Width*0.5, 0), (Width*0.5, Height))

        name.draw(win, (255,255,255))
    while 1:
        redraw()
        mx, my = pygame.mouse.get_pos()

        if slider_difficulty_move:
            if mx < slider_difficulty.x+40:
                slider_difficulty.width2 = 40
            elif mx > slider_difficulty.x+slider_difficulty.width:
                slider_difficulty.width2 = slider_difficulty.width
                slider_difficulty.selector_rect_x = slider_difficulty.x+slider_difficulty.width-40

            if settings["Permadeath Enabled"]:
                if mx-slider_difficulty.x <= 40:
                    slider_difficulty.width2 = 40
                elif mx-slider_difficulty.x > 40 and mx-slider_difficulty.x <= 150:
                    slider_difficulty.width2 = 150
                elif mx-slider_difficulty.x > 150 and mx-slider_difficulty.x <= 300:
                    slider_difficulty.width2 = 300
                elif mx-slider_difficulty.x > 300 and mx-slider_difficulty.x <= 450:
                    slider_difficulty.width2 = 450
            else:
                if mx-slider_difficulty.x <= 40:
                    slider_difficulty.width2 = 40
                elif mx-slider_difficulty.x > 40 and mx-slider_difficulty.x <= 225:
                    slider_difficulty.width2 = 225
                elif mx-slider_difficulty.x > 225 and mx-slider_difficulty.x <= 450:
                    slider_difficulty.width2 = 450
            

            #slider_difficulty.move([mx, my])
            #chosen_difficulty = slider_difficulty.set_value("easy", "hard", 0, "list", 150, ["easy", "normal", "hard"])

        if settings["Permadeath Enabled"]:
            if slider_difficulty.width2 == 40:
                chosen_difficulty = "easy"
                slider_difficulty.color2 = (0, 128, 0)
            elif slider_difficulty.width2 > 40 and slider_difficulty.width2 < 225:
                chosen_difficulty = "normal"
                slider_difficulty.color2 = (128, 64, 0)
            elif slider_difficulty.width2 >= 225 and slider_difficulty.width2 < 450:
                chosen_difficulty = "hard"
                slider_difficulty.color2 = (128, 0, 0)
            elif slider_difficulty.width2 == 450:
                chosen_difficulty = "permadeath"
                slider_difficulty.color2 = (64, 0, 0)
        else:
            if slider_difficulty.width2 == 40:
                chosen_difficulty = "easy"
                slider_difficulty.color2 = (0, 128, 0)
            elif slider_difficulty.width2 > 40 and slider_difficulty.width2 < 450:
                chosen_difficulty = "normal"
                slider_difficulty.color2 = (128, 64, 0)
            elif slider_difficulty.width2 == 450:
                chosen_difficulty = "hard"
                slider_difficulty.color2 = (128, 0, 0)
        

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                chosen_name = name.update_text(event)
            
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    for _class in classes:
                        if _class[0].isOver([mx, my]):
                            chosen_class = _class[0].text
                    '''for difficulty in difficulties:
                        if difficulty.isOver([mx, my]):
                            chosen_difficulty = difficulty.text.lower()
                    '''
                    if slider_difficulty.isOver([mx, my]):
                        slider_difficulty_move = True

                    if button_cancel.isOver([mx,my]):
                        return False
                    if button_apply.isOver([mx, my]):
                        Player.Pclass[0] = chosen_class
                        Player.difficulty = chosen_difficulty
                        Player.name = chosen_name
                        load_new_game()
                    name.isOver([mx, my])
                elif event.button == 4 or event.button == 5:
                    if slider_difficulty.isOver([mx, my]):
                        if settings["Permadeath Enabled"]:
                            slider_difficulty.scroll(event.button, 150)
                        else:
                            slider_difficulty.scroll(event.button, 225)

            if event.type == MOUSEBUTTONUP and event.button == 1:
                slider_difficulty_move = False
            
            if event.type == MOUSEMOTION:
                if button_cancel.isOver([mx, my]):
                    button_cancel.change_color((128, 0, 0))
                else:
                    button_cancel.change_color((0, 0, 0))

                if button_apply.isOver([mx, my]):
                    button_apply.change_color((0, 128, 0))
                else:
                    button_apply.change_color((0, 0, 0))
            
        pygame.display.flip()

def story():
    pages = [
        Story(["Once upon a time, a mysterious dark power", "took over the land of Bolgenra,", "corrupting it and forcing darkness upon it's people.", 'The people of Bolgenra called it: "Inseynia".']),
        Story(["There is a myth, saying that Inseynia", "will be stopped by a brave hero", 'who will rise when the "Brighter Sun" rises.', ""]),
        Story(["The Brighter Sun is summoned when", "the star, Thydor, explodes. The explosion is thought", "to outshine all other light and brighten the night sky.", ""]),
        Story(["Different people from different countries", "and cultures call the hero different names,", " but he is most commonly known as: Torisker.", ""]),
        Story(["People created theories about this creature,", "some were more realistic than others,", "but the most accepted theory is that Torisker", "is the son of the Inseynian Artakees."]),
        Story(["Torisker was thought to be and Inseynian", "like his father, but during the Rain of the Rays,", "Torisker was captured by the rays", "and had been deeply affected."]),
        Story(["These rays affected Torisker", "from being an Inseynian to an Illunian.", "", ""]),
        Story(["Torisker was locked away by the", "Biome Kings because of his awful mistakes", "of destroying their lands.", ""]),
        Story(["Torisker promised not to do it again", "and that he was deeply sorry,", "but no one trusted him or set him free.", ""]),
        Story(["And he is currently waiting for someone to", "defeat the Biome Kings and Artakees", "to set him free so that he can", "get out and destroy Inseynia. Once, and for all."])
    ]
    def redraw():
        win.fill((0,0,0))
        try:
            page.render(win, images[f"S{pg_num+1}"])
        except:
            page.render(win)
        brightness_overlay.draw(win)

    continue_text = Text(0, Height-50, "Press space to continue", os.path.join("assets", "fonts", "DefaultFont.TTF"), 25, (255,255,255))
    #continue_text = Text(0, Height-50, "Press space to continue", os.path.join("assets", "fonts", "Font.png"), (255,255,255))
    continue_text.x = Width-65-continue_text.get_width()

    last_call = time.time()
    for pg_num, page in enumerate(pages):
        space_pressed = False
        if pg_num > 0:
            fade_in(redraw, 2)
        else:
            fade_in(redraw, 0.7)

        redraw()
        pygame.display.flip()

        if page.update_text(redraw):
            fade_out(redraw, 3)
            if not new_game_creator():
                return

        while 1:
            if time.time() - last_call >= 1/FPS:
                redraw()
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    
                    if event.type == KEYDOWN:
                        if event.key == K_F11:
                            F11()
                        elif event.key == K_F3:
                            debug_menu = not debug_menu
                        elif event.key == K_SPACE:
                            space_pressed = True
                        else:
                            fade_out(redraw, 3)
                            if not new_game_creator():
                                return
                if space_pressed:
                    break
                continue_text.render(win)
                pygame.draw.polygon(win, (255,255,255), ((Width-50, Height-50), (Width-25, Height-37.5), (Width-50, Height-25)))
                pygame.display.flip()

                last_call = time.time()

        fade_out(redraw, 2)

    new_game_creator()

def main_game(loc):
    global debug_menu, scroll, show_hitboxes, show_mid
    
    pick_ups = load_json(["scripts", "data", "pick ups.json"])
    get_data = True

    last_time = time.time()

    # Room Data
    rdata = load_json(["scripts", "data", "rooms.json"])

    last_time = time.time()

    player = Player(0, 0, "Down")
    inventory = Inventory(resol, player, images['Inventory Slot'], images)
    camera = Camera(true_scroll, player)

    drops = []
    enemies = []
    

    brightness_night = Brightness((0, 0), (Width, Height), 100, -1)

    last_call = time.time()

    slots_updated = False

    def redraw():
        win.fill((0,0,0))
        game_map.draw_map(win, scroll)
        for item in drops:
            item[1].draw(win, scroll)

        for enemy in enemies:
            enemy.draw(win, scroll)
        player.draw(win, scroll)
        inventory.draw_inventory(win, (Width, Height))
        

        if debug_menu:
            debug(last_call, player, enemies, [drop_rects, game_map.tile_rects, player.projectiles, player.melee_dir_poly, enemies,  [enemy.projectiles for enemy in enemies]], scroll)

        if "Always Night" in rdata[loc]["extras"]:
            brightness_night.draw(win)

        brightness_overlay.draw(win)
        
    while 1:
        if time.time() - last_call >= 1/FPS:
            if get_data:
                try:
                    game_map = TileMap(os.path.join("scripts", "tiles", f"{Player.location.split(' ')[0]}", f"{Player.location.replace(' ', '').lower()}.csv"), "House", (Width, Height))
                except:
                    game_map = TileMap(os.path.join("scripts", "tiles", "House", "house1.csv"), "House", (Width, Height))

                player.rect.x, player.rect.y = game_map.start_x, game_map.start_y

                drops = []; enemies = []; exits = []
                for drop in rdata[loc]["drops"]:
                    drops.append([drop[0], Drop(drop[1][0], drop[1][1], images[drop[0]]), 0])
                for enemy in rdata[loc]["enemies"]:
                    enemies.append(Enemy(enemy[1][0], enemy[1][1], enemy[0], images))
                for room, rect in rdata[loc]["exits"].items():
                    rect = pygame.Rect(rect[0], rect[1], rect[2], rect[3])
                    exits.append([room, rect])
                drop_rects = [drop[1] for drop in drops]

                try:
                    for item_name in pick_ups[loc].keys():
                        if pick_ups[loc][item_name]:
                            for drop_index, drop in enumerate(drops):
                                if item_name in drop:
                                    del drops[drop_index]
                except KeyError:
                    pass

                get_data = False

            if (Width, Height) != game_map.screen_size:
                try:
                    game_map = TileMap(os.path.join("scripts", "tiles", f"{Player.location.split(' ')[0]}", f"{Player.location.replace(' ', '').lower()}.csv"), "House", (Width, Height))
                except:
                    game_map = TileMap(os.path.join("scripts", "tiles", "House", "house1.csv"), "House", (Width, Height))

            if len(player.equipment) == 3 and not slots_updated:
                inventory.update_slots()
                slots_updated = True
            player.update()

            if "Always Night" in rdata[loc]["extras"]:
                if old_Width != Width:
                    brightness_night.reconfigure(size=(Width, Height))

            redraw()

            dt = FPS_ind(last_time)
            last_time = time.time()

            for drop_index, item in enumerate(drops):
                item[2] -= 1*dt
                if player.rect.colliderect(item[1].rect) and item[2] <= 0:
                    inventory.grab_item(item[0])
                    try:
                        pick_ups[loc][item[0]] = True
                    except KeyError:
                        pass

                    del drops[drop_index]
                    drop_rects = [drop[1] for drop in drops]

            for enemy in enemies:
                s = enemy.ai(player, dt, game_map.tile_rects, game_map)

                if enemy.rect.colliderect(player.rect):
                    player.lose_hp(enemy.stats["Attack"])

                enemy.projectiles_move(game_map.tile_rects, dt, scroll, [player])
                for projectile in enemy.projectiles:
                    player, enemy.projectiles = projectile.damage([player], enemy.projectiles)
                    player = player[0]
                    enemy.projectiles = projectile.offmap(game_map, enemy.projectiles)

            for projectile in player.projectiles:
                enemies, player.projectiles = projectile.damage(enemies, player.projectiles)
                player.projectiles = projectile.offmap(game_map, player.projectiles)

            if not camera.forced_loc:  
                _ = player.move(game_map.tile_rects, dt, keys, enemies)
            player.projectiles_move(game_map.tile_rects, dt, scroll, enemies, pygame.mouse.get_pos())

            for exit in exits:
                if player.rect.colliderect(exit[1]):
                    loc = exit[0]
                    Player.location = exit[0]
                    get_data = True

                    save_game(pick_ups)
                    break

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    if event.key == keys["Equip"]:
                        d = inventory.equip_item([player.x, player.y])
                        if d:
                            drops.append(d)
                        del d
                    if event.key == keys["Throw"]:
                        x = inventory.throw_item([player.x, player.y])
                        if x: drops.append(x)
                    if event.key == keys["Switch"]:
                        inventory.inv = not inventory.inv
                    if event.key == keys["Pause"]:
                        pause(redraw, None)

                    if event.key == K_F11:
                        F11()
                    if event.key == K_F3:
                        debug_menu = not debug_menu
                    if event.key == K_b:
                        show_hitboxes = not show_hitboxes
                    if event.key == K_v:
                        show_mid = not show_mid
                        
                if event.type == MOUSEBUTTONDOWN:
                    player.strong_charging = True
                    player.strong_wind = time.time()

                if event.type == MOUSEBUTTONUP:
                    enemies = player.attack(enemies, event.button, pygame.mouse.get_pos(), (Width, Height), win, scroll)
                    player.strong_wind = 0; player.strong_charging = False; player.strong_charged = False
                inventory.select_item(event)
                
            scroll = camera.update(game_map, (Width, Height), dt)

            pygame.display.flip()

            last_call = time.time()

def dev_room():
    def global_redraw():
        win.fill((0,0,0))
    
    def access():
        user_input = ""
        input_pass = TextBox((0,0,0), (Width*0.5)-(500*0.5)-50, (Height*0.5)-(100*0.5), 500, 100, "Enter Password", clear_text_when_click=True)
        password = "66VnGz28HH"
        
        button_enter = Button(input_pass.x + input_pass.width+25, (Height*0.5)-(50*0.5)-25, 150, 40, (0,128,0), "Enter", outline=(255,255,255), font_path=os.path.join("assets", "fonts", "DefaultFont.TTF"))
        button_cancel = Button(input_pass.x + input_pass.width+25, (Height*0.5)-(50*0.5)+25, 150, 40, (128,0,0), "Cancel", outline=(255,255,255), font_path=os.path.join("assets", "fonts", "DefaultFont.TTF"))
        
        def redraw():
            global_redraw()

            input_pass.draw(win, (255,255,255), font_path=os.path.join("assets", "fonts", "DefaultFont.TTF"), font_size=32)
            button_enter.draw(win)
            button_cancel.draw(win)

            brightness_overlay.draw(win)
        while 1:
            redraw()
            for event in pygame.event.get():
                mx, my = pygame.mouse.get_pos()
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    user_input = input_pass.update_text(event)
                    if user_input == password:
                        return True

                    if event.key == K_F11:
                        F11()
                    if event.key == K_F3:
                        debug_menu = not debug_menu

                if event.type == MOUSEBUTTONDOWN:
                    input_pass.isOver([mx, my])

                    if button_enter.isOver([mx, my]):
                        user_input = input_pass.text
                        if user_input == password:
                            return True
                    if button_cancel.isOver([mx, my]):
                        return

                    pygame.display.flip()

            pygame.display.flip()

    def room():
        global true_scroll, scroll, debug_menu, show_hitboxes, show_mid

        game_map = TileMap(os.path.join("scripts", "tiles", "Dev Room", "untitled.csv"), "Dev Room", (Width, Height))
        last_time = time.time()

        player = Player(game_map.start_x, game_map.start_y, "Down") 
        inventory = Inventory(resol, player, images['Inventory Slot'], images)
        camera = Camera(true_scroll, player)

        txt = Text(game_map.x+game_map.w+200, 0, "Bonjour :)", os.path.join("assets", "fonts", "DefaultFont.TTF"), 32, (255,255,255))

        drops = [
            ["Wooden Bow", Drop(50+game_map.x, 250+game_map.y, images['Wooden Bow']), 0],
            ["Crossbow", Drop(50+game_map.x, 350+game_map.y, images["Crossbow"]), 0],
            ["Walking Staff", Drop(50+game_map.x, 450+game_map.y, images["Walking Staff"]), 0],
            ["Amateur Staff", Drop(50+game_map.x, 550+game_map.y, images["Amateur Staff"]), 0],
            ["Wooden Shield", Drop(50+game_map.x, 650+game_map.y, images["Wooden Shield"]), 0]
        ]
        enemies = []
        last_call = time.time()
        slots_updated = False
        def redraw():
            global_redraw()
            game_map.draw_map(win, scroll)

            for item in drops:
                item[1].draw(win, scroll)

            for enemy in enemies:
                enemy.draw(win, scroll)
            player.draw(win, scroll)
            inventory.draw_inventory(win, (Width, Height))
            txt.render(win, scroll)

            if debug_menu:
                drop_rects = []
                for drop in drops:
                    drop_rects.append(drop[1])
                debug(last_call, player, enemies, [drop_rects, game_map.tile_rects, player.projectiles, player.melee_dir_poly, enemies,  [enemy.projectiles for enemy in enemies]], scroll)

            brightness_overlay.draw(win)
            
        while 1:
            if time.time() - last_call >= 1/FPS:
                #game_map.update_map(os.path.join("scripts", "tiles", "Dev Room", "untitled.csv"), (Width, Height))
                if (Width, Height) != game_map.screen_size:
                    game_map = TileMap(os.path.join("scripts", "tiles", "Dev Room", "untitled.csv"), "Dev Room", (Width, Height))
                if len(player.equipment) == 3 and not slots_updated:
                    inventory.update_slots()
                    slots_updated = True
                player.update()
                redraw()

                dt = FPS_ind(last_time)
                last_time = time.time()

                for drop_index, item in enumerate(drops):
                    item[2] -= 1*dt
                    if player.rect.colliderect(item[1].rect) and item[2] <= 0:
                        if inventory.grab_item(item[0], 1):
                            del drops[drop_index]

                for enemy in enemies:
                    s = enemy.ai(player, dt, game_map.tile_rects, game_map)

                    if enemy.rect.colliderect(player.rect):
                        player.lose_hp(enemy.stats["Attack"])

                    enemy.projectiles_move(game_map.tile_rects, dt, scroll, [player])
                    for projectile in enemy.projectiles:
                        player, enemy.projectiles = projectile.damage([player], enemy.projectiles)
                        player = player[0]
                        enemy.projectiles = projectile.offmap(game_map, enemy.projectiles)

                for projectile in player.projectiles:
                    enemies, player.projectiles = projectile.damage(enemies, player.projectiles)
                    player.projectiles = projectile.offmap(game_map, player.projectiles)

                if not camera.forced_loc:
                    _ = player.move(game_map.tile_rects, dt, keys, enemies)
                player.projectiles_move(game_map.tile_rects, dt, scroll, enemies, pygame.mouse.get_pos())

                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == KEYDOWN:
                        if event.key == keys["Equip"]:
                            d = inventory.equip_item([player.x, player.y])
                            if d:
                                drops.append(d)
                            del d
                        if event.key == keys["Throw"]:
                            x = inventory.throw_item([player.x, player.y])
                            if x: drops.append(x)
                        if event.key == keys["Switch"]:
                            inventory.inv = not inventory.inv
                        if event.key == keys["Pause"]:
                            pause(redraw, None)

                        if event.key == K_F11:
                            F11()
                        if event.key == K_F3:
                            debug_menu = not debug_menu
                        if event.key == K_b:
                            show_hitboxes = not show_hitboxes
                        if event.key == K_v:
                            show_mid = not show_mid

                        if event.key == K_x:
                            enemies.append(Test_Enemy(player.x+100, player.y, images))
                        if event.key == K_c:
                            enemies.append(Ranged_Enemy(player.x+200, player.y, images))
                        if event.key == K_z:
                            enemies.append(Test_Boss(game_map.x+game_map.w, game_map.y+game_map.h, images))

                        if event.key == K_BACKSPACE:
                            if camera.forced_loc:
                                camera.forced_loc = None
                            else:
                                camera.forced_loc = (txt.x+txt.get_width()*0.5, txt.y+txt.get_height()*0.5)

                    if event.type == MOUSEBUTTONDOWN:
                        player.strong_charging = True
                        player.strong_wind = time.time()

                    if event.type == MOUSEBUTTONUP:
                        enemies = player.attack(enemies, event.button, pygame.mouse.get_pos(), (Width, Height), win, scroll)
                        player.strong_wind = 0; player.strong_charging = False; player.strong_charged = False
                    inventory.select_item(event)
                    
                scroll = camera.update(game_map, (Width, Height), dt)

                pygame.display.flip()

                last_call = time.time()
    
    #if access():
    room()

def credits():
    last_time = time.time()
    texts = [
        Text(0, Height, "Inseynia", os.path.join("assets", "fonts", "DefaultFont.TTF"), 72, (255,255,255)),
        Text(0, Height+100, "Lead Developer", os.path.join("assets", "fonts", "DefaultFont.TTF"), 48, (255,255,255)),
        Text(0, Height+150, "Zeperox", os.path.join("assets", "fonts", "DefaultFont.TTF"), 32, (255,255,0)),
        Text(0, Height+200, "Lead Artist", os.path.join("assets", "fonts", "DefaultFont.TTF"), 48, (255,255,255)),
        Text(0, Height+250, "Bowie", os.path.join("assets", "fonts", "DefaultFont.TTF"), 32, (255,255,0)),
        Text(0, Height+300, "Composer", os.path.join("assets", "fonts", "DefaultFont.TTF"), 48, (255,255,255)),
        Text(0, Height+350, "Cthethan", os.path.join("assets", "fonts", "DefaultFont.TTF"), 32, (255,255,0)),
        Text(0, Height+400, "Manager", os.path.join("assets", "fonts", "DefaultFont.TTF"), 48, (255,255,255)),
        Text(0, Height+450, "Big Smoke", os.path.join("assets", "fonts", "DefaultFont.TTF"), 32, (255,255,0)),
        Text(0, Height+500, "Extra Developers", os.path.join("assets", "fonts", "DefaultFont.TTF"), 48, (255,255,255)),
        Text(0, Height+550, "Adam    DevHedron", os.path.join("assets", "fonts", "DefaultFont.TTF"), 32, (255,255,0)),
        Text(0, Height+600, "Extra Artists", os.path.join("assets", "fonts", "DefaultFont.TTF"), 48, (255,255,255)),
        Text(0, Height+650, "Big Smoke    Chaino    gyroc1", os.path.join("assets", "fonts", "DefaultFont.TTF"), 32, (255,255,0)),
        Text(0, Height+700, "Extra Team Members", os.path.join("assets", "fonts", "DefaultFont.TTF"), 48, (255,255,255)),
        Text(0, Height+750, "Invarrow    k..  -ACE-", os.path.join("assets", "fonts", "DefaultFont.TTF"), 32, (255,255,0)),
        Text(0, Height+800, "Special Thanks To:", os.path.join("assets", "fonts", "DefaultFont.TTF"), 48, (255,255,255)),
        Text(0, Height+850, "!MAD!    Alexey_045", os.path.join("assets", "fonts", "DefaultFont.TTF"), 32, (255,255,0)),
        Text(0, Height+890, "Anais Snow MY    CodeRxJesseJ", os.path.join("assets", "fonts", "DefaultFont.TTF"), 32, (255,255,0)),
        Text(0, Height+930, "Dark_Alliance    flakes", os.path.join("assets", "fonts", "DefaultFont.TTF"), 32, (255,255,0)),
        Text(0, Height+970, "Freddy Mercury    FADE_X", os.path.join("assets", "fonts", "DefaultFont.TTF"), 32, (255,255,0)),
        Text(0, Height+1010, "Grandster    Jaimses", os.path.join("assets", "fonts", "DefaultFont.TTF"), 32, (255,255,0)),
        Text(0, Height+1050, "Jumboost    K13", os.path.join("assets", "fonts", "DefaultFont.TTF"), 32, (255,255,0)),
        Text(0, Height+1090, "MartinWho    MightBeARobot", os.path.join("assets", "fonts", "DefaultFont.TTF"), 32, (255,255,0)),
        Text(0, Height+1130, "MKGamer    parapotato3", os.path.join("assets", "fonts", "DefaultFont.TTF"), 32, (255,255,0)),
        Text(0, Height+1170, "ItsGoat    Шкьрыоав)", os.path.join("assets", "fonts", "DefaultFont.TTF"), 32, (255,255,0)),
        Text(0, Height+1210, "wermz    X_X", os.path.join("assets", "fonts", "DefaultFont.TTF"), 32, (255,255,0)),
        Text(0, Height+1250, "And you... for playing!", os.path.join("assets", "fonts", "DefaultFont.TTF"), 32, (0,200,255)),
        Text(0, Height+1900, " ", os.path.join("assets", "fonts", "DefaultFont.TTF"), 1, (0,0,0)),
        # Text(0, Height, "Inseynia", os.path.join("assets", "fonts", "Font.png"), (255,255,255)),
        # Text(0, Height+100, "Lead Developer", os.path.join("assets", "fonts", "Font.png"), (255,255,255)),
        # Text(0, Height+150, "Zeperox", os.path.join("assets", "fonts", "Font.png"), (255,255,0)),
        # Text(0, Height+200, "Lead Artist", os.path.join("assets", "fonts", "Font.png"), (255,255,255)),
        # Text(0, Height+250, "Bowie", os.path.join("assets", "fonts", "Font.png"), (255,255,0)),
        # Text(0, Height+300, "Composer", os.path.join("assets", "fonts", "Font.png"), (255,255,255)),
        # Text(0, Height+350, "Cthethan", os.path.join("assets", "fonts", "Font.png"), (255,255,0)),
        # Text(0, Height+400, "Manager", os.path.join("assets", "fonts", "Font.png"), (255,255,255)),
        # Text(0, Height+450, "Big Smoke", os.path.join("assets", "fonts", "Font.png"), (255,255,0)),
        # Text(0, Height+500, "Extra Developers", os.path.join("assets", "fonts", "Font.png"), (255,255,255)),
        # Text(0, Height+550, "Adam_    DevHedron", os.path.join("assets", "fonts", "Font.png"), (255,255,0)),
        # Text(0, Height+600, "Extra Artists", os.path.join("assets", "fonts", "Font.png"), (255,255,255)),
        # Text(0, Height+650, "Big Smoke    Chaino", os.path.join("assets", "fonts", "Font.png"), (255,255,0)),
        # Text(0, Height+700, "Extra Team Members", os.path.join("assets", "fonts", "Font.png"), (255,255,255)),
        # Text(0, Height+750, "Invarrow", os.path.join("assets", "fonts", "Font.png"), (255,255,0)),
        # Text(0, Height+800, "Special Thanks To:", os.path.join("assets", "fonts", "Font.png"), (255,255,255)),
        # Text(0, Height+850, "!MAD!    Anais Snow", os.path.join("assets", "fonts", "Font.png"), (255,255,0)),
        # Text(0, Height+890, "LEO Thamoly    Fade_X", os.path.join("assets", "fonts", "Font.png"), (255,255,0)),
        # Text(0, Height+930, "Alexey_045    Gandster", os.path.join("assets", "fonts", "Font.png"), (255,255,0)),
        # Text(0, Height+970, "Jet Omnivore    Necrosway", os.path.join("assets", "fonts", "Font.png"), (255,255,0)),
        # Text(0, Height+1010, "AwesomeNoob999", os.path.join("assets", "fonts", "Font.png"), (255,255,0)),
        # Text(0, Height+1050, "And you... for playing!", os.path.join("assets", "fonts", "Font.png"), (0,200,255)),
        # Text(0, Height+1700, " ", os.path.join("assets", "fonts", "Font.png"), (0,0,0)),
    ]
    texaract_img_y = Height+1400
    for text in texts:
        text.x = (Width*0.5)-(text.get_width()*0.5)
    speed = 1
    def redraw():
        win.fill((0,0,0))
        for text in texts:
            text.render(win)

        win.blit(images["Texaract"], ((Width*0.5)-(images["Texaract"].get_width()*0.5), texaract_img_y))

    last_call = time.time()

    while 1:
        if time.time() - last_call >= 1/FPS:
            redraw()

            dt = FPS_ind(last_time)
            last_time = time.time()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN and event.key != K_SPACE:
                    return

                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 4:
                        speed += .5
                    elif event.button == 5:
                        if speed > 0:
                            speed -= .5

            for text in texts:
                text.y -= speed*dt

            if texts[-1].y < -50:
                return
            
            texaract_img_y -= speed*dt
            pygame.display.flip()

            last_call = time.time()

popup()

while 1:
    if main_menu():
        stored_data = load_json(["scripts", "data", "save.json"])
    
        Player.gender = stored_data["gender"]
        Player.Pclass = stored_data["class"]
        Player.difficulty = stored_data["difficulty"]
        Player.name = stored_data["name"]
        Player.inventory = stored_data["inventory"]
        Player.equipment = stored_data["equipment"]
        Player.stats = stored_data["stats"]
        Player.location = stored_data["location"]
        del stored_data

        if Player.location == "Story":
            story()
        elif Player.location == "Dev Room":
            dev_room()
        else:
            main_game(Player.location)
