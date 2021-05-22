# Import modules
import pygame, os, sys, random, json, time, math, platform

from pygame.locals import *
from pygame._sdl2.video import Window


# Create Dirs
def createFolder(directory):
    if not os.path.isdir(directory):
        try:
            os.mkdir(directory)
        except OSError:
            sys.exit()

if platform.system() == "Windows":
    createFolder(os.path.join(os.getenv("localappdata"), ".inseynia"))
    createFolder(os.path.join(os.getenv("localappdata"), ".inseynia", "saves"))
else: sys.exit()

# Import game scripts
import scripts.engine as engine

from scripts.UI.window import *
from scripts.UI.button import *
from scripts.UI.slider import *
from scripts.UI.textbox import *

from scripts.assets.sprites import *
from scripts.assets.SFX import *
from scripts.assets.music_player import *

#from scripts.game_logic.inventory import *

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
pygame.mixer.set_num_channels(128)
pygame.font.init()
pygame.init()


# Window
window = Window.from_display_module()
window.position = ((screen_w*0.5)-(Width*0.5), (screen_h*0.5)-(Height*0.5))

randcaption = random.choice([
    "The evil is growing",
    "Try Minceraft",
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
    "CRASH",
    "Full of lore",
    "なお　イン　じゃぱねせ",
    "Wasted",
    "¯\_(ツ)_/¯",
    "Totally not a rip-off, wdym"
])

if randcaption == "騙你":
    pygame.display.set_caption(f"印西尼亞: {randcaption}") # yinxi ni ya
elif randcaption == "Welcome":
    for _ in range(random.randint(5, 20)):
        randcaption += random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890")#`-=,./;'[]\\~!@#$%^&*()_+{}|:<>? ")
    pygame.display.set_caption(f"Inseynia: {randcaption}")
elif randcaption == "Opposite of Inseynia":
    pygame.display.set_caption(f"Calmia: {randcaption}")
elif randcaption == "ناو إن أرابيك":
    pygame.display.set_caption(f"إنسينيا: {randcaption}")
elif randcaption == "なお　イン　じゃぱねせ":
    pygame.display.set_caption(f"いんせいにあ: {randcaption}")
elif randcaption == "CRASH":
    with open("Crash Report.txt", "w") as f:
        text = random.choice([
            "The game crashed",
            "It do be crashin' doe",
            "Have you tried reopening the game?",
            "Exited with code 0",
            "Crash Report\n\nReason of crash: idk ¯\_(ツ)_/¯",
            "You were too beautiful that the game got so shy and jealous that it crashed... sorry",
            "The ••••---•-•--•--••••----• has caused it",
        ])
        f.write("The game crashed")
        pygame.quit()
        sys.exit()
elif randcaption == "¯\_(ツ)_/¯":
    pygame.display.set_caption(randcaption)
else:
    pygame.display.set_caption(f"Inseynia: {randcaption}")

icon = pygame.image.load(os.path.join("assets", os.path.join("icon", "InseyniaIcon.ico")))
pygame.display.set_icon(icon)


# Classes
class Story:
    def __init__(self, text_list):
        self.texts = text_list
        self.str = []

    def render(self, window, img=None):
        font = pygame.font.SysFont("comicsans", 45)
        labels = []
        for str_ in self.str:
            labels.append(font.render(str_, 1, (255,255,255)))
        if img:
            window.blit(img, (Width*0.5-img.get_width()*0.5, 75))
        x = 0
        for label in labels:
            window.blit(label, (Width*0.5-label.get_width()*0.5, 50*x+400))
            x += 1

    def update_text(self, window, func):
        str_ = 0
        for text in self.texts:
            global debug_menu
            self.str.append("")
            for x in range(1, len(text)+1):
                clock.tick(30)
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
                        else:
                            return True
                pygame.display.flip()
            str_ += 1

class Player:
    gender = random.choice(["male", "female"])
    Pclass = random.choice(["Warrior", "Archer", "Mage"])
    difficulty = random.choice(["easy", "normal", "hard"])
    name = "a"
    inventory = {}
    equipment = ["Fist", "No Shield"]
    stats = {
        "Health": 10,
        "Max Health": 10,
        "Attack": 1,
        "Defense": 2,
        "Stamina" if Pclass == "Warrior" else "Projectiles" if Pclass == "Archer" else "Mana": 10,
        "Max Stamina" if Pclass == "Warrior" else "Max Projectiles" if Pclass == "Archer" else "Max Mana": 10,
        "Max Projectiles": 10,
        "Money": 100,
        "XP": 0,
        "Level": 1,
        "Speed": 2
    }
    location = None
    xp = 0
    max_xp = 3
    directions = {
        "Up": None,
        "Down": None,
        "Right": None,
        "Left": None
    }
    
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.img = self.directions[direction]

        #self.rect = pygame.Rect(self.x, self.y, self.get_width(), self.get_height())
        self.rect = pygame.Rect(self.x, self.y, 38, 40)

    def draw(self, window, hpbar_loc=[Width-210, 10], esbar_loc=[Width-210, 45]):
        #window.blit(self.img, (self.x, self.y))
        pygame.draw.rect(window, (255,255,255), (self.x, self.y, 38, 40))
        self.bars(window, hpbar_loc, esbar_loc)

    def bars(self, window, hpbar_loc, esbar_loc):
        global Width, Height, old_Width
        
        if hpbar_loc[0] == old_Width-210:
            display_size = pygame.display.get_surface().get_size()
            Width, Height = display_size

            hpbar_loc[0] = Width-210
        if esbar_loc[0] == old_Width-210:
            display_size = pygame.display.get_surface().get_size()
            Width, Height = display_size

            esbar_loc[0] = Width-210
        
        old_Width = Width
        
        bar_font = pygame.font.SysFont("comicsans", 24)
        health_label = bar_font.render(f"{self.stats['Health']}/{self.stats['Max Health']}", 1, (255,255,255))
        #attack_label = bar_font.render(str(self.stats["Attack"]), 1, (255,255,255))
        #defense_label = bar_font.render(str(self.stats["Defense"]), 1, (255,255,255))
        if "Stamina" in self.stats:
            stamina_label = bar_font.render(f"{self.stats['Stamina']}/{self.stats['Max Stamina']}", 1, (255,255,255))
        if "Projectiles" in self.stats:
            projectiles_label = bar_font.render(f"{self.stats['Projectiles']}/{self.stats['Max Projectiles']}", 1, (255,255,255))
        if "Mana" in self.stats:
            mana_label = bar_font.render(f"{self.stats['Mana']}/{self.stats['Max Mana']}", 1, (255,255,255))
        pygame.draw.rect(window, (175,0,0), (hpbar_loc[0], hpbar_loc[1], 200, 25))
        pygame.draw.rect(window, (0,175,0), (hpbar_loc[0], hpbar_loc[1], 200 * (self.stats["Health"]/self.stats["Max Health"]), 25))
        pygame.draw.rect(window, (200,200,200), (hpbar_loc[0]-2, hpbar_loc[1]-2, 203, 27), 3)
        pygame.draw.rect(window, (0,0,0), (hpbar_loc[0]-3, hpbar_loc[1]-3, 205, 29), 1)
        window.blit(health_label, (((200*0.5)-(health_label.get_width()*0.5))+(hpbar_loc[0]), ((25*0.5)-(health_label.get_height()*0.5))+hpbar_loc[1]))
        if "Stamina" in self.stats:
            pygame.draw.rect(window, (175,0,0), (esbar_loc[0], esbar_loc[1], 200, 25))
            pygame.draw.rect(window, (175,175,0), (esbar_loc[0], esbar_loc[1], 200 * (self.stats["Stamina"]/self.stats["Max Stamina"]), 25))
            pygame.draw.rect(window, (200,200,200), (esbar_loc[0]-2, esbar_loc[1]-2, 203, 27), 3)
            pygame.draw.rect(window, (0,0,0), (esbar_loc[0]-3, esbar_loc[1]-3, 205, 29), 1)
            window.blit(stamina_label, (((200*0.5)-(stamina_label.get_width()*0.5))+(esbar_loc[0]), ((25*0.5)-(stamina_label.get_height()*0.5))+esbar_loc[1]))
        if "Projectiles" in self.stats:
            pygame.draw.rect(window, (175,0,0), (esbar_loc[0], esbar_loc[1], 200, 25))
            pygame.draw.rect(window, (175,88,0), (esbar_loc[0], esbar_loc[1], 200 * (self.stats["Projectiles"]/self.stats["Max Projectiles"]), 25))
            pygame.draw.rect(window, (200,200,200), (esbar_loc[0]-2, esbar_loc[1]-2, 203, 27), 3)
            pygame.draw.rect(window, (0,0,0), (esbar_loc[0]-3, esbar_loc[1]-3, 205, 29), 1)
            window.blit(projectiles_label, (((200*0.5)-(projectiles_label.get_width()*0.5))+(esbar_loc[0]), ((25*0.5)-(projectiles_label.get_height()*0.5))+esbar_loc[1]))
        if "Mana" in self.stats:
            pygame.draw.rect(window, (175,0,0), (esbar_loc[0], esbar_loc[1], 200, 25))
            pygame.draw.rect(window, (0,0,175), (esbar_loc[0], esbar_loc[1], 200 * (self.stats["Mana"]/self.stats["Max Mana"]), 25))
            pygame.draw.rect(window, (200,200,200), (esbar_loc[0]-2, esbar_loc[1]-2, 203, 27), 3)
            pygame.draw.rect(window, (0,0,0), (esbar_loc[0]-3, esbar_loc[1]-3, 205, 29), 1)
            window.blit(mana_label, (((200*0.5)-(mana_label.get_width()*0.5))+(esbar_loc[0]), ((25*0.5)-(mana_label.get_height()*0.5))+esbar_loc[1]))

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[keys["Up"]] and self.y >= 0:
            self.y -= self.stats["Speed"]
        if pressed_keys[keys["Down"]] and self.y+self.rect.height <= Height:
            self.y += self.stats["Speed"]
        if pressed_keys[keys["Right"]] and self.x+self.rect.width <= Width:
            self.x += self.stats["Speed"]
        if pressed_keys[keys["Left"]] and self.x >= 0:
            self.x -= self.stats["Speed"]

        self.rect = pygame.Rect(self.x, self.y, self.rect.width, self.rect.height)
        
