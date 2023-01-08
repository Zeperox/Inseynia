try:
	# python -m cProfile -m main.py >> output.txt
	#controller mapping: {'a': 'b0', 'b': 'b1', 'x': 'b2', 'y': 'b3', 'back': 'b6', 'guide': 'b10', 'start': 'b7', 'leftstick': 'b8', 'rightstick': 'b9', 'leftshoulder': 'b4', 'rightshoulder': 'b5', 'dpup': 'h0.1', 'dpdown': 'h0.4', 'dpleft': 'h0.8', 'dpright': 'h0.2', 'leftx': 'a0', 'lefty': 'a1', 'rightx': 'a2', 'righty': 'a3', 'lefttrigger': 'a4', 'righttrigger': 'a5'}

	# Import modules
	import pygame, sys, os, random, time, platform, warnings, math, importlib

	from pygame.locals import *
	from pygame._sdl2 import controller as sdl2_controller
	from pypresence import Presence

	# Create the cache folder in case it's missing
	if "cache" not in os.listdir("scripts"):
		os.mkdir(os.path.join("scripts", "cache"))

	# Import Scripts
	from scripts.visuals.window import win, settings, Width, Height

	from scripts.loading.json_functions import load_json, dump_json
	from scripts.loading.music_player import musics
	from scripts.loading.SFX import SFX_list
	from scripts.loading.sprites import sprites

	from scripts.logic.drops import Drop, Spirit, ProjDrop
	from scripts.logic.inventory import Inventory
	from scripts.logic.player import Player, weapons
	from scripts.logic.npc import NPC

	from scripts.maps.tiles import TileMap, enemy_list

	from scripts.visuals.brightness import Brightness
	from scripts.visuals.button import Button
	from scripts.visuals.camera import Camera
	from scripts.visuals.text import Text
	from scripts.visuals.textbox import Textbox
	from scripts.visuals.slider import Slider

	from scripts.custom_collisions.obb import OBB
	from scripts.custom_collisions.polygon import Polygon
	from scripts.custom_collisions.angle import AngleRect

	from scripts.AI.ekretatree import AI
	
	# pygame inits
	pygame.mixer.pre_init(44100, -16, 128, 512)
	pygame.init()
	sdl2_controller.init()
	try:
		controller = sdl2_controller.Controller(0)
	except:
		sdl2_controller.quit()

	texts_json = load_json(["scripts", "data", "text.json"])

	# Vars
	class FakeController:
		def __init__(self):
			pass

		def get_button(self, _):
			return 0

		def get_axis(self, _):
			return 0

	mod_loops = []
	for mod in os.scandir(os.path.join("mods")):
		if mod.is_dir():
			try:
				file = os.path.join("mods", mod.name, "main.py")
				mod = importlib.import_module(f'mods.{mod.name}.main')
				mod_loops.append(mod.update)
			except:
				continue

	for music in musics.values():
		music.set_volume(settings["volumes"]["music"], True)

	#debug menu
	debug_menu = False
	show_hitboxes = False
	show_mid = False
	show_view = False

	fps_text = Text(os.path.join("assets", "fontsDL", "font.png"), "0", 1, (255,255,255))
	pos_text = Text(os.path.join("assets", "fontsDL", "font.png"), "0", 1, (255,255,255))
	room_text = Text(os.path.join("assets", "fontsDL", "font.png"), "0", 1, (255,255,255))
	projnum_text = Text(os.path.join("assets", "fontsDL", "font.png"), "0", 1, (255,255,255))
	fps_update = 0

	fps_surf = pygame.Surface((fps_text.width*9+6, fps_text.height+6))
	fps_surf.fill((100,100,100))
	fps_surf.set_alpha(200)
	pos_surf = pygame.Surface((pos_text.width*17+6, pos_text.height+6))
	pos_surf.fill((100,100,100))
	pos_surf.set_alpha(200)
	room_surf = pygame.Surface((room_text.width*17+6, room_text.height+6))
	room_surf.fill((100,100,100))
	room_surf.set_alpha(200)
	projnum_surf = pygame.Surface((projnum_text.width*9+6, projnum_text.height+6))
	projnum_surf.fill((100,100,100))
	projnum_surf.set_alpha(200)
	projs = []

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
		if Player.map:
			rpc.update(
				state=f"Region: {Player.map}",
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


	def FPS_ind():
		return (time.time() - last_time) * 60, time.time()

	def F11(fullscreen_param=None):
		if platform.system() == "Windows":
			if fullscreen_param is not None:
				if settings["fullscreen"] != fullscreen_param:
					pygame.display.toggle_fullscreen()
					settings["fullscreen"] = fullscreen_param
			else:
				settings["fullscreen"] = not settings["fullscreen"]
				pygame.display.toggle_fullscreen()
			dump_json(["scripts", "data", "settings.json"], settings)

	def debug(display=win, player=None, enemies=[], rect_list=[]):
		global fps_update
		fps = str(int(clock.get_fps()))

		if player:
			pos = f"{int(player.x)}X, {int(player.y)}Y"
			pos = pos.strip("'")
		else:
			pos = "Nonexistent"

		if time.time()-fps_update >= 1:
			fps_text.content = f"FPS: {fps}"
			fps_update = time.time()
		pos_text.content = f"Pos: {pos}"
		room_text.content = f"Room: {Player.map}"
		projnum_text.content = f"Projs: {len(projs)}"

		def show_fps():
			display.blit(fps_surf, (5, Height-fps_surf.get_height()-pos_surf.get_height()-room_surf.get_height()-projnum_surf.get_height()-5))
			fps_text.render(display, (6.5, Height-fps_surf.get_height()-pos_surf.get_height()-room_surf.get_height()-projnum_surf.get_height()))
		
		def player_pos():
			display.blit(pos_surf, (5, Height-pos_surf.get_height()-room_surf.get_height()-projnum_surf.get_height()-5))
			pos_text.render(display, (6.5, Height-pos_surf.get_height()-room_surf.get_height()-projnum_surf.get_height()))
		
		def room_name():
			display.blit(room_surf, (5, Height-room_surf.get_height()-projnum_surf.get_height()-5))
			room_text.render(display, (6.5, Height-room_surf.get_height()-projnum_surf.get_height()))
		
		def show_projnum():
			display.blit(projnum_surf, (5, Height-projnum_surf.get_height()-5))
			projnum_text.render(display, (6.5, Height-projnum_surf.get_height()))

		def show_hitbox():
			def draw(_list):
				for rect in _list:
					if rect == None:
						continue
					elif type(rect) == pygame.Rect:
						pygame.draw.rect(display, (0, 255, 0), (rect.x-camera.scroll.x, rect.y-camera.scroll.y, rect.width, rect.height), 1)
					elif type(rect) == Polygon:
						rect.draw_poly(display, (0, 255, 0), camera.scroll)
					elif type(rect) == OBB:
						rect.draw_obb(display, (0, 255, 0), camera.scroll)
					elif type(rect) == list:
						draw(rect)
					elif type(rect) == AngleRect:
						pygame.draw.rect(display, (0, 255, 0), (rect.rect.x-camera.scroll.x, rect.rect.y-camera.scroll.y, rect.rect.width, rect.rect.height), 1)
			if player:
				pygame.draw.rect(display, (0, 255, 0), (player.rect.x-camera.scroll.x, player.rect.y-camera.scroll.y, player.rect.width, player.rect.height), 1)
			for rects in rect_list:
				draw(rects)
			
		def show_middle():
			pygame.draw.line(display, (128,128,128), (0, Height*0.5), (Width, Height*0.5))
			pygame.draw.line(display, (128,128,128), (Width*0.5, 0), (Width*0.5, Height))

		def show_eview():
			for enemy in enemies:
				enemy.sus_view.draw(display, (128, 128, 0), camera.scroll)
				enemy.view.draw(display, (128, 0, 0), camera.scroll)

		show_fps()
		player_pos()
		room_name()
		show_projnum()
		if show_hitboxes:
			show_hitbox()
		if show_mid:
			show_middle()
		if show_view:
			show_eview()

	def get_text(text_ID):
		try:
			i = langs.index(settings["lang"])
			text = texts_json[text_ID][i]
		except:
			text = texts_json[text_ID][0]
		
		return text

	inventory_menu = False
	inventory_brightness = Brightness((0, 0), (Width, Height), -230)
	item_text = item_box = []

	game_brightness = Brightness((0, 0), (Width, Height), settings["brightness"])
	brightness_slider = Brightness((0, 0), (200, 35), settings["brightness"])

	clock = pygame.time.Clock()
	last_time = time.time() # dt

	near_death_surf = pygame.Surface((Width, Height), SRCALPHA)
	for c in range(96):
		surf = pygame.Surface((Width-c*2, Height-c*2))
		surf.set_colorkey((0, 0, 0))
		pygame.draw.rect(surf, (96-c, 0, 0), (0, 0, surf.get_width(), surf.get_height()), 1)
		surf.set_alpha(96-c)
		near_death_surf.blit(surf, (c, c))
	near_death_surf.set_alpha(0)
	
	save_num = 0
	difficulty = "Normal"

	controller = FakeController()

	def menus(menu="main"):
		global debug_menu, game_map, projs, player, inventory, camera, save_num, difficulty, controller, last_time, music
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
		speed = 0.5
		set_lang = settings["lang"]


		def settings_update(event):
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 4:
					scroll[1] -= 30
					if scroll[1] < 0:
						scroll[1] = 0
				if event.button == 5:
					scroll[1] += 30
					if scroll[1] > buttons[-3][0].y+buttons[-3][0].height+45-Height:
						scroll[1] = buttons[-3][0].y+buttons[-3][0].height+45-Height
			
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
					if speed > 0:
						speed -= .25
				if event.button == 5:
					speed += .25


		def main():
			if not "main" in now:
				now.append("main")

			texts.append([Text(os.path.join("assets", "fontsDL", "font.png"), get_text("text:inseynia"), 5, (255, 255, 255), settings["lang"]), ["middle", 25]]),
			buttons.append([Button(Width*0.5-100, Height*0.5-17.5, 200, 35, text=get_text("button:start_game"), text_lang=settings["lang"], outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "font.png")), "goto saves", None, False])
			buttons.append([Button(Width*0.5-100, Height*0.5+32.5, 200, 35, text=get_text("button:settings"), text_lang=settings["lang"], outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "font.png")), "goto settings", None, False])
			buttons.append([Button(Width*0.5-100, Height*0.5+82.5, 200, 35, text=get_text("button:quit_game"), text_lang=settings["lang"], outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "font.png")), "quit", None, False])
			texts.append([Text(os.path.join("assets", "fontsDL", "font.png"), "Pre-Alpha 0", 2, (75, 75, 75), "english"), ["middle", 315]])
			texts.append([Text(os.path.join("assets", "fontsDL", "font.png"), "© Texaract", 2, (75, 75, 75), "english"), ["middle", 335]])

		def edit_settings():
			if not "settings" in now:
				now.append("settings")

			texts.append([Text(os.path.join("assets", "fontsDL", "font.png"), get_text("text:graphics"), 3, (255, 255, 255), settings["lang"]), ["middle", 25]])
			buttons.append([Button(Width*0.5-100, 62.5, 200, 35, text=get_text("button:fullscreen")+get_text(f"status:{'on' if settings['fullscreen'] else 'off'}"), text_lang=settings["lang"], outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "font.png")), "toggle", None, False])
			sliders.append([Slider(Width*0.5-212.5, 112.5, 200, 35, None, 10, 501, [x*5+10 for x in range(100)], width_fill=((settings['FPS']-10)/500)*(200-20)+20 if settings['FPS'] < 2**32 else 200, text=f"{get_text('slider:fps')}{settings['FPS'] if settings['FPS'] < 2**32 else '∞'}", text_lang=settings["lang"], outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "font.png")), "list"])
			sliders.append([Slider(Width*0.5+12.5, 112.5, 200, 35, None, -200, 50, width_fill=int((((settings['brightness']+200)/2.5)/100)*(200-20)+20), text=get_text("slider:brightness"), text_lang=settings["lang"], outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "font.png")), "percent"])
			sliders[-1][0].text_content = f"{get_text('slider:brightness')}{round((sliders[-1][0].width_fill-20)/(sliders[-1][0].width-20)*100)}%"

			texts.append([Text(os.path.join("assets", "fontsDL", "font.png"), get_text("text:volume"), 3, (255, 255, 255), settings["lang"]), ["middle", 175]])
			sliders.append([Slider(Width*0.5-212.5, 212.5, 200, 35, None, 0, 1, width_fill=settings['volumes']['music']*(200-20)+20, text=f"{get_text('slider:music')}{int(settings['volumes']['music']*100)}%", text_lang=settings["lang"], outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "font.png")), "percent"])
			sliders.append([Slider(Width*0.5+12.5, 212.5, 200, 35, None, 0, 1, width_fill=settings['volumes']['SFX']*(200-20)+20, text=f"{get_text('slider:sfx')}{int(settings['volumes']['SFX']*100)}%", text_lang=settings["lang"], outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "font.png")), "percent"])

			texts.append([Text(os.path.join("assets", "fontsDL", "font.png"), get_text("text:controls"), 3, (255, 255, 255), settings["lang"]), ["middle", 275]])
			buttons.append([Button(Width*0.5-237.5, 312.5, 225, 35, text=f"Up: {pygame.key.name(settings['keys']['up']).capitalize()}", outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "font.png"), change_width=False), "ctrl up", None, False])
			buttons.append([Button(Width*0.5+12.5, 312.5, 225, 35, text=f"Down: {pygame.key.name(settings['keys']['down']).capitalize()}", outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "font.png"), change_width=False), "ctrl down", None, False])
			buttons.append([Button(Width*0.5-237.5, 362.5, 225, 35, text=f"Left: {pygame.key.name(settings['keys']['left']).capitalize()}", outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "font.png"), change_width=False), "ctrl left", None, False])
			buttons.append([Button(Width*0.5+12.5, 362.5, 225, 35, text=f"Right: {pygame.key.name(settings['keys']['right']).capitalize()}", outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "font.png"), change_width=False), "ctrl right", None, False])
			buttons.append([Button(Width*0.5-237.5, 412.5, 225, 35, text=f"Dash: {pygame.key.name(settings['keys']['dash']).capitalize()}", outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "font.png"), change_width=False), "ctrl dash", None, False])
			buttons.append([Button(Width*0.5+12.5, 412.5, 225, 35, text=f"Inventory: {pygame.key.name(settings['keys']['inventory']).capitalize()}", outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "font.png"), change_width=False), "ctrl inventory", None, False])
			buttons.append([Button(Width*0.5-237.5, 462.5, 225, 35, text=f"Sleep: {pygame.key.name(settings['keys']['sleep']).capitalize()}", outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "font.png"), change_width=False), "ctrl sleep", None, False])
			buttons.append([Button(Width*0.5+12.5, 462.5, 225, 35, text=f"Interact: {pygame.key.name(settings['keys']['interact']).capitalize()}", outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "font.png"), change_width=False), "ctrl interact", None, False])
			buttons.append([Button(Width*0.5-112.5, 512.5, 225, 35, text=f"Pause Game: {pygame.key.name(settings['keys']['pause']).capitalize()}", outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "font.png"), change_width=False), "ctrl pause game", None, False])
			buttons.append([Button(Width*0.5-112.5, 562.5, 225, 35, text=get_text("button:controller"), text_lang=settings["lang"], outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "font.png"), change_width=False), "controller", None, False])
			buttons[-1][0].text_content += get_text("status:connected") if sdl2_controller.get_init() else get_text("status:disconnected")

			texts.append([Text(os.path.join("assets", "fontsDL", "font.png"), get_text("text:languages"), 3, (255, 255, 255), settings["lang"]), ["middle", 625]])
			buttons.append([Button(Width*0.5-212.5, 662.5, 200, 35, text="English", text_lang="english", outline=(255, 255, 255), font_path=os.path.join("assets", "fontsDL", "font.png")), "lang english", None, False])
			buttons.append([Button(Width*0.5+12.5, 662.5, 200, 35, text="العربية", text_lang="arabic", outline=(255, 255, 255), font_path=os.path.join("assets", "fontsDL", "font.png")), "lang arabic", None, False])
			buttons.append([Button(Width*0.5-212.5, 712.5, 200, 35, text="にほんご", text_lang="japanese", outline=(255, 255, 255), font_path=os.path.join("assets", "fontsDL", "font.png")), "lang japanese", None, False])
			buttons.append([Button(Width*0.5+12.5, 712.5, 200, 35, text="Русский", text_lang="russian", outline=(255, 255, 255), font_path=os.path.join("assets", "fontsDL", "font.png")), "lang russian", None, False])
			buttons.append([Button(Width*0.5-212.5, 762.5, 200, 35, text="Español", text_lang="spanish", outline=(255, 255, 255), font_path=os.path.join("assets", "fontsDL", "font.png")), "lang spanish", None, False])
			buttons.append([Button(Width*0.5+12.5, 762.5, 200, 35, text="Français", text_lang="french", outline=(255, 255, 255), font_path=os.path.join("assets", "fontsDL", "font.png")), "lang french", None, False])

			buttons.append([Button(Width*0.5-137.5, Height-25, 100, 20, (0, 0, 0), get_text("button:back"), text_lang=settings["lang"], outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "font.png")), "back", None, True])
			buttons.append([Button(Width*0.5+37.5, Height-25, 100, 20, (0, 0, 0), get_text("button:apply"), text_lang=settings["lang"], outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "font.png")), "apply", None, True])

		def saves():
			if not "saves" in now:
				now.append("saves")

			texts.append([Text(os.path.join("assets", "fontsDL", "font.png"), get_text("text:saves"), 5, (255, 255, 255), settings["lang"]), ["middle", 25]])
			buttons.append([Button(Width*0.5-100, Height*0.5-17.5, 200, 35, text=f"{get_text('button:save')} 1", outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "font.png")), "save 1", None, False])
			if "save1.json" in os.listdir(os.path.join("scripts", "saves")):
				buttons.append([Button(Width*0.5+105, Height*0.5-17.5, 75, 35, (128, 0, 0), get_text("button:delete"), text_lang=settings["lang"], outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "font.png")), "del save 1", None, False])
				buttons[-2][0].text_content = load_json(["scripts", "saves", "save1.json"])["name"]
			else:
				buttons[-1][0].text_content = (buttons[-1][0].text_content, settings["lang"])

			buttons.append([Button(Width*0.5-100, Height*0.5+32.5, 200, 35, text=f"{get_text('button:save')} 2", outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "font.png")), "save 2", None, False])
			if "save2.json" in os.listdir(os.path.join("scripts", "saves")):
				buttons.append([Button(Width*0.5+105, Height*0.5+32.5, 75, 35, (128, 0, 0), get_text("button:delete"), text_lang=settings["lang"], outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "font.png")), "del save 2", None, False])
				buttons[-2][0].text_content = load_json(["scripts", "saves", "save2.json"])["name"]
			else:
				buttons[-1][0].text_content = (buttons[-1][0].text_content, settings["lang"])

			buttons.append([Button(Width*0.5-100, Height*0.5+82.5, 200, 35, text=f"{get_text('button:save')} 3", outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "font.png")), "save 3", None, False])
			if "save3.json" in os.listdir(os.path.join("scripts", "saves")):
				buttons.append([Button(Width*0.5+105, Height*0.5+82.5, 75, 35, (128, 0, 0), get_text("button:delete"), text_lang=settings["lang"], outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "font.png")), "del save 3", None, False])
				buttons[-2][0].text_content = load_json(["scripts", "saves", "save3.json"])["name"]
			else:
				buttons[-1][0].text_content = (buttons[-1][0].text_content, settings["lang"])

			buttons.append([Button(Width*0.5-50, Height-25, 100, 20, (0, 0, 0), get_text("button:back"), text_lang=settings["lang"], outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "font.png")), "back", None, True])

		def chosen_save():
			if not "chosen save" in now:
				now.append("chosen save")

			texts.append([Text(os.path.join("assets", "fontsDL", "font.png"), "[savenum]", 5, (255, 255, 255)), ["middle", 25]])
			
			buttons.append([Button(Width*0.5-102.5, Height*0.5-17.5, 100, 35, text="Archer", outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "font.png")), "class A", None, False])
			buttons.append([Button(Width*0.5+2.5, Height*0.5-17.5, 100, 35, text="Mage", outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "font.png")), "class M", None, False])
			
			textboxes.append([Textbox(Width*0.5-100, Height*0.5+32.5, 200, 35, None, "Character Name", outline=(255, 255, 255), font_path=os.path.join("assets", "fontsDL", "font.png"), change_width=False, clear_text_when_click=True, alnum=True)])

			sliders.append([Slider(Width*0.5-125, Height*0.5+82.5, 250, 35, None, "Easy", "Permadeath" if settings["permadeath"] else "Hard", ["Easy", "Normal", "Hard"], True, 40, (128, 64, 0), "Difficulty: Easy", outline=(255, 255, 255), font_path=os.path.join("assets", "fontsDL", "font.png")), "list"])
			if settings["permadeath"]: sliders[-1][0].list.append("Permadeath")
			
			buttons.append([Button(Width*0.5-137.5, Height-25, 100, 20, (0, 0, 0), get_text("button:back"), text_lang=settings["lang"], outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "font.png")), "back", None, True])
			buttons.append([Button(Width*0.5+37.5, Height-25, 100, 20, (0, 0, 0), "Start", outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "font.png")), "apply", None, True])

		def pause():
			if not "pause" in now:
				now.append("pause")

			texts.append([Text(os.path.join("assets", "fontsDL", "font.png"), get_text("text:paused"), 3, (255, 255, 255), settings["lang"]), ["middle", Height*0.5-65]])
			buttons.append([Button(Width*0.5-81, Height*0.5-25, 162, 25, text=get_text("button:resume_game"), text_lang=settings["lang"], outline=(255, 255, 255), font_path=os.path.join("assets", "fontsDL", "font.png")), "return", None, False])
			buttons.append([Button(Width*0.5-81, Height*0.5+5, 162, 25, text=get_text("button:settings"), text_lang=settings["lang"], outline=(255, 255, 255), font_path=os.path.join("assets", "fontsDL", "font.png")), "goto settings", None, False])
			buttons.append([Button(Width*0.5-81, Height*0.5+35, 162, 25, text=get_text("button:quit_game"), text_lang=settings["lang"], outline=(255, 255, 255), font_path=os.path.join("assets", "fontsDL", "font.png")), "goto main", None, False])
			
		def music_room():
			if not "music room" in now:
				now.append("music room")

			surf = pygame.Surface((30, 30), SRCALPHA)
			pygame.draw.polygon(surf, (255, 255, 255), ((0, 0), (30, 15), (0, 30)))
			texts.append([Text(os.path.join("assets", "fontsDL", "font.png"), "Music Room", 5, (255, 255, 255)), ["middle", 25]])
			buttons.append([Button(Width*0.5-100, Height*0.5-15, 200, 30, text=music_list[0][0], outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "font.png")), None, None, False])
			buttons[-1][0].x = Width*0.5-buttons[-1][0].width*0.5
			buttons.append([Button(buttons[0][0].x+buttons[0][0].width+5, Height*0.5-15, 30, 30, outline=(255,255,255)), "next music", surf, False])
			buttons.append([Button(buttons[0][0].x-35, Height*0.5-15, 30, 30, outline=(255,255,255)), "pre music", pygame.transform.flip(surf, True, False), False])
			buttons.append([Button(Width*0.5-50, Height-25, 100, 20, (0, 0, 0), "Back", outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "font.png")), "back", None, True])
			
		def gameover():
			if not "gameover" in now:
				now.append("gameover")

			texts.append([Text(os.path.join("assets", "fontsDL", "font.png"), get_text("text:gameover"), 5, (255, 255, 255), settings["lang"]), ["middle", 25]]),
			buttons.append([Button(Width*0.5-100, Height*0.5, 200, 35, text=get_text("button:continue"), text_lang=settings["lang"], outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "font.png")), "restart", None, False])
			buttons.append([Button(Width*0.5-100, Height*0.5+50, 200, 35, text=get_text("button:quit_game"), text_lang=settings["lang"], outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "font.png")), "goto main", None, False])

		def credits():
			if not "credits" in now:
				now.append("credits")

			texts.append([Text(os.path.join("assets", "fontsDL", "font.png"), "Inseynia", 5, (255, 255, 255)), ["middle", Height]])

			texts.append([Text(os.path.join("assets", "fontsDL", "font.png"), "Leads", 3, (89, 205, 255)), ["middle", Height+50]])
			texts.append([Text(os.path.join("assets", "fontsDL", "font.png"), "Zeperox    NPC", 2, (255, 255, 255)), ["middle", Height+75]])

			texts.append([Text(os.path.join("assets", "fontsDL", "font.png"), "Programmers", 3, (89, 205, 255)), ["middle", Height+110]])
			texts.append([Text(os.path.join("assets", "fontsDL", "font.png"), "Zeperox    DevHedron", 2, (255, 255, 255)), ["middle", Height+135]])
			
			texts.append([Text(os.path.join("assets", "fontsDL", "font.png"), "Artists", 3, (89, 205, 255)), ["middle", Height+170]])
			texts.append([Text(os.path.join("assets", "fontsDL", "font.png"), "Bowie    Zeperoxd    gyroc1    Nikolai", 2, (255, 255, 255)), ["middle", Height+195]])
			
			texts.append([Text(os.path.join("assets", "fontsDL", "font.png"), "Composer", 3, (89, 205, 255)), ["middle", Height+230]])
			texts.append([Text(os.path.join("assets", "fontsDL", "font.png"), "Cthethan", 2, (255, 255, 255)), ["middle", Height+255]])

			texts.append([Text(os.path.join("assets", "fontsDL", "font.png"), "Translators", 3, (89, 205, 255)), ["middle", Height+290]])
			texts.append([Text(os.path.join("assets", "fontsDL", "font.png"), "Russian Translation", 2, (89, 205, 255)), ["middle", Height+315]])
			texts.append([Text(os.path.join("assets", "fontsDL", "font.png"), "K13", 2, (255, 255, 255)), ["middle", Height+335]])

			texts.append([Text(os.path.join("assets", "fontsDL", "font.png"), "Special Thanks", 3, (89, 205, 255)), ["middle", Height+370]])
			texts.append([Text(os.path.join("assets", "fontsDL", "font.png"), "-ACE-    Adam_    Alexey_045    Anais Snow MY    Dark_Alliance", 2, (255, 255, 255)), ["middle", Height+395]])
			texts.append([Text(os.path.join("assets", "fontsDL", "font.png"), "CodeRxJesseJ    flakes    Invarrow    Jumboost", 2, (255, 255, 255)), ["middle", Height+415]])
			texts.append([Text(os.path.join("assets", "fontsDL", "font.png"), "MartinWho    noTme    parapotato3    slava Ukrajini!    suba", 2, (255, 255, 255)), ["middle", Height+435]])
			texts.append([Text(os.path.join("assets", "fontsDL", "font.png"), "wermz    X_X    smellyfrog    Hector Azurite", 2, (255, 255, 255)), ["middle", Height+455]])
			texts.append([Text(os.path.join("assets", "fontsDL", "font.png"), "And you... for playing!", 2, (255, 255, 255)), ["middle", Height+475]])


		pause()
		pause_surf = pygame.Surface((190, 150))
		pause_surf.fill((255, 255, 255))
		pause_surf.fill((0, 0, 0), (2, 2, 186, 146))
		for text in texts:
			if text[1][0] == "middle":
				text[1][0] = Width*0.5-text[0].width*0.5
			text[0].render(pause_surf, text[1])

		if menu == "pause":
			paused_timers = [
				time.time()-last_time,
				time.time()-player.inv_max_exceed_time,
				time.time()-player.dash_cooldown,
				time.time()-player.shielded[1],
				time.time()-player.i_frame
			]
			if player.weapons[0] != [None, None]:
				paused_timers.append(time.time()-player.weapons[0][1].cooldown_time)
			if player.weapons[1] != [None, None]:
				paused_timers.append(time.time()-player.weapons[1][1].cooldown_time)
			for drop in game_map.full_drops:
				paused_timers.append(time.time()-drop[2])
			for proj in projs:
				paused_timers.append(time.time()-proj.shot_time)
				paused_timers.append(time.time()-proj.ricochet)
			for enemy in game_map.full_enemies:
				paused_timers.append(time.time()-enemy.sus_time[0])
				paused_timers.append(time.time()-enemy.target_change_timer)
				paused_timers.append(time.time()-enemy.i_frame)
				paused_timers.append(time.time()-enemy.proj_cooldown)

		buttons = []
		texts = []
		now = []

		bg_num = 0

		index = 0

		pages = {
			"main": main,
			"settings": edit_settings,
			"saves": saves,
			"chosen save": chosen_save,
			"music room": music_room,
			"pause": pause,
			"gameover": gameover,
			"credits": credits
		}

		pages[menu]()
		if menu == "settings":
			update = settings_update

		if menu == "gameover":
			musics[music].end()
		elif menu == "pause":
			musics[music].toggle_pause()
		else:
			musics["main"].start()
		while 1:
			clock.tick(settings["FPS"])
			disable_presses = False

			if now[-1] == "credits":
				scroll[1] += speed
				win.fill((0, 0, 0))

				if scroll[1] >= texts[-1][1][1]+100+texts[-1][0].height:
					if len(now) > 1: now = now[:-1]

					buttons, sliders, textboxes, texts, update, scroll = reset()
					pages[now[-1]]()
					if now[-1] == "settings":
						update = settings_update

			if now[-1] not in ["pause", "credits", "gameover"]:
				win.fill((0, 0, 0))
				'''win.blit(sprites[f"mbg{bg_num}"], (0, 0)) # Should be released in Pre-Alpha 1

				elements = buttons+sliders+texts+textboxes
				surf = pygame.Surface((max([elem[0].width for elem in elements])+50, Height))
				surf.set_alpha(50)
				win.blit(surf, (Width*0.5-surf.get_width()*0.5, 0))'''
				
			elif now[-1] == "pause":
				win.blit(camera.main_display, (0, 0))
				inventory_brightness.draw(win)
				win.blit(pause_surf, (Width*0.5-95, Height*0.5-75))

			elif now[-1] == "gameover":
				win.fill((0, 0, 0))

			mp = pygame.mouse.get_pos()
			
			for text in texts:
				if text[1][0] == "middle":
					text[1][0] = Width*0.5-text[0].width*0.5
				text[0].render(win, text[1], scroll)
			
			for slider in sliders:
				slider[0].draw(win, scroll)
				if slider[0].selected:
					val = slider[0].update_value(mp)
					if slider[1] == "percent":
						slider[0].text_content = f"{slider[0].text_content.split(': ')[0]}: {round(((slider[0].width_fill-20)/(slider[0].width-20))*100)}%"
					elif slider[1] == "int":
						slider[0].text_content = f"{slider[0].text_content.split(': ')[0]}: {round(val)}"
					else:
						slider[0].text_content = f"{slider[0].text_content.split(': ')[0]}: {val}"
						if now[-1] == "chosen save":
							c = (0, 128, 0) if val == "Easy" else (128, 64, 0) if val == "Normal" else (128, 0, 0) if val == "Hard" else (64, 0, 0)
							slider[0].color_fill = c
							
					if sliders[0] == slider and slider[0].text_content.split(': ')[1] in ["505", "501"] and now[-1] == "settings":
						slider[0].text_content = f"{get_text('slider:fps')}∞"
		
			for textbox in textboxes:
				textbox[0].draw(win, scroll)

			for button in buttons:
				if not button[2]:
					if button[1] in ["back", "apply"]:
						button[0].draw(win)
					else:
						button[0].draw(win, scroll)
				else:
					win.blit(button[2], (button[0].x-scroll[0], button[0].y-scroll[1]))
			game_brightness.draw(win)

			if now[-1] == "settings":
				slider = sliders[1]
				brightness_slider.loc = (slider[0].x-scroll[0], slider[0].y-scroll[1])
				brightness_slider.brightness = 2.5*int(slider[0].text_content.split(": ")[1][:-1])-200
				brightness_slider.draw(win)

			if debug_menu:
				debug()

			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit(); sys.exit()
				
				if (event.type == MOUSEBUTTONDOWN and event.button == 1) or (event.type == KEYDOWN and event.key in [K_SPACE, K_RETURN]) or (event.type == CONTROLLERBUTTONDOWN and event.button == CONTROLLER_BUTTON_A):
					for button in buttons:
						if button[0].is_over(mp) and button[3]:
							if button[1]:
								if button[1] == "back":
									index = 0
									disable_presses = True
									if now[-1] == "music room":
										musics["main"].start()

									if len(now) > 1: now = now[:-1]

									buttons, sliders, textboxes, texts, update, scroll = reset()
									pages[now[-1]]()
									if now[-1] == "settings":
										update = settings_update

								elif button[1] == "apply":
									disable_presses = True
									if now[-1] == "settings":
										F11(True if get_text("status:on") in buttons[0][0].text_content else False)
										for button in buttons[1:8]:
											if button[0].text_content != "- Press the desired key -":
												settings["keys"][button[1].split(" ")[1].lower()] = pygame.key.key_code(button[0].text_content.split(": ")[1].lower())
										settings["FPS"] = 2**32 if "∞" in sliders[0][0].text_content else int(sliders[0][0].text_content.split(": ")[1])
										settings["brightness"] = 2.5*int(sliders[1][0].text_content.split(": ")[1][:-1])-200
										settings["volumes"]["music"] = int(sliders[2][0].text_content.split(": ")[1][:-1])/100
										settings["volumes"]["SFX"] = int(sliders[3][0].text_content.split(": ")[1][:-1])/100
										l = settings["lang"]
										settings["lang"] = set_lang
										dump_json(["scripts", "data", "settings.json"], settings)
										
										game_brightness.brightness = settings["brightness"]
										for music in musics.values():
											music.set_volume(settings["volumes"]["music"], True)

										if l != set_lang:
											s = scroll
											if len(now) > 1: now = now[:-1]
											buttons, sliders, textboxes, texts, update, scroll = reset()
											edit_settings()
											update = settings_update
											scroll = s
									elif now[-1] == "chosen save":
										chosen_class = None
										for i, button in enumerate(buttons[:2]):
											if button[0].outline == (232, 232, 106):
												chosen_class = "Archer" if i == 0 else "Mage"
										if not chosen_class:
											chosen_class = random.choice(["Archer", "Mage"])

										if textboxes[0][0].text.content == "" or (textboxes[0][0].text.content == "Character Name" and not textboxes[0][0].clicked):
											name = random.choice(["Akesta", "Barjuki", "John Cena", "Elat", "Inora"])
										else:
											name = textboxes[0][0].text.content

										Player.classes = [chosen_class, None]
										Player.name = name
										Player.inventory = []
										Player.equipment = [("No AWeapon", "No MWeapon")[chosen_class == "Mage"], "No Shield", "No Armor", "No Backpack"]
										Player.stats = {
											"HP": [10, 10],
											"SP": [10, 10],
											"AP": [0, None],
											"DP": 0,
											"EP": ([[200, 200], [None, None]], [[10, 10], [None, None]])[chosen_class == "Mage"],
											"M": 100,
											"XP": [0, 3, 1]
										}
										Player.map = "DevRoom"
										difficulty = sliders[0][0].text_content.split(" ")[-1]
										player = Player(100, 100)
										inventory = Inventory(player)

										game_map = TileMap(os.path.join("scripts", "cache", "maps", "DevRoom"), "DevRoom", (Width, Height))
										for drop in game_map.full_drops:
											if type(drop[1]) == ProjDrop:
												if drop[1].shooter:
													drop[1].shooter = player
												else:
													drop[1].shooter = None
												

										projs = []
										return game_map, projs, player, inventory

						elif button[0].is_over((mp[0]+scroll[0], mp[1]+scroll[1])) and not button[3]:
							if not disable_presses:
								if button[1]:
									if button[1] == "quit":
										pygame.quit(); sys.exit()
									
									elif "goto" in button[1]:
										index = 0
										if now[-1] == "pause" and button[1].split(" ")[1] == "main":
											musics["main"].start()
										buttons, sliders, textboxes, texts, update, scroll = reset()
										pages[button[1].split(" ")[1]]()
										if button[1].split(" ")[1] == "settings":
											update = settings_update
									
									elif button[1] == "restart":
										save = load_json(["scripts", "saves", f"save{save_num}.json"])
										Player.classes = save["classes"]
										Player.name = save["name"]
										difficulty = save["difficulty"]
										Player.inventory = save["inventory"]
										Player.equipment = save["equipment"]
										Player.stats = save["stats"]
										Player.map = save["map"]
										player = Player(0, 0)

										game_map = TileMap(os.path.join("scripts", "cache", "maps", save["map"]), save["map"], (Width, Height), False, save_num)
										for drop in game_map.full_drops:
											if type(drop[1]) == ProjDrop:
												if drop[1].shooter:
													drop[1].shooter = player
												else:
													drop[1].shooter = None
												
										projs = []
										player.x, player.y = save["loc"]
										player.inv_size = 5 if player.equipment[3] == "No Backpack" else equipment[3][player.equipment[3]]["slots"]
										player.inv_weight = [0, None] if player.equipment[3] == "No Backpack" else [0, equipment[3][player.equipment[3]]["max weight"]]
										if player.inv_weight[1] != None:
											for item in player.inventory:
												player.inv_weight[0] += items[item]["weight"]
										inventory = Inventory(player)
										near_death_surf.set_alpha(math.floor(255-((player.stats["HP"][0]-1)/(player.stats["HP"][1]-1))*255))

										return game_map, projs, player, inventory

									elif button[1] == "return":
										if now[-1] == "pause":
											last_time = time.time()-paused_timers[0]
											player.inv_max_exceed_time = time.time()-paused_timers[1]
											player.dash_cooldown = time.time()-paused_timers[2]
											player.shielded[1] = time.time()-paused_timers[3]
											player.i_frame = time.time()-paused_timers[4]
											
											i = 5
											if player.weapons[0] != [None, None]:
												player.weapons[0][1].cooldown_time = time.time()-paused_timers[i]
												i += 1
											if player.weapons[1] != [None, None]:
												player.weapons[1][1].cooldown_time = time.time()-paused_timers[i]
												i += 1
											for drop in game_map.full_drops:
												drop[2] = time.time()-paused_timers[i]
												i += 1
											for proj in projs:
												proj.shot_time = time.time()-paused_timers[i]
												proj.ricochet = time.time()-paused_timers[i+1]
												i += 2
											for enemy in game_map.full_enemies:
												enemy.sus_time[0] = time.time()-paused_timers[i]
												enemy.target_change_timer = time.time()-paused_timers[i+1]
												enemy.i_frame = time.time()-paused_timers[i+2]
												enemy.proj_cooldown = time.time()-paused_timers[i+3]
												i += 4
										return game_map, projs, player, inventory

									elif button[1] == "toggle":
										button[0].text_content = f"{button[0].text_content.split(':')[0]}: {get_text('status:on')}" if get_text('status:off') in button[0].text_content else f"{button[0].text_content.split(':')[0]}: {get_text('status:off')}"
									
									elif "ctrl" in button[1]:
										for name in edit_ctrl.keys():
											if edit_ctrl[name]:
												edit_ctrl[name] = False
												for _button in buttons:
													if _button[0].text and _button[1]:
														if name in _button[1]:
															_button[0].text_content = f"{name}: {pygame.key.name(settings['keys'][name.split(' ')[0]]).capitalize()}"
										
										edit_ctrl[" ".join(button[1].split(" ")[1:])] = True
										button[0].text_content = "- Press the desired key -"
									
									elif button[1].startswith("save"):
										save_num = button[1].split(" ")[1]
										if f"save{save_num}.json" not in os.listdir(os.path.join("scripts", "saves")):
											save_chosen = [False, False, False]
											save_chosen[int(save_num)-1] = True

											buttons, sliders, textboxes, texts, update, scroll = reset()
											chosen_save()
											texts[0][0].content = (f"{get_text('button:save')} {save_num}", settings["lang"])
										else:
											save = load_json(["scripts", "saves", f"save{save_num}.json"])
											Player.classes = save["classes"]
											Player.name = save["name"]
											difficulty = save["difficulty"]
											Player.inventory = save["inventory"]
											Player.equipment = save["equipment"]
											Player.stats = save["stats"]
											Player.map = save["map"]
											player = Player(0, 0)

											game_map = TileMap(os.path.join("scripts", "cache", "maps", save["map"]), save["map"], (Width, Height), False, save_num)
											for drop in game_map.full_drops:
												if type(drop[1]) == ProjDrop:
													if drop[1].shooter:
														drop[1].shooter = player
													else:
														drop[1].shooter = None
													
											projs = []
											player.x, player.y = save["loc"]
											player.inv_size = 5 if player.equipment[3] == "No Backpack" else equipment[3][player.equipment[3]]["slots"]
											player.inv_weight = [0, None] if player.equipment[3] == "No Backpack" else [0, equipment[3][player.equipment[3]]["max weight"]]
											if player.inv_weight[1] != None:
												for item in player.inventory:
													player.inv_weight[0] += items[item]["weight"]
											inventory = Inventory(player)
											near_death_surf.set_alpha(math.floor(255-((player.stats["HP"][0]-1)/(player.stats["HP"][1]-1))*255))

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

									elif button[1].startswith("lang"):
										set_lang = button[1].split(" ")[1]

									elif button[1] == "next music":
										if chosen_music < len(music_list)-1:
											chosen_music += 1
										else:
											chosen_music = 0
										buttons[0][0].text_content = music_list[chosen_music][0]
										music_list[chosen_music][1].start()

										buttons[0][0].x = Width*0.5-buttons[0][0].width*0.5
										buttons[1][0].x = buttons[0][0].x+buttons[0][0].width+5
										buttons[2][0].x = buttons[0][0].x-35
									
									elif button[1] == "pre music":
										if chosen_music > 0:
											chosen_music -= 1
										else:
											chosen_music = len(music_list)-1
										buttons[0][0].text_content = music_list[chosen_music][0]
										music_list[chosen_music][1].start()

										buttons[0][0].x = Width*0.5-buttons[0][0].width*0.5
										buttons[1][0].x = buttons[0][0].x+buttons[0][0].width+5
										buttons[2][0].x = buttons[0][0].x-35

									elif button[1] == "controller":
										if sdl2_controller.get_init():
											sdl2_controller.quit()
											controller = FakeController()
											button[0].text_content = get_text("button:controller")+get_text("status:disconnected")
										else:
											sdl2_controller.init()
											try:
												controller = sdl2_controller.Controller(0)
												button[0].text_content = get_text("button:controller")+get_text("status:connected")
											except:
												sdl2_controller.quit()

					for slider in sliders:
						if not disable_presses:
							slider[0].is_over((mp[0]+scroll[0], mp[1]+scroll[1]))

					for textbox in textboxes:
						textbox[0].is_over((mp[0]+scroll[0], mp[1]+scroll[1]))

				if event.type == MOUSEBUTTONUP:
					for slider in sliders:
						slider[0].selected = False

				if event.type == KEYDOWN:
					if event.key in [K_ESCAPE, K_BACKSPACE]:
						if "main" in now:
							now = []
							buttons, sliders, textboxes, texts, update, scroll = reset()
							main()
						elif "pause" in now and now[-1] != "pause":
							now = []
							buttons, sliders, textboxes, texts, update, scroll = reset()
							pause()
						elif now[-1] == "pause":
							last_time = time.time()-paused_timers[0]
							player.inv_max_exceed_time = time.time()-paused_timers[1]
							player.dash_cooldown = time.time()-paused_timers[2]
							player.shielded[1] = time.time()-paused_timers[3]
							player.i_frame = time.time()-paused_timers[4]
							
							i = 5
							if player.weapons[0] != [None, None]:
								player.weapons[0][1].cooldown_time = time.time()-paused_timers[i]
								i += 1
							if player.weapons[1] != [None, None]:
								player.weapons[1][1].cooldown_time = time.time()-paused_timers[i]
								i += 1
							for drop in game_map.full_drops:
								drop[2] = time.time()-paused_timers[i]
								i += 1
							for proj in projs:
								proj.shot_time = time.time()-paused_timers[i]
								proj.ricochet = time.time()-paused_timers[i+1]
								i += 2
							for enemy in game_map.full_enemies:
								enemy.sus_time[0] = time.time()-paused_timers[i]
								enemy.target_change_timer = time.time()-paused_timers[i+1]
								enemy.i_frame = time.time()-paused_timers[i+2]
								enemy.proj_cooldown = time.time()-paused_timers[i+3]
								i += 4

							return game_map, projs, player, inventory
					
					if event.key == K_F11:
						F11()
						if "Fullscreen" in buttons[0][0].text_content:
							buttons[0][0].text_content = f"{buttons[0][0].text_content.split(':')[0]}: {'On' if settings['fullscreen'] else 'Off'}"

					if event.key == K_F3:
						debug_menu = not debug_menu

					if event.key == K_F1 and now[-1] != "music room":
						musics[list(musics.keys())[0]].start()
						buttons, sliders, textboxes, texts, update, scroll = reset()
						pages["music room"]()

					if event.key == K_c and now[-1] != "credits":
						buttons, sliders, textboxes, texts, update, scroll = reset()
						speed = 0.5
						pages["credits"]()
						update = credits_update

					if event.key in [K_RIGHT, K_d] and now[-1] == "music room":
						if chosen_music < len(music_list)-1:
							chosen_music += 1
						else:
							chosen_music = 0
						buttons[0][0].text_content = music_list[chosen_music][0]
						music_list[chosen_music][1].start()

						buttons[0][0].x = Width*0.5-buttons[0][0].width*0.5
						buttons[1][0].x = buttons[0][0].x+buttons[0][0].width+10
						buttons[2][0].x = buttons[0][0].x-70

					if event.key in [K_LEFT, K_a] and now[-1] == "music room":
						if chosen_music > 0:
							chosen_music -= 1
						else:
							chosen_music = len(music_list)-1
						buttons[0][0].text_content = music_list[chosen_music][0]
						music_list[chosen_music][1].start()

						buttons[0][0].x = Width*0.5-buttons[0][0].width*0.5
						buttons[1][0].x = buttons[0][0].x+buttons[0][0].width+10
						buttons[2][0].x = buttons[0][0].x-70

					if event.key in [K_UP, K_w]:
						all_items = sliders+textboxes+buttons
						index = (index - 1) % len(all_items)

						pygame.mouse.set_pos(all_items[index][0].rect.center)
					
					if event.key in [K_DOWN, K_s]:
						all_items = sliders+textboxes+buttons
						index = (index + 1) % len(all_items)

						pygame.mouse.set_pos(all_items[index][0].rect.center)

				if event.type == CONTROLLERBUTTONDOWN:
					if event.button == CONTROLLER_BUTTON_B:
						if "main" in now:
							now = []
							buttons, sliders, textboxes, texts, update, scroll = reset()
							main()
						elif "pause" in now and now[-1] != "pause":
							now = []
							buttons, sliders, textboxes, texts, update, scroll = reset()
							pause()
						elif now[-1] == "pause":
							last_time = time.time()-paused_timers[0]
							player.inv_max_exceed_time = time.time()-paused_timers[1]
							player.dash_cooldown = time.time()-paused_timers[2]
							player.shielded[1] = time.time()-paused_timers[3]
							player.i_frame = time.time()-paused_timers[4]
							
							i = 5
							if player.weapons[0] != [None, None]:
								player.weapons[0][1].cooldown_time = time.time()-paused_timers[i]
								i += 1
							if player.weapons[1] != [None, None]:
								player.weapons[1][1].cooldown_time = time.time()-paused_timers[i]
								i += 1
							for drop in game_map.full_drops:
								drop[2] = time.time()-paused_timers[i]
								i += 1
							for proj in projs:
								proj.shot_time = time.time()-paused_timers[i]
								proj.ricochet = time.time()-paused_timers[i+1]
								i += 2
							for enemy in game_map.full_enemies:
								enemy.sus_time[0] = time.time()-paused_timers[i]
								enemy.target_change_timer = time.time()-paused_timers[i+1]
								enemy.i_frame = time.time()-paused_timers[i+2]
								enemy.proj_cooldown = time.time()-paused_timers[i+3]
								i += 4

							return game_map, projs, player, inventory
					
					if event.button == CONTROLLER_BUTTON_START and now[-1] == "pause":
						last_time = time.time()-paused_timers[0]
						player.inv_max_exceed_time = time.time()-paused_timers[1]
						player.dash_cooldown = time.time()-paused_timers[2]
						player.shielded[1] = time.time()-paused_timers[3]
						player.i_frame = time.time()-paused_timers[4]
						
						i = 5
						if player.weapons[0] != [None, None]:
							player.weapons[0][1].cooldown_time = time.time()-paused_timers[i]
							i += 1
						if player.weapons[1] != [None, None]:
							player.weapons[1][1].cooldown_time = time.time()-paused_timers[i]
							i += 1
						for drop in game_map.full_drops:
							drop[2] = time.time()-paused_timers[i]
							i += 1
						for proj in projs:
							proj.shot_time = time.time()-paused_timers[i]
							proj.ricochet = time.time()-paused_timers[i+1]
							i += 2
						for enemy in game_map.full_enemies:
							enemy.sus_time[0] = time.time()-paused_timers[i]
							enemy.target_change_timer = time.time()-paused_timers[i+1]
							enemy.i_frame = time.time()-paused_timers[i+2]
							enemy.proj_cooldown = time.time()-paused_timers[i+3]
							i += 4

						return game_map, projs, player, inventory
				
					if event.button == CONTROLLER_BUTTON_DPAD_UP:
						all_items = sliders+textboxes+buttons
						index = (index - 1) % len(all_items)

						pygame.mouse.set_pos(all_items[index][0].rect.center)
					
					if event.button == CONTROLLER_BUTTON_DPAD_DOWN:
						all_items = sliders+textboxes+buttons
						index = (index + 1) % len(all_items)

						pygame.mouse.set_pos(all_items[index][0].rect.center)
						
				for textbox in textboxes:
					textbox[0].update_text(event)

				if update is not None:
					update(event)

			pygame.display.update()

	equipment = load_json(["scripts", "cache", "equipment.json"])
	items = load_json(["scripts", "cache", "items.json"])
	langs = load_json(["scripts", "data", "langs.json"])

	tooltips = {
		avlang: {
			item: [
				t1 := Text(os.path.join("assets", "fontsDL", "font.png"), items[item]["name"][i], 2, (62, 41, 20) if item in weapons.keys() and weapons.get(item).player_class == "Archer" else (0, 58, 144) if item in weapons.keys() and weapons.get(item).player_class == "Mage" else (255, 255, 255), avlang),
				t2 := Text(os.path.join("assets", "fontsDL", "font.png"), items[item]["tooltip"][i], 2, (255, 255, 255), avlang),
				pygame.Surface((max([t1.width, t2.width])+5, t1.height+t2.height+7.5))
			] for item in items.keys()
		} for i, avlang in enumerate(langs)
	}
	for lang in tooltips.keys():
		for item, tooltip_data in tooltips[lang].items():
			tooltip_data[2].fill((255, 255, 255))
			tooltip_data[2].fill((0, 0, 0), (1, 1, tooltip_data[2].get_width()-2, tooltip_data[2].get_height()-2))
			tooltip_data[0].render(tooltip_data[2], (tooltip_data[2].get_width()*0.5-tooltip_data[0].width*0.5, 3))
			if lang != "arabic":
				tooltip_data[1].render(tooltip_data[2], (3, tooltip_data[0].height+5))
			else:
				tooltip_data[1].render(tooltip_data[2], (tooltip_data[2].get_width()-tooltip_data[1].width-3, tooltip_data[0].height+5))
			tooltips[lang][item] = tooltip_data[2]

	camera = Camera([0, 0], None)
	game_map, projs, player, inventory = menus()
	camera.target = player

	current_dialogue = None
	current_cutscene = None
	next_to_door = None
	cutscene_rects = 0
	music = None
	sleep_time = [time.time(), time.time()]
	sleep_brightness = [game_brightness.brightness, False]
	sleep_health_math = (player.stats["HP"][1]-player.stats["HP"][0])/3

	while 1:
		clock.tick(settings["FPS"])
		mpos = pygame.mouse.get_pos()
		dt, last_time = FPS_ind()
		bosses = [player]
		
		if dt >= 10:
			dt = 0

		if player.sleep[1]:
			try:
				pre_save = load_json(["scripts", "saves", f"save{save_num}.json"])
			except:
				pre_save = {
					"enemies": {},
					"drops": {},
					"dialogues": {}
				}
			if "enemies" not in pre_save.keys(): pre_save["enemies"] = {}
			pre_save["enemies"][game_map.room] = []
			for enemy in game_map.full_enemies:
				stats = {
					"health": enemy.stats["HP"],
					"attack": enemy.stats["AP"],
					"defense": enemy.stats["DP"],
					"speed": enemy.stats["SP"],
					"view": enemy.stats["V"],
					"suspicious view": enemy.stats["SV"],
					"XP": enemy.stats["XP"],
					"knockback resistence": enemy.knockback_resist
				}
				pre_save["enemies"][game_map.room].append([enemy.x, enemy.y, enemy.name, stats])
			
			if "drops" not in pre_save.keys(): pre_save["drops"] = {}
			pre_save["drops"][game_map.room] = []
			for drop in game_map.full_drops:
				if type(drop[1]) == Drop:
					pre_save["drops"][game_map.room].append([drop[1].x, drop[1].y, drop[0], "normal"])
				elif type(drop[1]) == ProjDrop:
					pre_save["drops"][game_map.room].append([drop[1].x, drop[1].y, drop[0], "proj", drop[1].shooter==player, drop[1].angle])
			
			if "dialogues" not in pre_save.keys(): pre_save["dialogues"] = {}
			pre_save["dialogues"][game_map.room] = {"npc": [], "dlg": [], "cut": []}
			for npc in game_map.full_npcs:
				pre_save["dialogues"][game_map.room]["npc"].append([npc.x, npc.y, npc.id])
			for dlg in game_map.dlg_trg_rects:
				if not dlg[1].triggered:
					pre_save["dialogues"][game_map.room]["dlg"].append([[dlg[0].x, dlg[0].y, dlg[0].w, dlg[0].h], dlg[1].id])
			for cut in game_map.cut_rects:
				if not cut[1].triggered:
					pre_save["dialogues"][game_map.room]["cut"].append([[cut[0].x, cut[0].y, cut[0].w, cut[0].h], cut[1].id])

			save = {
				"name": player.name,
				"difficulty": difficulty,
				"classes": player.classes,
				"stats": player.stats,
				"inventory": player.inventory,
				"equipment": player.equipment,
				"map": game_map.room,
				"loc": [player.x, player.y],
				"enemies": pre_save["enemies"],
				"drops": pre_save["drops"],
				"dialogues": pre_save["dialogues"]
			}

			dump_json(["scripts", "saves", f"save{save_num}.json"], save)
			player.sleep[1] = False
		if player.sleep[0]:
			if game_brightness.brightness > -255 and not sleep_brightness[1]:
				game_brightness.brightness -= 5*dt
				sleep_time = [time.time(), time.time()]
				sleep_health_math = (player.stats["HP"][1]-player.stats["HP"][0])/3
			else:
				sleep_brightness[1] = True
				player.stats["SP"][0] = player.stats["SP"][1]
				if "Mage" in player.classes:
					mi = player.classes.index("Mage")
					player.stats["EP"][mi][0] = player.stats["EP"][mi][1]
				if time.time()-sleep_time[1] >= 1:
					sleep_time[1] = time.time()
					player.stats["HP"][0] += sleep_health_math
					player.stats["HP"][0] = round(player.stats["HP"][0]) if player.stats["HP"][0] < player.stats["HP"][1]-1 else player.stats["HP"][1]
					if random.randint(0, 10) == 1:
						player.sleep[0] = False
						game_brightness.brightness = sleep_brightness[0]
						player.sleep[1] = True
			if game_brightness.brightness < sleep_brightness[0] and sleep_brightness[1] and time.time()-sleep_time[0] >= 3:
				game_brightness.brightness += 5*dt
			elif game_brightness.brightness >= sleep_brightness[0] and sleep_brightness[1]:
				player.sleep[0] = False
				player.sleep[1] = True
		player.sleep_stamina -= 1*dt
		
		# drawing
		win.fill((0, 0, 0))
		game_map.draw_map(camera.main_display, player, projs, camera.scroll)

		# action
		for enemy in reversed(game_map.full_enemies):
			enemy.dmg_counter_log(dt)

			if enemy.type == "boss" and enemy.active:
				bosses.append(enemy)
				if not inventory_menu:
					enemy.ai(game_map, player, projs, dt)

		if not inventory_menu and not current_dialogue and not current_cutscene:
			player.regen()
			player.move(game_map, dt, settings["keys"], controller)
			player.attack(game_map.enemies, mpos, controller, camera.scroll, projs)
			player.xp()

			for dlg in game_map.dlg_trg_rects:
				if player.rect.colliderect(dlg[0]) and not dlg[1].triggered:
					current_dialogue = dlg[1]
					player.vel = pygame.Vector2(0, 0)

			for cut in game_map.cut_rects:
				if player.rect.colliderect(cut[0]) and not cut[1].triggered:
					current_cutscene = cut[1]
					player.vel = pygame.Vector2(0, 0)
			
			for enemy in reversed(game_map.enemies):
				if enemy.type == "boss" and not enemy.active:
					enemy.active = True
				if enemy.type != "boss":
					enemy.ai(game_map, player, projs, dt)

			for drop in game_map.full_drops:
				drop[3] = time.time()
			for drop in reversed(game_map.drops):
				if type(drop[1]) == Spirit and "Mage" in player.classes:
					if drop[1].move(player, dt, sprites):
						if drop in game_map.full_drops:
							game_map.full_drops.remove(drop)

				if drop[1].rect.colliderect(player.rect) and time.time()-drop[2] >= 3 and drop in game_map.drops:
					if inventory.pick_item(drop[0], drop[1]) and type(drop[1]) != Spirit:
						game_map.full_drops.remove(drop)
						
			while len([drop for drop in game_map.full_drops if type(drop[1]) == ProjDrop]) >= 480:
				game_map.full_drops = game_map.full_drops[1:]

			for proj in reversed(projs):
				proj.despawn(game_map, projs)

				proj.move(game_map, dt, camera.scroll, mpos, game_map.enemies+game_map.npcs+[player], player, projs)
				entity_health, entity = proj.damage(game_map.enemies+game_map.npcs+[player], projs)
				if entity:
					if entity_health <= 0:
						if entity == player:
							game_map, projs, player, inventory = menus("gameover")
							current_dialogue = None
							current_cutscene = None
							camera = Camera([player.rect.centerx+Width*0.5, player.rect.centery+Height*0.5], player)
							near_death_surf.set_alpha(0)

							break
						else:
							if entity in game_map.full_enemies:
								game_map.full_enemies.remove(entity)
							elif entity in game_map.full_npcs and proj.shooter == player:
								game_map.full_npcs.remove(entity)

							if "Mage" in player.classes:
								game_map.full_drops.append(["spirit", Spirit(entity.rect.centerx-6, entity.rect.centery-8, sprites["Spirit"]), 0, time.time()])
							if proj.shooter == player:
								player.stats["XP"][0] += entity.stats["XP"]
					else:
						if entity in game_map.npcs and entity.anger_attack and proj.shooter == player:
							game_map.full_enemies.append(enemy_list[entity.name]["AI"].AI(entity.x, entity.y, enemy_list[entity.name]["Anim"], entity.stats, entity.name))
							game_map.full_enemies[-1].damage_counters = entity.damage_counters

							current_dialogue = entity.anger_dialogue
							if entity in game_map.full_npcs:
								game_map.full_npcs.remove(entity)

			for connector in game_map.connectors:
				if connector[0].colliderect(player.door_rect) and len(bosses) == 1:
					next_to_door = connector
					break
			else:
				next_to_door = None

		if debug_menu:
			debug(camera.main_display, player, game_map.enemies, [game_map.tile_rects, [drop[1].rect for drop in game_map.drops], game_map.enemies, projs])
		
		for mod_loop in mod_loops:
			mod_loop()

		# event
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit(); sys.exit()

			if event.type == WINDOWLEAVE and not inventory_menu:
				game_map, projs, player, inventory = menus("pause")
				musics[music].toggle_pause()
				camera.target = player

			if event.type == KEYDOWN:
				if event.key == K_F11:
					F11()
				
				elif event.key == K_F3:
					debug_menu = not debug_menu
				elif event.key == K_b and debug_menu:
					show_hitboxes = not show_hitboxes
				elif event.key == K_m and debug_menu:
					show_mid = not show_mid
				elif event.key == K_n and debug_menu:
					show_view = not show_view

				elif event.key == settings["keys"]["inventory"] and not player.sleep[0] and [current_dialogue, current_cutscene] == [None, None]:
					inventory_menu = not inventory_menu
					player._generate_UI(inventory_menu)
					if not inventory_menu:
						for proj in projs:
							proj.shot_time = time.time()-(proj.pre_pause_time-proj.shot_time)
							proj.ricochet = time.time()-(proj.pre_pause_ricochet-proj.ricochet)
							
						for drop in game_map.full_drops:
							drop[2] = time.time()-(drop[3]-drop[2])
					for enemy in game_map.enemies:
						enemy.animate = False
					player.animate = False
				
				elif event.key == settings["keys"]["pause"] and not player.sleep[0]:
					if inventory_menu:
						inventory_menu = False
					else:
						game_map, projs, player, inventory = menus("pause")
						musics[music].toggle_pause()
						camera.target = player
				
				elif event.key == settings["keys"]["sleep"] and not player.sleep[0] and [current_dialogue, current_cutscene] == [None, None]:
					player.check_sleep(game_map.full_enemies)
					if player.sleep[0]:
						sleep_brightness = [game_brightness.brightness, False]

				elif event.key == settings["keys"]["interact"] and not player.sleep[0] and [current_dialogue, current_cutscene] == [None, None]:
					if next_to_door:
						player.x = next_to_door[2]
						player.y = next_to_door[3]
						if next_to_door[1] in save["enemies"].keys():
							load_from_files = False
						else:
							load_from_files = True
						game_map = TileMap(os.path.join("scripts", "cache", "maps", next_to_door[1]), next_to_door[1], (Width, Height), load_from_files, save_num)
						for drop in game_map.full_drops:
							if type(drop[1]) == ProjDrop:
								if drop[1].shooter:
									drop[1].shooter = player
								else:
									drop[1].shooter = None

						camera.immediate = True
						camera.update((Width, Height), dt, game_map)
						camera.immediate = False

					else:
						for npc in game_map.npcs:
							if npc.trigger_dialogue(player):
								current_dialogue = npc.dialogue
								player.vel = pygame.Vector2(0, 0)
								break

				else:
					if current_dialogue:
						if current_dialogue.text_index < len(current_dialogue.texts[settings["lang"]])-1:
							if current_dialogue.text_portion < len(current_dialogue.texts[settings["lang"]][current_dialogue.text_index][2])-1:
								current_dialogue.text_portion = len(current_dialogue.texts[settings["lang"]][current_dialogue.text_index][2])
								current_dialogue.texts[settings["lang"]][current_dialogue.text_index][1].content = current_dialogue.texts[settings["lang"]][current_dialogue.text_index][2][:current_dialogue.text_portion]
							else:
								current_dialogue.text_index += 1
								current_dialogue.text_portion = 0
								current_dialogue.text_portion_time = 0
						else:
							if current_dialogue.text_portion < len(current_dialogue.texts[settings["lang"]][current_dialogue.text_index][2])-1:
								current_dialogue.text_portion = len(current_dialogue.texts[settings["lang"]][current_dialogue.text_index][2])
								current_dialogue.texts[settings["lang"]][current_dialogue.text_index][1].content = current_dialogue.texts[settings["lang"]][current_dialogue.text_index][2][:current_dialogue.text_portion]
							else:
								current_dialogue.text_index = 0
								current_dialogue.text_portion = 0
								current_dialogue.text_portion_time = 0
								current_dialogue.triggered = True
								current_dialogue = None
								if current_cutscene:
									current_cutscene._next_frame("dialogue")
									current_cutscene.dialogue = False
									current_cutscene.dialogue_num += 1


				# Testing Only
				if event.key == K_p:
					enemies_data = load_json(["scripts", "cache", "enemies.json"])
					game_map.full_enemies.append(AI(player.x+100, player.y, os.path.join("assets", "ANIMATIONSDL", "Ekreta Tree"), enemies_data["Ekreta Tree"], "Ekreta"))

				if event.key == K_l and not player.classes[1]:
					player.classes[1] = ("Archer", "Mage")[player.classes[0] == "Archer"]
					player.stats["AP"][1] = 0
					player.stats["EP"][1] = ([10, 10], [200, 200])[player.classes[1] == "Archer"]

			if event.type == CONTROLLERDEVICEREMOVED and not inventory_menu:
				controller = FakeController()
				sdl2_controller.quit()
				game_map, projs, player, inventory = menus("pause")
				musics[music].toggle_pause()
				camera.target = player
			
			if event.type == CONTROLLERDEVICEADDED and type(controller) == FakeController:
				sdl2_controller.init()
				controller = sdl2_controller.Controller(0)

			if event.type == CONTROLLERBUTTONDOWN:
				if event.button == CONTROLLER_BUTTON_BACK and not player.sleep[0] and [current_dialogue, current_cutscene] == [None, None]:
					inventory_menu = not inventory_menu
					player._generate_UI(inventory_menu)
					if not inventory_menu:
						for proj in projs:
							proj.shot_time = time.time()-(proj.pre_pause_time-proj.shot_time)
							proj.ricochet = time.time()-(proj.pre_pause_ricochet-proj.ricochet)
							
						for drop in game_map.full_drops:
							drop[2] = time.time()-(drop[3]-drop[2])
					for enemy in game_map.enemies:
						enemy.animate = False
					player.animate = False

				elif event.button == CONTROLLER_BUTTON_B and inventory_menu:
					inventory_menu = False

				elif event.button == CONTROLLER_BUTTON_START and not player.sleep[0]:
					if inventory_menu:
						inventory_menu = False
					else:
						game_map, projs, player, inventory = menus("pause")
						musics[music].toggle_pause()
						camera.target = player

				elif event.button == CONTROLLER_BUTTON_LEFTSHOULDER and not player.sleep[0] and [current_dialogue, current_cutscene] == [None, None]:
					player.check_sleep(game_map.full_enemies)
					if player.sleep[0]:
						sleep_brightness = [game_brightness.brightness, False]

				elif event.button == CONTROLLER_BUTTON_RIGHTSHOULDER and not player.sleep[0] and [current_dialogue, current_cutscene] == [None, None]:
					if next_to_door:
						player.x = next_to_door[2]
						player.y = next_to_door[3]
						if next_to_door[1] in save["enemies"].keys():
							load_from_files = False
						else:
							load_from_files = True
						game_map = TileMap(os.path.join("scripts", "cache", "maps", next_to_door[1]), next_to_door[1], (Width, Height), load_from_files, save_num)
						for drop in game_map.full_drops:
							if type(drop[1]) == ProjDrop:
								if drop[1].shooter:
									drop[1].shooter = player
								else:
									drop[1].shooter = None

						camera.immediate = True
						camera.update((Width, Height), dt, game_map)
						camera.immediate = False

					else:
						for npc in game_map.npcs:
							if npc.trigger_dialogue(player):
								current_dialogue = npc.dialogue
								player.vel = pygame.Vector2(0, 0)
								break

				elif current_dialogue:
					if current_dialogue.text_portion < len(current_dialogue.texts[settings["lang"]][current_dialogue.text_index][2])-1:
						current_dialogue.text_portion = len(current_dialogue.texts[settings["lang"]][current_dialogue.text_index][2])
						current_dialogue.texts[settings["lang"]][current_dialogue.text_index][1].content = current_dialogue.texts[settings["lang"]][current_dialogue.text_index][2][:current_dialogue.text_portion]
					else:
						current_dialogue.text_index = 0
						current_dialogue.text_portion = 0
						current_dialogue.text_portion_time = 0
						current_dialogue.triggered = True
						current_dialogue = None
						if current_cutscene:
							current_cutscene._next_frame("dialogue")
							current_cutscene.dialogue = False
							current_cutscene.dialogue_num += 1

			if event.type in [MOUSEBUTTONDOWN, KEYDOWN, CONTROLLERBUTTONDOWN] and inventory_menu:
				button = None
				if event.type == MOUSEBUTTONDOWN:
					button = event.button
				elif event.type == KEYDOWN:
					if event.key in [K_SPACE, K_RETURN]:
						button = 1
					elif event.key in [K_LSHIFT, K_RSHIFT, K_BACKSPACE]:
						button = 3
				else:
					if event.button == CONTROLLER_BUTTON_A:
						button = 1
					elif event.button == CONTROLLER_BUTTON_X:
						button = 3

				if button:
					if inventory.index < 4:
						rect = inventory.rects[1][inventory.index]
						if button == 1:
							inventory.unequip_item(rect[1])
						elif button == 3:
							game_map.full_drops.append(inventory.throw_eq_item(rect[1]))
							if game_map.full_drops[-1] == None:
								game_map.full_drops = game_map.full_drops[:-1]
					else:
						rect = inventory.rects[0][inventory.index-4]

						if button == 1:
							inventory.equip_item(rect[1])
						elif button == 3:
							game_map.full_drops.append(inventory.throw_inv_item(rect[1]))
							if game_map.full_drops[-1] == None:
								game_map.full_drops = game_map.full_drops[:-1]

						if inventory.index == len(player.equipment+player.inventory):
							inventory.index -= 1
					
			if event.type == MOUSEBUTTONUP:
				if player.equipment[1] in equipment[1].keys() and event.button == 3:
					player.shielded = [None, 0]

			if event.type == CONTROLLERAXISMOTION:
				if event.axis in [CONTROLLER_AXIS_RIGHTX, CONTROLLER_AXIS_RIGHTY]:
					x = (controller.get_axis(CONTROLLER_AXIS_RIGHTX)/32767*100)+(player.rect.centerx)-camera.scroll.x
					y = (controller.get_axis(CONTROLLER_AXIS_RIGHTY)/32767*100)+(player.rect.centery)-camera.scroll.y

					if x <= 1:
						x = 1
					elif x >= 639:
						x = 639
					if y <= 1:
						y = 1
					elif y >= 359:
						y = 359
					pygame.mouse.set_pos((x, y))

				if player.equipment[1] in equipment[1].keys() and event.axis == CONTROLLER_AXIS_TRIGGERRIGHT and event.value/32767 < 0.5:
					player.shielded = [None, 0]

			if inventory_menu and event.type in [KEYDOWN, CONTROLLERBUTTONDOWN]:
				if event.type == KEYDOWN:
					if event.key in [K_w, K_UP]:
						button = CONTROLLER_BUTTON_DPAD_UP
					elif event.key in [K_s, K_DOWN]:
						button = CONTROLLER_BUTTON_DPAD_DOWN
					elif event.key in [K_a, K_LEFT]:
						button = CONTROLLER_BUTTON_DPAD_LEFT
					elif event.key in [K_d, K_RIGHT]:
						button = CONTROLLER_BUTTON_DPAD_RIGHT
					else:
						continue
				else:
					if event.button in [CONTROLLER_BUTTON_DPAD_UP, CONTROLLER_BUTTON_DPAD_DOWN, CONTROLLER_BUTTON_DPAD_LEFT, CONTROLLER_BUTTON_DPAD_RIGHT]:
						button = event.button
					else:
						continue
				
				inventory.select_slot(button)


		if len(bosses) > 1:
			try:
				if bosses[1].music and not musics[bosses[1].music].playing:
					musics[bosses[1].music].start()
					music = bosses[1].music
			except AttributeError:
				pass

			num_of_bosses = len(bosses)
			x = 0
			y = 0
			for boss in bosses:
				try:
					if not boss.camera or boss not in game_map.enemies:
						continue
				except:
					pass
				x += boss.rect.centerx
				y += boss.rect.centery
			camera.forced_loc = (x/num_of_bosses, y/num_of_bosses)
			if (x, y) == player.rect.center:
				camera.forced_loc = []
				camera.target = player
		else:
			room_data = load_json(["scripts", "cache", "rooms.json"])
			if room_data[game_map.room]["music"]:
				if not musics[room_data[game_map.room]["music"]].playing:
					musics[room_data[game_map.room]["music"]].start()
					music = room_data[game_map.room]["music"]
			else:
				pygame.mixer.music.stop()
			camera.forced_loc = []

		camera.update((Width, Height), dt, game_map)

		# UI
		if player.cached_stats["HP"] != player.stats["HP"]:
			near_death_surf.set_alpha(math.floor(255-((player.stats["HP"][0]-1)/(player.stats["HP"][1]-1))*255))
		camera.display.blit(near_death_surf, (0, 0))
		
		for enemy in game_map.full_enemies:
			enemy.draw_UI(camera.display, camera.scroll)

		if current_cutscene:
			if cutscene_rects < 50:
				cutscene_rects += 2*dt
			pygame.draw.rect(camera.display, (0, 0, 0), (0, cutscene_rects-50, Width, 50))
			pygame.draw.rect(camera.display, (0, 0, 0), (0, Height-cutscene_rects+1, Width, 50))
			returned = current_cutscene.animate(game_map, player, camera, dt)
			if returned == True:
				current_cutscene = None
			elif returned != None:
				current_dialogue = returned

		elif cutscene_rects > 0:
			cutscene_rects -= 2*dt
			pygame.draw.rect(camera.display, (0, 0, 0), (0, cutscene_rects-50, Width, 50))
			pygame.draw.rect(camera.display, (0, 0, 0), (0, Height-cutscene_rects, Width, 50))

		if current_dialogue:
			current_dialogue.render(camera.display, settings["lang"])

		ui_return1 = player.UI(camera.display, False, game_map)

		if inventory_menu:
			inventory_brightness.draw(camera.display)
			ui_return2 = player.UI(camera.display, True, game_map)
			if ui_return1 or ui_return2:
				inventory.update_surf()

			pygame.draw.line(camera.display, (255, 255, 255), (Width*0.5, 0), (Width*0.5, Height), 2)

			inventory.draw(camera.display, [Width, Height])
			for rect in inventory.rects[0] + inventory.rects[1]:
				if rect[0].collidepoint(mpos):
					if len(item_box) == 0:
						item_box.append(tooltips[settings["lang"]][rect[1]])
						item_box.append([mpos[0]+15 if mpos[0]+15+item_box[0].get_width() < Width else mpos[0]-item_box[0].get_width()-15, mpos[1]-15])
		
					camera.display.blit(item_box[0], (item_box[1][0], item_box[1][1]))
				else:
					item_box = []

		for interactable in game_map.npcs+game_map.connectors:
			if type(interactable) == list and interactable[0].colliderect(player.rect) and len(bosses) == 1:
				camera.display.blit(sprites["interact"], (player.x-camera.scroll.x, player.y-21-camera.scroll.y))
			elif type(interactable) == NPC and interactable.trigger_rect.colliderect(player.rect) and interactable.dialogue:
				camera.display.blit(sprites["interact"], (player.x-camera.scroll.x, player.y-21-camera.scroll.y))

		if game_brightness.brightness != 0:
			game_brightness.draw(camera.display)
		win.blit(camera.display, (0, 0))
		pygame.display.update()

