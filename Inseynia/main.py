try:
	# python -m cProfile -m main.py >> output.txt

	# Import modules
	import pygame, sys, os, random, time, platform, warnings, math, importlib, subprocess

	from pygame._sdl2 import controller as sdl2_controller
	from pypresence import Presence

	# Create the cache folder in case it's missing
	if "cacheDL" not in os.listdir("scripts"):
		os.mkdir(os.path.join("scripts", "cacheDL"))

	# Import Scripts
	from scripts.visuals.windowDL import win, settings, Width, Height

	from scripts.loadingDL.files import files

	from scripts.loadingDL.json_functions import load_json, dump_json
	from scripts.loadingDL.SFX import SFX_list
	from scripts.loadingDL.sprites import sprite

	Drop = files["drops"].Drop; Spirit = files["drops"].Spirit; ProjDrop = files["drops"].ProjDrop
	Inventory = files["inventory"].Inventory
	Player = files["player"].Player
	NPC = files["npc"].NPC

	TileMap = files["tiles"].TileMap; enemy_list = files["tiles"].enemy_list

	Button = files["button"].Button
	Camera = files["camera"].Camera
	Text = files["text"].Text
	Textbox = files["textbox"].Textbox
	Slider = files["slider"].Slider

	OBB = files["obb"].OBB
	Polygon = files["polygon"].Polygon
	AngleRect = files["angle"].AngleRect

	AI = files["ekretatree"].AI
	
	game_input = files["input"].game_input
	
	# pygame inits
	pygame.mixer.pre_init(44100, -16, 128, 512)
	pygame.init()
	sdl2_controller.init()
	try:
		controller = sdl2_controller.Controller(0)
	except:
		sdl2_controller.quit()

	texts_json = load_json(["scripts", "dataDL", "text.json"])

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

	#debug menu
	debug_menu = False
	show_hitboxes = False
	show_mid = False
	show_view = False
	show_active_rects = False

	fps_text = Text(os.path.join("assets", "fontsDL", "font.ttf"), "0", 16, (255,255,255), bg_color=(100, 100, 100), alpha=200)
	pos_text = Text(os.path.join("assets", "fontsDL", "font.ttf"), "0", 16, (255,255,255), bg_color=(100, 100, 100), alpha=200)
	room_text = Text(os.path.join("assets", "fontsDL", "font.ttf"), "0", 16, (255,255,255), bg_color=(100, 100, 100), alpha=200)
	projnum_text = Text(os.path.join("assets", "fontsDL", "font.ttf"), "0", 16, (255,255,255), bg_color=(100, 100, 100), alpha=200)
	fps_update = 0

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

	paused_timers = {}

	def delta_time():
		return (time.time() - last_time) * 60, time.time()

	def debug(rect_list=[]):
		global fps_update
		fps = str(int(clock.get_fps()))

		if player:
			pos = f"{int(player.x)}X, {int(player.y)}Y"
			pos = pos.strip("'")
		else:
			pos = "Nonexistent"

		if time.time()-fps_update >= 0.5:
			fps_text.content = f"FPS: {fps}"
			fps_update = time.time()
		pos_text.content = f"Pos: {pos}"
		room_text.content = f"Room: {Player.map}"
		projnum_text.content = f"Projs: {len(game_map.full_projs)}"

		top = Height-fps_text.height-pos_text.height-room_text.height-projnum_text.height-5

		win.fblits((
			(fps_text.surf, (6, top)),
			(pos_text.surf, (6, top+fps_text.height)),
			(room_text.surf, (6, top+fps_text.height+pos_text.height)),
			(projnum_text.surf, (6, top+fps_text.height+pos_text.height+room_text.height))
		))

		def show_hitbox():
			def draw(_list):
				for rect in _list:
					if rect == None:
						continue
					elif isinstance(rect, pygame.Rect):
						pygame.draw.rect(win, (0, 255, 0), (rect.x-camera.scroll.x, rect.y-camera.scroll.y, rect.width, rect.height), 1)
					elif isinstance(rect, Polygon):
						rect.draw_poly(win, (0, 255, 0), camera.scroll)
					elif isinstance(rect, OBB):
						rect.draw_obb(win, (0, 255, 0), camera.scroll)
					elif isinstance(rect, list):
						draw(rect)
					elif isinstance(rect, AngleRect):
						pygame.draw.rect(win, (0, 255, 0), (rect.rect.x-camera.scroll.x, rect.rect.y-camera.scroll.y, rect.rect.width, rect.rect.height), 1)
			if player:
				pygame.draw.rect(win, (0, 255, 0), (player.rect.x-camera.scroll.x, player.rect.y-camera.scroll.y, player.rect.width, player.rect.height), 1)
			for rects in rect_list:
				draw(rects)
			
		def show_middle():
			pygame.draw.line(win, (128,128,128), (0, Height*0.5), (Width, Height*0.5))
			pygame.draw.line(win, (128,128,128), (Width*0.5, 0), (Width*0.5, Height))

		def show_eview():
			for enemy in game_map.enemies:
				enemy.sus_view.draw(win, (128, 128, 0), camera.scroll)
				enemy.view.draw(win, (128, 0, 0), camera.scroll)
				pygame.draw.circle(win, (128, 128, 0), (enemy.rect.centerx-camera.scroll.x, enemy.rect.centery-camera.scroll.y), enemy.hearing_radius*player.stealth, 1)

		if show_hitboxes:
			show_hitbox()
		if show_mid:
			show_middle()
		if show_view:
			show_eview()

	def get_text(text_ID):
		i = langs.index(settings["lang"])
		if i >= len(texts_json[text_ID]):
			i = 0
		text = texts_json[text_ID][i]
		
		return text

	def save(player):
		global save_data
		
		try:
			pre_save = load_json(["scripts", "saves", f"save{save_num}.json"])
		except:
			pre_save = {
				"enemies": {},
				"drops": {},
				"dialogues": {}
			}
		
		for loaded_map in maps.values():
			if "enemies" not in pre_save.keys(): pre_save["enemies"] = {}
			pre_save["enemies"][loaded_map.room] = []
			for enemy in loaded_map.full_enemies:
				stats = {
					"health": enemy.stats["HP"],
					"attack": enemy.stats["AP"],
					"defense": enemy.stats["DP"],
					"speed": enemy.stats["SP"],
					"view": enemy.stats["V"],
					"suspicious view": enemy.stats["SV"],
					"hearing radius": enemy.stats["HR"],
					"XP": enemy.stats["XP"],
					"knockback resistence": enemy.knockback_resist,
					"drops": enemy.drops
				}
				pre_save["enemies"][loaded_map.room].append([enemy.x, enemy.y, enemy.name, stats])
			
			if "drops" not in pre_save.keys(): pre_save["drops"] = {}
			pre_save["drops"][loaded_map.room] = []
			for drop in loaded_map.full_drops:
				if isinstance(drop[1], ProjDrop):
					pre_save["drops"][loaded_map.room].append([drop[1].x, drop[1].y, drop[0], "proj", drop[1].name, drop[1].angle])
				elif isinstance(drop[1], Drop):
					pre_save["drops"][loaded_map.room].append([drop[1].x, drop[1].y, drop[0], "normal"])
			
			if "dialogues" not in pre_save.keys(): pre_save["dialogues"] = {}
			pre_save["dialogues"][loaded_map.room] = {"npc": [], "trg": [], "cut": []}
			for npc in loaded_map.full_npcs:
				pre_save["dialogues"][loaded_map.room]["npc"].append([npc.x, npc.y, npc.id])
			for dlg in loaded_map.trg_rects:
				if not dlg[1].triggered:
					pre_save["dialogues"][loaded_map.room]["trg"].append([[dlg[0].x, dlg[0].y, dlg[0].w, dlg[0].h], dlg[1].id])
			for cut in loaded_map.cut_rects:
				if not cut[1].triggered:
					pre_save["dialogues"][loaded_map.room]["cut"].append([[cut[0].x, cut[0].y, cut[0].w, cut[0].h], cut[1].id])

		save_data = {
			"name": player.name,
			"difficulty": difficulty,
			"classes": player.classes,
			"stats": player.stats,
			"available levels": player.available_levels,
			"inventory": player.inventory,
			"equipment": player.equipment,
			"killed enemies": player.killed_enemies,
			"quests": {quest.file_name: quest.current_req for quest in player.quests},
			"map": game_map.room,
			"loc": [player.x, player.y],
			"enemies": pre_save["enemies"],
			"drops": pre_save["drops"],
			"dialogues": pre_save["dialogues"],
		}

		dump_json(["scripts", "saves", f"save{save_num}.json"], save_data)

	def load():
		global difficulty
		
		Player.classes = save_data["classes"]
		Player.name = save_data["name"]
		difficulty = save_data["difficulty"]
		Player.inventory = save_data["inventory"]
		Player.equipment = save_data["equipment"]
		Player.stats = save_data["stats"]
		Player.available_levels = save_data["available levels"]
		Player.killed_enemies = save_data["killed enemies"]
		Player.map = save_data["map"]
		Player.quests = []
		for quest, requirement in save_data["quests"].items():
			Player.quests.append(files[quest].Quest())
			Player.quests[-1].current_req = requirement
		player = Player(0, 0)

		try:
			scroll = camera.scroll
		except NameError:
			scroll = None
				
		player.x, player.y = save_data["loc"]
		player.inv_size = 5 if player.equipment[2] == "No Backpack" else equipment[2][player.equipment[2]]["slots"]
		player.inv_weight = [0, None] if player.equipment[2] == "No Backpack" else [0, equipment[2][player.equipment[2]]["max weight"]]
		if player.inv_weight[1] != None:
			for item in player.inventory:
				player.inv_weight[0] += items[item]["weight"]
		inventory = Inventory(player)
		near_death_surf.set_alpha(math.floor(255-((player.stats["HP"][0]-1)/(player.stats["HP"][1]-1))*255))

		return player, inventory

	def get_control_sprite(key, prioritize):
		if prioritize == "keys":
			if key > 5:
				key = pygame.key.name(key)
				if key.startswith("[") and key.endswith("]"):
					if key[1:-1] == "/":
						key = key.replace("/", "slash",)
					elif key[1:-1] == "*":
						key = key.replace("*", "multiply")
					elif key[1:-1] == "equals":
						key = key.replace("equals", "=")
					key = f"KP_{key[1:-1]}"
				if key == "/":
					key = "slash"
				elif key == "\\":
					key = "backslash"
				elif key == "enter":
					key = "KP_enter"
				elif key == "equals":
					key = "="

				return f"K_{key}"
			else:
				return f"mouse_{key}"
		else:
			if key == 0:
				return "button_a"
			elif key == 1:
				return "button_b"
			elif key == 2:
				return "button_x"
			elif key == 3:
				return "button_y"
			elif key == 4:
				return "button_back"
			elif key == 6:
				return "button_start"
			elif key == 7:
				return "button_lstick"
			elif key == 8:
				return "button_rstick"
			elif key == 9:
				return "lb"
			elif key == 10:
				return "rb"
			elif key == 11:
				return "dpad_up"
			elif key == 12:
				return "dpad_down"
			elif key == 13:
				return "dpad_left"
			elif key == 14:
				return "dpad_right"
			elif key == 15:
				return "lt"
			elif key == 16:
				return "rt"
			else:
				return "asedriuyo"

	def play_music(path: str):
		global music
		music = path

		pygame.mixer_music.load(path)
		pygame.mixer_music.set_volume(settings["volumes"]["music"])
		pygame.mixer_music.play(-1, 0, 1000)

	def pause_time():
		global paused_timers

		if paused_timers == {}:
			player.pause_anim()
			for effect in player.effects:
				effect.pause()
			paused_timers["last time"] = time.time()-last_time
			paused_timers["inv max"] = time.time()-player.inv_max_exceed_time
			paused_timers["dash"] = time.time()-player.dash_cooldown
			paused_timers["shield"] = time.time()-player.shielded[1]
			paused_timers["player i-frame"] = time.time()-player.i_frame

			if player.weapons[0] != [None, None]:
				paused_timers["weapon 1"] = time.time()-player.weapons[0][1].cooldown_time
			if player.weapons[1] != [None, None]:
				paused_timers["weapon 2"] = time.time()-player.weapons[1][1].cooldown_time

			for i, drop in enumerate(game_map.full_drops):
				paused_timers[f"{i}-drop"] = time.time()-drop[2]

			for i, proj in enumerate(game_map.full_projs):
				paused_timers[f"{i}-proj"] = []
				paused_timers[f"{i}-proj"].append(time.time()-proj.shot_time)
				paused_timers[f"{i}-proj"].append(time.time()-proj.ricochet)
			
			for i, enemy in enumerate(game_map.full_enemies):
				enemy.pause_anim()
				paused_timers[f"{i}-enemy"] = []
				paused_timers[f"{i}-enemy"].append(time.time()-enemy.sus_time[0])
				paused_timers[f"{i}-enemy"].append(time.time()-enemy.target_change_timer)
				paused_timers[f"{i}-enemy"].append(time.time()-enemy.i_frame)
				paused_timers[f"{i}-enemy"].append(time.time()-enemy.proj_cooldown)
				for effect in enemy.effects:
					effect.pause()
			
	def unpause_time():
		global paused_timers, last_time

		if paused_timers != {}:
			last_time = time.time()-paused_timers["last time"]
			for effect in player.effects:
				effect.unpause()
			player.inv_max_exceed_time = time.time()-paused_timers["inv max"]
			player.dash_cooldown = time.time()-paused_timers["dash"]
			player.shielded[1] = time.time()-paused_timers["shield"]
			player.i_frame = time.time()-paused_timers["player i-frame"]
			
			if "weapon 1" in paused_timers and player.weapons[0][1] is not None:
				player.weapons[0][1].cooldown_time = time.time()-paused_timers["weapon 1"]
			if "weapon 2" in paused_timers and player.weapons[1][1] is not None:
				player.weapons[1][1].cooldown_time = time.time()-paused_timers["weapon 2"]

			for i, drop in enumerate(game_map.full_drops):
				if f"{i}-drop" in paused_timers:
					drop[2] = time.time()-paused_timers[f"{i}-drop"]
				else:
					break
			
			for i, proj in enumerate(game_map.full_projs):
				if f"{i}-proj" in paused_timers:
					proj.shot_time = time.time()-paused_timers[f"{i}-proj"][0]
					proj.ricochet = time.time()-paused_timers[f"{i}-proj"][1]
				else:
					continue

			for i, enemy in enumerate(game_map.full_enemies):
				if f"{i}-enemy" in paused_timers:
					enemy.unpause_anim()
					enemy.sus_time[0] = time.time()-paused_timers[f"{i}-enemy"][0]
					enemy.target_change_timer = time.time()-paused_timers[f"{i}-enemy"][1]
					enemy.i_frame = time.time()-paused_timers[f"{i}-enemy"][2]
					enemy.proj_cooldown = time.time()-paused_timers[f"{i}-enemy"][3]
					for effect in enemy.effects:
						effect.unpause()
				else:
					break
			
			paused_timers = {}

	def update_setting_texts():
		text_settings.content = get_text("button:settings"); text_settings.language = settings["lang"]
		button_graphics.text_content = get_text("text:graphics"); button_graphics.text_language = settings["lang"]
		button_volume.text_content = get_text("text:volume"); button_volume.text_language = settings["lang"]
		button_controls.text_content = get_text("text:controls"); button_controls.text_language = settings["lang"]
		button_language.text_content = get_text("text:languages"); button_language.text_language = settings["lang"]
		button_settings_back.text_content = get_text("button:back"); button_settings_back.text_language = settings["lang"]

		# graphics
		text_graphics.content = get_text("text:graphics"); text_graphics.language = settings["lang"]
		button_fullscreen.text_content = get_text("button:fullscreen")+get_text(f"status:{'on' if settings['fullscreen'] else 'off'}"); button_fullscreen.text_language = settings["lang"]
		button_vsync.text_content = f"Vsync: {'on' if settings['vsync'] else 'off'}"; button_vsync.text_language = "english"
		slider_fps.text_content = f"{get_text('slider:fps')}{settings['FPS'] if settings['FPS'] < 2**32 else '∞'}"; slider_fps.text_language = settings["lang"]
		slider_brightness.text_content = f"{get_text('slider:brightness')}{round((slider_brightness.width_fill-20)/(slider_brightness.width-20)*100)}%"; slider_brightness.text_language = settings["lang"]

		# volume
		text_volume.content = get_text("text:volume"); text_volume.language = settings["lang"]
		slider_music.text_content = f"{get_text('slider:music')}{int(settings['volumes']['music']*100)}%"; slider_music.text_language = settings["lang"]
		slider_sfx.text_content = f"{get_text('slider:sfx')}{int(settings['volumes']['SFX']*100)}%"; slider_sfx.text_language = settings["lang"]

		# controls
		button_key.text_content = "Keyboard Controls"; button_key.text_language = "english"
		button_con.text_content = "Controller Controls"; button_con.text_language = "english"
		button_connect.text_content = f"{get_text('button:controller')}{get_text('status:connected') if sdl2_controller.get_init() else get_text('status:disconnected')}"; button_connect.text_language = settings["lang"]

		# languages
		text_language.content = get_text("text:languages"); text_language.language = settings["lang"]
		text_currlang.content = lang_dict[settings["lang"]]; text_currlang.language = settings["lang"]

	def update_inv_stats():
		text_hp.content = f"{player.stats['HP'][0]}/{player.stats['HP'][1]}"
		text_sp.content = f"{player.stats['SP'][0]}/{player.stats['SP'][1]}"
		text_ep[0].content = f"{player.stats['EP'][0][0]}/{player.stats['EP'][0][1]}"
		text_ep[1].content = f"{player.stats['EP'][1][0]}/{player.stats['EP'][1][1]}" if player.classes[1] else "No second class"
		text_ap[0].content = f"{'Ranged' if player.classes[0] == 'Archer' else 'Magic' if player.classes[0] == 'Mage' else 'Swing' if player.classes[0] == 'Swordsman' else 'Stab'} Attack: {player.stats['AP'][0]}"
		text_ap[1].content = f"{'Ranged' if player.classes[1] == 'Archer' else 'Magic' if player.classes[1] == 'Mage' else 'Swing' if player.classes[1] == 'Swordsman' else 'Stab'} Attack: {player.stats['AP'][1]}" if player.classes[1] else "You don't have a second class"
		text_dp.content = f"Defense: {player.stats['DP']}"
		text_lp.content = f"{player.stats['XP'][2]} | {player.stats['XP'][0]}/{player.stats['XP'][1]}"
		text_mp.content = f"Money: {player.stats['M']}"
		text_ip.content = f"2%"
		text_cl[0].content = f"Class 1: {player.classes[0]}"
		text_cl[1].content = f"Class 2: {player.classes[1]}" if player.classes[1] else "You don't have a second class"

	def load_stats(save):
		stat_names = []
		for x in range(2):
			if save['classes'][x] == "Archer":
				stat_names.append("p")
			elif save['classes'][x] == "Mage":
				stat_names.append("m")
			elif save['classes'][x] == "Swordsman":
				stat_names.append("v")
			elif save['classes'][x] == "Thief":
				stat_names.append("d")
			else:
				continue
			
		xp_text = Text(os.path.join("assets", "fontsDL", "font.ttf"), f"{save['stats']['XP'][2]}", 13, (255, 255, 255))
		es_text = [Text(os.path.join("assets", "fontsDL", "font.ttf"), f"{save['stats']['EP'][0][0]}", 13, (255, 255, 255))]
		if save["classes"][1]:
			es_text.append(Text(os.path.join("assets", "fontsDL", "font.ttf"), f"{save['stats']['EP'][1][0]}", 13, (255, 255, 255)))

		xp_surf = pygame.Surface(sprite("hf").get_size())
		xp_surf.blits((
			(sprite("le"), (0, 0)),
			(sprite("lf"), (0, int((save['stats']["XP"][1]-save['stats']["XP"][0])/save['stats']["XP"][1]*100/6.25)), (0, int((save['stats']["XP"][1]-save['stats']["XP"][0])/save['stats']["XP"][1]*100/6.25), sprite("hf").get_width(), sprite("hf").get_height()-(int((save['stats']["XP"][1]-save['stats']["XP"][0])/save['stats']["XP"][1]*100/6.5)))),
			(xp_text.surf, (32-xp_text.width*0.5, 8-xp_text.height*0.5))
		))

		c1_surf = pygame.Surface(sprite(f"{stat_names[0]}f").get_size())
		c1_surf.blits((
			(sprite(f"{stat_names[0]}e"), (0, 0)),
			(sprite(f"{stat_names[0]}f"), (0, int((save['stats']["EP"][0][1]-save['stats']["EP"][0][0])/save['stats']["EP"][0][1]*100/6.25)), (0, int((save['stats']["EP"][0][1]-save['stats']["EP"][0][0])/save['stats']["EP"][0][1]*100/6.25), sprite("hf").get_width(), sprite("hf").get_height()-(int((save['stats']["EP"][0][1]-save['stats']["EP"][0][0])/save['stats']["EP"][0][1]*100/6.25)))),
			(es_text[0].surf, (32-es_text[0].width*0.5, 8-es_text[0].height*0.5))
		))
		
		if save['stats']['EP'][1] != [None, None]:
			c2_surf = pygame.Surface(sprite(f"{stat_names[1]}f").get_size())
			c2_surf.blits((
				(sprite(f"{stat_names[1]}e"), (0, 0)),
				(sprite(f"{stat_names[1]}f"), (0, int((save['stats']["EP"][1][1]-save['stats']["EP"][1][0])/save['stats']["EP"][1][1]*100/6.25)), (0, int((save['stats']["EP"][1][1]-save['stats']["EP"][1][0])/save['stats']["EP"][1][1]*100/6.25), sprite("hf").get_width(), sprite("hf").get_height()-(int((save['stats']["EP"][1][1]-save['stats']["EP"][1][0])/save['stats']["EP"][1][1]*100/6.25)))),
				(es_text[1].surf, (32-es_text[1].width*0.5, 8-es_text[1].height*0.5))
			))
		else:
			c2_surf = pygame.Surface((1, 1))

		'''c1_surf = sprite(save["classes"][0].lower())
		if save["classes"][1]:
			c2_surf = sprite(save["classes"][1].lower())
		else:
			c2_surf = pygame.Surface((16, 16))'''

		return xp_surf, c1_surf, c2_surf

	def grab_mods(mod_type):
		global mod_buttons
		
		if mod_type != "addon":
			mod_buttons = [[Button((Width-50-250)*0.5+150, 65, 200, 35, (0, 0, 0), outline=(255, 255, 255)), None, None, Button((Width-50-250)*0.5+329, 79, 16, 16)]]
			
			img = pygame.image.load(os.path.join("assets", "brokenDL.png"))
			text = Text(os.path.join("assets", "fontsDL", "font.ttf"), "Default", 16, (255, 255, 255))
			mod_buttons[0][0].surf.fblits((
				(img, (1, mod_buttons[0][0].height*0.5-img.get_height()*0.5)),
				(text.surf, (5+img.get_width(), mod_buttons[0][0].height*0.5-text.height*0.5))
			))
		else:
			mod_buttons = []

		x = 0
		for mod in os.scandir("mods"):
			if mod.is_dir():
				data = load_json(["mods", mod.name, "data.json"])
				if data["type"] == mod_type:
					mod_buttons.append([Button((Width-50-250)*0.5+150, 115+50*x, 200, 35, (0, 0, 0), outline=(255, 255, 255)), mod.name, data, Button((Width-50-250)*0.5+329, 129+50*x, 16, 16)])
					text = Text(os.path.join("assets", "fontsDL", "font.ttf"), data["name"], 16, (255, 255, 255))
					
					if data["icon"] or len(data["icon"]):
						location = data["icon"][0]
						for location_entry in data["icon"][1:]:
							location = os.path.join(location, location_entry)

						img = pygame.image.load(os.path.join("mods", mod.name, location))
					else:
						img = pygame.Surface((1, 1))

					blits = [
						(img, (1, mod_buttons[-1][0].height*0.5-img.get_height()*0.5)),
						(text.surf, (5+img.get_width(), mod_buttons[-1][0].height*0.5-text.height*0.5))
					]
					if data["info"]:
						blits.append((sprite("info"), (179, 14)))

					mod_buttons[-1][0].surf.fblits(blits)
					x += 1


	inventory_brightness = pygame.Surface((Width, Height))
	inventory_brightness.fill((0, 0, 0))
	inventory_brightness.set_alpha(150)

	brightness = pygame.Surface((Width, Height))
	brightness.fill((0, 0, 0) if settings["brightness"] <= 0 else (255, 255, 255))
	brightness.set_alpha(abs(settings["brightness"]))

	clock = pygame.time.Clock()
	last_time = time.time() # dt

	near_death_surf = pygame.Surface((Width, Height), pygame.SRCALPHA)
	for c in range(96):
		menu_surf = pygame.Surface((Width-c*2, Height-c*2))
		menu_surf.set_colorkey((0, 0, 0))
		pygame.draw.rect(menu_surf, (96-c, 0, 0), (0, 0, menu_surf.get_width(), menu_surf.get_height()), 1)
		menu_surf.set_alpha(96-c)
		near_death_surf.blit(menu_surf, (c, c))
	near_death_surf.set_alpha(0)
	
	save_num = 0
	difficulty = "Normal"

	if not sdl2_controller.get_init():
		controller = FakeController()
	prioritize = "keys"

	equipment = load_json(["scripts", "cacheDL", "equipment.json"])
	items = load_json(["scripts", "cacheDL", "items.json"])
	langs = tuple(load_json(["scripts", "dataDL", "langs.json"]).keys())
	room_data = load_json(["scripts", "cacheDL", "rooms.json"])
	enemies_data = load_json(["scripts", "cacheDL", "enemies.json"])

	current_dialogue = None
	current_cutscene = None
	next_to_door = None
	cutscene_rects = 0
	music = None

	sleep_time = time.time()
	sleep_brightness = [pygame.Surface((Width, Height)), False]
	sleep_brightness[0].fill((0, 0, 0)); sleep_brightness[0].set_alpha(0)

	save_data = None
	target_boss = None
	maps = {}

	last_enemy_killed = None
	reloading = 0

	dialogue_button_index = -1

	bg_num = random.randint(0, 1)
	bg = sprite(f"mbg{bg_num}")
	bg.set_alpha(0)
	update_bg_alpha = time.time()
	backdrop_surf = None

	shadow_surf = pygame.Surface((Width, Height))
	shadow_surf.fill((0, 0, 0))
	shadow_surf.set_alpha(150)

	menu_surf = pygame.Surface((Width-50, Height-50))
	fps_setting_surf = pygame.Surface((200, 35))
	fps_setting_surf.set_alpha(128)


	# main menu
	text_title = Text(os.path.join("assets", "fontsDL", "font.ttf"), "Inseynia", 48, (255, 255, 255))
	button_start = Button(25, 100, 200, 35, (0, 0, 0), get_text("button:start_game"), settings["lang"], (255, 255, 255), (255, 255, 255), 1, os.path.join("assets", "fontsDL", "font.ttf"))
	button_settings = Button(25, 150, 200, 35, (0, 0, 0), get_text("button:settings"), settings["lang"], (255, 255, 255), (255, 255, 255), 1, os.path.join("assets", "fontsDL", "font.ttf"))
	button_mods = Button(25, 200, 200, 35, (0, 0, 0), get_text("button:mods"), settings["lang"], (255, 255, 255), (255, 255, 255), 1, os.path.join("assets", "fontsDL", "font.ttf"))
	button_quit = Button(25, 250, 200, 35, (0, 0, 0), get_text("button:quit_game"), settings["lang"], (255, 255, 255), (255, 255, 255), 1, os.path.join("assets", "fontsDL", "font.ttf"))
	
	text_version = Text(os.path.join("assets", "fontsDL", "font.ttf"), "Pre-Alpha 0.2.1", 16, (75, 75, 75))
	text_cw = Text(os.path.join("assets", "fontsDL", "font.ttf"), "© Texaract", 16, (75, 75, 75))


	# settings menu
	lang_dict = {
		"english": "English",
		"arabic": "العربية",
		"japanese": "にほんご",
		"russian": "Русский",
		"spanish": "Español",
		"french": "Français"
	}

	con_scroll = 0
	key_ids = tuple(settings["keys"].values())
	keys = settings["keys"].copy()
	for name, key in keys.items():
		keys[name] = get_control_sprite(key, 'keys')
	cons = settings["cons"].copy()
	for name, con in cons.items():
		cons[name] = get_control_sprite(con, 'cons')
	currently_choosing = [None, None]
	
	control_warning = False
	mouse_warning = False
	
	title_warning = Text(os.path.join("assets", "fontsDL", "font.ttf"), "Warning", 32, (255, 0, 0), settings["lang"])
	text_cwarning = Text(os.path.join("assets", "fontsDL", "font.ttf"), "2 or more tasks share the same button. It is possible, but not recommended\nPress anything to proceed", 16, (255, 255, 255), settings["lang"], align=pygame.FONT_CENTER)
	text_mwarning = Text(os.path.join("assets", "fontsDL", "font.ttf"), "The mouse button chosen is sadly not supported due to framework limitations\nTry another mouse button\nPress anything to proceed", 16, (255, 255, 255), settings["lang"], align=pygame.FONT_CENTER)
	
	control_warning_surf = pygame.Surface((text_cwarning.width+5, 10+title_warning.height+text_cwarning.height))
	control_warning_surf.fill((255, 255, 255))
	control_warning_surf.fill((0, 0, 0), (1, 1, text_cwarning.width+3, 8+title_warning.height+text_cwarning.height))
	control_warning_surf.fblits((
		(title_warning.surf, (control_warning_surf.get_width()*0.5-title_warning.width*0.5, 0)),
		(text_cwarning.surf, (control_warning_surf.get_width()*0.5-text_cwarning.width*0.5, title_warning.height+5))
	))

	mouse_warning_surf = pygame.Surface((text_mwarning.width+5, 10+title_warning.height+text_mwarning.height))
	mouse_warning_surf.fill((255, 255, 255))
	mouse_warning_surf.fill((0, 0, 0), (1, 1, text_mwarning.width+3, 8+title_warning.height+text_mwarning.height))
	mouse_warning_surf.fblits((
		(title_warning.surf, (mouse_warning_surf.get_width()*0.5-title_warning.width*0.5, 0)),
		(text_mwarning.surf, (mouse_warning_surf.get_width()*0.5-text_mwarning.width*0.5, title_warning.height+5))
	))
	

	#main
	text_settings = Text(os.path.join("assets", "fontsDL", "font.ttf"), get_text("button:settings"), 32, (255, 255, 255), settings["lang"])
	button_graphics = Button(25, 65, 200, 35, (0, 0, 0), get_text("text:graphics"), settings["lang"], (255, 255, 255), (255, 255, 255), 1, os.path.join("assets", "fontsDL", "font.ttf"))
	button_volume = Button(25, 115, 200, 35, (0, 0, 0), get_text("text:volume"), settings["lang"], (255, 255, 255), (255, 255, 255), 1, os.path.join("assets", "fontsDL", "font.ttf"))
	button_controls = Button(25, 165, 200, 35, (0, 0, 0), get_text("text:controls"), settings["lang"], (255, 255, 255), (255, 255, 255), 1, os.path.join("assets", "fontsDL", "font.ttf"))
	button_language = Button(25, 215, 200, 35, (0, 0, 0), get_text("text:languages"), settings["lang"], (255, 255, 255), (255, 255, 255), 1, os.path.join("assets", "fontsDL", "font.ttf"))
	button_settings_back = Button(25, 265, 200, 35, (0, 0, 0), get_text("button:back"), settings["lang"], (255, 255, 255), (255, 255, 255), 1, os.path.join("assets", "fontsDL", "font.ttf"))
	
	# graphics
	text_graphics = Text(os.path.join("assets", "fontsDL", "font.ttf"), get_text("text:graphics"), 32, (255, 255, 255), settings["lang"])
	button_fullscreen = Button((Width-50-250)*0.5+150, 65, 200, 35, (0, 0, 0), get_text("button:fullscreen")+get_text(f"status:{'on' if settings['fullscreen'] else 'off'}"), settings["lang"], (255, 255, 255), (255, 255, 255), 1, os.path.join("assets", "fontsDL", "font.ttf"))
	button_vsync = Button((Width-50-250)*0.5+150, 115, 200, 35, (0, 0, 0), f"Vsync: {'on' if settings['vsync'] else 'off'}", "english", (255, 255, 255), (255, 255, 255), 1, os.path.join("assets", "fontsDL", "font.ttf"))
	slider_fps = Slider((Width-50-250)*0.5+150, 165, 200, 35, (0, 0, 0), 10, 501, [x*5+10 for x in range(100)], width_fill=((settings['FPS']-10)/500)*(200-20)+20 if settings['FPS'] <= 500 else 200, text=f"{get_text('slider:fps')}{settings['FPS'] if settings['FPS'] < 2**32 else '∞'}", text_lang=settings["lang"], outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "font.ttf"))
	slider_brightness = Slider((Width-50-250)*0.5+150, 215, 200, 35, (0, 0, 0), -200, 50, width_fill=int((((settings['brightness']+200)/2.5)/100)*(200-20)+20), text=get_text("slider:brightness"), text_lang=settings["lang"], outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "font.ttf"))
	slider_brightness.text_content = f"{get_text('slider:brightness')}{round((slider_brightness.width_fill-20)/(slider_brightness.width-20)*100)}%"

	# volume
	text_volume = Text(os.path.join("assets", "fontsDL", "font.ttf"), get_text("text:volume"), 32, (255, 255, 255), settings["lang"])
	slider_music = Slider((Width-50-250)*0.5+150, 65, 200, 35, (0, 0, 0), 0, 1, width_fill=settings['volumes']['music']*(200-20)+20, text=f"{get_text('slider:music')}{int(settings['volumes']['music']*100)}%", text_lang=settings["lang"], outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "font.ttf"))
	slider_sfx = Slider((Width-50-250)*0.5+150, 115, 200, 35, (0, 0, 0), 0, 1, width_fill=settings['volumes']['SFX']*(200-20)+20, text=f"{get_text('slider:sfx')}{int(settings['volumes']['SFX']*100)}%", text_lang=settings["lang"], outline=(255,255,255), font_path=os.path.join("assets", "fontsDL", "font.ttf"))

	# controls
	button_key = Button(255, 5, 162, 35, (0, 0, 0), "Keyboard Controls", settings["lang"], (255, 255, 255), (255, 255, 255), 1, os.path.join("assets", "fontsDL", "font.ttf"))
	button_con = Button(422, 5, 162, 35, (0, 0, 0), "Controller Controls", settings["lang"], (255, 255, 255), (255, 255, 255), 1, os.path.join("assets", "fontsDL", "font.ttf"))

	button_connect = Button(255, 55, 330, 35, (0, 0, 0), f"{get_text('button:controller')}{get_text('status:connected') if sdl2_controller.get_init() else get_text('status:disconnected')}", settings["lang"], (255, 255, 255), (255, 255, 255), 1, os.path.join("assets", "fontsDL", "font.ttf"))
	button_invert_sticks = Button(255, 105, 330, 35, (0, 0, 0), "Invert Sticks", "english", (255, 255, 255), (255, 255, 255), 1, os.path.join("assets", "fontsDL", "font.ttf"))
	button_move = Button(255, 155, 330, 35, (0, 0, 0), "Move Around", "english", (128, 128, 128), (128, 128, 128), 1, os.path.join("assets", "fontsDL", "font.ttf"), text_align="left")
	button_aim = Button(255, 189, 330, 35, (0, 0, 0), "Aim", "english", (128, 128, 128), (128, 128, 128), 1, os.path.join("assets", "fontsDL", "font.ttf"), text_align="left")
	button_up = Button(255, 55, 330, 35, (0, 0, 0), "Move Up", "english", (255, 255, 255), (255, 255, 255), 1, os.path.join("assets", "fontsDL", "font.ttf"), text_align="left")
	button_down = Button(255, 89, 330, 35, (0, 0, 0), "Move Down", "english", (255, 255, 255), (255, 255, 255), 1, os.path.join("assets", "fontsDL", "font.ttf"), text_align="left")
	button_left = Button(255, 123, 330, 35, (0, 0, 0), "Move Left", "english", (255, 255, 255), (255, 255, 255), 1, os.path.join("assets", "fontsDL", "font.ttf"), text_align="left")
	button_right = Button(255, 157, 330, 35, (0, 0, 0), "Move Right", "english", (255, 255, 255), (255, 255, 255), 1, os.path.join("assets", "fontsDL", "font.ttf"), text_align="left")
	button_dash = Button(255, 191, 330, 35, (0, 0, 0), "Dash", "english", (255, 255, 255), (255, 255, 255), 1, os.path.join("assets", "fontsDL", "font.ttf"), text_align="left")
	button_sneak = Button(255, 225, 330, 35, (0, 0, 0), "Sneak", "english", (255, 255, 255), (255, 255, 255), 1, os.path.join("assets", "fontsDL", "font.ttf"), text_align="left")
	button_sleep = Button(255, 259, 330, 35, (0, 0, 0), "Sleep & Save", "english", (255, 255, 255), (255, 255, 255), 1, os.path.join("assets", "fontsDL", "font.ttf"), text_align="left")
	button_interact = Button(255, 293, 330, 35, (0, 0, 0), "Interact", "english", (255, 255, 255), (255, 255, 255), 1, os.path.join("assets", "fontsDL", "font.ttf"), text_align="left")
	button_settings_inventory = Button(255, 327, 330, 35, (0, 0, 0), "Inventory", "english", (255, 255, 255), (255, 255, 255), 1, os.path.join("assets", "fontsDL", "font.ttf"), text_align="left")
	button_pause = Button(255, 361, 330, 35, (0, 0, 0), "Pause", "english", (255, 255, 255), (255, 255, 255), 1, os.path.join("assets", "fontsDL", "font.ttf"), text_align="left")
	button_weapon1 = Button(255, 495, 330, 35, (0, 0, 0), "Primary Attack", "english", (255, 255, 255), (255, 255, 255), 1, os.path.join("assets", "fontsDL", "font.ttf"), text_align="left")
	button_weapon2 = Button(255, 529, 330, 35, (0, 0, 0), "Secondry Attack", "english", (255, 255, 255), (255, 255, 255), 1, os.path.join("assets", "fontsDL", "font.ttf"), text_align="left")
	button_sweapon1 = Button(255, 563, 330, 35, (0, 0, 0), "Special Primary Attack", "english", (255, 255, 255), (255, 255, 255), 1, os.path.join("assets", "fontsDL", "font.ttf"), text_align="left")
	button_sweapon2 = Button(255, 597, 330, 35, (0, 0, 0), "Special Secondry Attack", "english", (255, 255, 255), (255, 255, 255), 1, os.path.join("assets", "fontsDL", "font.ttf"), text_align="left")
	
	control_buttons = [[button_up, "up", False, False], [button_down, "down", False, False], [button_left, "left", False, False], [button_right, "right", False, False], [button_dash, "dash", False, False], [button_sneak, "sneak", False, False], [button_sleep, "sleep", False, False], [button_interact, "interact", False, False], [button_settings_inventory, "inventory", False, False], [button_pause, "pause", False, False], [button_weapon1, "primary", False, False], [button_weapon2, "secondary", False, False], [button_sweapon1, "pspecial", False, False], [button_sweapon2, "sspecial", False, False]]


	# languages
	text_language = Text(os.path.join("assets", "fontsDL", "font.ttf"), get_text("text:languages"), 32, (255, 255, 255), settings["lang"])
	text_currlang = Text(os.path.join("assets", "fontsDL", "font.ttf"), lang_dict[settings["lang"]], 16, (255, 255, 255), settings["lang"])
	button_random = Button((Width-50-250)*0.5+250, 90, 1, 1)
	button_prevlang = Button((Width-50-250)*0.5-64+250, 65, 20, 20)
	button_postlang = Button((Width-50-250)*0.5+44+250, 65, 20, 20)

	changing_menu = False


	# Start Game Menu
	save1 = save2 = save3 = None

	text_saves = Text(os.path.join("assets", "fontsDL", "font.ttf"), get_text("text:saves"), 32, (255, 255, 255), settings["lang"])
	button_save1 = Button(25, 100, 200, 50, outline=(255, 255, 255))
	text_save1 = Text(os.path.join("assets", "fontsDL", "font.ttf"), f"{get_text('button:save')} 1", 16, (255, 255, 255), settings["lang"])
	if "save1.json" in os.listdir(os.path.join("scripts", "saves")):
		save1 = load_json(["scripts", "saves", "save1.json"])
		text_save1.content = save1["name"]; text_save1.language = "english"
		button_save1_trash = Button(204, 129, 16, 16)
		save1_xp, save1_c1, save1_c2 = load_stats(save1)

	button_save2 = Button(25, 165, 200, 50, outline=(255, 255, 255))
	text_save2 = Text(os.path.join("assets", "fontsDL", "font.ttf"), f"{get_text('button:save')} 2", 16, (255, 255, 255), settings["lang"])
	if "save2.json" in os.listdir(os.path.join("scripts", "saves")):
		save2 = load_json(["scripts", "saves", "save2.json"])
		text_save2.content = save2["name"]; text_save2.language = "english"
		button_save2_trash = Button(204, 194, 16, 16)
		save2_xp, save2_c1, save2_c2 = load_stats(save2)

	button_save3 = Button(25, 230, 200, 50, outline=(255, 255, 255))
	text_save3 = Text(os.path.join("assets", "fontsDL", "font.ttf"), f"{get_text('button:save')} 3", 16, (255, 255, 255), settings["lang"])
	if "save3.json" in os.listdir(os.path.join("scripts", "saves")):
		save3 = load_json(["scripts", "saves", "save3.json"])
		text_save3.content = save3["name"]; text_save3.language = "english"
		button_save3_trash = Button(204, 259, 16, 16)
		save3_xp, save3_c1, save3_c2 = load_stats(save3)
	button_start_back = Button(25, 295, 200, 35, (0, 0, 0), get_text("button:back"), settings["lang"], (255, 255, 255), (255, 255, 255), 1, os.path.join("assets", "fontsDL", "font.ttf"))


	# New Save Menu
	difficulties = ["Easy", "Normal", "Hard", "Permadeath"]
	newsave_player_class = None
	newsave_name = None
	newsave_diff = difficulties[0]

	text_newsave = Text(os.path.join("assets", "fontsDL", "font.ttf"), f"{get_text('button:save')} save_num", 32, (255, 255, 255), settings["lang"])

	# classes
	button_archer = Button(35, 65, 100, 100, outline=(255, 255, 255))
	text_archer = Text(os.path.join("assets", "fontsDL", "font.ttf"), "Archer", 16, (255, 255, 255))
	button_mage = Button(35*2+100, 65, 100, 100, outline=(255, 255, 255))
	text_mage = Text(os.path.join("assets", "fontsDL", "font.ttf"), "Mage", 16, (255, 255, 255))
	button_swordsman = Button(35*3+200, 65, 100, 100, outline=(255, 255, 255))
	text_swordsman = Text(os.path.join("assets", "fontsDL", "font.ttf"), "Swordsman", 16, (255, 255, 255))
	button_thief = Button(35*4+300, 65, 100, 100, outline=(255, 255, 255))
	text_thief = Text(os.path.join("assets", "fontsDL", "font.ttf"), "Thief", 16, (255, 255, 255))

	# name
	textbox_name = Textbox(menu_surf.get_width()*0.5-100, 180, 200, 35, pre_text="Name", outline=(255, 255, 255), font_path=os.path.join("assets", "fontsDL", "font.ttf"), change_width=False, clear_text_when_click=True)

	# difficulty
	text_currdiff = Text(os.path.join("assets", "fontsDL", "font.ttf"), difficulties[0], 16, (255, 255, 255))
	button_prevdiff = Button(menu_surf.get_width()*0.5-70, 230, 20, 20)
	button_postdiff = Button(menu_surf.get_width()*0.5+50, 230, 20, 20)
	button_random = Button((Width-50)*0.5, 232+text_currdiff.height*0.5, 1, 1)

	button_start_newsave = Button(menu_surf.get_width()*0.5-105, Height-95, 100, 35, (0, 0, 0), "start", settings["lang"], (255, 255, 255), (255, 255, 255), 1, os.path.join("assets", "fontsDL", "font.ttf"))
	button_newsave_back = Button(menu_surf.get_width()*0.5+5, Height-95, 100, 35, (0, 0, 0), get_text("button:back"), settings["lang"], (255, 255, 255), (255, 255, 255), 1, os.path.join("assets", "fontsDL", "font.ttf"))


	# Inventory, Stats, Map, Quests, and Bestiary menus
	button_inventory = Button(10, 5, 116, 25, (0, 0, 0), "Inventory", "english", outline=(255, 255, 255), font_path=os.path.join("assets", "fontsDL", "font.ttf"))
	button_stats = Button(136, 5, 116, 25, (0, 0, 0), "Stats", "english", outline=(255, 255, 255), font_path=os.path.join("assets", "fontsDL", "font.ttf"))
	button_map = Button(262, 5, 116, 25, (0, 0, 0), "Map", "english", outline=(255, 255, 255), font_path=os.path.join("assets", "fontsDL", "font.ttf"))
	button_quests = Button(388, 5, 116, 25, (0, 0, 0), "Quests", "english", outline=(255, 255, 255), font_path=os.path.join("assets", "fontsDL", "font.ttf"))
	button_bestiary = Button(514, 5, 116, 25, (0, 0, 0), "Bestiary", "english", outline=(255, 255, 255), font_path=os.path.join("assets", "fontsDL", "font.ttf"))

	button_level = Button(Width*0.5-100, Height-40, 200, 35, (0, 0, 0), f"Level Up (player_level)", outline=(255, 255, 255), font_path=os.path.join("assets", "fontsDL", "font.ttf"))
	text_hp = Text(os.path.join("assets", "fontsDL", "font.ttf"), f"player_hp", 16, (255, 255, 255))
	text_sp = Text(os.path.join("assets", "fontsDL", "font.ttf"), f"player_sp", 16, (255, 255, 255))
	text_ep = [Text(os.path.join("assets", "fontsDL", "font.ttf"), f"player_ep1", 16, (255, 255, 255)), Text(os.path.join("assets", "fontsDL", "font.ttf"), "No second class", 16, (255, 255, 255))]
	text_ap = [Text(os.path.join("assets", "fontsDL", "font.ttf"), f"player_ap1", 16, (255, 255, 255)), Text(os.path.join("assets", "fontsDL", "font.ttf"), "You don't have a second class", 16, (255, 255, 255))]
	text_dp = Text(os.path.join("assets", "fontsDL", "font.ttf"), f"player_df", 16, (255, 255, 255))
	text_lp = Text(os.path.join("assets", "fontsDL", "font.ttf"), f"player_xp", 16, (255, 255, 255))
	text_mp = Text(os.path.join("assets", "fontsDL", "font.ttf"), f"player_mp", 16, (255, 255, 255))
	text_ip = Text(os.path.join("assets", "fontsDL", "font.ttf"), f"2%", 16, (255, 255, 255))
	text_cl = [Text(os.path.join("assets", "fontsDL", "font.ttf"), f"player_cl1", 16, (255, 255, 255)), Text(os.path.join("assets", "fontsDL", "font.ttf"), "You don't have a second class", 16, (255, 255, 255))]

	button_hp = Button(Width*0.5-220, 50, 200, 25)
	button_sp = Button(Width*0.5-220, 75, 200, 25)
	button_ep1 = Button(Width*0.5-220, 100, 200, 25)
	button_ep2 = Button(Width*0.5-220, 125, 200, 25)
	button_ap1 = Button(Width*0.5+45, 50, text_ap[0].width, text_ap[0].height)
	button_ap2 = Button(Width*0.5+45, 75, text_ap[1].width, text_ap[1].height)
	button_dp = Button(Width*0.5+45, 100, text_dp.width, text_dp.height)

	bar = pygame.Surface((200, 25))
	pygame.draw.rect(bar, (255, 255, 255), (1, 1, 198, 23))
	pygame.draw.rect(bar, (150, 0, 0), (2, 2, 196, 21))

	text_map = Text(os.path.join("assets", "fontsDL", "font.ttf"), f"Map coming soon! :) (I have no clue how I would implement it :( )", 16, (255, 255, 255))
	text_quest = Text(os.path.join("assets", "fontsDL", "font.ttf"), f"You have no quests", 16, (255, 255, 255))

	inv_scroll = 0
	quests = []
	bestiary_buttons = []
	bestiary_imgs = {}

	button_inv_back = Button(Width*0.5-100, Height-40, 200, 35, (0, 0, 0), "Back", outline=(255, 255, 255), font_path=os.path.join("assets", "fontsDL", "font.ttf"))

	quemy_info_surf = pygame.Surface((Width-10, Height-130))
	quemy_info_surf.fill((255, 255, 255))
	quemy_info_surf.fill((0, 0, 0), (1, 1, Width-12, Height-132))

	chosen_quest = []
	leveling = False
	level_alpha = 255
	alpha_counter = 0
	chosen_enemy = None


	# Pause Menu
	pause_surf = pygame.Surface((228, 150))

	text_pause = Text(os.path.join("assets", "fontsDL", "font.ttf"), get_text("text:paused"), 32, (255, 255, 255), settings["lang"])
	button_resume = Button(14, 42, 200, 25, (0, 0, 0), get_text("button:resume_game"), text_lang=settings["lang"], outline=(255, 255, 255), font_path=os.path.join("assets", "fontsDL", "font.ttf"))
	button_pause_settings = Button(14, 72, 200, 25, (0, 0, 0), get_text("button:settings"), text_lang=settings["lang"], outline=(255, 255, 255), font_path=os.path.join("assets", "fontsDL", "font.ttf"))
	button_pause_quit = Button(14, 103, 200, 25, (0, 0, 0), get_text("button:quit_game"), text_lang=settings["lang"], outline=(255, 255, 255), font_path=os.path.join("assets", "fontsDL", "font.ttf"))


	# Mods
	text_mods = Text(os.path.join("assets", "fontsDL", "font.ttf"), "Mods", 32, (255, 255, 255), settings["lang"])
	button_assets = Button(25, 65, 200, 35, (0, 0, 0), "Asset Packs", settings["lang"], (255, 255, 255), (255, 255, 255), 1, os.path.join("assets", "fontsDL", "font.ttf"))
	button_behavior = Button(25, 115, 200, 35, (0, 0, 0), "Behavior Packs", settings["lang"], (255, 255, 255), (255, 255, 255), 1, os.path.join("assets", "fontsDL", "font.ttf"))
	button_addons = Button(25, 165, 200, 35, (0, 0, 0), "Add-ons", settings["lang"], (255, 255, 255), (255, 255, 255), 1, os.path.join("assets", "fontsDL", "font.ttf"))
	button_mods_back = Button(25, 265, 200, 35, (0, 0, 0), get_text("button:back"), settings["lang"], (255, 255, 255), (255, 255, 255), 1, os.path.join("assets", "fontsDL", "font.ttf"))
	button_info_back = Button((Width-50)*0.5-100, Height-100, 200, 35, (0, 0, 0), get_text("button:back"), settings["lang"], (255, 255, 255), (255, 255, 255), 1, os.path.join("assets", "fontsDL", "font.ttf"))

	texts = {
		"asset": Text(os.path.join("assets", "fontsDL", "font.ttf"), "Asset Packs", 32, (255, 255, 255), settings["lang"]),
		"behavior": Text(os.path.join("assets", "fontsDL", "font.ttf"), "Behavior Packs", 32, (255, 255, 255), settings["lang"]),
		"addon": Text(os.path.join("assets", "fontsDL", "font.ttf"), "Add-ons", 32, (255, 255, 255), settings["lang"])
	}

	buttons = [button_assets, button_behavior, button_addons, button_mods_back]
	main_buttons = [button_assets, button_behavior, button_addons, button_mods_back]
	mod_buttons = []

	starting_mods = load_json(["mods", "loaded_mods.json"])
	loaded_mods = starting_mods.copy()
	mod_info = False


	# Music Room
	if platform.system() == "Windows":
		splitter = "\\"
	else:
		splitter = "/"

	musics = []
	text_widths = []
	for file in os.listdir(os.path.join("assets", "SOUND", "music")):
		musics.append(os.path.join("assets", "SOUND", "music", file))
		text_widths.append(Text(os.path.join("assets", "fontsDL", "font.ttf"), file[:-4], 16, (255, 255, 255)).width)
	text_width = max(text_widths)

	text_musicroom = Text(os.path.join("assets", "fontsDL", "font.ttf"), "Music Room", 32, (255, 255, 255))
	text_music = Text(os.path.join("assets", "fontsDL", "font.ttf"), musics[0].split(splitter)[-1][:-4], 16, (255, 255, 255))
	button_prevmus = Button(Width*0.5-text_width*0.5-30, 82, 20, 20)
	button_postmus = Button(Width*0.5+text_width*0.5+10, 82, 20, 20)
	button_mus_back = Button(Width*0.5-100, Height-50, 200, 35, (0, 0, 0), get_text("button:back"), settings["lang"], (255, 255, 255), (255, 255, 255), 1, os.path.join("assets", "fontsDL", "font.ttf"))

	menus = ["main"]
	sub_menu = None
	main_buttons = []
	buttons = [button_start, button_settings, button_mods, button_quit]
	default_menu_buttons = {
		"main": [button_start, button_settings, button_mods, button_quit],
		"settings": [button_graphics, button_volume, button_controls, button_language, button_settings_back],
		"start": [button_save1, button_save2, button_save3, button_start_back],
		"save": [[button_archer, button_mage, button_swordsman, button_thief], [textbox_name], [button_random], [button_start_newsave, button_newsave_back]],
		"inv": [],
		"pause": [button_resume, button_pause_settings, button_pause_quit],
		"mods": [button_assets, button_behavior, button_addons, button_mods_back],
		"music": []
	}
	chosen_button = -1
	chosen_button_group = -1
	post_arrow_surf = pygame.Surface((21, 21))
	pygame.draw.polygon(post_arrow_surf, (255, 255, 255), ((0, 0), (0, 20), (20, 10)))
	pre_arrow_surf = pygame.transform.flip(post_arrow_surf, True, False)

	while 1:
		clock.tick(settings["FPS"])
		mp = pygame.mouse.get_pos()
		dt, last_time = delta_time()

		if not len(menus):
			bosses = [player]

			game_map.load_tiles(camera.scroll, player)
			game_map.enemies = []; game_map.drops = []; game_map.projs = []; game_map.npcs = []
			
			if dt >= 10:
				dt = 0

			if player.sleep[1]:
				save(player)
				player.sleep[1] = False
			if player.sleep[0]:
				if sleep_brightness[0].get_alpha() < 255 and not sleep_brightness[1]:
					sleep_brightness[0].set_alpha(sleep_brightness[0].get_alpha()+10*dt)
					sleep_time = time.time()
				elif sleep_brightness[0].get_alpha() >= 255 and not sleep_brightness[1]:
					sleep_brightness[1] = True
					sleep_brightness[0].set_alpha(255)

				if sleep_brightness[0].get_alpha() > 0 and sleep_brightness[1] and time.time()-sleep_time >= 1:
					player.stats["SP"][0] = player.stats["SP"][1]
					player.stats["HP"][0] = player.stats["HP"][1]
					if "Mage" in player.classes:
						mi = player.classes.index("Mage")
						player.stats["EP"][mi][0] = player.stats["EP"][mi][1]

					sleep_brightness[0].set_alpha(sleep_brightness[0].get_alpha()-10*dt)
				elif sleep_brightness[0].get_alpha() <= 3 and sleep_brightness[1]:
					player.sleep[0] = False
					player.sleep[1] = True
					player.sleep_stamina = time.time()
					player.sleep_affect = 0
					sleep_brightness[0].set_alpha(0)
					sleep_brightness[1] = False

			if True in pygame.key.get_pressed()+pygame.mouse.get_pressed(5):
				prioritize = "keys"
			elif not isinstance(controller, FakeController):
				for i in range(15):
					if controller.get_button(i):
						prioritize = "cons"
						break
				else:
					if abs(controller.get_axis(pygame.CONTROLLER_AXIS_LEFTX)/32767) >= 0.1 or abs(controller.get_axis(pygame.CONTROLLER_AXIS_LEFTY)/32767) >= 0.1 or abs(controller.get_axis(pygame.CONTROLLER_AXIS_RIGHTX)/32767) >= 0.1 or abs(controller.get_axis(pygame.CONTROLLER_AXIS_RIGHTX)/32767) >= 0.1 or abs(controller.get_axis(pygame.CONTROLLER_AXIS_TRIGGERLEFT)/32767) >= 0.1 or abs(controller.get_axis(pygame.CONTROLLER_AXIS_TRIGGERRIGHT)/32767) >= 0.1:
						prioritize = "cons"


			# action
			if not current_dialogue and not current_cutscene:
				#player.regen()
				for effect in player.effects:
					effect.affect()
				if not True in player.sleep:
					player.move(game_map, dt, settings, prioritize, controller)
				player.attack(game_map.enemies, mp, settings, prioritize, controller, camera.scroll, game_map.full_projs, difficulty)
				player.xp()
				if player.stats["HP"][0] <= 0:
					menus = ["main"]
					'''player, inventory = load()
					maps = {}
					current_dialogue = None
					current_cutscene = None
					camera = Camera([player.rect.centerx+Width*0.5, player.rect.centery+Height*0.5], player, True)
					maps[save_data["map"]] = TileMap(save_data["map"], save_data)
					game_map = maps[save_data["map"]]
					camera.update([Width, Height], dt, game_map)
					camera.immediate = False
					near_death_surf.set_alpha(0)'''

			for dlg in game_map.trg_rects:
				if player.rect.colliderect(dlg[0]) and not dlg[1].triggered:
					current_dialogue = dlg[1]
					player.vel = pygame.Vector2(0, 0)

			for cut in game_map.cut_rects:
				if player.rect.colliderect(cut[0]) and not cut[1].triggered:
					current_cutscene = cut[1]
					player.vel = pygame.Vector2(0, 0)
			
			for enemy in reversed(game_map.full_enemies):
				for effect in enemy.effects:
					effect.affect()
				if enemy.rect.colliderect(camera.scroll):
					game_map.enemies.append(enemy)
				enemy.dmg_counter_log(dt)

				if not current_dialogue and not current_cutscene:
					if (enemy.type == "boss" and enemy.active) or enemy in game_map.enemies:
						if enemy.type == "boss" and not enemy.active and enemy in game_map.enemies:
							enemy.active = True
						if enemy.type == "boss" and enemy.active:
							bosses.append(enemy)
						enemy.ai(game_map, player, dt, difficulty)

			for drop in game_map.full_drops:
				if drop[1].rect.colliderect(camera.scroll):
					game_map.drops.append(drop)
					
					drop[3] = time.time()

					if isinstance(drop[1], Spirit) and "Mage" in player.classes:
						if drop[1].move(player, dt) and drop in game_map.full_drops:
							game_map.full_drops.remove(drop)

					if drop[1].rect.colliderect(player.rect) and time.time()-drop[2] >= 3 and drop in game_map.drops:
						if inventory.pick_item(drop[0], drop[1]) and not isinstance(drop[1], Spirit) and drop in game_map.full_drops:
							game_map.full_drops.remove(drop)

			for npc in game_map.full_npcs:
				if npc.rect.colliderect(camera.scroll):
					game_map.npcs.append(npc)
				
					npc.move(game_map, dt)

			for proj in game_map.full_projs:
				proj.despawn(game_map)

				if proj.rect.colliderect(camera.scroll):
					game_map.projs.append(proj)
					
				if not current_dialogue and not current_cutscene:
					proj.move(game_map, dt, camera.scroll, mp, game_map.enemies+game_map.npcs+[player], player)
					entity_health, entity = proj.damage(game_map, game_map.enemies+game_map.npcs+[player])
					if entity:
						if entity_health <= 0:
							if entity != player:
								if entity in game_map.full_enemies:
									for drop in entity.drops:
										game_map.full_drops.append([drop, Drop(random.randint(entity.rect.centerx-50, entity.rect.centerx+50), random.randint(entity.rect.centery-50, entity.rect.centery+50), sprite(drop)), 0, time.time()])
									game_map.full_enemies.remove(entity)
									target_boss = None
								elif entity in game_map.full_npcs and proj.shooter == player:
									game_map.full_npcs.remove(entity)

								last_enemy_killed = entity

								if "Mage" in player.classes:
									game_map.full_drops.append(["spirit", Spirit(entity.rect.centerx-6, entity.rect.centery-8, sprite("Spirit")), 0, time.time()])
								if proj.shooter == player:
									player.stats["XP"][0] += entity.stats["XP"]
						else:
							if entity in game_map.enemies and entity.type == "boss":
								target_boss = entity

							if entity in game_map.npcs and entity.anger_attack and proj.shooter == player:
								game_map.full_enemies.append(enemy_list[entity.name]["AI"].AI(entity.x, entity.y, enemy_list[entity.name]["Anim"], entity.stats, entity.name))
								game_map.full_enemies[-1].damage_counters = entity.damage_counters

								current_dialogue = entity.anger_dialogue
								if entity in game_map.full_npcs:
									game_map.full_npcs.remove(entity)

						if proj.shooter == player:
							player.power_gauge += 1
							player.killed_enemies.append(entity.name)

			
			for connector in game_map.connectors:
				if connector[0].colliderect(player.door_rect) and len(bosses) == 1:
					next_to_door = connector
					break
			else:
				next_to_door = None

			for mod_loop in mod_loops:
				mod_loop()

			for quest in player.quests:
				quest.check(game_map, current_dialogue, player, last_enemy_killed)

			for entity in game_map.enemies+game_map.npcs+game_map.projs+[player]:
				tile = entity.tile_collision(game_map.tiles | game_map.bgs)
				if tile: tile.special(entity)

			# drawing
			win.fill((0, 0, 0))
			if reloading == False: game_map.draw_map(camera.main_display, player, camera.scroll)


			# event
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit(); sys.exit()

				if event.type == pygame.WINDOWLEAVE:
					menus = ["pause"]
					buttons = default_menu_buttons[menus[-1]]
					backdrop_surf = camera.display.copy()

				if event.type == pygame.KEYDOWN:
					# Debug
					if event.key == pygame.K_F11:
						pygame.display.toggle_fullscreen()
					
					elif event.key == pygame.K_F3:
						debug_menu = not debug_menu
					elif event.key == pygame.K_b and debug_menu:
						show_hitboxes = not show_hitboxes
					elif event.key == pygame.K_m and debug_menu:
						show_mid = not show_mid
					elif event.key == pygame.K_n and debug_menu:
						show_view = not show_view
					elif event.key == pygame.K_v and debug_menu:
						show_active_rects = not show_active_rects

					# Dialogue
					else:
						if current_dialogue:
							text_data = current_dialogue.get_data(settings["lang"])
							if current_dialogue.next_index(settings["lang"], player) and not len(text_data[4]):
								current_dialogue.text_portion = 0
								if len(current_dialogue.previous_id):
									current_dialogue.id = current_dialogue.previous_id[0][0]
								current_dialogue.triggered = True
								current_dialogue = None
								if current_cutscene:
									current_cutscene._next_frame("dialogue")
									current_cutscene.dialogue = False
									current_cutscene.dialogue_num += 1
								else:
									unpause_time()
							elif len(text_data[4]):
								if event.key in [pygame.K_a, pygame.K_LEFT]:
									if dialogue_button_index == -1:
										dialogue_button_index = 0
									else:
										if dialogue_button_index == 0:
											dialogue_button_index = len(text_data[4])-1
										else:
											dialogue_button_index -= 1
									pygame.mouse.set_pos(text_data[4][dialogue_button_index][0].x+text_data[4][dialogue_button_index][0].width*0.5, text_data[4][dialogue_button_index][0].y+text_data[4][dialogue_button_index][0].height*0.5)
								elif event.key in [pygame.K_d, pygame.K_RIGHT]:
									if dialogue_button_index == -1:
										dialogue_button_index = 0
									else:
										if dialogue_button_index == len(text_data[4])-1:
											dialogue_button_index = 0
										else:
											dialogue_button_index += 1
									pygame.mouse.set_pos(text_data[4][dialogue_button_index][0].x+text_data[4][dialogue_button_index][0].width*0.5, text_data[4][dialogue_button_index][0].y+text_data[4][dialogue_button_index][0].height*0.5)
								elif event.key in [pygame.K_RETURN, pygame.K_SPACE, pygame.K_KP_ENTER]:
									if current_dialogue.button_press(mp, settings["lang"], player):
										current_dialogue.text_portion = 0
										if len(current_dialogue.previous_id):
											current_dialogue.id = current_dialogue.previous_id[0][0]
										current_dialogue.triggered = True
										current_dialogue = None
										if current_cutscene:
											current_cutscene._next_frame("dialogue")
											current_cutscene.dialogue = False
											current_cutscene.dialogue_num += 1

					# Testing Only
					if event.key == pygame.K_p:
						game_map.full_enemies.append(AI(player.x+100, player.y, os.path.join("assets", "ANIMATIONSDL", "Ekreta Tree"), enemies_data["Ekreta Tree"], "Ekreta"))

				if event.type == pygame.CONTROLLERDEVICEREMOVED:
					controller = FakeController()
					sdl2_controller.quit()
					menus = ["pause"]
					buttons = default_menu_buttons[menus[-1]]
					backdrop_surf = camera.display.copy()
				
				if event.type == pygame.CONTROLLERDEVICEADDED and not sdl2_controller.get_init():
					sdl2_controller.init()
					controller = sdl2_controller.Controller(0)

				if event.type == pygame.CONTROLLERBUTTONDOWN:
					if current_dialogue:
						text_data = current_dialogue.get_data(settings["lang"])
						if current_dialogue.next_index(settings["lang"], player) and not len(text_data[4]):
							current_dialogue.text_portion = 0
							if len(current_dialogue.previous_id):
								current_dialogue.id = current_dialogue.previous_id[0][0]
							current_dialogue.triggered = True
							current_dialogue = None
							if current_cutscene:
								current_cutscene._next_frame("dialogue")
								current_cutscene.dialogue = False
								current_cutscene.dialogue_num += 1
						elif len(text_data[4]):
							if event.button == pygame.CONTROLLER_BUTTON_DPAD_LEFT:
								if dialogue_button_index == -1:
									dialogue_button_index = 0
								else:
									if dialogue_button_index == 0:
										dialogue_button_index = len(text_data[4])-1
									else:
										dialogue_button_index -= 1
								pygame.mouse.set_pos(text_data[4][dialogue_button_index][0].x+text_data[4][dialogue_button_index][0].width*0.5, text_data[4][dialogue_button_index][0].y+text_data[4][dialogue_button_index][0].height*0.5)
							elif event.button == pygame.CONTROLLER_BUTTON_DPAD_RIGHT:
								if dialogue_button_index == -1:
									dialogue_button_index = 0
								else:
									if dialogue_button_index == len(text_data[4])-1:
										dialogue_button_index = 0
									else:
										dialogue_button_index += 1
								pygame.mouse.set_pos(text_data[4][dialogue_button_index][0].x+text_data[4][dialogue_button_index][0].width*0.5, text_data[4][dialogue_button_index][0].y+text_data[4][dialogue_button_index][0].height*0.5)
							elif event.button == pygame.CONTROLLER_BUTTON_A:
								if current_dialogue.button_press(mp, settings["lang"], player):
									current_dialogue.text_portion = 0
									if len(current_dialogue.previous_id):
										current_dialogue.id = current_dialogue.previous_id[0][0]
									current_dialogue.triggered = True
									current_dialogue = None
									if current_cutscene:
										current_cutscene._next_frame("dialogue")
										current_cutscene.dialogue = False
										current_cutscene.dialogue_num += 1
								

				if event.type == pygame.MOUSEBUTTONDOWN and current_dialogue:
					if event.button == 1:
						if current_dialogue.button_press(mp, settings["lang"], player):
							current_dialogue.text_portion = 0
							if len(current_dialogue.previous_id):
								current_dialogue.id = current_dialogue.previous_id[0][0]
							current_dialogue.triggered = True
							current_dialogue = None
							if current_cutscene:
								current_cutscene._next_frame("dialogue")
								current_cutscene.dialogue = False
								current_cutscene.dialogue_num += 1
						
				if event.type == pygame.MOUSEBUTTONUP:
					if player.equipment[1] in equipment[1].keys() and event.button == 3:
						player.shielded = [None, 0]

				if event.type == pygame.CONTROLLERAXISMOTION:
					if not settings["sticks invert"]:
						stickx = pygame.CONTROLLER_AXIS_RIGHTX
						sticky = pygame.CONTROLLER_AXIS_RIGHTY
					else:
						stickx = pygame.CONTROLLER_AXIS_LEFTX
						sticky = pygame.CONTROLLER_AXIS_LEFTY
					if event.axis in [stickx, sticky]:
						x = (controller.get_axis(stickx)/32767*100)+(player.rect.centerx)-camera.scroll.x
						y = (controller.get_axis(sticky)/32767*100)+(player.rect.centery)-camera.scroll.y

						if x <= 1:
							x = 1
						elif x >= 639:
							x = 639
						if y <= 1:
							y = 1
						elif y >= 359:
							y = 359
						pygame.mouse.set_pos((x, y))

					if player.equipment[1] in equipment[1].keys() and event.axis == pygame.CONTROLLER_AXIS_TRIGGERRIGHT and event.value/32767 < 0.5:
						player.shielded = [None, 0]


			# Controls
			if game_input.press(settings[prioritize]["inventory"], prioritize, controller) and not player.sleep[0] and [current_dialogue, current_cutscene] == [None, None]:
				player_quests = player.quests.copy()
				player_quests.sort(key=lambda quest: quest.completed)
				for i, quest in enumerate(player_quests):
					if quest.completed:
						quests.append(Button(Width*0.5-200, 40+50*i, 400, 35, (0, 0, 0), quest.data["title"][langs.index(settings["lang"])], text_color=(128, 128, 128), outline=(128, 128, 128), font_path=os.path.join("assets", "fontsDL", "font.ttf")))
					else:
						quests.append(Button(Width*0.5-200, 40+50*i, 400, 35, (0, 0, 0), quest.data["title"][langs.index(settings["lang"])], outline=(255, 255, 255), font_path=os.path.join("assets", "fontsDL", "font.ttf")))
				
				y = 0
				null_enemies = 0
				for x, data in enumerate(enemies_data.items()):
					if data[1]["bestiary"]:
						x -= null_enemies					
						if x % 14 == 0 and x > 0:
							y += 1
						bestiary_buttons.append(Button((x-y*10)*40+40, y*40+40, 36, 36, (0, 0, 0), data[0], font_path=os.path.join("assets", "fontsDL", "font.ttf"), change_width=False))

						img = sprite("Inventory Slot").copy()
						if player.killed_enemies.count(data[0]):
							img.blit(sprite(f"bestiary_{data[0]}"), (2, 2))
						else:
							img.blit(sprite("bestiary_unknown"), (2, 2))
						bestiary_imgs[data[0]] = img
					else:
						null_enemies += 1
						
				update_inv_stats()
				button_level.text_content = f"Level Up ({player.available_levels})"
				backdrop_surf = camera.display.copy()
				sub_menu = "inv"
				main_buttons = [button_inventory, button_stats, button_map, button_quests, button_bestiary]
				pause_time()
				inventory.index = 6
				menus = ["inv"]

			if game_input.press(settings[prioritize]["pause"], prioritize, controller) and not player.sleep[0] and [current_dialogue, current_cutscene] == [None, None]:
				menus = ["pause"]
				buttons = default_menu_buttons[menus[-1]]
				backdrop_surf = camera.display.copy()

			if game_input.press(settings[prioritize]["sleep"], prioritize, controller) and not player.sleep[0] and [current_dialogue, current_cutscene] == [None, None]:
				player.check_sleep(game_map.enemies)

			if game_input.press(settings[prioritize]["interact"], prioritize, controller) and not player.sleep[0] and [current_dialogue, current_cutscene] == [None, None]:
				if next_to_door:
					player.x = next_to_door[2]
					player.y = next_to_door[3]
					camera.immediate = True
					camera.update((Width, Height), dt, game_map)
					camera.immediate = False

					if next_to_door[1] not in maps:
						maps[next_to_door[1]] = TileMap(next_to_door[1], save_data)
					game_map = maps[next_to_door[1]]

				else:
					for npc in game_map.npcs:
						if npc.trigger_dialogue(player):
							current_dialogue = npc.dialogue
							player.vel = pygame.Vector2(0, 0)
							break

			if game_input.press(settings[prioritize]["sneak"], prioritize, controller) and not player.sleep[0] and [current_dialogue, current_cutscene] == [None, None]:
				player.sneak = not player.sneak
				if player.sneak:
					player.stealth = 0.1
				else:
					if "Thief" in player.classes:
						player.stealth = 1
					else:
						player.stealth = 2

			if current_dialogue:
				for button in current_dialogue.get_data(settings["lang"])[4]:
					button[0].outline = (255, 255, 255)
					if button[0].rect.collidepoint(mp):
						button[0].outline = (255, 128, 0)

			if len(bosses) > 1:
				try:
					if bosses[1].music and music != bosses[1].music:
						play_music(bosses[1].music)
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
				if room_data[game_map.room]["music"]:
					if music != room_data[game_map.room]["music"]:
						play_music(room_data[game_map.room]["music"])
				else:
					pygame.mixer.music.stop()
				camera.forced_loc = []

			camera.update((Width, Height), dt, game_map)

			# UI
			if not target_boss and len(bosses) > 1:
				target_boss = random.choice(bosses[1:])

			if player.cached_stats["HP"] != player.stats["HP"]:
				near_death_surf.set_alpha(math.floor(255-((player.stats["HP"][0]-1)/(player.stats["HP"][1]-1))*255))
			camera.display.blit(near_death_surf, (0, 0))
			
			[enemy.draw_UI(camera.display, camera.scroll, True) if enemy == target_boss else enemy.draw_UI(camera.display, camera.scroll) for enemy in game_map.enemies]
			[npc.draw_UI(camera.display, camera.scroll) for npc in game_map.npcs]
			ui_return1 = player.draw_UI(camera.display, game_map, camera.scroll)

			if current_cutscene:
				pause_time()
				if cutscene_rects < 50:
					cutscene_rects += 2*dt
				pygame.draw.rect(camera.display, (0, 0, 0), (0, cutscene_rects-50, Width, 50))
				pygame.draw.rect(camera.display, (0, 0, 0), (0, Height-cutscene_rects+1, Width, 50))
				returned = current_cutscene.animate(game_map, camera.scroll, player, camera, dt)
				if returned == True:
					current_cutscene = None
				elif returned != None:
					current_dialogue = returned

			elif cutscene_rects > 0:
				cutscene_rects -= 2*dt
				pygame.draw.rect(camera.display, (0, 0, 0), (0, cutscene_rects-50, Width, 50))
				pygame.draw.rect(camera.display, (0, 0, 0), (0, Height-cutscene_rects, Width, 50))

			if current_dialogue:
				pause_time()
				current_dialogue.render(camera.display, settings["lang"])


			for interactable in game_map.npcs+list(game_map.connectors):
				if (isinstance(interactable, list) and interactable[0].colliderect(player.rect) and len(bosses) == 1) or (isinstance(interactable, NPC) and interactable.trigger_rect.colliderect(player.rect) and interactable.dialogue):
					inter_sprite = sprite(get_control_sprite(settings[prioritize]["interact"], prioritize))
					camera.display.blit(inter_sprite, (player.rect.centerx-inter_sprite.get_width()*0.5-camera.scroll.x, player.y-inter_sprite.get_height()-5-camera.scroll.y))

			blits = [(camera.display, (0, 0))]
			if brightness.get_alpha() != 0:
				blits.append((brightness, (0, 0)))
			if sleep_brightness[0].get_alpha() != 0:
				blits.append((sleep_brightness[0], (0, 0)))

			win.fblits(blits)
		
		elif menus[-1] == "main":
			if not music:
				play_music("assets/SOUND/music/main.ogg")
			win.fill((0, 0, 0))
			if time.time()-update_bg_alpha >= 0.05 and bg.get_alpha() < 255:
				bg.set_alpha(bg.get_alpha()+2)
				update_bg_alpha = time.time()

			for button in buttons:
				button.outline = (255, 255, 255)
				if button.rect.collidepoint(mp) or (isinstance(button, Slider) and button.selected):
					button.outline = (255, 128, 0)

			win.fblits((
				(bg, (0, 0)),
				(text_title.surf, (232*0.5-text_title.width*0.5, 20)),
				(button_start.surf, (button_start.x, button_start.y)),
				(button_settings.surf, (button_settings.x, button_settings.y)),
				(button_mods.surf, (button_mods.x, button_mods.y)),
				(button_quit.surf, (button_quit.x, button_quit.y)),
				(text_version.surf, (232*0.5-text_version.width*0.5, 300)),
				(text_cw.surf, (232*0.5-text_cw.width*0.5, 320)),
				(brightness, (0, 0))
			))

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit(); sys.exit()

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_F1:
						menus.append("music")
						buttons = default_menu_buttons[menus[-1]]
						play_music(musics[0])
					

			if (game_input.press(pygame.K_UP, "keys", controller) or game_input.press(pygame.K_w, "keys", controller) or game_input.press(pygame.CONTROLLER_BUTTON_DPAD_UP, "cons", controller)):
				if chosen_button == -1:
					chosen_button = 0
				else:
					if chosen_button == 0:
						chosen_button = len(buttons)-1
					else:
						chosen_button -= 1
				pygame.mouse.set_pos(buttons[chosen_button].x+buttons[chosen_button].width*0.5, buttons[chosen_button].y+buttons[chosen_button].height*0.5)
			elif (game_input.press(pygame.K_DOWN, "keys", controller) or game_input.press(pygame.K_s, "keys", controller) or game_input.press(pygame.CONTROLLER_BUTTON_DPAD_DOWN, "cons", controller)):
				if chosen_button == -1:
					chosen_button = 0
				else:
					if chosen_button == len(buttons)-1:
						chosen_button = 0
					else:
						chosen_button += 1
				pygame.mouse.set_pos(buttons[chosen_button].x+buttons[chosen_button].width*0.5, buttons[chosen_button].y+buttons[chosen_button].height*0.5)
			elif (game_input.press(pygame.K_RETURN, "keys", controller) or game_input.press(pygame.K_SPACE, "keys", controller) or game_input.press(pygame.K_KP_ENTER, "keys", controller) or game_input.press(pygame.CONTROLLER_BUTTON_A, "cons", controller) or game_input.press(pygame.CONTROLLER_BUTTON_START, "cons", controller) or game_input.press(1, "keys", controller)):
				if button_start.rect.collidepoint(mp):
					menus.append("start")
					buttons = default_menu_buttons[menus[-1]]
				elif button_settings.rect.collidepoint(mp):
					menus.append("settings")
					main_buttons = [button_graphics, button_volume, button_controls, button_language, button_settings_back]
					buttons = default_menu_buttons[menus[-1]]
					backdrop_surf = win.copy()
				elif button_mods.rect.collidepoint(mp):
					menus.append("mods")
					buttons = default_menu_buttons[menus[-1]]
					main_buttons = [button_assets, button_behavior, button_addons, button_mods_back]
					backdrop_surf = win.copy()
				elif button_quit.rect.collidepoint(mp):
					pygame.quit(); sys.exit()
		elif menus[-1] == "settings":
			mp = list(mp)
			mp[0] -= 25
			mp[1] -= 25
			mp = tuple(mp)

			menu_surf.fill((0, 0, 0))
			pygame.draw.line(menu_surf, (255, 255, 255), (250, 0), (250, menu_surf.get_height()))

			for button in main_buttons:
				if sub_menu != button.text_content.lower() or (sub_menu and sub_menu.endswith("_controls") and button.text_content == "Controls") or (sub_menu == "langs" and button.text_content == "Languages"):
					button.outline = (255, 255, 255)
				if button.rect.collidepoint(mp) or (sub_menu and sub_menu.endswith("_controls") and button.text_content == "Controls") or (sub_menu == "langs" and button.text_content == "Languages"):
					button.outline = (255, 128, 0)
			for button in buttons:
				button.outline = (255, 255, 255)
				if (button.rect.collidepoint((mp[0], mp[1]+con_scroll)) or (isinstance(button, Slider) and button.selected)) and not (button in [button_connect, button_invert_sticks]):
					button.outline = (255, 128, 0)
				elif button in [button_connect, button_invert_sticks] and button.rect.collidepoint(mp):
					button.outline = (255, 128, 0)

			if sub_menu == "key_controls":
				button_key.outline = (255, 128, 0)
				button_con.outline = (255, 255, 255)
			elif sub_menu == "con_controls":
				button_con.outline = (255, 128, 0)
				button_key.outline = (255, 255, 255)
			if button_key.rect.collidepoint(mp):
				button_key.outline = (255, 128, 0)
			elif sub_menu == "con_controls":
				button_key.outline = (255, 255, 255)
			if button_con.rect.collidepoint(mp):
				button_con.outline = (255, 128, 0)
			elif sub_menu == "key_controls":
				button_con.outline = (255, 255, 255)
			

			win.fblits((
				(backdrop_surf, (0, 0)),
				(shadow_surf, (0, 0))
			))
			blits = [
				(text_settings.surf, (250*0.5-text_settings.width*0.5, 0)),
				(button_graphics.surf, (button_graphics.x, button_graphics.y)),
				(button_volume.surf, (button_volume.x, button_volume.y)),
				(button_controls.surf, (button_controls.x, button_controls.y)),
				(button_language.surf, (button_language.x, button_language.y)),
				(button_settings_back.surf, (button_settings_back.x, button_settings_back.y))
			]
			if sub_menu == "graphics":
				blits.append((text_graphics.surf, ((Width-50-250)*0.5-text_graphics.width*0.5+250, 0)))
				blits.append((button_fullscreen.surf, (button_fullscreen.x, button_fullscreen.y)))
				blits.append((button_vsync.surf, (button_vsync.x, button_vsync.y)))
				blits.append((slider_fps.surf, (slider_fps.x, slider_fps.y)))
				blits.append((slider_brightness.surf, (slider_brightness.x, slider_brightness.y)))
				
				if settings["vsync"]:
					blits.append((fps_setting_surf, (slider_fps.x, slider_fps.y)))

				if slider_fps.selected and not settings["vsync"]:
						val = slider_fps.update_value(mp)
						slider_fps.text_content = f"{get_text('slider:fps')}{val if val <= 500 else '∞'}"
						settings["FPS"] = val if val <= 500 else 2 ** 32
				elif slider_brightness.selected:
					val = slider_brightness.update_value(mp)
					slider_brightness.text_content = f"{slider_brightness.text_content.split(': ')[0]}: {round(((slider_brightness.width_fill-20)/(slider_brightness.width-20))*100)}%"
					settings["brightness"] = val
					brightness.fill((0, 0, 0) if settings["brightness"] <= 0 else (255, 255, 255))
					brightness.set_alpha(abs(settings["brightness"]))
			elif sub_menu == "volume":
				blits.append((text_volume.surf, ((Width-50-250)*0.5-text_volume.width*0.5+250, 0)))
				blits.append((slider_music.surf, (slider_music.x, slider_music.y)))
				blits.append((slider_sfx.surf, (slider_sfx.x, slider_sfx.y)))

				if slider_music.selected:
					val = round(slider_music.update_value(mp), 2)
					slider_music.text_content = f"{slider_music.text_content.split(': ')[0]}: {round(((slider_music.width_fill-20)/(slider_music.width-20))*100)}%"
					settings["volumes"]["music"] = val
					pygame.mixer_music.set_volume(val)
					
				elif slider_sfx.selected:
					val = round(slider_sfx.update_value(mp), 2)
					slider_sfx.text_content = f"{slider_sfx.text_content.split(': ')[0]}: {round(((slider_sfx.width_fill-20)/(slider_sfx.width-20))*100)}%"
					settings["volumes"]["SFX"] = val
			elif sub_menu and sub_menu.endswith("_controls"):
				blits.append((button_key.surf, (button_key.x, button_key.y)))
				blits.append((button_con.surf, (button_con.x, button_con.y)))
				
				if sub_menu == "con_controls":
					blits.append((button_connect.surf, (button_connect.x, button_connect.y)))
					if sdl2_controller.get_init():
						blits.append((button_invert_sticks.surf, (button_invert_sticks.x, button_invert_sticks.y)))
						if con_scroll <= 0:
							blits.append((button_move.surf, (button_move.x, button_move.y-con_scroll)))
							blits.append((sprite("right_stick" if settings["sticks invert"] else "left_stick"), (button_move.x+button_move.width-sprite("left_stick").get_width()-10, button_move.y+button_move.height*0.5-8-con_scroll)))
						if con_scroll <= 34:
							blits.append((button_aim.surf, (button_aim.x, button_aim.y-con_scroll)))
							blits.append((sprite("left_stick" if settings["sticks invert"] else "right_stick"), (button_aim.x+button_aim.width-sprite("left_stick").get_width()-10, button_aim.y+button_aim.height*0.5-8-con_scroll)))
						

						button_up.y = button_up.rect.y = 223
						button_down.y = button_down.rect.y = 257
						button_left.y = button_left.rect.y = 291
						button_right.y = button_right.rect.y = 325
						button_dash.y = button_dash.rect.y = 359
						button_sneak.y = button_sneak.rect.y = 393
						button_sleep.y = button_sleep.rect.y = 427
						button_interact.y = button_interact.rect.y = 461
						button_settings_inventory.y = button_settings_inventory.rect.y = 495
						button_pause.y = button_pause.rect.y = 529
						button_weapon1.y = button_weapon1.rect.y = 563
						button_weapon2.y = button_weapon2.rect.y = 597
						button_sweapon1.y = button_sweapon1.rect.y = 631
						button_sweapon2.y = button_sweapon2.rect.y = 665

						for button in control_buttons:
							button[0].update_surf()
							con_sprite = sprite(cons[button[1]])
							button[0].surf.blit(con_sprite, (button[0].width-con_sprite.get_width()-10-(16-con_sprite.get_width())*0.5, button[0].height*0.5-con_sprite.get_height()*0.5))

							x = button[0].width-con_sprite.get_width()-10-(16-con_sprite.get_width())*0.5
							if button[1] in ["up", "down", "left", "right"]:
								button[0].surf.blit(sprite("right_stick" if settings["sticks invert"] else "left_stick"), (x-20, button[0].height*0.5-8))
				else:
					button_up.y = button_up.rect.y = 55
					button_down.y = button_down.rect.y = 89
					button_left.y = button_left.rect.y = 123
					button_right.y = button_right.rect.y = 157
					button_dash.y = button_dash.rect.y = 191
					button_sneak.y = button_sneak.rect.y = 225
					button_sleep.y = button_sleep.rect.y = 259
					button_interact.y = button_interact.rect.y = 293
					button_settings_inventory.y = button_settings_inventory.rect.y = 327
					button_pause.y = button_pause.rect.y = 361
					button_weapon1.y = button_weapon1.rect.y = 395
					button_weapon2.y = button_weapon2.rect.y = 429
					button_sweapon1.y = button_sweapon1.rect.y = 463
					button_sweapon2.y = button_sweapon2.rect.y = 497

					for button in control_buttons:
						button[0].update_surf()
						button[0].surf.blit(sprite(keys[button[1]]), (button[0].width-sprite(keys[button[1]]).get_width()-10, button[0].height*0.5-8))

				if (sub_menu == "con_controls" and sdl2_controller.get_init()) or (sub_menu == "key_controls"):
					adder = 68 if sub_menu == "con_controls" else 0
					if con_scroll <= 0+adder:
						blits.append((button_up.surf, (button_up.x, button_up.y-con_scroll)))
					if con_scroll <= 34+adder:
						blits.append((button_down.surf, (button_down.x, button_down.y-con_scroll)))
					if con_scroll <= 68+adder:
						blits.append((button_left.surf, (button_left.x, button_left.y-con_scroll)))
					if con_scroll <= 102+adder:
						blits.append((button_right.surf, (button_right.x, button_right.y-con_scroll)))
					if con_scroll <= 136+adder:
						blits.append((button_dash.surf, (button_dash.x, button_dash.y-con_scroll)))
					if con_scroll <= 170+adder:
						blits.append((button_sneak.surf, (button_sneak.x, button_sneak.y-con_scroll)))
					if con_scroll <= 204+adder:
						blits.append((button_sleep.surf, (button_sleep.x, button_sleep.y-con_scroll)))
					if con_scroll <= 238+adder:
						blits.append((button_interact.surf, (button_interact.x, button_interact.y-con_scroll)))
					if con_scroll <= 340:
						blits.append((button_settings_inventory.surf, (button_settings_inventory.x, button_settings_inventory.y-con_scroll)))
					if con_scroll <= 374:
						blits.append((button_pause.surf, (button_pause.x, button_pause.y-con_scroll)))
					blits.append((button_weapon1.surf, (button_weapon1.x, button_weapon1.y-con_scroll)))
					blits.append((button_weapon2.surf, (button_weapon2.x, button_weapon2.y-con_scroll)))
					blits.append((button_sweapon1.surf, (button_sweapon1.x, button_sweapon1.y-con_scroll)))
					blits.append((button_sweapon2.surf, (button_sweapon2.x, button_sweapon2.y-con_scroll)))
			elif sub_menu == "langs":
				blits.append((text_language.surf, ((Width-50-250)*0.5-text_language.width*0.5+250, 0)))
				blits.append((text_currlang.surf, ((Width-50-250)*0.5-text_currlang.width*0.5+250, 67)))
				blits.append((pre_arrow_surf, (button_prevlang.x, button_prevlang.y)))
				blits.append((post_arrow_surf, (button_postlang.x, button_postlang.y)))
			
			menu_surf.fblits(blits)
			pygame.draw.rect(menu_surf, (255, 255, 255), (0, 0, menu_surf.get_width(), menu_surf.get_height()), 1)
			win.fblits(((menu_surf, (25, 25)), (brightness, (0, 0))))
			if control_warning:
				win.fblits(((shadow_surf, (0, 0)), (control_warning_surf, (Width*0.5-control_warning_surf.get_width()*0.5, Height*0.5-control_warning_surf.get_height()*0.5))))
			if mouse_warning:
				win.fblits(((shadow_surf, (0, 0)), (mouse_warning_surf, (Width*0.5-mouse_warning_surf.get_width()*0.5, Height*0.5-mouse_warning_surf.get_height()*0.5))))

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit(); sys.exit()

				if event.type == pygame.MOUSEBUTTONDOWN:
					if not control_warning and not mouse_warning:
						if currently_choosing[0] and event.button not in [4, 5] and sub_menu == "key_controls":
							if event.button < 4:
								settings["keys"][currently_choosing[0]] = event.button
							else:
								if event.button > 7:
									mouse_warning = True
								else:
									settings["keys"][currently_choosing[0]] = event.button-2

							warned = []
							key_ids = tuple(settings["keys"].values())
							keys = settings["keys"].copy()
							for name, key in keys.items():
								if key_ids.count(key) > 1:
									control_warning = True
									warned.append(name)

								keys[name] = get_control_sprite(key, 'keys')

							for button in control_buttons:
								button[0].color = (0, 0, 0)
								if button[1] in warned:
									button[0].color = (100, 0, 0)
								button[2] = False
							currently_choosing[0] = None

							dump_json(["scripts", "dataDL", "settings.json"], settings)
						else:
							if event.button == 4 and sub_menu and sub_menu.endswith("_controls") and con_scroll > 0:
								con_scroll -= 34
							elif event.button == 5 and sub_menu and sub_menu.endswith("_controls") and ((con_scroll < 170 and sub_menu == "key_controls") or (con_scroll < 340 and sub_menu == "con_controls")):
								con_scroll += 34
					else:
						control_warning = False
						mouse_warning = False

				if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and sub_menu:
					slider_fps.selected = False
					slider_brightness.selected = False
					slider_music.selected = False
					slider_sfx.selected = False
					dump_json(["scripts", "dataDL", "settings.json"], settings)
			
				if (currently_choosing[1] and sub_menu == "con_controls") and (event.type == pygame.CONTROLLERBUTTONDOWN  or (event.type == pygame.CONTROLLERAXISMOTION and event.axis in [4, 5] and event.value/32767 >= 0.5)):
					settings["cons"][currently_choosing[1]] = event.button if event.type == pygame.CONTROLLERBUTTONDOWN else event.axis + 11
										
					warned = []
					con_ids = tuple(settings["cons"].values())
					cons = settings["cons"].copy()
					for name, con in cons.items():
						if con_ids.count(con) > 1:
							warned.append(name)
							control_warning = True

						cons[name] = get_control_sprite(con, 'cons')

					for button in control_buttons:
						button[0].color = (0, 0, 0)
						if button[1] in warned:
							button[0].color = (100, 0, 0)
						button[3] = False
					currently_choosing[1] = None

					dump_json(["scripts", "dataDL", "settings.json"], settings)

				if event.type == pygame.KEYDOWN:
					if not control_warning and not mouse_warning:
						if not currently_choosing[0]:
							if event.key == pygame.K_F1:
								menus.append("music")
								buttons = default_menu_buttons[menus[-1]]
								play_music(musics[0])
						else:
							if event.key not in [pygame.K_LMETA, pygame.K_RMETA] and sub_menu == "key_controls":
								settings["keys"][currently_choosing[0]] = event.key

								warned = []
								key_ids = tuple(settings["keys"].values())
								keys = settings["keys"].copy()
								for name, key in keys.items():
									if key_ids.count(key) > 1:
										warned.append(name)
										control_warning = True

									keys[name] = get_control_sprite(key, 'keys')

								for button in control_buttons:
									button[0].color = (0, 0, 0)
									if button[1] in warned:
										button[0].color = (100, 0, 0)
									button[2] = False
								currently_choosing[0] = None

								dump_json(["scripts", "dataDL", "settings.json"], settings)
					else:
						control_warning = False
						mouse_warning = False

			if currently_choosing == [None, None]:
				if (game_input.press(pygame.K_UP, "keys", controller) or game_input.press(pygame.K_w, "keys", controller) or game_input.press(pygame.CONTROLLER_BUTTON_DPAD_UP, "cons", controller)):
					if isinstance(buttons[chosen_button], Slider):
						buttons[chosen_button].selected = False
					if chosen_button == -1:
						chosen_button = 0
					else:
						if chosen_button == 0:
							chosen_button = len(buttons)-1
						else:
							chosen_button -= 1
					
					if sub_menu and ((buttons[chosen_button].y-con_scroll < button_up.y and sub_menu == "key_controls") or (buttons[chosen_button].y-con_scroll < button_move.y and sub_menu == "con_controls" and chosen_button > 1)):
						con_scroll -= 34
						print(con_scroll)
					if sub_menu and sub_menu.endswith("_controls") and chosen_button == len(buttons)-1:
						con_scroll = 238 if sub_menu == "key_controls" else 408
					if isinstance(buttons[chosen_button], Button):
						pygame.mouse.set_pos(buttons[chosen_button].x+buttons[chosen_button].width*0.5+25, buttons[chosen_button].y+buttons[chosen_button].height*0.5+25-con_scroll)
					elif isinstance(buttons[chosen_button], Slider):
						pygame.mouse.set_pos(buttons[chosen_button].x+buttons[chosen_button].width_fill+25, buttons[chosen_button].y+buttons[chosen_button].height*0.5+25)
						buttons[chosen_button].selected = True
				if (game_input.press(pygame.K_DOWN, "keys", controller) or game_input.press(pygame.K_s, "keys", controller) or game_input.press(pygame.CONTROLLER_BUTTON_DPAD_DOWN, "cons", controller)):
					if isinstance(buttons[chosen_button], Slider):
						buttons[chosen_button].selected = False
					if chosen_button == -1:
						chosen_button = 0
					else:
						if chosen_button == len(buttons)-1:
							chosen_button = 0
						else:
							chosen_button += 1
					
					if sub_menu and sub_menu.endswith("_controls") and ((con_scroll < 238 and sub_menu == "key_controls") or (con_scroll < 408 and sub_menu == "con_controls" and chosen_button > 2)):
						con_scroll += 34
						print(con_scroll)
					if sub_menu and sub_menu.endswith("_controls") and chosen_button == 0:
						con_scroll = 0
					if isinstance(buttons[chosen_button], Button):
						pygame.mouse.set_pos(buttons[chosen_button].x+buttons[chosen_button].width*0.5+25, buttons[chosen_button].y+buttons[chosen_button].height*0.5+25-con_scroll)
					elif isinstance(buttons[chosen_button], Slider):
						pygame.mouse.set_pos(buttons[chosen_button].x+buttons[chosen_button].width_fill+25, buttons[chosen_button].y+buttons[chosen_button].height*0.5+25)
						buttons[chosen_button].selected = True
				if (game_input.press(pygame.K_LEFT, "keys", controller) or game_input.press(pygame.K_a, "keys", controller) or game_input.press(pygame.CONTROLLER_BUTTON_DPAD_LEFT, "cons", controller)):
					if sub_menu == "langs":
						lang_index = list(lang_dict.keys()).index(settings["lang"])
						if lang_index == 0:
							settings["lang"] = langs[len(langs)-1]
						else:
							settings["lang"] = langs[lang_index-1]

						update_setting_texts()
					elif sub_menu and sub_menu.endswith("_controls"):
						sub_menu = ("key_controls", "con_controls")[sub_menu == "key_controls"]
						con_scroll = 0
						chosen_button = 0
						buttons = [button_up, button_down, button_left, button_right, button_dash, button_sneak, button_sleep, button_interact, button_settings_inventory, button_pause, button_weapon1, button_weapon2, button_sweapon1, button_sweapon2]
						if sub_menu == "con_controls":
							buttons.insert(0, button_aim)
							buttons.insert(0, button_move)
							buttons.insert(0, button_invert_sticks)
							buttons.insert(0, button_connect)
				if (game_input.hold(pygame.K_LEFT, "keys", controller) or game_input.hold(pygame.K_a, "keys", controller) or game_input.hold(pygame.CONTROLLER_BUTTON_DPAD_LEFT, "cons", controller)):
					if isinstance(buttons[chosen_button], Slider):
						if mp[0] > buttons[chosen_button].x+20:
							pygame.mouse.set_pos(buttons[chosen_button].x+buttons[chosen_button].width_fill-(2*dt)+25, buttons[chosen_button].y+buttons[chosen_button].height*0.5+25)
						else:
							pygame.mouse.set_pos(buttons[chosen_button].x+20+25, buttons[chosen_button].y+buttons[chosen_button].height*0.5+25)
				if (game_input.press(pygame.K_RIGHT, "keys", controller) or game_input.press(pygame.K_d, "keys", controller) or game_input.press(pygame.CONTROLLER_BUTTON_DPAD_RIGHT, "cons", controller)):
					if sub_menu == "langs":
						lang_index = list(lang_dict.keys()).index(settings["lang"])
						if lang_index == len(langs)-1:
							settings["lang"] = langs[0]
						else:
							settings["lang"] = langs[lang_index+1]

						update_setting_texts()
					elif sub_menu and sub_menu.endswith("_controls"):
						sub_menu = ("key_controls", "con_controls")[sub_menu == "key_controls"]
						con_scroll = 0
						chosen_button = 0
						buttons = [button_up, button_down, button_left, button_right, button_dash, button_sneak, button_sleep, button_interact, button_settings_inventory, button_pause, button_weapon1, button_weapon2, button_sweapon1, button_sweapon2]
						if sub_menu == "con_controls":
							buttons.insert(0, button_aim)
							buttons.insert(0, button_move)
							buttons.insert(0, button_invert_sticks)
							buttons.insert(0, button_connect)
				if (game_input.hold(pygame.K_RIGHT, "keys", controller) or game_input.hold(pygame.K_d, "keys", controller) or game_input.hold(pygame.CONTROLLER_BUTTON_DPAD_RIGHT, "cons", controller)):
					if isinstance(buttons[chosen_button], Slider):
						if mp[0] < buttons[chosen_button].x+buttons[chosen_button].width:
							pygame.mouse.set_pos(buttons[chosen_button].x+buttons[chosen_button].width_fill+(3*dt)+25, buttons[chosen_button].y+buttons[chosen_button].height*0.5+25)
						else:
							pygame.mouse.set_pos(buttons[chosen_button].x+buttons[chosen_button].width+25, buttons[chosen_button].y+buttons[chosen_button].height*0.5+25)
				if (game_input.press(pygame.K_RETURN, "keys", controller) or game_input.press(pygame.K_SPACE, "keys", controller) or game_input.press(pygame.K_KP_ENTER, "keys", controller) or game_input.press(pygame.CONTROLLER_BUTTON_A, "cons", controller) or game_input.press(pygame.CONTROLLER_BUTTON_START, "cons", controller) or game_input.press(1, "keys", controller)):
					if button_graphics.rect.collidepoint(mp):
						sub_menu = "graphics"
						changing_menu = True
					elif button_volume.rect.collidepoint(mp):
						sub_menu = "volume"
						changing_menu = True
					elif button_controls.rect.collidepoint(mp):
						if sdl2_controller.get_init():
							sub_menu = "con_controls"
						else:
							sub_menu = "key_controls"
						changing_menu = True
						con_scroll = 0
					elif button_language.rect.collidepoint(mp):
						sub_menu = "langs"
						changing_menu = True
					elif button_settings_back.rect.collidepoint(mp):
						del menus[-1]
						buttons = default_menu_buttons[menus[-1]]
					else:
						if sub_menu == "graphics":
							if button_fullscreen.rect.collidepoint(mp):
								settings["fullscreen"] = not settings["fullscreen"]
								pygame.display.toggle_fullscreen()
								button_fullscreen.text_content = get_text("button:fullscreen")+get_text(f"status:{'on' if settings['fullscreen'] else 'off'}")
							elif button_vsync.rect.collidepoint(mp):
								settings["vsync"] = (0, 1)[settings["vsync"] == 0]
								pygame.display.set_mode((Width, Height), pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.SCALED, vsync=settings["vsync"])
								if settings["fullscreen"]:
									pygame.display.toggle_fullscreen()
								button_vsync.text_content = f"Vsync: {'on' if settings['vsync'] else 'off'}"
								fps_setting_surf.set_alpha(128 if settings["vsync"] else 0)
							elif slider_fps.rect.collidepoint(mp):
								slider_fps.selected = True
							elif slider_brightness.rect.collidepoint(mp):
								slider_brightness.selected = True
						elif sub_menu == "volume":
							if slider_music.rect.collidepoint(mp):
								slider_music.selected = True
							elif slider_sfx.rect.collidepoint(mp):
								slider_sfx.selected = True
						elif sub_menu and sub_menu.endswith("_controls"):
							if button_key.rect.collidepoint(mp):
								sub_menu = "key_controls"
								con_scroll = 0
								
								key_ids = tuple(settings["keys"].values())
								for button in control_buttons:
									button[0].color = (0, 0, 0)
									if key_ids.count(settings["keys"][button[1]]) > 1:
										button[0].color = (100, 0, 0)
							elif button_con.rect.collidepoint(mp):
								sub_menu = "con_controls"
								con_scroll = 0
								
								con_ids = tuple(settings["cons"].values())
								for button in control_buttons:
									button[0].color = (0, 0, 0)
									if con_ids.count(settings["cons"][button[1]]) > 1:
										button[0].color = (100, 0, 0)

							elif button_connect.rect.collidepoint(mp) and sub_menu == "con_controls":
								if sdl2_controller.get_init():
									sdl2_controller.quit()
									controller = FakeController()
									button_connect.text_content = get_text("button:controller")+get_text("status:disconnected")
								else:
									sdl2_controller.init()
									try:
										controller = sdl2_controller.Controller(0)
										button_connect.text_content = get_text("button:controller")+get_text("status:connected")
									except:
										sdl2_controller.quit()
							elif button_invert_sticks.rect.collidepoint(mp) and sub_menu == "con_controls" and sdl2_controller.get_init():
								settings["sticks invert"] = not settings["sticks invert"]
							for button in control_buttons:
								if button[0].rect.collidepoint((mp[0], mp[1]+con_scroll)):
									if sub_menu == "key_controls":
										keys = settings["keys"].copy()
										for name, key in keys.items():
											if name != button[1]:
												key = get_control_sprite(key, 'keys')
											else:
												key = "K_choosing"

											keys[name] = key

										for _button in control_buttons:
											_button[0].color = (0, 0, 0)
											_button[2] = False
										button[2] = True

										currently_choosing[0] = button[1]

									if sub_menu == "con_controls" and sdl2_controller.get_init():
										cons = settings["cons"].copy()
										for name, con in cons.items():
											if name != button[1]:
												con = get_control_sprite(con, 'cons')
											else:
												con = "C_choosing"

											cons[name] = con

										for _button in control_buttons:
											_button[0].color = (0, 0, 0)
											_button[3] = False
										button[3] = True

										currently_choosing[1] = button[1]
						elif sub_menu == "langs":
							lang_index = list(lang_dict.keys()).index(settings["lang"])
							if button_postlang.rect.collidepoint(mp):
								if lang_index == len(langs)-1:
									settings["lang"] = langs[0]
								else:
									settings["lang"] = langs[lang_index+1]
							elif button_prevlang.rect.collidepoint(mp):
								if lang_index == 0:
									settings["lang"] = langs[len(langs)-1]
								else:
									settings["lang"] = langs[lang_index-1]

							update_setting_texts()

					if changing_menu:
						if sub_menu == "graphics":
							buttons = [button_fullscreen, button_vsync, slider_fps, slider_brightness]
							chosen_button = 0
						elif sub_menu == "volume":
							buttons = [slider_music, slider_sfx]
							chosen_button = 0
						elif sub_menu and sub_menu.endswith("_controls"):
							buttons = [button_up, button_down, button_left, button_right, button_dash, button_sneak, button_sleep, button_interact, button_settings_inventory, button_pause, button_weapon1, button_weapon2, button_sweapon1, button_sweapon2]
							if sub_menu == "con_controls":
								buttons.insert(0, button_aim)
								buttons.insert(0, button_move)
								buttons.insert(0, button_invert_sticks)
								buttons.insert(0, button_connect)
							chosen_button = 0
						elif sub_menu == "langs":
							buttons = [button_random]
							chosen_button = 0
							
						if not game_input.hold(1, "keys", controller):
							if isinstance(buttons[chosen_button], Button):
								pygame.mouse.set_pos(buttons[chosen_button].x+buttons[chosen_button].width*0.5+25, buttons[chosen_button].y+buttons[chosen_button].height*0.5+25)
							elif isinstance(buttons[chosen_button], Slider):
								buttons[chosen_button].selected = True
								pygame.mouse.set_pos(buttons[chosen_button].x+buttons[chosen_button].width_fill+25, buttons[chosen_button].y+buttons[chosen_button].height*0.5+25)
					changing_menu = False
				if (game_input.press(pygame.K_LSHIFT, "keys", controller) or game_input.press(pygame.K_RSHIFT, "keys", controller) or game_input.press(pygame.K_BACKSPACE, "keys", controller) or game_input.press(pygame.K_ESCAPE, "keys", controller) or game_input.press(pygame.CONTROLLER_BUTTON_B, "cons", controller) or game_input.press(pygame.CONTROLLER_BUTTON_BACK, "cons", controller) or game_input.press(3, "keys", controller)):
					if sub_menu:
						sub_menu = None
						buttons = [button_graphics, button_volume, button_controls, button_language, button_settings_back]
						for i, button in enumerate(buttons):
							if button.outline == (255, 128, 0):
								chosen_button = i
								break
						pygame.mouse.set_pos(buttons[chosen_button].x+buttons[chosen_button].width*0.5+25, buttons[chosen_button].y+buttons[chosen_button].height*0.5+25)
					else:
						del menus[-1]
						buttons = default_menu_buttons[menus[-1]]
				if (game_input.press(pygame.K_r, "keys", controller) or game_input.press(pygame.CONTROLLER_BUTTON_Y, "cons", controller) or game_input.press(2, "keys", controller)):
					settings = {
						"FPS": 60,
						"fullscreen": True,
						"vsync": 1,
						"keys": {
							"up": pygame.K_w,
							"down": pygame.K_s,
							"left": pygame.K_a,
							"right": pygame.K_d,
							"dash": pygame.K_SPACE,
							"sneak": pygame.K_LSHIFT,
							"sleep": pygame.K_f,
							"interact": pygame.K_r,
							"inventory": pygame.K_TAB,
							"pause": pygame.K_ESCAPE,
							"primary": 1,
							"secondary": 3,
							"pspecial": pygame.K_q,
							"sspecial": pygame.K_e
						},
						"cons": {
							"up": pygame.CONTROLLER_BUTTON_DPAD_UP,
							"down": pygame.CONTROLLER_BUTTON_DPAD_DOWN,
							"left": pygame.CONTROLLER_BUTTON_DPAD_LEFT,
							"right": pygame.CONTROLLER_BUTTON_DPAD_RIGHT,
							"dash": pygame.CONTROLLER_BUTTON_A,
							"sneak": pygame.CONTROLLER_BUTTON_LEFTSTICK,
							"sleep": pygame.CONTROLLER_BUTTON_Y,
							"interact": pygame.CONTROLLER_BUTTON_X,
							"inventory": pygame.CONTROLLER_BUTTON_BACK,
							"pause": pygame.CONTROLLER_BUTTON_START,
							"primary": 16,
							"secondary": 15,
							"pspecial": pygame.CONTROLLER_BUTTON_RIGHTSHOULDER,
							"sspecial": pygame.CONTROLLER_BUTTON_LEFTSHOULDER
						},
						"sticks invert": False,
						"brightness": 0,
						"permadeath": False,
						"volumes": {
							"music": 1,
							"SFX": 1
						},
						"lang": "english"
					}
					slider_fps.width_fill = ((settings['FPS']-10)/500)*(200-20)+20 if settings['FPS'] <= 500 else 200
					slider_fps.update_surf()
					slider_brightness.width_fill = int((((settings['brightness']+200)/2.5)/100)*(200-20)+20)
					slider_brightness.update_surf()
					slider_music.width_fill = settings['volumes']['music']*(200-20)+20
					slider_music.update_surf()
					slider_sfx.width_fill = settings['volumes']['SFX']*(200-20)+20
					slider_sfx.update_surf()
					fps_setting_surf.set_alpha(128)
					update_setting_texts()

					pygame.display.set_mode((Width, Height), pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.SCALED, vsync=settings["vsync"])
					if settings["fullscreen"]:
						pygame.display.toggle_fullscreen()
		elif menus[-1] == "start":
			for button in buttons:
				button.outline = (255, 255, 255)
				if button.rect.collidepoint(mp) or (isinstance(button, Slider) and button.selected):
					button.outline = (255, 128, 0)

			win.fill((0, 0, 0))
			blits = [
				(bg, (0, 0)),
				(text_saves.surf, (232*0.5-text_saves.width*0.5, 20)),
				(button_save1.surf, (button_save1.x, button_save1.y)),
				(text_save1.surf, (30, button_save1.y)),
				(button_save2.surf, (button_save2.x, button_save2.y)),
				(text_save2.surf, (30, button_save2.y)),
				(button_save3.surf, (button_save3.x, button_save3.y)),
				(text_save3.surf, (30, button_save3.y)),
				(button_start_back.surf, (button_start_back.x, button_start_back.y)),
			]
			if save1:
				blits.append((sprite("trash"), (button_save1_trash.x, button_save1_trash.y)))
				blits.append((save1_xp, (30, button_save1_trash.y)))
				blits.append((save1_c1, (81, button_save1_trash.y)))
				blits.append((save1_c2, (132, button_save1_trash.y)))
				blits.append((sprite(save1["difficulty"].lower()), (184, button_save1_trash.y)))
			if save2:
				blits.append((sprite("trash"), (button_save2_trash.x, button_save2_trash.y)))
				blits.append((save2_xp, (30, button_save2_trash.y)))
				blits.append((save2_c1, (81, button_save2_trash.y)))
				blits.append((save2_c2, (132, button_save2_trash.y)))
				blits.append((sprite(save2["difficulty"].lower()), (184, button_save2_trash.y)))
			if save3:
				blits.append((sprite("trash"), (button_save3_trash.x, button_save3_trash.y)))
				blits.append((save3_xp, (30, button_save3_trash.y)))
				blits.append((save3_c1, (81, button_save3_trash.y)))
				blits.append((save3_c2, (132, button_save3_trash.y)))
				blits.append((sprite(save3["difficulty"].lower()), (184, button_save3_trash.y)))
			win.fblits(blits)
				
			if time.time()-update_bg_alpha >= 0.05 and bg.get_alpha() < 255:
				bg.set_alpha(bg.get_alpha()+2)
				update_bg_alpha = time.time()

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit(); sys.exit()

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_F1:
						menus.append("music")
						buttons = default_menu_buttons[menus[-1]]
						play_music(musics[0])


			if (game_input.press(pygame.K_UP, "keys", controller) or game_input.press(pygame.K_w, "keys", controller) or game_input.press(pygame.CONTROLLER_BUTTON_DPAD_UP, "cons", controller)):
				if chosen_button == -1:
					chosen_button = 0
				else:
					if chosen_button == 0:
						chosen_button = len(buttons)-1
					else:
						chosen_button -= 1
				pygame.mouse.set_pos(buttons[chosen_button].x+buttons[chosen_button].width*0.5, buttons[chosen_button].y+buttons[chosen_button].height*0.5)
			elif (game_input.press(pygame.K_DOWN, "keys", controller) or game_input.press(pygame.K_s, "keys", controller) or game_input.press(pygame.CONTROLLER_BUTTON_DPAD_DOWN, "cons", controller)):
				if chosen_button == -1:
					chosen_button = 0
				else:
					if chosen_button == len(buttons)-1:
						chosen_button = 0
					else:
						chosen_button += 1
				pygame.mouse.set_pos(buttons[chosen_button].x+buttons[chosen_button].width*0.5, buttons[chosen_button].y+buttons[chosen_button].height*0.5)
			elif (game_input.press(pygame.K_RETURN, "keys", controller) or game_input.press(pygame.K_SPACE, "keys", controller) or game_input.press(pygame.K_KP_ENTER, "keys", controller) or game_input.press(pygame.CONTROLLER_BUTTON_A, "cons", controller) or game_input.press(pygame.CONTROLLER_BUTTON_START, "cons", controller) or game_input.press(1, "keys", controller)):
				if button_save1.rect.collidepoint(mp):
					if save1:
						if button_save1_trash.rect.collidepoint(mp):
							os.remove(os.path.join("scripts", "saves", f"save1.json"))
							save1 = None
							text_save1.content = f"{get_text('button:save')} 1"
						else:
							save_data = save1
							save_num = 1
							difficulty = save_data["difficulty"]
							menus = []

							maps = {}
							current_dialogue = None
							current_cutscene = None
							near_death_surf.set_alpha(0)

							player, inventory = load()
							camera = Camera([player.rect.centerx+Width*0.5, player.rect.centery+Height*0.5], player, True)
							maps[save_data["map"]] = TileMap(save_data["map"], save_data)
							game_map = maps[save_data["map"]]

							camera.update([Width, Height], 1, game_map)
							camera.immediate = False
					else:
						save_num = 1
						menus.append("save")
						buttons = default_menu_buttons[menus[-1]]
						backdrop_surf = win.copy()
						text_newsave.content = text_newsave.content.replace("save_num", "1")
				elif button_save2.rect.collidepoint(mp):
					if save2:
						if button_save2_trash.rect.collidepoint(mp):
							os.remove(os.path.join("scripts", "saves", f"save2.json"))
							save2 = None
							text_save2.content = f"{get_text('button:save')} 2"
						else:
							save_data = save2
							save_num = 2
							difficulty = save_data["difficulty"]
							menus = []

							maps = {}
							current_dialogue = None
							current_cutscene = None
							near_death_surf.set_alpha(0)

							player, inventory = load()
							camera = Camera([player.rect.centerx+Width*0.5, player.rect.centery+Height*0.5], player, True)
							maps[save_data["map"]] = TileMap(save_data["map"], save_data)
							game_map = maps[save_data["map"]]

							camera.update([Width, Height], 1, game_map)
							camera.immediate = False
					else:
						save_num = 2
						menus.append("save")
						buttons = default_menu_buttons[menus[-1]]
						backdrop_surf = win.copy()
						text_newsave.content = text_newsave.content.replace("save_num", "2")
				elif button_save3.rect.collidepoint(mp):
					if save3:
						if button_save3_trash.rect.collidepoint(mp):
							os.remove(os.path.join("scripts", "saves", f"save3.json"))
							save3 = None
							text_save3.content = f"{get_text('button:save')} 3"
						else:
							save_data = save3
							save_num = 3
							difficulty = save_data["difficulty"]
							menus = []

							maps = {}
							current_dialogue = None
							current_cutscene = None
							near_death_surf.set_alpha(0)

							player, inventory = load()
							camera = Camera([player.rect.centerx+Width*0.5, player.rect.centery+Height*0.5], player, True)
							maps[save_data["map"]] = TileMap(save_data["map"], save_data)
							game_map = maps[save_data["map"]]

							camera.update([Width, Height], 1, game_map)
							camera.immediate = False
					else:
						save_num = 3
						menus.append("save")
						buttons = default_menu_buttons[menus[-1]]
						backdrop_surf = win.copy()
						text_newsave.content = text_newsave.content.replace("save_num", "3")
				elif button_start_back.rect.collidepoint(mp):
					del menus[-1]
					buttons = default_menu_buttons[menus[-1]]
			elif (game_input.press(pygame.K_LSHIFT, "keys", controller) or game_input.press(pygame.K_RSHIFT, "keys", controller) or game_input.press(pygame.K_BACKSPACE, "keys", controller) or game_input.press(pygame.K_ESCAPE, "keys", controller) or game_input.press(pygame.CONTROLLER_BUTTON_B, "cons", controller) or game_input.press(pygame.CONTROLLER_BUTTON_BACK, "cons", controller) or game_input.press(3, "keys", controller)):
				del menus[-1]
				buttons = default_menu_buttons[menus[-1]]
			elif (game_input.press(pygame.K_DELETE, "keys", controller) or game_input.press(pygame.CONTROLLER_BUTTON_X, "cons", controller)) and chosen_button < 3:
				if chosen_button == 0 and save1:
					os.remove(os.path.join("scripts", "saves", f"save1.json"))
					save1 = None
					text_save1.content = f"{get_text('button:save')} 1"
				elif chosen_button == 1 and save2:
					os.remove(os.path.join("scripts", "saves", f"save2.json"))
					save2 = None
					text_save2.content = f"{get_text('button:save')} 2"
				elif chosen_button == 2 and save3:
					os.remove(os.path.join("scripts", "saves", f"save3.json"))
					save3 = None
					text_save3.content = f"{get_text('button:save')} 3"
		elif menus[-1] == "save":
			mp = list(mp)
			mp[0] -= 25
			mp[1] -= 25
			mp = tuple(mp)

			for button_group in buttons:
				for button in button_group:
					button.outline = (255, 255, 255)
					if button.rect.collidepoint(mp):
						button.outline = (255, 128, 0)

			menu_surf.fill((255, 255, 255))
			menu_surf.fill((0, 0, 0), (1, 1, Width-52, Height-52))
			menu_surf.fblits((
				(text_newsave.surf, (menu_surf.get_width()*0.5-text_newsave.width*0.5, 10)),
				(button_archer.surf, (button_archer.x, button_archer.y)),
				(text_archer.surf, (button_archer.x+(50-text_archer.width*0.5), button_archer.y+90-text_archer.height)),
				(button_mage.surf, (button_mage.x, button_mage.y)),
				(text_mage.surf, (button_mage.x+(50-text_mage.width*0.5), button_mage.y+90-text_mage.height)),
				(button_swordsman.surf, (button_swordsman.x, button_swordsman.y)),
				(text_swordsman.surf, (button_swordsman.x+(50-text_swordsman.width*0.5), button_swordsman.y+90-text_swordsman.height)),
				(button_thief.surf, (button_thief.x, button_thief.y)),
				(text_thief.surf, (button_thief.x+(50-text_thief.width*0.5), button_thief.y+90-text_thief.height)),
				(textbox_name.surf, (textbox_name.x, textbox_name.y)),
				(text_currdiff.surf, (menu_surf.get_width()*0.5-text_currdiff.width*0.5, 232)),
				(pre_arrow_surf, (button_prevdiff.x, button_prevdiff.y)),
				(post_arrow_surf, (button_postdiff.x, button_postdiff.y)),
				(button_start_newsave.surf, (button_start_newsave.x, button_start_newsave.y)),
				(button_newsave_back.surf, (button_newsave_back.x, button_newsave_back.y)),
			))
			win.fblits((
				(backdrop_surf, (0, 0)),
				(shadow_surf, (0, 0)),
				(menu_surf, (Width*0.5-menu_surf.get_width()*0.5, Height*0.5-menu_surf.get_height()*0.5)),
				(brightness, (0, 0))
			))

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit(); sys.exit()

				if event.type == pygame.KEYDOWN:
					if event.key in [pygame.K_LSHIFT, pygame.K_RSHIFT, pygame.K_ESCAPE, pygame.K_BACKSPACE] and not textbox_name.selected:
						del menus[-1]
						try:
							menu = menus[-1]
						except IndexError:
							menu = None
					elif event.key == pygame.K_ESCAPE and textbox_name.selected:
						textbox_name.selected = False
					else:
						textbox_name.update_text(event)

			if (game_input.press(pygame.K_UP, "keys", controller) or game_input.press(pygame.K_w, "keys", controller) or game_input.press(pygame.CONTROLLER_BUTTON_DPAD_UP, "cons", controller)):
				if chosen_button_group == -1:
					chosen_button_group = 0
				if chosen_button_group == 0:
					chosen_button_group = 3
				else:
					chosen_button_group -= 1
				chosen_button = 0
				pygame.mouse.set_pos(buttons[chosen_button_group][chosen_button].x+buttons[chosen_button_group][chosen_button].width*0.5+25, buttons[chosen_button_group][chosen_button].y+buttons[chosen_button_group][chosen_button].height*0.5+25)
			elif (game_input.press(pygame.K_DOWN, "keys", controller) or game_input.press(pygame.K_s, "keys", controller) or game_input.press(pygame.CONTROLLER_BUTTON_DPAD_DOWN, "cons", controller)):
				if chosen_button_group == -1:
					chosen_button_group = 0
				if chosen_button_group == 3:
					chosen_button_group = 0
				else:
					chosen_button_group += 1
				chosen_button = 0
				pygame.mouse.set_pos(buttons[chosen_button_group][chosen_button].x+buttons[chosen_button_group][chosen_button].width*0.5+25, buttons[chosen_button_group][chosen_button].y+buttons[chosen_button_group][chosen_button].height*0.5+25)
			elif (game_input.press(pygame.K_LEFT, "keys", controller) or game_input.press(pygame.K_a, "keys", controller) or game_input.press(pygame.CONTROLLER_BUTTON_DPAD_LEFT, "cons", controller)):
				if chosen_button_group in [0, 3]:
					if chosen_button == -1:
						chosen_button = 0
					if chosen_button == 0:
						chosen_button = len(buttons[chosen_button_group])-1
					else:
						chosen_button -= 1
					pygame.mouse.set_pos(buttons[chosen_button_group][chosen_button].x+buttons[chosen_button_group][chosen_button].width*0.5+25, buttons[chosen_button_group][chosen_button].y+buttons[chosen_button_group][chosen_button].height*0.5+25)
				elif chosen_button_group == 2:
					diff_index = difficulties.index(newsave_diff)
					if diff_index == 0:
						newsave_diff = difficulties[len(difficulties)-1]
					else:
						newsave_diff = difficulties[diff_index-1]
					text_currdiff.content = newsave_diff
			elif (game_input.press(pygame.K_RIGHT, "keys", controller) or game_input.press(pygame.K_d, "keys", controller) or game_input.press(pygame.CONTROLLER_BUTTON_DPAD_RIGHT, "cons", controller)):
				if chosen_button_group in [0, 3]:
					if chosen_button == -1:
						chosen_button = 0
					if chosen_button == len(buttons[chosen_button_group])-1:
						chosen_button = 0
					else:
						chosen_button += 1
					pygame.mouse.set_pos(buttons[chosen_button_group][chosen_button].x+buttons[chosen_button_group][chosen_button].width*0.5+25, buttons[chosen_button_group][chosen_button].y+buttons[chosen_button_group][chosen_button].height*0.5+25)
				elif chosen_button_group == 2:
					diff_index = difficulties.index(newsave_diff)
					if diff_index == len(difficulties)-1:
						newsave_diff = difficulties[0]
					else:
						newsave_diff = difficulties[diff_index+1]
					text_currdiff.content = newsave_diff
			elif (game_input.press(pygame.K_RETURN, "keys", controller) or game_input.press(pygame.K_SPACE, "keys", controller) or game_input.press(pygame.K_KP_ENTER, "keys", controller) or game_input.press(pygame.CONTROLLER_BUTTON_A, "cons", controller) or game_input.press(pygame.CONTROLLER_BUTTON_START, "cons", controller) or game_input.press(1, "keys", controller)):
				diff_index = difficulties.index(newsave_diff)

				if button_archer.rect.collidepoint(mp):
					newsave_player_class = "Archer"
					button_archer.outline = text_archer.color = (62, 41, 20)
					button_mage.outline = text_mage.color = (255, 255, 255)
					button_swordsman.outline = text_swordsman.color = (255, 255, 255)
					button_thief.outline = text_thief.color = (255, 255, 255)
				elif button_mage.rect.collidepoint(mp):
					newsave_player_class = "Mage"
					button_archer.outline = text_archer.color = (255, 255, 255)
					button_mage.outline = text_mage.color = (0, 58, 144)
					button_swordsman.outline = text_swordsman.color = (255, 255, 255)
					button_thief.outline = text_thief.color = (255, 255, 255)
				elif button_swordsman.rect.collidepoint(mp):
					newsave_player_class = "Swordsman"
					button_archer.outline = text_archer.color = (255, 255, 255)
					button_mage.outline = text_mage.color = (255, 255, 255)
					button_swordsman.outline = text_swordsman.color = (150, 33, 13)
					button_thief.outline = text_thief.color = (255, 255, 255)
				elif button_thief.rect.collidepoint(mp):
					newsave_player_class = "Thief"
					button_archer.outline = text_archer.color = (255, 255, 255)
					button_mage.outline = text_mage.color = (255, 255, 255)
					button_swordsman.outline = text_swordsman.color = (255, 255, 255)
					button_thief.outline = text_thief.color = (120, 120, 120)

				elif button_postdiff.rect.collidepoint(mp):
					if diff_index == len(difficulties)-1:
						newsave_diff = difficulties[0]
					else:
						newsave_diff = difficulties[diff_index+1]
					text_currdiff.content = newsave_diff
				elif button_prevdiff.rect.collidepoint(mp):
					if diff_index == 0:
						newsave_diff = difficulties[len(difficulties)-1]
					else:
						newsave_diff = difficulties[diff_index-1]
					text_currdiff.content = newsave_diff
				
				elif button_start_newsave.rect.collidepoint(mp):
					if not newsave_player_class:
						newsave_player_class = random.choice(["Archer", "Mage", "Swordsman", "Thief"])

					if textbox_name.text.content == "" or (textbox_name.text.content == "Name" and not textbox_name.clicked):
						newsave_name = random.choice(["Akesta", "Limena", "John Cena", "Elat", "Inora"])
					else:
						newsave_name = textbox_name.text.content

					Player.name = newsave_name
					difficulty = newsave_diff
					Player.classes = [newsave_player_class, None]
					Player.stats = {
						"HP": [10, 10], # current_HP, max_HP
						"SP": [10, 10], #current_SP, max_SP
						"AP": [0, None], # weapon_1, weapon_2
						"DP": 0,
						"EP": [[200 if newsave_player_class == "Archer" else 3 if newsave_player_class == "Thief" else 10, 200 if newsave_player_class == "Archer" else 3 if newsave_player_class == "Thief" else 10], [None, None]], # current_stat_1, max_stat_1 | current_stat_2, max_stat_2
						"M": 100,
						"XP": [0, 3, 1] # xp, max_xp, level
					}
					Player.inventory = []
					Player.equipment = [f"No {newsave_player_class[0]}Weapon", "No Shield", "No Backpack", "No Helmet", "No Chest", "No Leggings"]
					maps["DevRoom"] = TileMap("DevRoom")
					game_map = maps["DevRoom"]

					player = Player(100, 100)
					
					save(player)

					current_dialogue = None
					current_cutscene = None
					near_death_surf.set_alpha(0)

					player, inventory = load()
					camera = Camera([player.rect.centerx+Width*0.5, player.rect.centery+Height*0.5], player, True)
					maps[save_data["map"]] = TileMap(save_data["map"], save_data)
					game_map = maps[save_data["map"]]

					camera.update([Width, Height], 1, game_map)
					camera.immediate = False
				elif button_newsave_back.rect.collidepoint(mp):
					del menus[-1]
					buttons = default_menu_buttons[menus[-1]]
				textbox_name.is_over(mp)
			elif (game_input.press(pygame.K_LSHIFT, "keys", controller) or game_input.press(pygame.K_RSHIFT, "keys", controller) or game_input.press(pygame.K_BACKSPACE, "keys", controller) or game_input.press(pygame.K_ESCAPE, "keys", controller) or game_input.press(pygame.CONTROLLER_BUTTON_B, "cons", controller) or game_input.press(pygame.CONTROLLER_BUTTON_BACK, "cons", controller) or game_input.press(3, "keys", controller)):
				del menus[-1]
				buttons = default_menu_buttons[menus[-1]]
		elif menus[-1] == "inv":
			win.fblits((
				(backdrop_surf, (0, 0)),
				(shadow_surf, (0, 0)),
				(button_inventory.surf, (button_inventory.x, button_inventory.y)),
				(button_stats.surf, (button_stats.x, button_stats.y)),
				(button_map.surf, (button_map.x, button_map.y)),
				(button_quests.surf, (button_quests.x, button_quests.y)),
				(button_bestiary.surf, (button_bestiary.x, button_bestiary.y))
			))
			if sub_menu == "inv":
				inventory.draw(win, settings["lang"], prioritize)
			elif sub_menu == "stats":
				hp_bar = bar.copy()
				sp_bar = bar.copy()
				ep1_bar = bar.copy()
				ep2_bar = bar.copy()
				lp_bar = bar.copy()
				ip_bar = bar.copy()

				pygame.draw.rect(hp_bar, (0, 150, 0), (2, 2,  196*(player.stats['HP'][0]/player.stats['HP'][1]), 21))
				pygame.draw.rect(sp_bar, (150, 150, 0), (2, 2,  196*(player.stats['SP'][0]/player.stats['SP'][1]), 21))
				pygame.draw.rect(ep1_bar, (62, 41, 20) if player.classes[0] == "Archer" else (0, 58, 144) if player.classes[0] == "Mage" else (185, 167, 122) if player.classes[0] == "Swordsman" else (103, 103, 103), (2, 2,  196*(player.stats['EP'][0][0]/player.stats['EP'][0][1]), 21))
				if player.classes[1]: pygame.draw.rect(ep2_bar, (62, 41, 20) if player.classes[1] == "Archer" else (0, 58, 144) if player.classes[1] == "Mage" else (185, 167, 122) if player.classes[1] == "Swordsman" else (103, 103, 103), (2, 2,  196*(player.stats['EP'][1][0]/player.stats['EP'][1][1]), 21))
				pygame.draw.rect(lp_bar, (0, 150, 0), (2, 2,  196*(player.stats['XP'][0]/player.stats['XP'][1]), 21))
				pygame.draw.rect(ip_bar, (0, 0, 0), (2, 2,  196*(2/100), 21))

				surf_health = sprite("health").copy()
				surf_stamina = sprite("stamina").copy()
				surf_stat1 = sprite('projectiles' if player.classes[0] == 'Archer' else 'mana' if player.classes[0] == 'Mage' else 'vigor' if player.classes[0] == 'Swordsman' else 'darkness').copy()
				surf_stat2 = sprite("none" if not player.classes[1] else 'projectiles' if player.classes[1] == 'Archer' else 'mana' if player.classes[1] == 'Mage' else 'vigor' if player.classes[1] == 'Swordsman' else 'darkness').copy()
				surf_attack1 = sprite(str(player.classes[0]).lower()).copy()
				surf_attack2 = sprite(str(player.classes[1]).lower()).copy()
				surf_defense = sprite("defense")
				
				if leveling:
					level_alpha = (math.cos(counter)*64+192)
					counter += 0.1*dt

					hp_bar.set_alpha(level_alpha)
					sp_bar.set_alpha(level_alpha)
					ep1_bar.set_alpha(level_alpha)
					if player.classes[1]: ep2_bar.set_alpha(level_alpha)
					
					surf_health.set_alpha(level_alpha)
					surf_stamina.set_alpha(level_alpha)
					surf_stat1.set_alpha(level_alpha)
					if player.classes[1]: surf_stat2.set_alpha(level_alpha)
					surf_attack1.set_alpha(level_alpha)
					if player.classes[1]: surf_attack2.set_alpha(level_alpha)
					surf_defense.set_alpha(level_alpha)

					text_hp.alpha = level_alpha
					text_sp.alpha = level_alpha
					text_ep[0].alpha = level_alpha
					if player.classes[1]: text_ep[1].alpha = level_alpha
					text_ap[0].alpha = level_alpha
					if player.classes[1]: text_ap[1].alpha = level_alpha
					text_dp.alpha = level_alpha
					

				win.fblits((
					(hp_bar, (Width*0.5-220, 50)),
					(sp_bar, (Width*0.5-220, 75)),
					(ep1_bar, (Width*0.5-220, 100)),
					(ep2_bar, (Width*0.5-220, 125)),
					(lp_bar, (Width*0.5-220, 150)),
					(ip_bar, (Width*0.5-220, 175)),

					(surf_health, (Width*0.5-215, 55)), 
					(surf_stamina, (Width*0.5-215, 80)),
					(surf_stat1, (Width*0.5-215, 105)),
					(surf_stat2, (Width*0.5-215, 130)),
					(surf_attack1, (Width*0.5+20, 50)),
					(surf_attack2, (Width*0.5+20, 75)),
					(surf_defense, (Width*0.5+20, 100)),
					(sprite("level"), (Width*0.5-215, 155)),
					(sprite("money"), (Width*0.5+20, 125)),
					(sprite("health"), (Width*0.5-215, 180)),
					(sprite(str(player.classes[0]).lower()), (Width*0.5+20, 150)),
					(sprite(str(player.classes[1]).lower()), (Width*0.5+20, 175)),

					(text_hp.surf, (Width*0.5-220+(100-text_hp.width*0.5), 55)),
					(text_sp.surf, (Width*0.5-220+(100-text_sp.width*0.5), 80)),
					(text_ep[0].surf, (Width*0.5-220+(100-text_ep[0].width*0.5), 105)),
					(text_ep[1].surf, (Width*0.5-220+(100-text_ep[1].width*0.5), 130)),
					(text_ap[0].surf, (Width*0.5+45, 50)),
					(text_ap[1].surf, (Width*0.5+45, 75)),
					(text_dp.surf, (Width*0.5+45, 100)),
					(text_lp.surf, (Width*0.5-220+(100-text_lp.width*0.5), 155)),
					(text_mp.surf, (Width*0.5+45, 125)),
					(text_ip.surf, (Width*0.5-220+(100-text_ip.width*0.5), 180)),
					(text_cl[0].surf, (Width*0.5+45, 150)),
					(text_cl[1].surf, (Width*0.5+45, 175)),

					(button_level.surf, (button_level.x, button_level.y))
				))
			elif sub_menu == "map":
				win.blit(text_map.surf, (Width*0.5-text_map.width*0.5, Height*0.5-text_map.height*0.5))
			elif sub_menu == "quests":
				if len(quests):
					if len(chosen_quest) == 0:
						blits = []
						for quest in quests:
							blits.append((quest.surf, (quest.x, quest.y)))
						win.fblits(blits)
					else:
						blits = [
							(chosen_quest[0].surf, (chosen_quest[0].x, 40)),
							(quemy_info_surf, (5, 80)),
							(chosen_quest[1].surf, ((Width-81)*0.5-chosen_quest[1].width*0.5, 85)),
							(chosen_quest[2].surf, (10, 85+chosen_quest[1].height)),
							(chosen_quest[4].surf, (Width-71, 85)),
							(button_inv_back.surf, (button_inv_back.x, button_inv_back.y))
						]
						for i, requirement in enumerate(chosen_quest[3]):
							blits.append((sprite("check" if requirement.color == (128, 128, 128) else "uncheck"), (10, 85+chosen_quest[1].height+chosen_quest[2].height + 18 + 23*i)))
							blits.append((requirement.surf, (27, 85+chosen_quest[1].height+chosen_quest[2].height + 15 + 23*i)))

						for i, item in enumerate(chosen_quest[5][:-2]):
							blits.append((sprite(item[0]), (Width-71, 85+chosen_quest[4].height + 6 + 23*i)))
							blits.append((item[1].surf, (Width-50, 85+chosen_quest[4].height + 5 + 23*i)))
						if chosen_quest[5][-2].content != "":
							blits.append((sprite("money"), (Width-71, 85+chosen_quest[4].height + 6 + 23*(i+1))))
							blits.append((chosen_quest[5][-2].surf, (Width-50, 85+chosen_quest[4].height + 5 + 23*(i+1))))
						if chosen_quest[5][-1].content != "":
							adder = 2 if chosen_quest[5][-2].content != "" else 1
							blits.append((sprite("level"), (Width-71, 85+chosen_quest[4].height + 6 + 23*(i+adder))))
							blits.append((chosen_quest[5][-1].surf, (Width-50, 85+chosen_quest[4].height + 5 + 23*(i+adder))))
						
						win.fblits(blits)
						pygame.draw.line(win, (255, 255, 255), (Width-76, 80), (Width-76, Height-52))
				else:
					win.blit(text_quest.surf, (Width*0.5-text_quest.width*0.5, Height*0.5-text_quest.height*0.5))
			elif sub_menu == "bestiary":
				if not chosen_enemy:
					for button in bestiary_buttons:
						win.blit(bestiary_imgs[button.text_content], (button.x, button.y-scroll))
				else:
					blits = [
						(bestiary_imgs[chosen_enemy[0].content], (Width*0.5-18, 40)),
						(quemy_info_surf, (5, 80)),
						(chosen_enemy[0].surf, (Width*0.5-chosen_enemy[0].width*0.5, 85)),
						(chosen_enemy[1].surf, (10, 85+chosen_enemy[0].height)),
						(chosen_enemy[2].surf, (Width*0.25-chosen_enemy[2].width*0.5, 95+chosen_enemy[0].height+chosen_enemy[1].height)),
						(chosen_enemy[3][0].surf, (20, 100+chosen_enemy[0].height+chosen_enemy[1].height+chosen_enemy[2].height)),
						(chosen_enemy[3][1].surf, (100, 100+chosen_enemy[0].height+chosen_enemy[1].height+chosen_enemy[2].height)),
						(chosen_enemy[3][2].surf, (180, 100+chosen_enemy[0].height+chosen_enemy[1].height+chosen_enemy[2].height)),
						(chosen_enemy[3][3].surf, (260, 100+chosen_enemy[0].height+chosen_enemy[1].height+chosen_enemy[2].height)),
						(chosen_enemy[4].surf, (Width*0.5+Width*0.25-chosen_enemy[4].width*0.5, 95+chosen_enemy[0].height+chosen_enemy[1].height)),
						(button_inv_back.surf, (button_inv_back.x, button_inv_back.y))
					]

					y = 0
					for i, drop in enumerate(chosen_enemy[5]):
						if i%3 == 0 and i != 0:
							y += 1
						
						
						x = Width*0.5+10 if i%3 == 0 else Width*0.5+Width*0.25-drop.width*0.5 if i%3 == 1 else Width-15-drop.width
						blits.append((drop.surf, (x, (100+chosen_enemy[0].height+chosen_enemy[1].height+drop.height)+23*y)))
											
					win.fblits(blits)
					pygame.draw.line(win, (255, 255, 255), (5, 90+chosen_enemy[0].height+chosen_enemy[1].height), (Width-7, 90+chosen_enemy[0].height+chosen_enemy[1].height))
					pygame.draw.line(win, (255, 255, 255), (Width*0.5, 90+chosen_enemy[0].height+chosen_enemy[1].height), (Width*0.5, 308))

			for button in main_buttons:
				button.outline = (255, 255, 255)
				if button.text_content.lower().startswith(sub_menu) or button.rect.collidepoint(mp):
					button.outline = (255, 128, 0)
			for button in buttons:
				if sub_menu == "bestiary" and button.rect.collidepoint(mp):
					pygame.draw.rect(win, (255, 128, 0), button, 1)
				else:
					button.outline = (255, 255, 255)
					if button.rect.collidepoint(mp):
						button.outline = (255, 128, 0)


			win.blit(brightness, (0, 0))


			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit(); sys.exit()

				if event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1:
						if button_inventory.rect.collidepoint(mp):
							sub_menu = "inv"
							buttons = []
						elif button_stats.rect.collidepoint(mp):
							sub_menu = "stats"
							buttons = [button_level]
						elif button_map.rect.collidepoint(mp):
							sub_menu = "map"
							buttons = []
						elif button_quests.rect.collidepoint(mp):
							scroll = 0
							sub_menu = "quests"
							buttons = quests
						elif button_bestiary.rect.collidepoint(mp):
							scroll = 0
							sub_menu = "bestiary"
							buttons = bestiary_buttons

				if event.type in [pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN, pygame.CONTROLLERBUTTONDOWN] and sub_menu == "inv":
					button = None
					if event.type == pygame.MOUSEBUTTONDOWN:
						button = event.button
					elif event.type == pygame.KEYDOWN:
						if event.key in [pygame.K_SPACE, pygame.K_RETURN]:
							button = 1
						elif event.key in [pygame.K_LSHIFT, pygame.K_RSHIFT, pygame.K_BACKSPACE]:
							button = 3
					else:
						if event.button == pygame.CONTROLLER_BUTTON_A:
							button = 1
						elif event.button == pygame.CONTROLLER_BUTTON_X:
							button = 3

					if button:
						if inventory.index < 6:
							rect = inventory.rects[1][inventory.index]
							if button == 1:
								inventory.unequip_item(rect[1])
							elif button == 3:
								game_map.full_drops.append(inventory.throw_eq_item(rect[1]))
								if game_map.full_drops[-1] == None:
									game_map.full_drops = game_map.full_drops[:-1]
						else:
							rect = inventory.rects[0][inventory.index-6]
							if rect[1] is not None:

								if button == 1:
									inventory.equip_item(rect[1])
								elif button == 3:
									game_map.full_drops.append(inventory.throw_inv_item(rect[1]))
									if game_map.full_drops[-1] == None:
										game_map.full_drops = game_map.full_drops[:-1]
						
						update_inv_stats()

				if event.type in [pygame.KEYDOWN, pygame.CONTROLLERBUTTONDOWN, pygame.CONTROLLERAXISMOTION] and sub_menu == "inv":
					button = None
					if event.type == pygame.KEYDOWN:
						if event.key in [pygame.K_w, pygame.K_UP]:
							button = pygame.CONTROLLER_BUTTON_DPAD_UP
						elif event.key in [pygame.K_s, pygame.K_DOWN]:
							button = pygame.CONTROLLER_BUTTON_DPAD_DOWN
						elif event.key in [pygame.K_a, pygame.K_LEFT]:
							button = pygame.CONTROLLER_BUTTON_DPAD_LEFT
						elif event.key in [pygame.K_d, pygame.K_RIGHT]:
							button = pygame.CONTROLLER_BUTTON_DPAD_RIGHT
						elif event.key == pygame.K_z:
							button = 0.1
						elif event.key == pygame.K_c:
							button = 0.2
						else:
							continue
					elif event.type == pygame.CONTROLLERAXISMOTION:
						if event.axis == 4 and event.value/32767 >= 0.5:
							button = 0.1
						elif event.axis == 5 and event.value/32767 >= 0.5:
							button = 0.2
						else:
							continue
					elif event.type == pygame.CONTROLLERBUTTONDOWN:
						if event.button in [pygame.CONTROLLER_BUTTON_DPAD_UP, pygame.CONTROLLER_BUTTON_DPAD_DOWN, pygame.CONTROLLER_BUTTON_DPAD_LEFT, pygame.CONTROLLER_BUTTON_DPAD_RIGHT]:
							button = event.button
						else:
							continue
					
					if button:
						inventory.select_slot(button)


			if (game_input.press(pygame.K_UP, "keys", controller) or game_input.press(pygame.K_w, "keys", controller) or game_input.press(pygame.CONTROLLER_BUTTON_DPAD_UP, "cons", controller)):
				if len(buttons) and sub_menu != "bestiary":
					if chosen_button == -1:
						chosen_button = 0
					else:
						if chosen_button == 0:
							chosen_button = len(buttons)-1
						else:
							chosen_button -= 1
					pygame.mouse.set_pos(buttons[chosen_button].x+buttons[chosen_button].width*0.5, buttons[chosen_button].y+buttons[chosen_button].height*0.5)
				elif sub_menu == "bestiary" and not chosen_enemy:
					inv_rows = len(bestiary_buttons) // 14
					last_row = len(bestiary_buttons) % 14
					ind_row = chosen_button // 14
					ind_col = chosen_button % 14
					ind_row_length = 14 if ind_row < inv_rows else last_row
					
					if ind_row > 0:
						chosen_button -= 14
					else:
						if ind_col < last_row:
							chosen_button = (inv_rows)*14+ind_col
						else:
							chosen_button = (inv_rows-1)*14+ind_col
					if chosen_button < 0:
						chosen_button = 0
					pygame.mouse.set_pos(buttons[chosen_button].x+buttons[chosen_button].width*0.5, buttons[chosen_button].y+buttons[chosen_button].height*0.5)
			elif (game_input.press(pygame.K_DOWN, "keys", controller) or game_input.press(pygame.K_s, "keys", controller) or game_input.press(pygame.CONTROLLER_BUTTON_DPAD_DOWN, "cons", controller)):
				if len(buttons) and sub_menu != "bestiary":
					if chosen_button == -1:
						chosen_button = 0
					else:
						if chosen_button == len(buttons)-1:
							chosen_button = 0
						else:
							chosen_button += 1
					pygame.mouse.set_pos(buttons[chosen_button].x+buttons[chosen_button].width*0.5, buttons[chosen_button].y+buttons[chosen_button].height*0.5)
				elif sub_menu == "bestiary" and not chosen_enemy:
					inv_rows = len(bestiary_buttons) // 14
					last_row = len(bestiary_buttons) % 14
					ind_row = chosen_button // 14
					ind_col = chosen_button % 14
					ind_row_length = 14 if ind_row < inv_rows else last_row
					
					if (ind_col < last_row and ind_row >= inv_rows) or (ind_col > last_row-1 and ind_row >= inv_rows-1):
						chosen_button = ind_col
					else:
						chosen_button += 14
					if chosen_button < 0:
						chosen_button = 0
					pygame.mouse.set_pos(buttons[chosen_button].x+buttons[chosen_button].width*0.5, buttons[chosen_button].y+buttons[chosen_button].height*0.5)
			elif (game_input.press(pygame.K_LEFT, "keys", controller) or game_input.press(pygame.K_a, "keys", controller) or game_input.press(pygame.CONTROLLER_BUTTON_DPAD_LEFT, "cons", controller)):
				if leveling:
					if buttons[0] == button_hp:
						buttons = [button_ap1, button_dp]
						if player.classes[1]:
							buttons.insert(1, button_ap2)
						chosen_button = 0
						pygame.mouse.set_pos(buttons[chosen_button].x+buttons[chosen_button].width*0.5, buttons[chosen_button].y+buttons[chosen_button].height*0.5)
				elif sub_menu == "bestiary" and not chosen_enemy:
					inv_rows = len(bestiary_buttons) // 14
					last_row = len(bestiary_buttons) % 14
					ind_row = chosen_button // 14
					ind_col = chosen_button % 14
					ind_row_length = 14 if ind_row < inv_rows else last_row
					
					if ind_col > 0:
						chosen_button -= 1
					else:
						chosen_button = ind_row*14+ind_row_length-1
					if chosen_button < 0:
						chosen_button = 0
					pygame.mouse.set_pos(buttons[chosen_button].x+buttons[chosen_button].width*0.5, buttons[chosen_button].y+buttons[chosen_button].height*0.5)
			elif (game_input.press(pygame.K_RIGHT, "keys", controller) or game_input.press(pygame.K_d, "keys", controller) or game_input.press(pygame.CONTROLLER_BUTTON_DPAD_RIGHT, "cons", controller)):
				if leveling:
					if buttons[0] == button_hp:
						buttons = [button_ap1, button_dp, button_level]
						if player.classes[1]:
							buttons.insert(1, button_ap2)
						chosen_button = 0
						pygame.mouse.set_pos(buttons[chosen_button].x+buttons[chosen_button].width*0.5, buttons[chosen_button].y+buttons[chosen_button].height*0.5)
				elif sub_menu == "bestiary" and not chosen_enemy:
					inv_rows = len(bestiary_buttons) // 14
					last_row = len(bestiary_buttons) % 14
					ind_row = chosen_button // 14
					ind_col = chosen_button % 14
					ind_row_length = 14 if ind_row < inv_rows else last_row
					
					if ind_col < ind_row_length-1:
						chosen_button += 1
					else:
						chosen_button = ind_row*14
					if chosen_button < 0:
						chosen_button = 0
					pygame.mouse.set_pos(buttons[chosen_button].x+buttons[chosen_button].width*0.5, buttons[chosen_button].y+buttons[chosen_button].height*0.5)
			elif (game_input.press(pygame.K_RETURN, "keys", controller) or game_input.press(pygame.K_SPACE, "keys", controller) or game_input.press(pygame.K_KP_ENTER, "keys", controller) or game_input.press(pygame.CONTROLLER_BUTTON_A, "cons", controller) or game_input.press(pygame.CONTROLLER_BUTTON_START, "cons", controller) or game_input.press(1, "keys", controller)):
				if sub_menu == "stats":
					leveled = False
					if button_level.rect.collidepoint(mp) and player.available_levels > 0:
						k_c = (game_input.hold(pygame.K_RETURN, "keys", controller) or game_input.hold(pygame.K_SPACE, "keys", controller) or game_input.hold(pygame.K_KP_ENTER, "keys", controller) or game_input.hold(pygame.CONTROLLER_BUTTON_A, "cons", controller) or game_input.hold(pygame.CONTROLLER_BUTTON_START, "cons", controller))
						leveling = not leveling
						if leveling:
							button_level.text_content = f"Leveling... ({player.available_levels})"

							buttons = [button_hp, button_sp, button_ep1, button_level]
							if player.classes[1]:
								buttons.insert(3, button_ep2)
							if k_c:
								chosen_button = 0
								pygame.mouse.set_pos(buttons[chosen_button].x+buttons[chosen_button].width*0.5, buttons[chosen_button].y+buttons[chosen_button].height*0.5)
						else:
							level_alpha = 255
							counter = 0
							button_level.text_content = f"Level Up ({player.available_levels})"
							leveled = True

							buttons = [button_level]
							if k_c:
								chosen_button = 0
								pygame.mouse.set_pos(buttons[chosen_button].x+buttons[chosen_button].width*0.5, buttons[chosen_button].y+buttons[chosen_button].height*0.5)

					elif button_hp.rect.collidepoint(mp) and leveling:
						player.stats["HP"][0] += 1
						player.stats["HP"][1] += 1
						leveled = True
					elif button_sp.rect.collidepoint(mp) and leveling:
						player.stats["SP"][0] += 1
						player.stats["SP"][1] += 1
						leveled = True
					elif button_ep1.rect.collidepoint(mp) and leveling:
						player.stats["EP"][0][0] += 1
						player.stats["EP"][0][1] += 1
						leveled = True
					elif button_ep2.rect.collidepoint(mp) and leveling and player.classes[1]:
						player.stats["EP"][1][0] += 1
						player.stats["EP"][1][1] += 1
						leveled = True
					elif button_ap1.rect.collidepoint(mp) and leveling:
						player.stats["AP"][0] += 1
						leveled = True
					elif button_ap2.rect.collidepoint(mp) and leveling and player.classes[1]:
						player.stats["AP"][1] += 1
						leveled = True
					elif button_dp.rect.collidepoint(mp) and leveling:
						player.stats["DP"] += 1
						leveled = True

					if leveled:
						player.available_levels -= 1

						if player.available_levels == 0:
							leveling = False
							button_level.text_content = f"Level Up ({player.available_levels})"
							level_alpha = 255
							counter = 0
						else:
							button_level.text_content = f"Leveling... ({player.available_levels})"

						hp_bar.set_alpha(level_alpha)
						sp_bar.set_alpha(level_alpha)
						ep1_bar.set_alpha(level_alpha)
						ep2_bar.set_alpha(level_alpha)
						
						surf_health.set_alpha(level_alpha)
						surf_stamina.set_alpha(level_alpha)
						surf_stat1.set_alpha(level_alpha)
						surf_stat2.set_alpha(level_alpha)
						surf_attack1.set_alpha(level_alpha)
						surf_attack2.set_alpha(level_alpha)
						surf_defense.set_alpha(level_alpha)

						text_hp.alpha = level_alpha
						text_sp.alpha = level_alpha
						text_ep[0].alpha = level_alpha
						text_ep[1].alpha = level_alpha
						text_ap[0].alpha = level_alpha
						text_ap[1].alpha = level_alpha
						text_dp.alpha = level_alpha

						update_inv_stats()
				elif sub_menu == "quests":
					for i, quest in enumerate(quests):
						if quest.rect.collidepoint([mp[0], mp[1]+scroll]) and not len(chosen_quest):
							desc_title = Text(os.path.join("assets", "fontsDL", "font.ttf"), "Description", 16, (255, 255, 255), bold=True)
							desc_text = Text(os.path.join("assets", "fontsDL", "font.ttf"), player_quests[i].data["desc"][langs.index(settings["lang"])], 16, (255, 255, 255), max_width=Width-91)
							requirements = []
							for ri, requirement in enumerate(player_quests[i].data["requirements_text"]):
								requirements.append(Text(os.path.join("assets", "fontsDL", "font.ttf"), requirement[langs.index(settings["lang"])], 16, (128, 128, 128) if player_quests[i].current_req == None or player_quests[i].data["requirements"].index(player_quests[i].current_req) > ri else (255, 255, 255), max_width=Width-91))
							
							reward_title = Text(os.path.join("assets", "fontsDL", "font.ttf"), "Rewards", 16, (255, 255, 255), bold=True)
							rewards = []
							for item in player_quests[i].reward["items"]:
								rewards.append((item[0], Text(os.path.join("assets", "fontsDL", "font.ttf"), f"x{item[1]}", 16, (255, 255, 255))))
							rewards.append(Text(os.path.join("assets", "fontsDL", "font.ttf"), str(player_quests[i].reward["money"]) if player_quests[i].reward["money"] else "", 16, (255, 255, 255)))
							rewards.append(Text(os.path.join("assets", "fontsDL", "font.ttf"), str(player_quests[i].reward["XP"]) if player_quests[i].reward["XP"] else "", 16, (255, 255, 255)))
							
							chosen_quest = [quest, desc_title, desc_text, requirements, reward_title, rewards]
							buttons = [button_inv_back]

							quest.outline = (255, 255, 255)
							k_c = (game_input.hold(pygame.K_RETURN, "keys", controller) or game_input.hold(pygame.K_SPACE, "keys", controller) or game_input.hold(pygame.K_KP_ENTER, "keys", controller) or game_input.hold(pygame.CONTROLLER_BUTTON_A, "cons", controller) or game_input.hold(pygame.CONTROLLER_BUTTON_START, "cons", controller))
							if k_c:
								chosen_button = 0
								pygame.mouse.set_pos(buttons[chosen_button].x+buttons[chosen_button].width*0.5, buttons[chosen_button].y+buttons[chosen_button].height*0.5)

						elif button_inv_back.rect.collidepoint(mp) and len(chosen_quest):
							buttons = quests
							k_c = (game_input.hold(pygame.K_RETURN, "keys", controller) or game_input.hold(pygame.K_SPACE, "keys", controller) or game_input.hold(pygame.K_KP_ENTER, "keys", controller) or game_input.hold(pygame.CONTROLLER_BUTTON_A, "cons", controller) or game_input.hold(pygame.CONTROLLER_BUTTON_START, "cons", controller))
							if k_c:
								chosen_button = quests.index(chosen_quest[0])
								pygame.mouse.set_pos(buttons[chosen_button].x+buttons[chosen_button].width*0.5, buttons[chosen_button].y+buttons[chosen_button].height*0.5)
							chosen_quest = []
				elif sub_menu == "bestiary":
					for button in bestiary_buttons:
						if button.rect.collidepoint([mp[0], mp[1]+scroll]) and not chosen_enemy and player.killed_enemies.count(button.text_content):
							enemy_name = Text(os.path.join("assets", "fontsDL", "font.ttf"), button.text_content, 16, (255, 255, 255), bold=True)
							info_text = Text(os.path.join("assets", "fontsDL", "font.ttf"), enemies_data[button.text_content]["bestiary"][langs.index(settings["lang"])], 16, (255, 255, 255), max_width=Width-20)
							stats_text = Text(os.path.join("assets", "fontsDL", "font.ttf"), "Stats", 16, (255, 255, 255), bold=True)
							stats = [
								Text(os.path.join("assets", "fontsDL", "font.ttf"), f"<sp:health> {enemies_data[button.text_content]['health'] if player.killed_enemies.count(button.text_content) >= 2 else '???'}", 16, (255, 255, 255)),
								Text(os.path.join("assets", "fontsDL", "font.ttf"), f"<sp:ap> {enemies_data[button.text_content]['attack'] if player.killed_enemies.count(button.text_content) >= 3 else '???'}", 16, (255, 255, 255)),
								Text(os.path.join("assets", "fontsDL", "font.ttf"), f"<sp:defense> {enemies_data[button.text_content]['defense'] if player.killed_enemies.count(button.text_content) >= 4 else '???'}", 16, (255, 255, 255)),
								Text(os.path.join("assets", "fontsDL", "font.ttf"), f"<sp:level> {enemies_data[button.text_content]['XP'] if player.killed_enemies.count(button.text_content) >= 2 else '???'}", 16, (255, 255, 255))
							]
							drops_text = Text(os.path.join("assets", "fontsDL", "font.ttf"), "Drops", 16, (255, 255, 255), bold=True)
							drops = []
							for drop in enemies_data[button.text_content]["drops"]:
								drops.append(Text(os.path.join("assets", "fontsDL", "font.ttf"), f"<sp:{drop[0]}> {f'{drop[1]}-{drop[2]}' if drop[1] != drop[2] else ''} {round((1/drop[3])*100, 1)if drop[3] else '100'}%", 16, (255, 255, 255)))
							
							chosen_enemy = [enemy_name, info_text, stats_text, stats, drops_text, drops, button]
							buttons = [button_inv_back]

							k_c = (game_input.hold(pygame.K_RETURN, "keys", controller) or game_input.hold(pygame.K_SPACE, "keys", controller) or game_input.hold(pygame.K_KP_ENTER, "keys", controller) or game_input.hold(pygame.CONTROLLER_BUTTON_A, "cons", controller) or game_input.hold(pygame.CONTROLLER_BUTTON_START, "cons", controller))
							if k_c:
								chosen_button = 0
								pygame.mouse.set_pos(buttons[chosen_button].x+buttons[chosen_button].width*0.5, buttons[chosen_button].y+buttons[chosen_button].height*0.5)

						elif button_inv_back.rect.collidepoint(mp) and chosen_enemy:
							buttons = bestiary_buttons
							k_c = (game_input.hold(pygame.K_RETURN, "keys", controller) or game_input.hold(pygame.K_SPACE, "keys", controller) or game_input.hold(pygame.K_KP_ENTER, "keys", controller) or game_input.hold(pygame.CONTROLLER_BUTTON_A, "cons", controller) or game_input.hold(pygame.CONTROLLER_BUTTON_START, "cons", controller))
							if k_c:
								chosen_button = bestiary_buttons.index(chosen_enemy[-1])
								pygame.mouse.set_pos(buttons[chosen_button].x+buttons[chosen_button].width*0.5, buttons[chosen_button].y+buttons[chosen_button].height*0.5)
							chosen_enemy = None
			elif (game_input.press(pygame.K_BACKSPACE, "keys", controller) or game_input.press(pygame.K_ESCAPE, "keys", controller) or game_input.press(settings["keys"]["inventory"], "keys", controller) or game_input.press(pygame.CONTROLLER_BUTTON_B, "cons", controller) or game_input.press(pygame.CONTROLLER_BUTTON_BACK, "cons", controller) or game_input.press(settings["cons"]["inventory"], "cons", controller)):
				unpause_time()
				menus = []
			elif game_input.press(pygame.K_e, "keys", controller) or game_input.press(pygame.CONTROLLER_BUTTON_RIGHTSHOULDER, "cons", controller):
				sub_menus = ["inv", "stats", "map", "quests", "bestiary"]
				i = sub_menus.index(sub_menu)
				if sub_menu == "bestiary":
					i = 0
				else:
					i += 1
				sub_menu = sub_menus[i]

				if sub_menu == "stats":
					buttons = [button_level]
				elif sub_menu == "quests":
					buttons = quests
				elif sub_menu == "bestiary":
					buttons = bestiary_buttons
			elif game_input.press(pygame.K_q, "keys", controller) or game_input.press(pygame.CONTROLLER_BUTTON_LEFTSHOULDER, "cons", controller):
				sub_menus = ["inv", "stats", "map", "quests", "bestiary"]
				i = sub_menus.index(sub_menu)
				if sub_menu == "inv":
					i = 4
				else:
					i -= 1
				sub_menu = sub_menus[i]

				if sub_menu == "stats":
					buttons = [button_level]
				elif sub_menu == "quests":
					buttons = quests
				elif sub_menu == "bestiary":
					buttons = bestiary_buttons
		elif menus[-1] == "pause":
			mp = list(mp)
			mp[0] -= Width*0.5-pause_surf.get_width()*0.5
			mp[1] -= Height*0.5-pause_surf.get_height()*0.5
			mp = tuple(mp)

			for button in buttons:
				button.outline = (255, 255, 255)
				if button.rect.collidepoint(mp) or (isinstance(button, Slider) and button.selected):
					button.outline = (255, 128, 0)

			pause_surf.fill((255, 255, 255))
			pause_surf.fill((0, 0, 0), (1, 1, 226, 148))
			pause_surf.fblits((
				(text_pause.surf, (114-text_pause.width*0.5, 0)),
				(button_resume.surf, (button_resume.x, button_resume.y)),
				(button_pause_settings.surf, (button_pause_settings.x, button_pause_settings.y)),
				(button_pause_quit.surf, (button_pause_quit.x, button_pause_quit.y))
			))
			win.fblits((
				(backdrop_surf, (0, 0)),
				(shadow_surf, (0, 0)),
				(pause_surf, (Width*0.5-pause_surf.get_width()*0.5, Height*0.5-pause_surf.get_height()*0.5)),
				(brightness, (0, 0))
			))

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit(); sys.exit()


			if (game_input.press(pygame.K_UP, "keys", controller) or game_input.press(pygame.K_w, "keys", controller) or game_input.press(pygame.CONTROLLER_BUTTON_DPAD_UP, "cons", controller)):
				if chosen_button == -1:
					chosen_button = 0
				else:
					if chosen_button == 0:
						chosen_button = len(buttons)-1
					else:
						chosen_button -= 1
				pygame.mouse.set_pos((buttons[chosen_button].x+buttons[chosen_button].width*0.5)+(Width*0.5-pause_surf.get_width()*0.5), (buttons[chosen_button].y+buttons[chosen_button].height*0.5)+(Height*0.5-pause_surf.get_height()*0.5))
			elif (game_input.press(pygame.K_DOWN, "keys", controller) or game_input.press(pygame.K_s, "keys", controller) or game_input.press(pygame.CONTROLLER_BUTTON_DPAD_DOWN, "cons", controller)):
				if chosen_button == -1:
					chosen_button = 0
				else:
					if chosen_button == len(buttons)-1:
						chosen_button = 0
					else:
						chosen_button += 1
				pygame.mouse.set_pos((buttons[chosen_button].x+buttons[chosen_button].width*0.5)+(Width*0.5-pause_surf.get_width()*0.5), (buttons[chosen_button].y+buttons[chosen_button].height*0.5)+(Height*0.5-pause_surf.get_height()*0.5))
			elif (game_input.press(pygame.K_RETURN, "keys", controller) or game_input.press(pygame.K_SPACE, "keys", controller) or game_input.press(pygame.K_KP_ENTER, "keys", controller) or game_input.press(pygame.CONTROLLER_BUTTON_A, "cons", controller) or game_input.press(pygame.CONTROLLER_BUTTON_START, "cons", controller) or game_input.press(1, "keys", controller)):
				if button_resume.rect.collidepoint(mp):
					unpause_time()
					pygame.mixer_music.unpause()
					camera.target = player
					menus = []
				elif button_pause_settings.rect.collidepoint(mp):
					menus.append("settings")
					buttons = default_menu_buttons[menus[-1]]
				elif button_pause_quit.rect.collidepoint(mp):
					menus = ["main"]
					buttons = default_menu_buttons[menus[-1]]
					play_music("assets/SOUND/music/main.ogg")

					paused_timers = {}
					near_death_surf.set_alpha(0)
					current_dialogue = None
					current_cutscene = None
					next_to_door = None
					cutscene_rects = 0
					save_data = None
					target_boss = None
					maps = {}
					bg_num = random.randint(0, 1)
					bg = sprite(f"mbg{bg_num}")
					bg.set_alpha(0)

					Player.classes = [None, None]
					Player.name = ""
					Player.equipment = equipment = ["No Primary", "No Secondry", "No Backpack", "No Helmet", "No Chest", "No Leggings"]
					Player.inventory = []
					Player.inv_size = 5
					Player.inv_weight = [0, None]
					Player.inv_max_exceed_time = 0
					Player.quests = []
					Player.stats = {}
					Player.available_levels = 0
					Player.map = None
					Player.killed_enemies = []
			elif (game_input.press(pygame.K_LSHIFT, "keys", controller) or game_input.press(pygame.K_RSHIFT, "keys", controller) or game_input.press(pygame.K_BACKSPACE, "keys", controller) or game_input.press(pygame.K_ESCAPE, "keys", controller) or game_input.press(pygame.CONTROLLER_BUTTON_B, "cons", controller) or game_input.press(pygame.CONTROLLER_BUTTON_BACK, "cons", controller) or game_input.press(3, "keys", controller)):
				unpause_time()
				menus = []
		elif menus[-1] == "mods":
			mp = list(mp)
			mp[0] -= 25
			mp[1] -= 25
			mp = tuple(mp)

			if not mod_info:
				menu_surf.fill((0, 0, 0))
				pygame.draw.line(menu_surf, (255, 255, 255), (250, 0), (250, menu_surf.get_height()))

				for button in main_buttons:
					if sub_menu != button.text_content.lower():
						button.outline = (255, 255, 255)
					if button.rect.collidepoint(mp):
						button.outline = (255, 128, 0)
				for button in buttons:
					if button in mod_buttons:
						button_surf = button[0].surf.subsurface((1, 1, button[0].width-2, button[0].height-2))
					else:
						button_surf = pygame.Surface((1, 1))
						button_surf.set_alpha(0)

					if isinstance(button, list):
						button = button[0]

					button.outline = (255, 255, 255)
					if button.rect.collidepoint(mp):
						button.outline = (255, 128, 0)

					button.surf.blit(button_surf, (1, 1))

				win.fblits((
					(backdrop_surf, (0, 0)),
					(shadow_surf, (0, 0))
				))
				blits = [
					(text_mods.surf, (250*0.5-text_mods.width*0.5, 0)),
					(button_assets.surf, (button_assets.x, button_assets.y)),
					(button_behavior.surf, (button_behavior.x, button_behavior.y)),
					(button_addons.surf, (button_addons.x, button_addons.y)),
					(button_mods_back.surf, (button_mods_back.x, button_mods_back.y))
				]
				if sub_menu:
					blits.append((texts[sub_menu].surf, ((Width-50-250)*0.5-texts[sub_menu].width*0.5+250, 0)))
					for button in mod_buttons:
						blits.append((button[0].surf, (button[0].x, button[0].y)))

				menu_surf.fblits(blits)
				pygame.draw.rect(menu_surf, (255, 255, 255), (0, 0, menu_surf.get_width(), menu_surf.get_height()), 1)
				win.fblits(((menu_surf, (25, 25)), (brightness, (0, 0))))
			else:
				win.fblits(((menu_surf, (25, 25)), (brightness, (0, 0))))

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit(); sys.exit()

				if event.type == pygame.KEYDOWN and event.key == pygame.K_F1:
					menus.append("music")
					buttons = default_menu_buttons[menus[-1]]
					play_music(musics[0])

			if (game_input.press(pygame.K_UP, "keys", controller) or game_input.press(pygame.K_w, "keys", controller) or game_input.press(pygame.CONTROLLER_BUTTON_DPAD_UP, "cons", controller)):
				if chosen_button == -1:
					chosen_button = 0
				else:
					if chosen_button == 0:
						chosen_button = len(buttons)-1
					else:
						chosen_button -= 1
				
				if isinstance(buttons[chosen_button], list):
					button = buttons[chosen_button][0]
				else:
					button = buttons[chosen_button]
				pygame.mouse.set_pos(button.x+button.width*0.5+25, button.y+button.height*0.5+25)
			if (game_input.press(pygame.K_DOWN, "keys", controller) or game_input.press(pygame.K_s, "keys", controller) or game_input.press(pygame.CONTROLLER_BUTTON_DPAD_DOWN, "cons", controller)):
				if chosen_button == -1:
					chosen_button = 0
				else:
					if chosen_button == len(buttons)-1:
						chosen_button = 0
					else:
						chosen_button += 1
				
				if isinstance(buttons[chosen_button], list):
					button = buttons[chosen_button][0]
				else:
					button = buttons[chosen_button]
				pygame.mouse.set_pos(button.x+button.width*0.5+25, button.y+button.height*0.5+25)
			if (game_input.press(pygame.K_RETURN, "keys", controller) or game_input.press(pygame.K_SPACE, "keys", controller) or game_input.press(pygame.K_KP_ENTER, "keys", controller) or game_input.press(pygame.CONTROLLER_BUTTON_A, "cons", controller) or game_input.press(pygame.CONTROLLER_BUTTON_START, "cons", controller) or game_input.press(1, "keys", controller)):
				if not mod_info:
					if button_assets.rect.collidepoint(mp):
						sub_menu = "asset"
						changing_menu = True
					elif button_behavior.rect.collidepoint(mp):
						sub_menu = "behavior"
						changing_menu = True
					elif button_addons.rect.collidepoint(mp):
						sub_menu = "addon"
						changing_menu = True
					elif button_mods_back.rect.collidepoint(mp):
						if loaded_mods != starting_mods:
							dump_json(["mods", "loaded_mods.json"], loaded_mods)
							pygame.quit()
							subprocess.call([sys.executable, os.path.realpath(__file__)] + sys.argv[1:])
							sys.exit()
						else:
							del menus[-1]
							try:
								menu = menus[-1]
							except IndexError:
								menu = None
					elif sub_menu:
						for button in mod_buttons:
							button, mod_name, data, info_button = button

							if info_button.rect.collidepoint(mp) and data and data["info"]:
								mod_info = True

								title = Text(os.path.join("assets", "fontsDL", "font.ttf"), f"{data['name']}'s Info", 32, (255, 255, 255))
								text = Text(os.path.join("assets", "fontsDL", "font.ttf"), data["info"], 16, (255, 255, 255), max_width=menu_surf.get_width()-10, align=pygame.FONT_CENTER)

								menu_surf.fill((0, 0, 0))
								menu_surf.fblits((
									(title.surf, (menu_surf.get_width()*0.5-title.width*0.5, 0)),
									(text.surf, (menu_surf.get_width()*0.5-text.width*0.5, title.height+5)),
									(button_info_back.surf, (button_info_back.x, button_info_back.y))
								))
								pygame.draw.rect(menu_surf, (255, 255, 255), (0, 0, menu_surf.get_width(), menu_surf.get_height()), 1)

								buttons = [button_info_back]
								chosen_button = 0

							elif button.rect.collidepoint(mp):
								if sub_menu == "asset":
									loaded_mods[0] = mod_name
								elif sub_menu == "behavior":
									loaded_mods[1] = mod_name
								else:
									if mod_name in loaded_mods[2]:
										loaded_mods[2].remove(mod_name)
									else:
										loaded_mods[2].append(mod_name)
				else:
					if button_info_back.rect.collidepoint(mp):
						mod_info = False
			
				if changing_menu:
					buttons = []
					chosen_button = 0

					grab_mods(sub_menu)
						
						
					buttons = mod_buttons


					if not game_input.hold(1, "keys", controller):
						if isinstance(buttons[chosen_button], list):
							button = buttons[chosen_button][0]
						else:
							button = buttons[chosen_button]
						pygame.mouse.set_pos(button.x+button.width*0.5+25, button.y+button.height*0.5+25)
				changing_menu = False
			if (game_input.press(pygame.K_LSHIFT, "keys", controller) or game_input.press(pygame.K_RSHIFT, "keys", controller) or game_input.press(pygame.K_BACKSPACE, "keys", controller) or game_input.press(pygame.K_ESCAPE, "keys", controller) or game_input.press(pygame.CONTROLLER_BUTTON_B, "cons", controller) or game_input.press(pygame.CONTROLLER_BUTTON_BACK, "cons", controller) or game_input.press(3, "keys", controller)):
				if sub_menu:
					sub_menu = None
					buttons = [button_assets, button_behavior, button_addons, button_mods_back]
					for i, button in enumerate(buttons):
						if button.outline == (255, 128, 0):
							chosen_button = i
							break
					pygame.mouse.set_pos(buttons[chosen_button].x+buttons[chosen_button].width*0.5+25, buttons[chosen_button].y+buttons[chosen_button].height*0.5+25)
				else:
					if loaded_mods != starting_mods:
						dump_json(["mods", "loaded_mods.json"], loaded_mods)
						pygame.quit()
						subprocess.call([sys.executable, os.path.realpath(__file__)] + sys.argv[1:])
						sys.exit()
					else:
						del menus[-1]
						buttons = default_menu_buttons[menus[-1]]
			if (game_input.press(pygame.K_r, "keys", controller) or game_input.press(pygame.CONTROLLER_BUTTON_Y, "cons", controller) or game_input.press(2, "keys", controller)):
				pass
		elif menus[-1] == "music":
			win.fill((0, 0, 0))
			win.fblits((
				(text_musicroom.surf, (Width*0.5-text_musicroom.width*0.5, 20)),
				(text_music.surf, (Width*0.5-text_music.width*0.5, 84)),
				(pre_arrow_surf, (button_prevmus.x, button_prevmus.y)),
				(post_arrow_surf, (button_postmus.x, button_postmus.y)),
				(button_mus_back.surf, (button_mus_back.x, button_mus_back.y)),
				(brightness, (0, 0))
			))

			if button_mus_back.rect.collidepoint(mp):
				button_mus_back.outline = (255, 128, 0)
			else:
				button_mus_back.outline = (255, 255, 255)

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit(); sys.exit()

				if event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1:
						mus_index = musics.index(music)
						if button_postmus.rect.collidepoint(mp):
							if mus_index == len(musics)-1:
								play_music(musics[0])
							else:
								play_music(musics[mus_index+1])
							text_music.content = music.split(splitter)[-1][:-4]
						elif button_prevmus.rect.collidepoint(mp):
							if mus_index == 0:
								play_music(musics[len(musics)-1])
							else:
								play_music(musics[mus_index-1])
							text_music.content = music.split(splitter)[-1][:-4]
						elif button_mus_back.rect.collidepoint(mp):
							del menus[-1]
							buttons = default_menu_buttons[menus[-1]]
					elif event.button == 3:
						del menus[-1]
						buttons = default_menu_buttons[menus[-1]]
			
				if event.type == pygame.KEYDOWN:
					if event.key in [pygame.K_LSHIFT, pygame.K_RSHIFT, pygame.K_BACKSPACE, pygame.K_ESCAPE, pygame.K_F1]:
						del menus[-1]
						buttons = default_menu_buttons[menus[-1]]
					elif event.key in [pygame.K_LEFT, pygame.K_a]:
						mus_index = musics.index(music)
						if mus_index == 0:
							play_music(musics[len(musics)-1])
						else:
							play_music(musics[mus_index-1])
						text_music.content = music.split(splitter)[-1][:-4]
					elif event.key in [pygame.K_RIGHT, pygame.K_d]:
						mus_index = musics.index(music)
						if mus_index == len(musics)-1:
							play_music(musics[0])
						else:
							play_music(musics[mus_index+1])
						text_music.content = music.split(splitter)[-1][:-4]


		if debug_menu:
			debug([[tile.main_rect for tile in game_map.tiles.values()], [drop[1].rect for drop in game_map.drops], [enemy.rect for enemy in game_map.enemies], [proj.rect for proj in game_map.projs]] if not len(menus) else [])
		
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
	ctypes.windll.user32.MessageBoxW(0, f"{error}\n\nPlease check \"scripts{splitter}logs.txt\" for the complete error and report it at https://discord.com/channels/797430217819291688/797430218251173916 (the server link: https://discord.gg/sXNeuPdeEj)\n Thank you :)", error_title, 0x10)

	with open(os.path.join("scripts", "logs.txt"), "w", errors="ignore", encoding="utf-8") as f:
		f.write(crash_logs)