class Enemy(engine.Entity):
    def __init__(self, x, y, name):
        super().__init__(x, y, sprites_Enemies[name])
        enemies = load_json(["scripts", "data", "enemies.json"])
        self.name = name
        self.stats = enemies[name]
        self.in_fight = False

    def draw_bars(self, window, hpbar_loc:list):
        bar_font = pygame.font.SysFont("comicsans", 24)
        health_label = bar_font.render(f"{self.stats['Health']}/{self.stats['Max Health']}", 1, (255,255,255))

        pygame.draw.rect(window, (175,0,0), (hpbar_loc[0], hpbar_loc[1], 200, 25))
        pygame.draw.rect(window, (0,175,0), (hpbar_loc[0], hpbar_loc[1], 200 * (self.stats["Health"]/self.stats["Max Health"]), 25))
        pygame.draw.rect(window, (200,200,200), (hpbar_loc[0]-2, hpbar_loc[1]-2, 203, 27), 3)
        pygame.draw.rect(window, (0,0,0), (hpbar_loc[0]-3, hpbar_loc[1]-3, 205, 29), 1)
        window.blit(health_label, (((200*0.5)-(health_label.get_width()*0.5))+(hpbar_loc[0]), ((25*0.5)-(health_label.get_height()*0.5))+hpbar_loc[1]))

    def move(self, player_pos):
        if player_pos[0] < self.x:
            self.x -= 1
            self.rect.x -= 1
        if player_pos[0] > self.x:
            self.x += 1
            self.rect.x += 1
        if player_pos[1] < self.y:
            self.y -= 1
            self.rect.y -= 1
        if player_pos[1] > self.y:
            self.y += 1
            self.rect.y += 1

class Drop(engine.Entity):
    def __init__(self, x, y, drop):
        super().__init__(x, y, drop)
        self.rect = pygame.Rect(x-20, y-20, drop.get_width()+20, drop.get_height()+20)

class Inventory:
    inv_length = 10
    equip_length = 2
    inv = True
    eq = False
    inv_index = 0
    eq_index = 0
        
    def __init__(self):
        pass

    def draw_inventory(self, font_name:str=None):
        try:
            font = pygame.font.Font(font_name, 24)
            quant_font = pygame.font.Font(font_name, 12)
        except FileNotFoundError():
            font = pygame.font.SysFont(font_name, 24)
            quant_font = pygame.font.SysFont(font_name, 30)

        inv_label = font.render("Inventory", 1, (255,255,255))
        equip_label = font.render("Equipment", 1, (255,255,255))

        no = 0
        y = 10
        x = 10

        if self.inv:
            if resol:
                if round((resol[0]/resol[1])*100) <= 133:
                    win.blit(inv_label, (320*0.5-inv_label.get_width()*0.5, y))
                else:
                    win.blit(inv_label, (620*0.5-inv_label.get_width()*0.5, y))
            else:
                win.blit(inv_label, (620/2-inv_label.get_width()/2, y))
            for _ in range(self.inv_length):
                win.blit(sprites_Misc["Inventory Slot"], (x, y+inv_label.get_height()+5))
                x += 60
                no += 1
                if resol:
                    if round((resol[0]/resol[1])*100) <= 133 and no >= 5:
                        x = 10
                        y += 60
                        no = 0
            
            offset_x = 13
            offset_y = 18
            no = 0
            for item in Player.inventory.keys():
                win.blit(sprites_Equipment[item], (offset_x, inv_label.get_height()+offset_y))
                offset_x += 60
                no += 1
                if resol:
                    if round((resol[0]/resol[1])*100) <= 133 and no >= 5:
                        offset_x = 13
                        offset_y += 60
                        no = 0
            
            offset_x = 50
            offset_y = 48
            no = 0
            for item_quantity in Player.inventory.values():
                if not item_quantity == 1:
                    quantity = quant_font.render(str(item_quantity), 1, (255,255,255))
                    win.blit(quantity, (offset_x-quantity.get_width()+8, inv_label.get_height()+offset_y))
                offset_x += 60
                no += 1
                if resol:
                    if round((resol[0]/resol[1])*100) <= 133 and no >= 5:
                        offset_x = 50
                        offset_y += 60
                        no = 0

            if self.inv_index <= 4:
                pygame.draw.rect(win, (200,200,200), (self.inv_index*60+10,10+inv_label.get_height()+5,54,54),3)
            else:
                if resol:
                    if round((resol[0]/resol[1])*100) <= 133:
                        pygame.draw.rect(win, (200,200,200), ((self.inv_index-5)*60+10, 10+inv_label.get_height()+65, 54, 54), 3)
                    else:
                        pygame.draw.rect(win, (200,200,200), (self.inv_index*60+10, 10+inv_label.get_height()+5, 54, 54), 3)
                else:
                    pygame.draw.rect(win, (200,200,200), (self.inv_index*60+10, 10+inv_label.get_height()+5, 54, 54), 3)

        else:
            x = 95
            win.blit(equip_label, (310*0.5-equip_label.get_width()*0.5, y))
            for _ in range(self.equip_length):
                win.blit(sprites_Misc["Inventory Slot"], (x, y+equip_label.get_height()+5))
                x += 60
            
            offset_x = 98
            offset_y = 8
            for item in Player.equipment:
                win.blit(sprites_Equipment[item], (offset_x, y+inv_label.get_height()+offset_y))
                offset_x += 60

            if self.eq_index <= 1:
                pygame.draw.rect(win, (200,200,200), (self.eq_index*60+95,10+equip_label.get_height()+5,54,54),3)

    def select_item(self, event):
        if self.inv:
            if event.type == KEYDOWN:
                if event.key >= K_0 and event.key <= K_9:
                    self.inv_index = event.key - K_1
                    if event.key == K_0:
                        self.inv_index = 9
                
                if event.key >= K_KP_1 and event.key <= K_KP_0:
                    self.inv_index = event.key - K_KP_1

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 4:
                    if not self.inv_index <= 0:
                        self.inv_index -= 1
                    else:
                        self.inv_index = 9
                if event.button == 5:
                    if not self.inv_index >= 9:
                        self.inv_index += 1
                    else:
                        self.inv_index = 0
        else:
            if event.type == KEYDOWN:
                if event.key >= K_1 and event.key <= K_2:
                    self.eq_index = event.key - K_1
                
                if event.key >= K_KP_1 and event.key <= K_KP_2:
                    self.eq_index = event.key - K_KP_1

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 4:
                    if not self.eq_index <= 0:
                        self.eq_index -= 1
                    else:
                        self.eq_index = 1
                if event.button == 5:
                    if not self.eq_index >= 1:
                        self.eq_index += 1
                    else:
                        self.eq_index = 0

    def equip_item(self):
        if self.inv:
            self.inv = False

            try:
                equipment = load_json(["scripts", "data", "equipment.json"])

                l = list(Player.inventory.keys())
                item = l[self.inv_index]

                if item in equipment[0].keys():
                    ind = 0
                elif item in equipment[1].keys():
                    ind = 1
                else:
                    self.inv = True
                    return

                l = list(equipment[ind].keys())

                if not item in Player.equipment:
                    if ind == 0:
                        if equipment[0][item]["Class"] != Player.Pclass:
                            self.inv = True
                            return
                            
                    if Player.inventory[item] > 1:
                        Player.inventory[item] -= 1
                    else:
                        del Player.inventory[item]

                    if Player.equipment[ind] != "Fist" and Player.equipment[ind] != "No Shield":
                        if item in Player.inventory.keys():
                            Player.inventory[Player.equipment[ind]] += 1
                        else:
                            Player.inventory[Player.equipment[ind]] = 1
                    del Player.equipment[ind]
                    Player.equipment.insert(ind, item)

                    if ind == 0:
                        Player.stats["Attack"] = equipment[0][item]["AP"]
                    else:
                        Player.stats["Defense"] = equipment[1][item]["DP"]
                        Player.stats["Speed"] = int(2-((2*equipment[1][item]["Speed"])/100))
                else:
                    self.inv = True
                    return
            except:
                self.inv = True
        else:
            if Player.equipment[self.eq_index] != "Fist" and Player.equipment[self.eq_index] != "No Shield":
                if Player.equipment[self.eq_index] in Player.inventory.keys():
                    Player.inventory[Player.equipment[self.eq_index]] += 1
                else:
                    Player.inventory[Player.equipment[self.eq_index]] = 1

                del Player.equipment[self.eq_index]
                if self.eq_index == 0:
                    Player.equipment.insert(0, "Fist")
                    Player.stats["Attack"] = 1
                else:
                    Player.equipment.insert(1, "No Shield")
                    Player.stats["Defense"] = 0
                    Player.stats["Speed"] = 2
                
                self.inv = True
    
    def throw_item(self, player_loc:list):
        if self.inv:
            l = list(Player.inventory.keys())
            try:
                item = l[self.inv_index]
            except:
                return
            
            if Player.inventory[item] > 1:
                Player.inventory[item] -= 1
            else:
                del Player.inventory[item]

            return [item, Drop(player_loc[0], player_loc[1], sprites_Equipment[item]), 3*60]
        else:
            if Player.equipment[self.eq_index] != "Fist" and Player.equipment[self.eq_index] != "No Shield":
                item = Player.equipment[self.eq_index]
                del Player.equipment[self.eq_index]
                if self.eq_index == 0:
                    Player.equipment.insert(0, "Fist")
                    Player.stats["Attack"] = 1
                else:
                    Player.equipment.insert(1, "No Shield")
                    Player.stats["Defense"] = 0
                    Player.stats["Speed"] = 2

                return [item, Drop(player_loc[0], player_loc[1], sprites_Equipment[item]), 3*60]

    def grab_item(self, item, quantity:int=1):
        if len(Player.inventory) < 10:
            if not item in Player.inventory.keys():
                Player.inventory[item] = quantity
            else:
                items = load_json(["scripts", "data", "items.json"])
                if Player.inventory[item] < items[item]["stack"]:
                    Player.inventory[item] += quantity
                    if Player.inventory[item] > items[item]["stack"]:
                        Player.inventory[item] = quantity


