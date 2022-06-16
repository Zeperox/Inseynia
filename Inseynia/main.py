try:
    # python -m cProfile -m main.py >> output.txt

    # Import modules
    import pygame, sys, os, random, time, platform, warnings

    from pygame.locals import *
    from pypresence import Presence

    # Import Scripts
    from scripts.UI.window import settings, Width, Height, win

    from scripts.loading.json_functions import load_json, dump_json
    from scripts.loading.music_player import musics
    from scripts.loading.SFX import SFX_list
    from scripts.loading.sprites import sprites

    from scripts.logic.drops import Drop
    from scripts.logic.inventory import Inventory
    from scripts.logic.player import Player, weapons

    from scripts.maps.tiles import TileMap

    from scripts.UI.brightness import Brightness
    from scripts.UI.button import Button
    from scripts.UI.camera import Camera
    from scripts.UI.text import Text
    from scripts.UI.textbox import Textbox
    from scripts.UI.slider import Slider

    from scripts.custom_collisions.obb import OBB
    from scripts.custom_collisions.polygon import Polygon

    from scripts.AI.ekretatree import AI


    # pygame inits
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()
    pygame.mixer.set_num_channels(128)

    pygame.event.set_allowed([KEYDOWN, MOUSEBUTTONDOWN, MOUSEMOTION, MOUSEBUTTONUP, QUIT])


    # Vars
    true_scroll = [0, 0]; scroll = [0, 0]
    brightness_overlay = Brightness((0, 0), (Width, Height), settings["Brightness"])

    for music in musics.values():
        music.set_volume(settings["Volumes"]["Music"], True)

    sprites["Main Menu BG"] = pygame.transform.scale(sprites["Main Menu BG"], (Width, Height))

    #debug menu
    debug_menu = False
    show_hitboxes = False
    show_mid = False
    show_view = False

    fps_text = Text(os.path.join("assets", "fontsDL", "Font.png"), "0", 24, (255,255,255))
    pos_text = Text(os.path.join("assets", "fontsDL", "Font.png"), "0", 24, (255,255,255))
    room_text = Text(os.path.join("assets", "fontsDL", "Font.png"), "0", 24, (255,255,255))

    fps_surf = pygame.Surface((fps_text.width*9+6, fps_text.height+6))
    fps_surf.fill((100,100,100))
    fps_surf.set_alpha(200)
    pos_surf = pygame.Surface((pos_text.width*17+6, pos_text.height+6))
    pos_surf.fill((100,100,100))
    pos_surf.set_alpha(200)
    room_surf = pygame.Surface((room_text.width*17+6, room_text.height+6))
    room_surf.fill((100,100,100))
    room_surf.set_alpha(200)

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
                state="In Menu",
                large_image="inseynia",
                large_text="Inseynia",
                start=start_time
            )

    warnings.filterwarnings("ignore")
    start_rpc()
    warnings.filterwarnings("default")

    def FPS_ind(last_time):
        return (time.time() - last_time) * 60, time.time()

    def F11(fullscreen_param=None):
        if platform.system() == "Windows":
            if fullscreen_param is not None:
                settings["Fullscreen"] = fullscreen_param
                if settings["Fullscreen"]:
                    pygame.display.set_mode((Width, Height), DOUBLEBUF | HWSURFACE | SCALED)
                else:
                    pygame.display.set_mode((Width, Height), DOUBLEBUF | HWSURFACE | SCALED)
            else:
                settings["Fullscreen"] = not settings["Fullscreen"]
                pygame.display.toggle_fullscreen()
            dump_json(["scripts", "data", "settings.json"], settings)

    def debug(player=None, enemies=[], rect_list=[], scroll=[0, 0]):
        fps = str(int(clock.get_fps()))

        if player:
            pos = f"{int(player.x)}X, {int(player.y)}Y"
            pos = pos.strip("'")
        else:
            pos = "Nonexistent"

        fps_text.content = f"FPS: {fps}"
        pos_text.content = f"Pos: {pos}"
        room_text.content = f"Room: {Player.location}"

        def show_fps():
            win.blit(fps_surf, (10, Height-fps_text.height-75))
            fps_text.render(win, (13, Height-fps_text.height-70))
        
        def player_pos():
            win.blit(pos_surf, (10, Height-pos_text.height-45))
            pos_text.render(win, (13, Height-pos_text.height-40))
        
        def room_name():
            win.blit(room_surf, (10, Height-room_text.height-15))
            room_text.render(win, (13, Height-room_text.height-10))
        
        def show_hitbox():
            def draw(_list):
                for rect in _list:
                    if type(rect) == pygame.Rect:
                        pygame.draw.rect(win, (0, 255, 0), (rect.x-scroll[0], rect.y-scroll[1], rect.width, rect.height), 1)
                    elif type(rect) == Polygon:
                        rect.draw_poly(win, (0, 255, 0), scroll)
                    elif type(rect) == OBB:
                        rect.draw_obb(win, (0, 255, 0), scroll)
                    elif type(rect) == list:
                        draw(rect)
                    else:
                        pygame.draw.rect(win, (0, 255, 0), (rect.rect.x-scroll[0], rect.rect.y-scroll[1], rect.rect.width, rect.rect.height), 1)
            if player:
                pygame.draw.rect(win, (0, 255, 0), (player.rect.x-scroll[0], player.rect.y-scroll[1], player.rect.width, player.rect.height), 1)
                pygame.draw.rect(win, (255, 0, 0), (player.tile_rect.x-scroll[0], player.tile_rect.y-scroll[1], player.tile_rect.width, player.tile_rect.height), 1)
            for rects in rect_list:
                draw(rects)
            
        def show_middle():
            pygame.draw.line(win, (128,128,128), (0, Height*0.5), (Width, Height*0.5))
            pygame.draw.line(win, (128,128,128), (Width*0.5, 0), (Width*0.5, Height))

        def show_eview():
            for enemy in enemies:
                enemy.sus_view.draw(win, (128, 128, 0), scroll)
                enemy.view.draw(win, (128, 0, 0), scroll)

        show_fps()
        player_pos()
        room_name()
        if show_hitboxes:
            show_hitbox()
        if show_mid:
            show_middle()
        if show_view:
            show_eview()

    inventory_menu = False
    inventory_brightness = Brightness((0, 0), (Width, Height), -230)
    item_text = item_box = []

    game_brightness = Brightness((0, 0), (Width, Height), settings["Brightness"])
    brightness_slider = Brightness((0, 0), (400, 70), settings["Brightness"])

    clock = pygame.time.Clock()
    last_time = time.time() # dt

    def menus(menu="main"):
        global debug_menu, game_map, projs, player, inventory, camera
        def reset():
            buttons, sliders, textboxes, texts = [], [], [], []
            update = None
            scroll = [0, 0]
            return buttons, sliders, textboxes, texts, update, scroll

        buttons, sliders, textboxes, texts, update, scroll = reset()
        now = []
        scroll = [0, 0]

        # Special Vars
        edit_ctrl = {
            "Up": False, 
            "Down": False, 
            "Left": False, 
            "Right": False, 
            "Dash": False,
            "Inventory": False,
            "Pause Game": False
        }
        save_chosen = [False, False, False]
        music_list = [[name, music] for name, music in musics.items()]
        chosen_music = 0
        disable_presses = False
        save_num = 0
        speed = [1]


        def settings_update(event):
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 4:
                    scroll[1] -= 30
                    if scroll[1] < 0:
                        scroll[1] = 0
                if event.button == 5:
                    scroll[1] += 30
                    if scroll[1] > 1575-Height:
                        scroll[1] = 1575-Height
            
            if event.type == KEYDOWN:
                for name in edit_ctrl.keys():
                    if edit_ctrl[name] == True:
                        edit_ctrl[name] = False
                        for button in buttons:
                            if button[0].text and button[1]:
                                if name in button[1]:
                                    button[0].text_content = f"{name}: {pygame.key.name(event.key).capitalize()}"

        def credits_update(event):
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 4:
                    if speed[0] > 0:
                        speed[0] -= .5
                if event.button == 5:
                    speed[0] += .5

                
        def main():
            if not "main" in now:
                now.append("main")

            texts.append([Text(os.path.join("assets", "fontsDL", "Font.png"), "Inseynia", 72, (255, 255, 255)), ["middle", 50]])
            buttons.append([Button(Width*0.5-200, Height*0.5-35, 400, 70, text="Start Game", outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "Font.png")), "goto saves", None])
            buttons.append([Button(Width*0.5-200, Height*0.5+65, 400, 70, text="Settings", outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "Font.png")), "goto settings", None])
            buttons.append([Button(Width*0.5-200, Height*0.5+165, 400, 70, text="Quit Game", outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "Font.png")), "quit", None])

        def edit_settings():
            if not "settings" in now:
                now.append("settings")

            texts.append([Text(os.path.join("assets", "fontsDL", "Font.png"), "Graphics", 48, (255, 255, 255)), ["middle", 50]])
            buttons.append([Button(Width*0.5-200, 125, 400, 70, text=f"Fullscreen: {'On' if settings['Fullscreen'] else 'Off'}", outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "Font.png")), "toggle", None])
            sliders.append([Slider(Width*0.5-200, 225, 400, 70, None, 10, 501, [x*5+10 for x in range(100)], width_fill=((settings['FPS']-10)/500)*(400-40)+40 if settings['FPS'] < 2**32 else 400, text=f"FPS: {settings['FPS'] if settings['FPS'] < 2**32 else 'Unlimited'}", outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "Font.png")), "list"])
            sliders.append([Slider(Width*0.5-200, 325, 400, 70, None, -200, 50, width_fill=int((((settings['Brightness']+200)/2.5)/100)*(400-40)+40), text=f"Brightness:", outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "Font.png")), "percent"])
            sliders[-1][0].text_content = f"Brightness: {round((sliders[-1][0].width_fill-40)/(sliders[-1][0].width-40)*100)}"

            texts.append([Text(os.path.join("assets", "fontsDL", "Font.png"), "Volume", 48, (255, 255, 255)), ["middle", 450]])
            sliders.append([Slider(Width*0.5-200, 525, 400, 70, None, 0, 1, width_fill=settings['Volumes']['Music']*(400-40)+40, text=f"Music: {int(settings['Volumes']['Music']*100)}", outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "Font.png")), "percent"])
            sliders.append([Slider(Width*0.5-200, 625, 400, 70, None, 0, 1, width_fill=settings['Volumes']['SFX']*(400-40)+40, text=f"SFX: {int(settings['Volumes']['SFX']*100)}", outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "Font.png")), "percent"])

            texts.append([Text(os.path.join("assets", "fontsDL", "Font.png"), "Controls", 48, (255, 255, 255)), ["middle", 750]])
            buttons.append([Button(Width*0.5-225, 825, 450, 70, text=f"Up: {pygame.key.name(settings['Keys']['Up']).capitalize()}", outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "Font.png"), change_width=False), "ctrl Up", None])
            buttons.append([Button(Width*0.5-225, 925, 450, 70, text=f"Down: {pygame.key.name(settings['Keys']['Down']).capitalize()}", outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "Font.png"), change_width=False), "ctrl Down", None])
            buttons.append([Button(Width*0.5-225, 1025, 450, 70, text=f"Left: {pygame.key.name(settings['Keys']['Left']).capitalize()}", outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "Font.png"), change_width=False), "ctrl Left", None])
            buttons.append([Button(Width*0.5-225, 1125, 450, 70, text=f"Right: {pygame.key.name(settings['Keys']['Right']).capitalize()}", outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "Font.png"), change_width=False), "ctrl Right", None])
            buttons.append([Button(Width*0.5-225, 1225, 450, 70, text=f"Dash: {pygame.key.name(settings['Keys']['Dash']).capitalize()}", outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "Font.png"), change_width=False), "ctrl Dash", None])
            buttons.append([Button(Width*0.5-225, 1325, 450, 70, text=f"Inventory: {pygame.key.name(settings['Keys']['Inventory']).capitalize()}", outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "Font.png"), change_width=False), "ctrl Inventory", None])
            buttons.append([Button(Width*0.5-225, 1425, 450, 70, text=f"Pause Game: {pygame.key.name(settings['Keys']['Pause']).capitalize()}", outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "Font.png"), change_width=False), "ctrl Pause Game", None])

            buttons.append([Button(Width*0.5-275, Height-50, 200, 35, (0, 0, 0), "Back", outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "Font.png")), "back", None])
            buttons.append([Button(Width*0.5+75, Height-50, 200, 35, (0, 0, 0), "Apply", outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "Font.png")), "apply", None])

        def saves():
            if not "saves" in now:
                now.append("saves")

            texts.append([Text(os.path.join("assets", "fontsDL", "Font.png"), "Saves", 72, (255, 255, 255)), ["middle", 50]])
            buttons.append([Button(Width*0.5-200, Height*0.5-35, 400, 70, text="Save 1", outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "Font.png")), "save 1", None])
            if "save1.json" in os.listdir(os.path.join("scripts", "saves")):
                buttons.append([Button(Width*0.5+210, Height*0.5-35, 150, 70, (128, 0, 0), "Delete", outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "Font.png")), "del save 1", None])
                buttons[-2][0].text_content = load_json(["scripts", "saves", "save1.json"])["name"]

            buttons.append([Button(Width*0.5-200, Height*0.5+65, 400, 70, text="Save 2", outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "Font.png")), "save 2", None])
            if "save2.json" in os.listdir(os.path.join("scripts", "saves")):
                buttons.append([Button(Width*0.5+210, Height*0.5+65, 150, 70, (128, 0, 0), "Delete", outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "Font.png")), "del save 2", None])
                buttons[-2][0].text_content = load_json(["scripts", "saves", "save2.json"])["name"]

            buttons.append([Button(Width*0.5-200, Height*0.5+165, 400, 70, text="Save 3", outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "Font.png")), "save 3", None])
            if "save3.json" in os.listdir(os.path.join("scripts", "saves")):
                buttons.append([Button(Width*0.5+210, Height*0.5+165, 150, 70, (128, 0, 0), "Delete", outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "Font.png")), "del save 3", None])
                buttons[-2][0].text_content = load_json(["scripts", "saves", "save3.json"])["name"]

            buttons.append([Button(Width*0.5-100, Height-50, 200, 35, (0, 0, 0), "Back", outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "Font.png")), "back", None])

        def chosen_save():
            if not "chosen save" in now:
                now.append("chosen save")

            texts.append([Text(os.path.join("assets", "fontsDL", "Font.png"), "[savenum]", 72, (255, 255, 255)), ["middle", 50]])
            
            buttons.append([Button(Width*0.5-205, Height*0.5-35, 200, 70, text="Archer", outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "Font.png")), "class A", None])
            buttons.append([Button(Width*0.5+5, Height*0.5-35, 200, 70, text="Mage", outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "Font.png")), "class M", None])
            
            textboxes.append(Textbox(Width*0.5-200, Height*0.5+65, 400, 70, None, "Character Name", outline=(255, 255, 255), font_path=os.path.join("assets", "fontsDL", "Font.png"), change_width=False, clear_text_when_click=True, alnum=True))
            
            sliders.append([Slider(Width*0.5-250, Height*0.5+165, 500, 70, None, "Easy", "Permadeath" if settings["Permadeath"] else "Hard", ["Easy", "Normal", "Hard"], True, 40, (128, 64, 0), "Difficulty: Easy", outline=(255, 255, 255), font_path=os.path.join("assets", "fontsDL", "Font.png")), "list"])
            if settings["Permadeath"]: sliders[-1][0].list.append("Permadeath")
            
            buttons.append([Button(Width*0.5-275, Height-50, 200, 35, (0, 0, 0), "Back", outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "Font.png")), "back", None])
            buttons.append([Button(Width*0.5+75, Height-50, 200, 35, (0, 0, 0), "Start", outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "Font.png")), "apply", None])

        def pause():
            if not "pause" in now:
                now.append("pause")

            texts.append([Text(os.path.join("assets", "fontsDL", "Font.png"), "Paused", 48, (255, 255, 255)), ["middle", Height*0.5-70]])
            buttons.append([Button(Width*0.5-107.5, Height*0.5, 50, 50), "goto settings", sprites["SettingsNOver"]])
            buttons.append([Button(Width*0.5-37.5, Height*0.5-12.5, 75, 75), "return", sprites["ResumeNOver"]])
            buttons.append([Button(Width*0.5+57.5, Height*0.5, 50, 50), "goto main", sprites["ReturnNOver"]])
            
        def music_room():
            if not "music room" in now:
                now.append("music room")

            surf = pygame.Surface((60, 60), SRCALPHA)
            pygame.draw.polygon(surf, (255, 255, 255), ((0, 0), (60, 30), (0, 60)))
            texts.append([Text(os.path.join("assets", "fontsDL", "Font.png"), "Music Room", 72, (255, 255, 255)), ["middle", 50]])
            buttons.append([Button(Width*0.5-200, Height*0.5-35, 400, 70, text=music_list[0][0], outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "Font.png")), None, None])
            buttons[-1][0].x = Width*0.5-buttons[-1][0].width*0.5
            buttons.append([Button(buttons[0][0].x+buttons[0][0].width+10, Height*0.5-30, 60, 60, outline=(255,255,255)), "next music", surf])
            buttons.append([Button(buttons[0][0].x-70, Height*0.5-30, 60, 60, outline=(255,255,255)), "pre music", pygame.transform.flip(surf, True, False)])
            buttons.append(([Button(Width*0.5-100, Height-50, 200, 35, (0, 0, 0), "Back", outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "Font.png")), "back", None]))
            
        def credits():
            if not "credits" in now:
                now.append("credits")

            texts.append([Text(os.path.join("assets", "fontsDL", "Font.png"), "Inseynia", 72, (255, 255, 255)), ["middle", Height]])

            texts.append([Text(os.path.join("assets", "fontsDL", "Font.png"), "Managers", 48, (89, 205, 255)), ["middle", Height+100]])
            texts.append([Text(os.path.join("assets", "fontsDL", "Font.png"), "Zeperox    Adonis", 32, (255, 255, 255)), ["middle", Height+150]])

            texts.append([Text(os.path.join("assets", "fontsDL", "Font.png"), "Lead Developer", 48, (89, 205, 255)), ["middle", Height+200]])
            texts.append([Text(os.path.join("assets", "fontsDL", "Font.png"), "Zeperox", 32, (255, 255, 255)), ["middle", Height+250]])
            
            texts.append([Text(os.path.join("assets", "fontsDL", "Font.png"), "Artists", 48, (89, 205, 255)), ["middle", Height+300]])
            texts.append([Text(os.path.join("assets", "fontsDL", "Font.png"), "Bowie    Zeperox    Chaino    gyroc1    Adonis", 32, (255, 255, 255)), ["middle", Height+350]])
            
            texts.append([Text(os.path.join("assets", "fontsDL", "Font.png"), "Composer", 48, (89, 205, 255)), ["middle", Height+400]])
            texts.append([Text(os.path.join("assets", "fontsDL", "Font.png"), "Cthethan", 32, (255, 255, 255)), ["middle", Height+450]])

            texts.append([Text(os.path.join("assets", "fontsDL", "Font.png"), "Special Thanks", 48, (89, 205, 255)), ["middle", Height+500]])
            texts.append([Text(os.path.join("assets", "fontsDL", "Font.png"), "-ACE-    Adam_    Alexey_045    Anais Snow MY    Dark_Alliance", 32, (255, 255, 255)), ["middle", Height+550]])
            texts.append([Text(os.path.join("assets", "fontsDL", "Font.png"), "CodeRxJesseJ    flakes    Invarrow    Jumboost    K13", 32, (255, 255, 255)), ["middle", Height+590]])
            texts.append([Text(os.path.join("assets", "fontsDL", "Font.png"), "MartinWho    noTme    parapotato3    slava Ukrajini!    suba", 32, (255, 255, 255)), ["middle", Height+630]])
            texts.append([Text(os.path.join("assets", "fontsDL", "Font.png"), "wermz    X_X", 32, (255, 255, 255)), ["middle", Height+670]])
            texts.append([Text(os.path.join("assets", "fontsDL", "Font.png"), "And you... for playing!", 32, (255, 255, 255)), ["middle", Height+710]])


        pause()
        pause_surf = pygame.Surface((230, 170))
        pause_surf.fill((255, 255, 255))
        pause_surf.fill((0, 0, 0), (2, 2, 226, 166))
        for button in buttons:
            pause_surf.blit(button[2], (button[0].x, button[0].y))         
        for text in texts:
            if text[1][0] == "middle":
                text[1][0] = Width*0.5-text[0].width*0.5
            text[0].render(pause_surf, text[1])

        buttons = []
        texts = []
        now = []

        pages = {
            "main": main,
            "settings": edit_settings,
            "saves": saves,
            "chosen save": chosen_save,
            "music room": music_room,
            "pause": pause,
            "credits": credits
        }

        pages[menu]()
        if menu == "settings":
            update = settings_update

        musics["main"].start()
        while 1:
            clock.tick(settings["FPS"])
            disable_presses = False

            if now[-1] == "credits":
                scroll[1] += speed[0]

                if scroll[1] >= texts[-1][1][1]+100+texts[-1][0].height:
                    if len(now) > 1: now = now[:-1]

                    buttons, sliders, textboxes, texts, update, scroll = reset()
                    pages[now[-1]]()
                    if now[-1] == "settings":
                        update = settings_update

            if now[-1] != "pause":
                win.blit(sprites["Main Menu BG"], (0, 0))
                if not musics["main"].get_busy():
                    musics["main"].start()
            else:
                win.blit(camera.display, (0, 0))
                inventory_brightness.draw(win)
                win.blit(pause_surf, (Width*0.5-115, Height*0.5-85))

            mp = pygame.mouse.get_pos()

            for text in texts:
                if text[1][0] == "middle":
                    text[1][0] = Width*0.5-text[0].width*0.5
                text[0].render(win, text[1], scroll)
            
            for slider in sliders:
                if "Brightness" not in slider[0].text_content:
                    slider[0].draw(win, scroll)
                    if slider[0].selected:
                        val = slider[0].update_value(mp)
                        if slider[1] == "percent":
                            slider[0].text_content = f"{slider[0].text_content.split(':')[0]}: {round(((slider[0].width_fill-40)/(slider[0].width-40))*100)}"
                        elif slider[1] == "int":
                            slider[0].text_content = f"{slider[0].text_content.split(':')[0]}: {round(val)}"
                        else:
                            slider[0].text_content = f"{slider[0].text_content.split(':')[0]}: {val}"
                            if now[-1] == "chosen save":
                                c = (0, 128, 0) if val == "Easy" else (128, 64, 0) if val == "Normal" else (128, 0, 0) if val == "Hard" else (64, 0, 0)
                                slider[0].color_fill = c
                        if "FPS" in slider[0].text_content and slider[0].text_content.split(': ')[1] == "501":
                            slider[0].text_content = "FPS: Unlimited"
            
            for textbox in textboxes:
                textbox.draw(win, scroll)

            for button in buttons:
                if not button[2]:
                    if button[1] in ["back", "apply"]:
                        button[0].draw(win)
                    else:
                        button[0].draw(win, scroll)
                else:
                    win.blit(button[2], (button[0].x-scroll[0], button[0].y-scroll[1]))
            game_brightness.draw(win)

            if now[-1] == "settings" and "Brightness" in sliders[1][0].text_content:
                slider = sliders[1]
                slider[0].draw(win, scroll)

                if slider[0].selected:
                    val = slider[0].update_value(mp)
                    slider[0].text_content = f"{slider[0].text_content.split(':')[0]}: {round(((slider[0].width_fill-40)/(slider[0].width-40))*100)}"

                brightness_slider.loc = (slider[0].x-scroll[0], slider[0].y-scroll[1])
                brightness_slider.brightness = 2.5*int(slider[0].text_content.split(": ")[1])-200
                brightness_slider.draw(win)

            if debug_menu:
                debug()


            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit(); sys.exit()
                
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for button in buttons:
                            if button[0].is_over(mp):
                                if button[1]:
                                    if button[1] == "back":
                                        if now[-1] == "music room":
                                            musics["main"].start()

                                        if len(now) > 1: now = now[:-1]

                                        buttons, sliders, textboxes, texts, update, scroll = reset()
                                        pages[now[-1]]()
                                        if now[-1] == "settings":
                                            update = settings_update

                                    elif button[1] == "apply":
                                        if now[-1] == "settings":
                                            F11(True if "On" in buttons[0][0].text_content else False)
                                            for button in buttons[-8:-2]:
                                                if button[0].text_content != "- Changing -":
                                                    settings["Keys"][button[1].split(" ")[1]] = pygame.key.key_code(button[0].text_content.split(": ")[1].lower())
                                            settings["FPS"] = 2**32 if "Unlimited" in sliders[0][0].text_content else int(sliders[0][0].text_content.split(": ")[1])
                                            settings["Brightness"] = 2.5*int(sliders[1][0].text_content.split(": ")[1])-200
                                            settings["Volumes"]["Music"] = int(sliders[2][0].text_content.split(": ")[1])/100
                                            settings["Volumes"]["SFX"] = int(sliders[3][0].text_content.split(": ")[1])/100
                                            dump_json(["scripts", "data", "settings.json"], settings)
                                            
                                            game_brightness.brightness = settings["Brightness"]
                                            for music in musics.values():
                                                music.set_volume(settings["Volumes"]["Music"], True)
                                            disable_presses = True
                                        elif now[-1] == "chosen save":
                                            chosen_class = None
                                            for i, button in enumerate(buttons[:2]):
                                                if button[0].outline == (232, 232, 106):
                                                    chosen_class = "Archer" if i == 0 else "Mage"
                                            if not chosen_class:
                                                chosen_class = random.choice(["Archer", "Mage"])

                                            if textboxes[0].text.content == "" or (textboxes[0].text.content == "Character Name" and not textboxes[0].clicked):
                                                name = random.choice(["Akesta", "Barjuki", "John Cena", "Elat", "Inora"])
                                            else:
                                                name = textboxes[0].text.content

                                            Player.classes = [chosen_class, None]
                                            Player.name = name
                                            Player.inventory = []
                                            Player.equipment = ["No Primary", "No Shield", "No Armor"]
                                            Player.stats = {
                                                "HP": [10, 10],
                                                "SP": [10, 10],
                                                "AP": [0, None],
                                                "DP": 0,
                                                "EP": [[10, 10], [None, None]],
                                                "M": 100,
                                                "XP": [0, 3, 1]
                                            }
                                            Player.location = "DevRoom"

                                            game_map = TileMap(os.path.join("scripts", "cache", "maps", "DevRoom", "devroom.csv"), "DevRoom", (Width, Height))
                                            projs = []
                                            player = Player(game_map.start_x, game_map.start_y)
                                            inventory = Inventory(player)

                                            save = {
                                                "classes": Player.classes,
                                                "name": Player.name,
                                                "difficulty": sliders[0][0].text_content.split(" ")[-1],
                                                "inventory": Player.inventory,
                                                "equipment": Player.equipment,
                                                "stats": Player.stats,
                                                "location": Player.location
                                            }
                                            dump_json(["scripts", "saves", f"save{save_num}.json"], save)
                                            return game_map, projs, player, inventory

                            if button[0].is_over((mp[0]+scroll[0], mp[1]+scroll[1])):
                                if not disable_presses:
                                    if button[1]:
                                        if button[1] == "quit":
                                            pygame.quit(); sys.exit()
                                        
                                        elif "goto" in button[1]:
                                            buttons, sliders, textboxes, texts, update, scroll = reset()
                                            pages[button[1].split(" ")[1]]()
                                            if button[1].split(" ")[1] == "settings":
                                                update = settings_update
                                        
                                        elif button[1] == "return":
                                            return game_map, projs, player, inventory

                                        elif button[1] == "toggle":
                                            button[0].text_content = f"{button[0].text_content.split(':')[0]}: On" if "Off" in button[0].text_content else f"{button[0].text_content.split(':')[0]}: Off"
                                        
                                        elif "ctrl" in button[1]:
                                            for name in edit_ctrl.keys():
                                                if edit_ctrl[name]:
                                                    edit_ctrl[name] = False
                                                    for _button in buttons:
                                                        if _button[0].text and _button[1]:
                                                            if name in _button[1]:
                                                                _button[0].text_content = f"{name}: {pygame.key.name(settings['Keys'][name.split(' ')[0]]).capitalize()}"
                                            
                                            edit_ctrl[" ".join(button[1].split(" ")[1:])] = True
                                            button[0].text_content = "- Changing -"
                                        
                                        elif button[1].startswith("save"):
                                            save_num = button[1].split(" ")[1]
                                            if f"save{save_num}.json" not in os.listdir(os.path.join("scripts", "saves")):
                                                save_chosen = [False, False, False]
                                                save_chosen[int(save_num)-1] = True

                                                buttons, sliders, textboxes, texts, update, scroll = reset()
                                                chosen_save()
                                                texts[0][0].content = f"Save {save_num}"
                                            else:
                                                save = load_json(["scripts", "saves", f"save{save_num}.json"])
                                                Player.classes = save["classes"]
                                                Player.name = save["name"]
                                                Player.inventory = save["inventory"]
                                                Player.equipment = save["equipment"]
                                                Player.stats = save["stats"]
                                                Player.location = save["location"]

                                                game_map = TileMap(os.path.join("scripts", "cache", "maps", "DevRoom", "devroom.csv"), "DevRoom", (Width, Height))
                                                projs = []
                                                player = Player(game_map.start_x, game_map.start_y)
                                                inventory = Inventory(player)

                                                return game_map, projs, player, inventory
                                        
                                        elif button[1].startswith("del save"):
                                            del_save_num = button[1].split(" ")[2]
                                            if os.path.exists(os.path.join("scripts", "saves", f"save{del_save_num}.json")):
                                                os.remove(os.path.join("scripts", "saves", f"save{del_save_num}.json"))
                                                save_button = buttons[buttons.index(button)-1]
                                                save_button[0].text_content = f"Save {del_save_num}"
                                                buttons.remove(button)

                                        elif button[1].startswith("class"):
                                            for _button in buttons[:-2]:
                                                _button[0].outline = (255, 255, 255)
                                            button[0].outline = (232, 232, 106)

                                        elif button[1] == "next music":
                                            if chosen_music < len(music_list)-1:
                                                chosen_music += 1
                                            else:
                                                chosen_music = 0
                                            buttons[0][0].text_content = music_list[chosen_music][0]
                                            music_list[chosen_music][1].start()

                                            buttons[0][0].x = Width*0.5-buttons[0][0].width*0.5
                                            buttons[1][0].x = buttons[0][0].x+buttons[0][0].width+10
                                            buttons[2][0].x = buttons[0][0].x-70
                                        
                                        elif button[1] == "pre music":
                                            if chosen_music > 0:
                                                chosen_music -= 1
                                            else:
                                                chosen_music = len(music_list)-1
                                            buttons[0][0].text_content = music_list[chosen_music][0]
                                            music_list[chosen_music][1].start()

                                            buttons[0][0].x = Width*0.5-buttons[0][0].width*0.5
                                            buttons[1][0].x = buttons[0][0].x+buttons[0][0].width+10
                                            buttons[2][0].x = buttons[0][0].x-70

                        for slider in sliders:
                            if not disable_presses:
                                slider[0].is_over((mp[0]+scroll[0], mp[1]+scroll[1]))

                        for textbox in textboxes:
                            textbox.is_over((mp[0]+scroll[0], mp[1]+scroll[1]))

                if event.type == MOUSEBUTTONUP:
                    for slider in sliders:
                        slider[0].selected = False

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        if "main" in now:
                            now = []
                            buttons, sliders, textboxes, texts, update, scroll = reset()
                            main()
                        elif "pause" in now and now[-1] != "pause":
                            now = []
                            buttons, sliders, textboxes, texts, update, scroll = reset()
                            pause()
                        elif now[-1] == "pause":
                            return game_map, projs, player, inventory
                    
                    if event.key == K_F11:
                        F11()
                        if "Fullscreen" in buttons[0][0].text_content:
                            buttons[0][0].text_content = f"{buttons[0][0].text_content.split(':')[0]}: {'On' if settings['Fullscreen'] else 'Off'}"

                    if event.key == K_F3:
                        debug_menu = not debug_menu

                    if event.key == K_F1 and now[-1] != "music room":
                        musics["main"].start()
                        buttons, sliders, textboxes, texts, update, scroll = reset()
                        pages["music room"]()

                    if event.key == K_c and now[-1] != "credits":
                        buttons, sliders, textboxes, texts, update, scroll = reset()
                        speed[0] = 1
                        pages["credits"]()
                        update = credits_update

                    if event.key == K_RIGHT and now[-1] == "music room":
                        if chosen_music < len(music_list)-1:
                            chosen_music += 1
                        else:
                            chosen_music = 0
                        buttons[0][0].text_content = music_list[chosen_music][0]
                        music_list[chosen_music][1].start()

                        buttons[0][0].x = Width*0.5-buttons[0][0].width*0.5
                        buttons[1][0].x = buttons[0][0].x+buttons[0][0].width+10
                        buttons[2][0].x = buttons[0][0].x-70

                    if event.key == K_LEFT and now[-1] == "music room":
                        if chosen_music > 0:
                            chosen_music -= 1
                        else:
                            chosen_music = len(music_list)-1
                        buttons[0][0].text_content = music_list[chosen_music][0]
                        music_list[chosen_music][1].start()

                        buttons[0][0].x = Width*0.5-buttons[0][0].width*0.5
                        buttons[1][0].x = buttons[0][0].x+buttons[0][0].width+10
                        buttons[2][0].x = buttons[0][0].x-70

                for textbox in textboxes:
                    textbox.update_text(event)

                if update is not None:
                    update(event)

            pygame.display.flip()


    equipment = load_json(["scripts", "cache", "equipment.json"])
    items = load_json(["scripts", "cache", "items.json"])

    tooltips = {
        item: [
            t1 := Text(os.path.join("assets", "fontsDL", "Font.png"), item, 25, (62, 41, 20) if item in weapons.keys() and weapons.get(item).player_class == "Archer" else (0, 58, 144) if item in weapons.keys() and weapons.get(item).player_class == "Mage" else (255, 255, 255)),
            t2 := Text(os.path.join("assets", "fontsDL", "Font.png"), items[item]["tooltip"], 20, (255, 255, 255)),
            pygame.Surface((sorted([t1.width, t2.width], reverse=True)[0]+10, t1.height+t2.height+15))
        ] for item in items.keys()
    }
    for item, tooltip_data in tooltips.items():
        tooltip_data[2].fill((255, 255, 255))
        tooltip_data[2].fill((0, 0, 0), (2, 2, tooltip_data[2].get_width()-4, tooltip_data[2].get_height()-4))
        tooltip_data[0].render(tooltip_data[2], (tooltip_data[2].get_width()*0.5-tooltip_data[0].width*0.5, 5))
        tooltip_data[1].render(tooltip_data[2], (5, tooltip_data[0].height+10))
        tooltips[item] = tooltip_data[2]

    camera = Camera([0, 0], None)
    game_map, projs, player, inventory = menus()
    camera.target = player

    while 1:
        clock.tick(settings["FPS"])
        mpos = pygame.mouse.get_pos()
        dt, last_time = FPS_ind(last_time)
        
        # drawing
        game_map.draw_map(camera.display, player, projs, dt, scroll)
        
        player.UI(camera.display, False)
        
        if inventory_menu:
            inventory_brightness.draw(camera.display)
            player.UI(camera.display, True)


            pygame.draw.line(camera.display, (255, 255, 255), (Width*0.5, 0), (Width*0.5, Height), 5)

            inventory.draw(camera.display, [Width, Height])
            for rect in inventory.rects[0] + inventory.rects[1]:
                if rect[0].collidepoint(mpos):
                    if len(item_box) == 0:
                        item_box.append(tooltips[rect[1]])
                        item_box.append([mpos[0]+15 if mpos[0]+15+item_box[0].get_width() < Width else mpos[0]-item_box[0].get_width()-15, mpos[1]-15])
        
                    camera.display.blit(item_box[0], (item_box[1][0], item_box[1][1]))
                else:
                    item_box = []

        # action
        if not inventory_menu:
            player.move(game_map.tile_rects, dt, settings["Keys"], (mpos[0]+scroll[0], mpos[1]+scroll[1]))
            player.attack(game_map.enemies, mpos, scroll, projs)
            scroll = camera.update(game_map, (Width, Height), dt)
            
            for enemy in game_map.enemies:
                enemy.ai(game_map.tile_rects, player, projs, dt)

            for drop in game_map.drops:
                if drop[0] == "spirit" and "Mage" in player.classes and player.stats["EP"][player.classes.index("Mage")][0] < player.stats["EP"][player.classes.index("Mage")][1]:
                    svec = pygame.Vector2(drop[1].rect.center)
                    pvec = pygame.Vector2(player.rect.center)
                    drop[1].speed += 0.1*dt
                    
                    vel = (pvec-svec).normalize()*drop[1].speed

                    drop[1].x += vel.x; drop[1].y += vel.y
                    drop[1].rect = pygame.Rect(drop[1].x-20, drop[1].y-20, drop[1].img.get_width()+40, drop[1].img.get_height()+40)

                if drop[1].rect.colliderect(player.rect) and time.time()-drop[2] >= 3:
                    if inventory.pick_item(drop[0]) and drop in game_map.drops:
                        game_map.drops.remove(drop)

            for proj in projs:
                projs = proj.move(game_map, dt, scroll, mpos, game_map.enemies+[player], projs)
                x, e, projs = proj.damage(game_map.enemies+[player], projs, (mpos[0]+scroll[0], mpos[1]+scroll[1]))
                if e:
                    if x <= 0:
                        if e == player:
                            game_map, projs, player, inventory = menus()
                            camera.target = player
                        else:
                            if e in game_map.enemies:
                                game_map.enemies.remove(e)
                                if "Mage" in player.classes:
                                    game_map.drops.append(["spirit", Drop(e.rect.centerx-6, e.rect.centery-8, sprites["Spirit"]), 0])

                projs = proj.despawn(game_map, projs)

        win.blit(camera.display, (0, 0))
        if debug_menu:
            debug(player, game_map.enemies, [game_map.tile_rects], scroll)
        

        # event
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit(); sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_F11:
                    F11()
                
                if event.key == K_F3:
                    debug_menu = not debug_menu
                if event.key == K_b and debug_menu:
                    show_hitboxes = not show_hitboxes
                if event.key == K_v and debug_menu:
                    show_mid = not show_mid
                if event.key == K_j and debug_menu:
                    show_view = not show_view

                if event.key == settings["Keys"]["Inventory"]:
                    inventory_menu = not inventory_menu
                    for enemy in game_map.enemies:
                        enemy.animate = False
                    player.animate = False
                
                if event.key == settings["Keys"]["Pause"]:
                    game_map, projs, player, inventory = menus("pause")
                    camera.target = player

                # Testing Only
                if event.key == K_x:
                    enemies_data = load_json(["scripts", "cache", "enemies.json"])
                    game_map.enemies.append(AI(player.x+100, player.y, [os.path.join("assets", "ANIMATIONSDL", "Ekreta Tree", animation) for animation in enemies_data["Ekreta Tree"]["animations"]], 4, enemies_data["Ekreta Tree"]))

            if event.type == MOUSEBUTTONDOWN and inventory_menu:
                for i, rect_group in enumerate(inventory.rects):
                    for rect in rect_group:
                        if rect[0].collidepoint(mpos):
                            if i == 0:
                                if event.button == 1:
                                    inventory.equip_item(rect[1], player)
                                elif event.button == 3:
                                    game_map.drops.append(inventory.throw_inv_item(rect[1], player))
                            else:
                                if event.button == 1:
                                    inventory.unequip_item(rect[1], player)
                                elif event.button == 3:
                                    game_map.drops.append(inventory.throw_eq_item(rect[1], player))

            if event.type == MOUSEBUTTONUP:
                if player.equipment[1] in equipment[1].keys() and event.button == 3:
                    player.shielded = [None, 0]


        pygame.display.flip()
        last_call = time.time()

except Exception as error:
    import traceback, ctypes, os, random
    from datetime import datetime

    trace = traceback.format_exception(type(error), error, error.__traceback__)

    hour = datetime.now().strftime("%H")
    if int(hour) > 12:
        hour = int(hour)-12
        am_pm = "PM"
    else:
        am_pm = "AM"

    try:
        with open(os.path.join("scripts", "logs.txt"), "r") as f:
            crash_logs = f.read()
    except FileNotFoundError:
        crash_logs = ""

    crash_logs += f"[{datetime.now().strftime(f'%d/%m/%Y | {hour}:%M:%S {am_pm}')}]\n{''.join(trace)}\n"
    print("".join(trace))

    error_title = "Error" if random.randint(0, 100) > 0 else "R.I.P Inseynia, you're such a broken game"
    ctypes.windll.user32.MessageBoxW(0, f"{error}\nCheck \"scripts\\logs.txt\" for the complete error and report it, thank you :)", error_title, 0)

    with open(os.path.join("scripts", "logs.txt"), "w", errors="ignore", encoding="utf-8") as f:
        f.write(crash_logs)