except Exception as error:
	import traceback, ctypes, os, random
	from datetime import datetime

	pygame.quit()
	trace = traceback.format_exception(type(error), error, error.__traceback__)

	hour = datetime.now().strftime("%H")
	if int(hour) > 12:
		hour = int(hour)-12
		am_pm = "PM"
	else:
		am_pm = "AM"

	try:
		with open(os.path.join("scripts", "logs.txt"), "r", encoding="utf-8") as f:
			crash_logs = f.read()
	except FileNotFoundError:
		crash_logs = ""

	crash_logs += f"[{datetime.now().strftime(f'%d/%m/%Y | {hour}:%M:%S {am_pm}')}]\n{''.join(trace)}\n"
	print("".join(trace))

	error_title = "Error" if random.randint(0, 1000) > 0 else "R.I.P Inseynia, you're such a broken game"
	error = "".join(trace).split("\n")[-2]
	if platform.system() == "Windows":
		splitter = "\\"
	else:
		splitter = "/"
	ctypes.windll.user32.MessageBoxW(0, f"{error}\n\nPlease check \"scripts{splitter}logs.txt\" for the complete error and report it at https://discord.com/channels/797430217819291688/797430218251173916 (the server link: https://discord.gg/sXNeuPdeEj)\n Thank you :)", error_title, 0)

	with open(os.path.join("scripts", "logs.txt"), "w", errors="ignore", encoding="utf-8") as f:
		f.write(crash_logs)