# Vars
#game data
clock = pygame.time.Clock()
FPS = settings["FPS"]
fullscreen = settings["Fullscreen"]
resol = tuple(settings["Resol"]) if settings["Resol"] else None
keys = settings["Keys"]
set_brightness = settings["Brightness"]

#debug menu
debug_menu = False


# Program Functions
def load_json(location_list:list):
    location = location_list[0]
    for location_entry in location_list[1:]:
        location = os.path.join(location, location_entry)

    with open(location, "r") as f:
        return json.load(f)

def dump_json(location_list:list, var):
    location = location_list[0]
    for location_entry in location_list[1:]:
        location = os.path.join(location, location_entry)

    with open(location, "w") as f:
        json.dump(var, f, indent=4)

def FPS_ind(last_time):
    return (time.time() - last_time) * 60

def render_text(text:str, size:int, color:tuple, background_color:tuple=None):
    font = pygame.font.Font(os.path.join("assets", os.path.join("Fonts", "DefaultFont.TTF")), size)
    if background_color:
        return font.render(text, 1, color, background_color)
    else:
        return font.render(text, 1, color)

def F11(fullscreen_param=None):
    global fullscreen, Width, Height, info
    if fullscreen_param != None:
        fullscreen = fullscreen_param
        if fullscreen:
            pygame.display.set_mode((Width, Height), FULLSCREEN | DOUBLEBUF | HWSURFACE)
        else:
            pygame.display.set_mode((Width, Height), DOUBLEBUF | HWSURFACE)
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

    if fullscreen:
        pygame.display.set_mode((Width, Height), FULLSCREEN | DOUBLEBUF | HWSURFACE)
    else:
        os.environ['SDL_VIDEO_CENTERED'] = '1'

        screen_w, screen_h = info.current_w, info.current_h
        x, y = (screen_w*0.5)-(Width*0.5), (screen_h*0.5)-(Height*0.5)
        os.environ['SDL_VIDEO_WINDOW_POS'] = '%d,%d' % (x,y)
        pygame.display.set_mode((Width, Height), DOUBLEBUF | HWSURFACE)

def save_settings():
    settings = load_json([os.getenv("localappdata"), ".inseynia", "saves", "settings.json"])

    settings["FPS"] = FPS
    settings["Fullscreen"] = fullscreen
    settings["Resol"] = list(resol) if resol else None
    settings["Keys"] = keys
    settings["Brightness"] = set_brightness

    dump_json([os.getenv("localappdata"), ".inseynia", "saves", "settings.json"], settings)

def debug(px=0, py=0):
    fps = str(int(clock.get_fps()))
    ticks = str(int(clock.get_time()))
    Ppos = str(f"{px}X, {py}Y")
    Ppos = Ppos.replace("'", "")

    def show_fps():
        x = render_text(f"FPS: {fps}", 24, (255,255,255))
        
        surf = pygame.Surface((x.get_width()+6, x.get_height()+6))
        surf.fill((100,100,100))
        surf.set_alpha(200)
        surf.blit(x, (3, 3))
        win.blit(surf, (10, Height-x.get_height()-105))
    def show_ticks():
        x = render_text(f"Ticks: {ticks}", 24, (255,255,255))

        surf = pygame.Surface((x.get_width()+6, x.get_height()+6))
        surf.fill((100,100,100))
        surf.set_alpha(200)
        surf.blit(x, (3, 3))
        win.blit(surf, (10, Height-x.get_height()-75))
    def player_pos():
        x = render_text(f"Ppos: {Ppos}", 24, (255,255,255))

        surf = pygame.Surface((x.get_width()+6, x.get_height()+6))
        surf.fill((100,100,100))
        surf.set_alpha(200)
        surf.blit(x, (3, 3))
        win.blit(surf, (10, Height-x.get_height()-45))
    def room_name():
        x = render_text(f"Room: {Player.location}", 24, (255,255,255))

        surf = pygame.Surface((x.get_width()+6, x.get_height()+6))
        surf.fill((100,100,100))
        surf.set_alpha(200)
        surf.blit(x, (3, 3))
        win.blit(surf, (10, Height-x.get_height()-15))

    show_fps()
    show_ticks()
    player_pos()
    room_name()

def save_game():
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
    dump_json([os.getenv("localappdata"), ".inseynia", "saves", "save.json"], data)

def brightness(loc = (0, 0), size = (Width, Height)):
    fade = pygame.Surface(size)
    if set_brightness < 0:
        fade.fill((0,0,0))
    elif set_brightness > 0:
        fade.fill((255,255,255))
    fade.set_alpha(abs(set_brightness))
    win.blit(fade, (0,0))

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
def fight(enemy:Enemy):
    global debug_menu
    player = Player(100, Height-90, "Right")
    enemy = Enemy(Width-164, Height-164, enemy.name)
    inventory = Inventory()

    pturn = True
    button_group = 0
    use_inv = False

    dodge = False
    shield = False
    counter = False

    if "Stamina" in player.stats.keys():
        ebar = "Stamina"
        ecolor = (175, 175, 0)
        ecolor_dark = (150, 150, 0)
    elif "Projectiles" in player.stats.keys():
        ebar = "Projectiles"
        ecolor = (175, 88, 0)
        ecolor_dark = (150, 63, 0)
    elif "Mana" in player.stats.keys():
        ebar = "Mana"
        ecolor = (0, 0, 175)
        ecolor_dark = (0, 0, 150)
    
    w1 = (enemy.x-200*0.5+30-250) - (((enemy.x-200*0.5+30-250)*0.5-20)*2)
    w2 = w1*0.33

    h1 = (Height-20)-(player.y-100) - 30*3
    h2 = h1*0.25

    buttons = [
        [Button(((player.x-200*0.5+15)+220)+w2, (player.y-100)+h2, (enemy.x-200*0.5+30-250)*0.5-20, 30, (71, 130, 158), "Attack"), 1],
        [Button(((player.x-200*0.5+15)+220)+((enemy.x-200*0.5+30-250)*0.5-20)+(w2*2), (player.y-100)+h2, (enemy.x-200*0.5+30-250)*0.5-20, 30, (71, 130, 158), "Evade"), 2],
        [Button(((player.x-200*0.5+15)+220)+w2, (player.y-100)+(h2*2)+30, (enemy.x-200*0.5+30-250)*0.5-20, 30, (71, 130, 158), "Run"), 0],
        [Button(((player.x-200*0.5+15)+220)+((enemy.x-200*0.5+30-250)*0.5-20)+(w2*2), (player.y-100)+(h2*2)+30, (enemy.x-200*0.5+30-250)*0.5-20, 30, (71, 130, 158), "Use Inv"), 0],

        [Button(((player.x-200*0.5+15)+220)+w2, (player.y-100)+h2, (enemy.x-200*0.5+30-250)*0.5-20, 30, (71, 130, 158), "Attack1"), 0, "NAtt"],
        [Button(((player.x-200*0.5+15)+220)+((enemy.x-200*0.5+30-250)*0.5-20)+(w2*2), (player.y-100)+h2, (enemy.x-200*0.5+30-250)*0.5-20, 30, (71, 130, 158), "Attack2"), 0, "NAtt"],
        [Button(((player.x-200*0.5+15)+220)+w2, (player.y-100)+(h2*2)+30, (enemy.x-200*0.5+30-250)*0.5-20, 30, (71, 130, 158), "Attack3"), 0, "NAtt"],
        [Button(((player.x-200*0.5+15)+220)+((enemy.x-200*0.5+30-250)*0.5-20)+(w2*2), (player.y-100)+(h2*2)+30, (enemy.x-200*0.5+30-250)*0.5-20, 30, ecolor, "Special"), 0, "SAtt"],

        [Button(((player.x-200*0.5+15)+220)+w2, (player.y-100)+h2, (enemy.x-200*0.5+30-250)*0.5-20, 30, ecolor, "Dodge"), 0],
        [Button(((player.x-200*0.5+15)+220)+((enemy.x-200*0.5+30-250)*0.5-20)+(w2*2), (player.y-100)+h2, (enemy.x-200*0.5+30-250)*0.5-20, 30, ecolor, "Shield"), 0],
        [Button(((player.x-200*0.5+15)+220)+w2, (player.y-100)+(h2*2)+30, (enemy.x-200*0.5+30-250)*0.5-20, 30, ecolor, "Counter"), 0],
        [Button(((player.x-200*0.5+15)+220)+((enemy.x-200*0.5+30-250)*0.5-20)+(w2*2), (player.y-100)+(h2*2)+30, (enemy.x-200*0.5+30-250)*0.5-20, 30, (175, 0, 0), "Heal"), 0]
    ]
    button_back = Button((Width/2)-100, (Height-20)-30-h2, 200, 25, (150, 0, 0), "Back")
    cooldown = 1*60
    def redraw():
        win.fill((0,0,0))

        # background
        try:
            win.blit(sprites_Fight[Player.location], (0, 0))
        except:
            pass

        # draw stuff
        player.draw(win, [player.x-200*0.5+15, player.y-95], [player.x-200*0.5+15, player.y-60])
        enemy.draw(win)
        enemy.draw_bars(win, [enemy.x-200*0.5+30, enemy.y-60])
        inventory.draw_inventory(os.path.join("assets", "Fonts", "DefaultFont.TTF"))

        # choosing panel
        if pturn:
            pygame.draw.rect(win, (142, 112, 41), ((player.x-200*0.5+15)+220, player.y-100, enemy.x-200*0.5+30-250, (Height-20)-(player.y-100)))

            for button in buttons[button_group*4:(button_group+1)*4]:
                button[0].draw(win, (255,255,255), 2, os.path.join("assets", "Fonts", "DefaultFont.TTF"))

            if button_group:
                button_back.draw(win, (255,255,255), 2, os.path.join("assets", "Fonts", "DefaultFont.TTF"))
    
        # debug screen
        if debug_menu:
            debug()
    while True:
        clock.tick(FPS)
        redraw()
        
        if player.stats["Health"] > 0 and enemy.stats["Health"] > 0:
            if not pturn:
                cooldown -= 1
                if cooldown <= 0:
                    if dodge:
                        if random.randint(1, 4) == 4:
                            player.stats["Health"] -= enemy.stats["Attack"]
                    elif shield:
                        player.stats["Health"] -= int(enemy.stats["Attack"]*0.5)
                    if counter:
                        if random.randint(1, 2) == 2:
                            enemy.stats["Health"] -= player.stats["Attack"]
                        else:
                            player.stats["Health"] -= enemy.stats["Attack"]
                    else:
                        player.stats["Health"] -= enemy.stats["Attack"]
                    choose = True
                    attack = False
                    evade = False
                    dodge = False
                    shield = False
                    counter = False
                    pturn = True
                    cooldown = 60

            for event in pygame.event.get():
                mx, my = pygame.mouse.get_pos()
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    if use_inv:
                        if event.key == keys["Equip"]:
                            inventory.equip_item()
                        if event.key == keys["Throw"]:
                            inventory.throw_item()
                        if event.key == keys["Switch"]:
                            inventory.inv = not inventory.inv

                    if event.key == K_F11:
                            F11()
                    
                    if event.key == K_F3:
                        debug_menu = not debug_menu
                
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if pturn:
                            for button in buttons[button_group*4:(button_group+1)*4]:
                                if button[0].isOver([mx, my]):
                                    if len(button) == 3:
                                        if button[2] == "NAtt":
                                            enemy.stats["Health"] -= player.stats["Attack"]
                                            pturn = False
                                        elif button[2] == "SAtt":
                                            if player.stats[ebar] > 0:
                                                enemy.stats["Health"] -= int(player.stats["Attack"]*1.33)+1
                                                player.stats[ebar] -= 1
                                                pturn = False

                                    else:
                                        if button[0].text == "Dodge":
                                            if player.stats[ebar] - 2 > 0:
                                                player.stats[ebar] -= 2
                                                dodge = True
                                                pturn = False
                                        elif button[0].text == "Shield":
                                            if player.stats[ebar] > 0:
                                                player.stats[ebar] -= 1
                                                shield = True
                                                pturn = False
                                        elif button[0].text == "Counter":
                                            if player.stats[ebar] - 2 > 0:
                                                player.stats[ebar] -= 2
                                                counter = True
                                                pturn = False
                                        elif button[0].text == "Heal":
                                            if player.stats["Health"] != player.stats["Max Health"]:
                                                player.stats["Health"] += 2
                                                pturn = False
                                        
                                        elif button[0].text == "Run":
                                            return False

                                        elif button[0].text == "Use Inv":
                                            use_inv = not use_inv

                                    button_group = button[1]

                            if button_group:
                                if button_back.isOver([mx, my]):
                                    button_group = 0

                if event.type == MOUSEMOTION:
                    for button in buttons:
                        if button[0].isOver([mx, my]):
                            if button[0].color == (71, 130, 158):
                                button[0].color = (58, 99, 142)
                            if button[0].color == ecolor:
                                button[0].color == ecolor_dark
                            if button[0].color == (175, 0, 0):
                                button[0].color == (150, 0, 0)
                        else:
                            if button[0].color == (58, 99, 142):
                                button[0].color = (71, 130, 158)
                            if button[0].color == ecolor_dark:
                                button[0].color == ecolor
                            if button[0].color == (150, 0, 0):
                                button[0].color == (175, 0, 0)

                    if button_back.isOver([mx, my]):
                        button_back.color = (128, 0, 0)
                    else:
                        button_back.color = (150, 0, 0)
                
                if use_inv:
                    inventory.select_item(event)
        else:
            if player.stats["Health"] <= 0:
                del enemy
                return "dead"
            elif enemy.stats["Health"] <= 0:
                del enemy
                return None
        pygame.display.flip()

def pause(func):
    global Width, Height
    set_button_over = False
    strt_button_over = False
    exit_button_over = False

    w1 = 400-(50*3)
    w2 = w1*0.25

    button_set = Button(((Width*0.5)-(400*0.5))+w2, Height*0.5+20, 50, 50, (0,0,0))
    button_strt = Button(((Width*0.5)-(400*0.5))+37.5+(w2*2), Height*0.5-5, 75, 75, (0,0,0))
    button_exit = Button(((Width*0.5)-(400*0.5))+(50*2)+(w2*3), Height*0.5+20, 50, 50, (0,0,0))

    surf = pygame.Surface((Width, Height))
    surf.fill((0,0,0))
    surf.set_alpha(200)
    def redraw(surf):
        func()
        win.blit(surf, (0,0))

        display_size = pygame.display.get_surface().get_size()
        Width, Height = display_size

        surf = pygame.transform.scale(surf, (Width, Height))
        surf.fill((0,0,0))

        try:
            loc = Player.location.split(" ")
        except AttributeError:
            loc = [None]

        if loc[0] == "House":
            pygame.draw.rect(win, (216, 201, 86), ((Width*0.5)-(400*0.5), (Height*0.5)-(200*0.5), 400, 200))
        else:
            pygame.draw.rect(win, (0, 0, 0), ((Width*0.5)-(400*0.5), (Height*0.5)-(200*0.5), 400, 200))
        pygame.draw.rect(win, (255,255,255), ((Width*0.5)-(400*0.5)-1, (Height*0.5)-(200*0.5)-1, 401, 201), 3)

        button_set.x, button_set.y = ((Width*0.5)-(400*0.5))+w2, Height*0.5+20
        button_strt.x, button_strt.y = ((Width*0.5)-(400*0.5))+37.5+(w2*2), Height*0.5-5
        button_exit.x, button_exit.y = ((Width*0.5)-(400*0.5))+(50*2)+(w2*3), Height*0.5+20
        

        if not set_button_over:
            win.blit(sprites_Misc["Settings NotOver"], (button_set.x, button_set.y))
        else:
            win.blit(sprites_Misc["Settings Over"], (button_set.x, button_set.y))
        if not strt_button_over:
            win.blit(sprites_Misc["Resume NotOver"], (button_strt.x, button_strt.y))
        else:
            win.blit(sprites_Misc["Resume Over"], (button_strt.x, button_strt.y))
        if not exit_button_over:
            win.blit(sprites_Misc["Quit NotOver"], (button_exit.x, button_exit.y))
        else:
            win.blit(sprites_Misc["Quit Over"], (button_exit.x, button_exit.y))

        win.blit(render_text("Paused Game", 28, (255,255,255)), ((Width*0.5)-(render_text("Paused Game", 28, (255,255,255)).get_width()*0.5), (Height*0.5)-(200*0.5)+20))

        brightness()

    while True:
        clock.tick(FPS)
        redraw(surf)

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
                    if button_exit.isOver([mx, my]):
                        pygame.quit()
                        sys.exit()

            if event.type == MOUSEMOTION:
                if button_set.isOver([mx, my]):
                    set_button_over = True
                else:
                    set_button_over = False
                if button_strt.isOver([mx, my]):
                    strt_button_over = True
                else:
                    strt_button_over = False
                if button_exit.isOver([mx, my]):
                    exit_button_over = True
                else:
                    exit_button_over = False
                
        pygame.display.flip()

def main_menu():
    global FPS, debug_menu
    last_time = time.time()
    set_button_over = False
    exit_button_over = False

    button_new = Button((Width*0.5)-(400*0.5), (Height*0.5)-(70*0.5), 400, 70, (0,0,0), "New Game")
    if os.path.isfile(os.path.join(os.getenv("localappdata"), ".inseynia", "saves", "save.json")):
        button_load = Button((Width*0.5)-(400*0.5), (Height*0.5)-(70*0.5)+100, 400, 70, (0,0,0), "Load Game")
    else:
        button_load = Button((Width*0.5)-(400*0.5), (Height*0.5)-(70*0.5)+100, 400, 70, (0,0,0), "Load Game", (128,128,128))

    button_tutor = Button((Width*0.5)-(400*0.5), (Height*0.5)-(70*0.5)+200, 400, 70, (0,0,0), "Tutorial")
    button_set = Button(25, Height-75, 50, 50, (0,0,0))
    button_exit = Button(Width-75, Height-75, 50, 50, (0,0,0))
    def redraw():
        win.fill((0,0,0))
        win.blit(BG["Main Menu"], (0,0))

        display_size = pygame.display.get_surface().get_size()
        Width, Height = display_size

        if debug_menu:
            debug()

        win.blit(render_text("Inseynia", 72, (255,255,255)), ((Width*0.5)-(render_text("Inseynia", 72, (255,255,255)).get_width()*0.5), 100))

        button_new.x, button_new.y = (Width*0.5)-(400*0.5), (Height*0.5)-(70*0.5)
        button_tutor.x, button_tutor.y = (Width*0.5)-(400*0.5), (Height*0.5)-(70*0.5)+200
        button_load.x, button_load.y = (Width*0.5)-(400*0.5), (Height*0.5)-(70*0.5)+100
        button_set.x, button_set.y = 25, Height-75
        button_exit.x, button_exit.y = Width-75, Height-75

        button_new.draw(win, (255,255,255), font_name=os.path.join("assets", "Fonts", "DefaultFont.TTF"))
        button_tutor.draw(win, (255,255,255), font_name=os.path.join("assets", "Fonts", "DefaultFont.TTF"))
        if os.path.isfile(os.path.join(os.getenv("localappdata"), ".inseynia", "saves", "save.json")):
            button_load.draw(win, (255,255,255), font_name=os.path.join("assets", "Fonts", "DefaultFont.TTF"))
        else:
            button_load.draw(win, (128,128,128), font_name=os.path.join("assets", "Fonts", "DefaultFont.TTF"))

        if set_button_over:
            win.blit(sprites_Misc["Settings Over"], (button_set.x, button_set.y))
        else:
            win.blit(sprites_Misc["Settings NotOver"], (button_set.x, button_set.y))
        
        if exit_button_over:
            win.blit(sprites_Misc["Quit Over"], (button_exit.x, button_exit.y))
        else:
            win.blit(sprites_Misc["Quit NotOver"], (button_exit.x, button_exit.y))

        win.blit(pygame.transform.scale(win, display_size), (0, 0))

        brightness()
    while True:
        redraw()
        clock.tick(FPS)

        dt = FPS_ind(last_time)
        last_time = time.time()

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
                    if button_new.isOver([mx, my]):
                        story()

                    if button_tutor.isOver([mx, my]):
                        tutorial()
                    
                    if button_load.isOver([mx, my]):
                        return True

                    if button_set.isOver([mx, my]):
                        settings_menu()
                    
                    if button_exit.isOver([mx, my]):
                        pygame.quit()
                        sys.exit()
                    
            if event.type == MOUSEMOTION:
                if button_new.isOver([mx, my]):
                    button_new.color = (0, 128, 0)
                else:
                    button_new.color = (0,0,0)

                if button_tutor.isOver([mx, my]):
                    button_tutor.color = (128, 0, 128)
                else:
                    button_tutor.color = (0,0,0)

                if os.path.isfile(os.path.join(os.getenv("localappdata"), ".inseynia", "saves", "save.json")):
                    if button_load.isOver([mx, my]):
                        button_load.color = (0, 0, 128)
                    else:
                        button_load.color = (0,0,0)


                if button_set.isOver([mx, my]):
                    set_button_over = True
                else:
                    set_button_over = False
                
                if button_exit.isOver([mx, my]):
                    exit_button_over = True
                else:
                    exit_button_over = False

        pygame.display.flip()

def settings_menu():
    global FPS
    def global_redraw():
        win.fill((0,0,0))
        win.blit(BG["Main Menu"], (0,0))

        if debug_menu:
            debug()
    
    def main():
        global debug_menu
        last_time = time.time()

        button_video = Button((Width*0.5)-(400*0.5), (Height*0.5)-(70*0.5), 400, 70, (0,0,0), "Video")
        button_volume = Button((Width*0.5)-(400*0.5), (Height*0.5)-(70*0.5)+100, 400, 70, (0,0,0), "Volume")
        button_controls = Button((Width*0.5)-(400*0.5), (Height*0.5)-(70*0.5)+200, 400, 70, (0,0,0), "Controls")
        button_back = Button((Width*0.5)-(200*0.5), (Height*0.5)-(35*0.5)+275, 200, 35, (0,0,0), "Back")
        def redraw():
            global_redraw()

            display_size = pygame.display.get_surface().get_size()
            Width, Height = display_size

            win.blit(render_text("Settings", 72, (255,255,255)), ((Width*0.5)-(render_text("Settings", 72, (255,255,255)).get_width()*0.5), 100))

            button_video.x, button_video.y = (Width*0.5)-(400*0.5), (Height*0.5)-(70*0.5)
            button_volume.x, button_volume.y = (Width*0.5)-(400*0.5), (Height*0.5)-(70*0.5)+100
            button_controls.x, button_controls.y = (Width*0.5)-(400*0.5), (Height*0.5)-(70*0.5)+200
            button_back.x, button_back.y = (Width*0.5)-(200*0.5), (Height*0.5)-(35*0.5)+275

            button_video.draw(win, (255,255,255), font_name=os.path.join("assets", "Fonts", "DefaultFont.TTF"))
            button_volume.draw(win, (255,255,255), font_name=os.path.join("assets", "Fonts", "DefaultFont.TTF"))
            button_controls.draw(win, (255,255,255), font_name=os.path.join("assets", "Fonts", "DefaultFont.TTF"))
            button_back.draw(win, (255,255,255), font_name=os.path.join("assets", "Fonts", "DefaultFont.TTF"))

            win.blit(pygame.transform.scale(win, display_size), (0,0))

            brightness()

        while True:
            redraw()
            clock.tick(FPS)

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
                        button_video.color = (0, 128, 0)
                    else:
                        button_video.color = (0,0,0)

                    if button_volume.isOver([mx, my]):
                        button_volume.color = (128, 0, 128)
                    else:
                        button_volume.color = (0,0,0)

                    if button_controls.isOver([mx, my]):
                        button_controls.color = (0, 0, 128)
                    else:
                        button_controls.color = (0,0,0)

                    if button_back.isOver([mx, my]):
                        button_back.color = (128, 0, 0)
                    else:
                        button_back.color = (0, 0, 0)

            pygame.display.flip()

    def video_settings():
        global fullscreen, resol, FPS, set_brightness, debug_menu
        fullscreen_init = fullscreen
        resol_init = resol
        FPS_init = FPS
        brightness_init = set_brightness
        
        last_time = time.time()

        resolutions = [
            None,
            (1920, 1080),
            (1600, 900),
            (1280, 720),
            (1024, 768),
            (960, 720),
            (800, 600)
        ]
        resol_index = 0
        for resolution in resolutions:
            if resolution == resol:
                break
            resol_index += 1

        resol_rect = pygame.Rect((Width*0.5)-(400*0.5), (Height*0.5)-(70*0.5)-75, 400, 70)
        resol_front = Button((Width*0.5)-(400*0.5)+425, (Height*0.5)-(70*0.5)-75, 100, 70, (128,128,128))
        resol_back = Button((Width*0.5)-(400*0.5)-125, (Height*0.5)-(70*0.5)-75, 100, 70, (128,128,128))

        button_fullscreen = Button((Width*0.5)-(500*0.5), (Height*0.5)-(70*0.5), 500, 70, (0,0,0), "Fullscreen")
        button_back = Button((Width*0.5)-(200*0.5)-175, (Height*0.5)-(35*0.5)+275, 200, 35, (0,0,0), "Back")
        button_apply = Button((Width*0.5)-(200*0.5)+175, (Height*0.5)-(35*0.5)+275, 200, 35, (0,0,0), "Apply")

        if FPS_init == 1:
            slider_FPS = SliderX((Width*0.5)-(500*0.5), (Height*0.5)-(70*0.5)+100, 500, 70, (0,0,0), 1, (99, 155, 255), "FPS")
        elif FPS_init == 2147483647:
            slider_FPS = SliderX((Width*0.5)-(500*0.5), (Height*0.5)-(70*0.5)+100, 500, 70, (0,0,0), 500, (99, 155, 255), "FPS")
        else:
            slider_FPS = SliderX((Width*0.5)-(500*0.5), (Height*0.5)-(70*0.5)+100, 500, 70, (0,0,0), int(FPS_init*2), (99, 155, 255), "FPS")

        slider_brightness = SliderX((Width*0.5)-(500*0.5), (Height*0.5)-(70*0.5)+200, 500, 70, (0,0,0), 0, (128, 0, 0), "brightness")
        slider_brightness.width2 = int((((brightness_init + 200) / 2.5) / 100) * (slider_brightness.width-40)+40)

        slider_FPS_slide = False
        slider_brightness_slide = False
        def redraw():
            global_redraw()

            if fullscreen_init == True:
                button_fullscreen.text = "Fullscreen On"
            else:
                button_fullscreen.text = "Fullscreen Off"

            display_size = pygame.display.get_surface().get_size()
            Width, Height = display_size

            win.blit(render_text("Video Settings", 48, (255,255,255)), ((Width*0.5)-(render_text("Video Settings", 48, (255,255,255)).get_width()*0.5), 50))

            button_fullscreen.x, button_fullscreen.y = (Width*0.5)-(500*0.5), (Height*0.5)-(70*0.5)
            button_back.x, button_back.y = (Width*0.5)-(200*0.5)-175, (Height*0.5)-(35*0.5)+275
            button_apply.x, button_apply.y = (Width*0.5)-(200*0.5)+175, (Height*0.5)-(35*0.5)+275

            resol_front.x, resol_front.y = (Width*0.5)-(400*0.5)+425, (Height*0.5)-(70*0.5)-100
            resol_back.x, resol_back.y = (Width*0.5)-(400*0.5)-125, (Height*0.5)-(70*0.5)-100
            resol_rect.x, resol_rect.y = (Width*0.5)-(400*0.5), (Height*0.5)-(70*0.5)-100

            slider_FPS.x, slider_FPS.y = (Width*0.5)-(500*0.5), (Height*0.5)-(70*0.5)+100
            slider_brightness.x, slider_brightness.y = (Width*0.5)-(500*0.5), (Height*0.5)-(70*0.5)+200
            
            if not FPS_init == 2147483647:
                slider_FPS.text = f"{FPS_init} FPS"
            else:
                slider_FPS.text = "Unlimited FPS"

            slider_brightness.text = f"Brightness {int(((slider_brightness.width2-40)/(slider_brightness.width-40))*100)}%"

            win.blit(sprites_Misc["Resol Next"], (resol_front.x, resol_front.y))
            win.blit(sprites_Misc["Resol Previous"], (resol_back.x, resol_back.y))
            pygame.draw.rect(win, (255,255,255), resol_rect, 3)
            if not resol_init:
                win.blit(render_text("Current", 32, (255,255,255)), ((Width*0.5)-(render_text("Current", 32, (255,255,255)).get_width()*0.5), (Height*0.5)-(render_text("Current", 32, (255,255,255)).get_height()*0.5)-100))
            else:
                win.blit(render_text(f"{resol_init[0]}x{resol_init[1]}", 32, (255,255,255)), ((Width*0.5)-(render_text(f"{resol_init[0]}x{resol_init[1]}", 32, (255,255,255)).get_width()*0.5), (Height*0.5)-(render_text(f"{resol_init[0]}x{resol_init[1]}", 32, (255,255,255)).get_height()*0.5)-100))

            button_fullscreen.draw(win, (255,255,255), font_name=os.path.join("assets", "Fonts", "DefaultFont.TTF"))
            button_back.draw(win, (255,255,255), font_name=os.path.join("assets", "Fonts", "DefaultFont.TTF"))
            button_apply.draw(win, (255,255,255), font_name=os.path.join("assets", "Fonts", "DefaultFont.TTF"))

            slider_FPS.draw(win, (255,255,255), font_name=os.path.join("assets", "Fonts", "DefaultFont.TTF"))
            
            brightness()
            
            slider_brightness.draw(win, (255,255,255), font_name=os.path.join("assets", "Fonts", "DefaultFont.TTF"))

            fade = pygame.Surface((slider_brightness.width+5, slider_brightness.height+5))
            if brightness_init < 0:
                fade.fill((0,0,0))
            elif brightness_init > 0:
                fade.fill((255,255,255))
            fade.set_alpha(abs(brightness_init))
            win.blit(fade, (slider_brightness.x-2,slider_brightness.y-2))
            
        while True:
            clock.tick(FPS)
            redraw()

            dt = FPS_ind(last_time)
            last_time = time.time()
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
            if slider_brightness.width2 <= 40:
                brightness_init = -200
            elif slider_brightness.width2 >= slider_brightness.width:
                brightness_init = 50
            else:
                brightness_init = int(2.5*((slider_brightness.width2-40)/(slider_brightness.width-40)*100)-200)

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
                        FPS = FPS_init
                        resol = resol_init
                        fullscreen = fullscreen_init
                        save_settings()

                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if button_fullscreen.isOver([mx, my]):
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
                            F11(fullscreen_param=fullscreen_init)
                            change_resol(resol_init)
                            FPS = FPS_init
                            resol = resol_init
                            fullscreen = fullscreen_init
                            set_brightness = brightness_init
                            save_settings()
                        
                    if event.button == 4 or event.button == 5:
                        if slider_FPS.isOver([mx, my]):
                            slider_FPS.scroll(event.button, 4)
                        
                        if slider_brightness.isOver([mx, my]):
                            slider_brightness.scroll(event.button, 4)

                if event.type == MOUSEBUTTONUP:
                    if event.button == 1:
                        if slider_FPS.isOver([mx, my]):
                            slider_FPS_slide = False

                        if slider_brightness.isOver([mx, my]):
                            slider_brightness_slide = False

                if event.type == MOUSEMOTION:
                    if button_fullscreen.isOver([mx, my]):
                        button_fullscreen.color = (0, 128, 128)
                    else:
                        button_fullscreen.color = (0,0,0)

                    if button_back.isOver([mx, my]):
                        button_back.color = (128, 0, 0)
                    else:
                        button_back.color = (0, 0, 0)

                    if button_apply.isOver([mx, my]):
                        button_apply.color = (0, 128, 0)
                    else:
                        button_apply.color = (0, 0, 0)

            pygame.display.flip()

    def volume_settings():
        global debug_menu
        last_time = time.time()

        #slider_master = SliderX((0,0,0), (Width*0.5)-(700*0.5), (Height*0.5)-(100*0.5)-25, 700, 100, (128,128,0), 700*0.5, "Master Volume")
        slider_music = SliderX((Width*0.5)-350, (Height*0.5)-(70*0.5)+75, 325, 70, (0,0,0), 325*0.5, (0,128,0), "Music")
        slider_sfx = SliderX((Width*0.5)+25, (Height*0.5)-(70*0.5)+75, 325, 70, (0,0,0), 325*0.5, (0,128,128), "SFX")

        slider_music_slide = False
        slider_sfx_slide = False

        button_back = Button((Width*0.5)-(200*0.5), (Height*0.5)-(35*0.5)+275, 200, 35, (0,0,0), "Back")
        def redraw():
            global_redraw()

            display_size = pygame.display.get_surface().get_size()
            Width, Height = display_size

            win.blit(render_text("Volume Settings", 48, (255,255,255)), ((Width*0.5)-(render_text("Volume Settings", 48, (255,255,255)).get_width()*0.5), 100))

            slider_music.x, slider_music.y = (Width*0.5)-350, (Height*0.5)-(70*0.5)+75
            slider_sfx.x, slider_sfx.y = (Width*0.5)+50, (Height*0.5)-(70*0.5)+75

            button_back.x, button_back.y = (Width*0.5)-(200*0.5), (Height*0.5)-(35*0.5)+275

            slider_music.draw(win, (255,255,255), font_name=os.path.join("assets", "Fonts", "DefaultFont.TTF"))
            slider_sfx.draw(win, (255,255,255), font_name=os.path.join("assets", "Fonts", "DefaultFont.TTF"))

            button_back.draw(win, (255,255,255), font_name=os.path.join("assets", "Fonts", "DefaultFont.TTF"))
        
            brightness()
        
        while True:
            clock.tick(FPS)
            redraw()

            dt = FPS_ind(last_time)
            last_time = time.time()
            mx, my = pygame.mouse.get_pos()

            if slider_music_slide:
                slider_music.move([mx, my])
            
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
                        button_back.color = (128, 0, 0)
                    else:
                        button_back.color = (0, 0, 0)

            pygame.display.flip()

    def controls():
        global debug_menu
        last_time = time.time()

        change = None

        new_key = None
        old_key = None
        
        buttons = {
            "Up": Button((Width*0.5)-(450*0.5), (Height*0.5)-160, 450, 35, (0,0,0), f"Up: {pygame.key.name(keys['Up'])}"),
            "Down": Button((Width*0.5)-(450*0.5), (Height*0.5)-115, 450, 35, (0,0,0), f"Down: {pygame.key.name(keys['Down'])}"),
            "Left": Button((Width*0.5)-(450*0.5), (Height*0.5)-25, 450, 35, (0,0,0), f"Left: {pygame.key.name(keys['Left'])}"),
            "Right": Button((Width*0.5)-(450*0.5), (Height*0.5)-70, 450, 35, (0,0,0), f"Right: {pygame.key.name(keys['Right'])}"),
            "Throw": Button((Width*0.5)-(450*0.5), (Height*0.5)+20, 450, 35, (0,0,0), f"Throw Item: {pygame.key.name(keys['Throw'])}"),
            "Equip": Button((Width*0.5)-(450*0.5), (Height*0.5)+65, 450, 35, (0,0,0), f"Equip/Unequip Item: {pygame.key.name(keys['Equip'])}"),
            "Switch": Button((Width*0.5)-(450*0.5), (Height*0.5)+110, 450, 35, (0,0,0), f"View Equipment/Inventory: {pygame.key.name(keys['Switch'])}"),
            "Pause": Button((Width*0.5)-(450*0.5), (Height*0.5)+155, 450, 35, (0,0,0), f"Pause Gme: {pygame.key.name(keys['Pause'])}")
        }
        
        button_back = Button((Width*0.5)-(200*0.5), (Height*0.5)-(35*0.5)+275, 200, 35, (0,0,0), "Back")
        def redraw():
            global_redraw()

            win.blit(render_text("Controls", 48, (255,255,255)), ((Width*0.5)-(render_text("Controls", 48, (255,255,255)).get_width()*0.5), 50))

            if not change:
                for name in buttons.keys():
                    buttons[name].text = f"{name.capitalize()}: {pygame.key.name(keys[name]).capitalize()}"
            else:
                for name, button in buttons.items():
                    if name == change:
                        buttons[name].text = "--Please Select A Key--"
                        break

            for button in buttons.values():
                button.draw(win, (255,255,255), font_name=os.path.join("assets", "Fonts", "DefaultFont.TTF"), dynamic_width=True)
            
            button_back.draw(win, (255,255,255), font_name=os.path.join("assets", "Fonts", "DefaultFont.TTF"))
        
            brightness()
        while True:
            clock.tick(FPS)
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
                        button_back.color = (128, 0, 0)
                    else:
                        button_back.color = (0, 0, 0)

            pygame.display.flip()

    main()
    return

def tutorial():
    pass

def story():
    pages = [
        Story(["Once upon a time, a mysterious dark power", "took over the land of Bolgenra,", "corrupting it and forcing darkness upon it's people.", 'The people of Bolgenra called it: "Inseynia".']),
        Story(["There is a myth, saying that Inseynia", "will be stopped by a brave hero", 'who will rise when the "Brighter Sun" rises.', ""]),
        Story(["The Brighter Sun is summoned when", "the star, Thydor, explodes. The explosion is thought", "to outshine all other light and brighten the night sky.", ""]),
        Story(["Different people from different countries", "and cultures call the hero different names,", " but he is most commonly known as: Hormanson.", ""]),
        Story(["People created theories about this creature,", "some were more realistic than others,", "but the most accepted theory is that Hormanson", "is the son of the Inseynian Horseman."]),
        Story(["Hormanson was thought to be and Inseynian", "flike his father, but during the Rain of the Rays,", "Hormanson was captured by the rays", "and had been deeply affected."]),
        Story(["These rays affected Hormanson", "from being an Inseynian to a Barbairniyan.", "", ""]),
        Story(["Hormanson was locked away by the", "Biome Kings because of his awful mistakes", "of destroying their lands.", ""]),
        Story(["Hormanson promised not to do it again", "and that he was deeply sorry,", "but no one trusted him or set him free.", ""]),
        Story(["And he is currently waiting for someone to", "defeat the Biome Kings and the Horseman", "to set him free so that he can", "get out and destroy Inseynia. Once. And for all."])
    ]
    def redraw():
        win.fill((0,0,0))
        try:
            page.render(win, sprites_Story_Photoes[f"S{pages.index(page)+1}"])
        except:
            page.render(win)
        brightness()

    def load_game():
        Player.location = "House 1"

        pick_ups = load_json(["scripts", "data", "pick ups.json"])

        for room, items in pick_ups.items():
            for item in items.keys():
                pick_ups[room][item] = False

        dump_json(["scripts", "data", "pick ups.json"], pick_ups)

        save_game()
        main_game("House 1")

    for page in pages:
        if pages.index(page) > 0:
            fade_in(redraw, 2)
        else:
            fade_in(redraw, 0.7)

        redraw()
        pygame.display.flip()

        if page.update_text(win, redraw):
            fade_out(redraw, 3)
            load_game()

        for _ in range(5*60):
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == KEYDOWN:
                    if event.key == K_F11:
                        F11()
                    elif event.key == K_F3:
                        debug_menu = not debug_menu
                    else:
                        fade_out(redraw, 3)
                        load_game()

        fade_out(redraw, 2)

    load_game()

def main_game(loc):
    global debug_menu
    
    pick_ups = load_json(["scripts", "data", "pick ups.json"])

    get_data = True

    # Room Data
    rdata = {
        "House 1": {
            "playerx": 1000,
            "playery": 600,
            "drops": [
                ["Wooden Sword", Drop(800, 500, sprites_Equipment["Wooden Sword"]), 0],
                ["Wooden Shield", Drop(800, 600, sprites_Equipment["Wooden Shield"]), 0],
            ],
            "enemies": [],
            "exits": {
                "House 2": pygame.Rect(200, 200, 100, 50)
            }
        },
        "House 2": {
            "playerx": 200,
            "playery": 300,
            "drops": [
                ["Crossbow", Drop(800, 200, sprites_Equipment["Crossbow"]), 0],
                ["ph1", Drop(600, 800, sprites_Equipment["ph1"]), 0],
            ],
            "enemies": [],
            "exits": {
                "House 1": pygame.Rect(200, Height-200, 100, 50)
            }
        }
    }

    last_time = time.time()

    inventory = Inventory()
    player = Player(0, 0, "Down")

    drops = []
    enemies = []

    def redraw():
        win.fill((0,0,0))
        player.draw(win)
        for item in drops:
            item[1].draw(win)

        for enemy in enemies:
            enemy.draw(win)
        inventory.draw_inventory(os.path.join("assets", "Fonts", "DefaultFont.TTF"))

        if debug_menu:
            debug(player.x, player.y)

        brightness()
        
    while True:
        if get_data:
            player.x, player.y = rdata[loc]["playerx"], rdata[loc]["playery"]
            player.rect.x, player.rect.y = rdata[loc]["playerx"], rdata[loc]["playery"]
            
            drops = rdata[loc]["drops"]
            enemies = rdata[loc]["enemies"]

            try:
                for item_name in pick_ups[loc].keys():
                    if pick_ups[loc][item_name]:
                        for drop in drops:
                            if item_name in drop:
                                del drops[drops.index(drop)]
            except KeyError:
                pass

            get_data = False

        redraw()

        dt = FPS_ind(last_time)
        last_time = time.time()

        for item in drops:
            item[2] -= 1*dt
            if player.rect.colliderect(item[1].rect) and item[2] <= 0:
                inventory.grab_item(item[0], 1)
                try:
                    pick_ups[loc][item[0]] = True
                except KeyError:
                    pass

                del drops[drops.index(item)]

        for enemy in enemies:
            enemy.move([player.x, player.y])

            if enemy.collision(player.rect):
                enemy.in_fight = True

            if enemy.in_fight:
                enemy.in_fight = fight(enemy)
                if enemy.in_fight == None:
                    del enemies[enemies.index(enemy)]
                elif enemy.in_fight == "dead":
                    return "dead"
                player.x -= 100
                player.rect.x -= 100

        player.move()

        for next_room, coll in rdata[loc]["exits"].items():
            if player.rect.colliderect(coll):
                loc = next_room
                Player.location = next_room
                get_data = True

                save_game()
                dump_json(["scripts", "data", "pick ups.json"], pick_ups)

                break

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == keys["Equip"]:
                    inventory.equip_item()
                if event.key == keys["Throw"]:
                    x = inventory.throw_item([player.x, player.y])
                    if x: drops.append(x)
                if event.key == keys["Switch"]:
                    inventory.inv = not inventory.inv
                if event.key == keys["Pause"]:
                    pause(redraw)

                if event.key == K_F11:
                    F11()
                if event.key == K_F3:
                    debug_menu = not debug_menu

            inventory.select_item(event)
        pygame.display.flip()

def dev_room():
    def global_redraw():
        win.fill((0,0,0))
    
    def access():
        user_input = ""
        input_pass = TextBox((0,0,0), (Width*0.5)-(500*0.5)-50, (Height*0.5)-(100*0.5), 500, 100, "Enter Password", clear_text_when_click=True)
        password = "66VnGz28HH"
        
        button_enter = Button(input_pass.width+(50+150), (Height*0.5)-(50*0.5)-25, 150, 40, (0,128,0), "Enter")
        button_cancel = Button(input_pass.width+(50+150), (Height*0.5)-(50*0.5)+25, 150, 40, (128,0,0), "Cancel")
        
        def redraw():
            global_redraw()

            input_pass.x, input_pass.y = (Width*0.5)-(500*0.5)-50, (Height*0.5)-(100*0.5)
            button_enter.x, button_enter.y = input_pass.width+(150-25), input_pass.y+5
            button_cancel.x, button_cancel.y = input_pass.width+(150-25), input_pass.y+55

            input_pass.draw(win, (255,255,255), font_name=os.path.join("assets", "Fonts", "DefaultFont.TTF"), font_size=32)
            button_enter.draw(win, (255,255,255), font_name=os.path.join("assets", "Fonts", "DefaultFont.TTF"))
            button_cancel.draw(win, (255,255,255), font_name=os.path.join("assets", "Fonts", "DefaultFont.TTF"))

            brightness()
        while True:
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
        global debug_menu
        last_time = time.time()

        inventory = Inventory()

        player = Player(100, 100, "Down")

        drops = [
            ["Crossbow", Drop(500, 500, sprites_Equipment['Crossbow']), 0],
            ["Wooden Sword", Drop(300, 300, sprites_Equipment["Wooden Sword"]), 0],
            ["ph1", Drop(300, 100, sprites_Equipment["ph1"]), 0],
            ["ph2", Drop(400, 200, sprites_Equipment["ph2"]), 0],
            ["ph3", Drop(500, 300, sprites_Equipment["ph3"]), 0],
            ["ph4", Drop(100, 300, sprites_Equipment["ph4"]), 0],
            ["Wooden Shield", Drop(600, 500, sprites_Equipment["Wooden Shield"]), 0]
        ]
        enemies = []
        def redraw():
            global_redraw()
            player.draw(win)
            for item in drops:
                item[1].draw(win)

            for enemy in enemies:
                enemy.draw(win)
            inventory.draw_inventory(os.path.join("assets", "Fonts", "DefaultFont.TTF"))

            if debug_menu:
                debug(player.x, player.y)

            brightness()
            
        while True:
            redraw()

            dt = FPS_ind(last_time)
            last_time = time.time()

            for item in drops:
                item[2] -= 1*dt
                if player.rect.colliderect(item[1].rect) and item[2] <= 0:
                    inventory.grab_item(item[0], 1)
                    del drops[drops.index(item)]

            for enemy in enemies:
                enemy.move([player.x, player.y])

                if enemy.collision(player.rect):
                    enemy.in_fight = True

                if enemy.in_fight:
                    enemy.in_fight = fight(enemy)
                    if enemy.in_fight == None:
                        del enemies[enemies.index(enemy)]
                    elif enemy.in_fight == "dead":
                        return "dead"
                    player.x -= 100
                    player.rect.x -= 100

            player.move()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    if event.key == keys["Equip"]:
                        inventory.equip_item()
                    if event.key == keys["Throw"]:
                        x = inventory.throw_item([player.x, player.y])
                        if x: drops.append(x)
                    if event.key == keys["Switch"]:
                        inventory.inv = not inventory.inv
                    if event.key == keys["Pause"]:
                        pause(redraw)

                    if event.key == K_F11:
                        F11()
                    if event.key == K_F3:
                        debug_menu = not debug_menu
                    
                    if event.key == K_x:
                        enemies.append(Enemy(player.x+100, player.y, "Test Enemy"))
                
                inventory.select_item(event)
            pygame.display.flip()
    
    #if access():
    room()

while True:
    if main_menu():
        stored_data = load_json([os.getenv("localappdata"), ".inseynia", "saves", "save.json"])
    
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