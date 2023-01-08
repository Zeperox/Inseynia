import random, time, os, copy
from scripts.loading.json_functions import load_json
from .entity import Entity
from scripts.loading.sprites import sprites
from scripts.visuals.dialogue import Dialogue
from scripts.visuals.text import Text

class NPC(Entity):
	def __init__(self, x, y, id, anger_attack, name, stats=None, dialogue=None, moveable=False, collideable=True):
		super().__init__(x, y, os.path.join("assets", "ANIMATIONSDL", name) if name in os.listdir(os.path.join("assets", "ANIMATIONSDL")) else sprites[name])
		self.id = id
		self.dialogue = dialogue
		self.moveable = moveable
		self.collideable = collideable
		self.name = name
		self.anger_attack = anger_attack

		self.attacked = False
		stats = copy.deepcopy(stats)
		if not stats:
			self.stats = {
				"HP": [30, 30],
				"SP": 2,
				"XP": 0
			}
			self.knockback_resist = 0
		else:
			self.stats = {
				"HP": [stats["health"], stats["health"]],
				"AP": stats["attack"],
				"DP": stats["defense"],
				"SP": stats["speed"],
				"V": stats["view"],
				"SV": stats["suspicious view"],
				"XP": stats["XP"],
				"knockback resistence": stats["knockback resistence"]
			}
			self.knockback_resist = stats["knockback resistence"]
		self.damage_counters = []

		anger_dialogues = []
		for anger_dialogue_id in load_json(["scripts", "data", "text.json"]).keys():
			if anger_dialogue_id.startswith(f"npc:attack={anger_attack}"):
				anger_dialogues.append(anger_dialogue_id)
		self.anger_dialogue = Dialogue(random.choice(anger_dialogues))
		for lang in self.anger_dialogue.texts.keys():
			self.anger_dialogue.texts[lang][0][0] = self.dialogue.texts[lang][0][0]

		self.trigger_rect = self.rect.inflate(self.rect.width*2, self.rect.height*2)
		self.trigger_rect.center = self.rect.center

	def draw(self, win, scroll: list[int, int]):
		super().draw(win, scroll)
		for dmg_counter in self.damage_counters:
			dmg_counter[0].render(win, (dmg_counter[1][0][0], dmg_counter[1][0][1]), scroll)

	def move(self, game_map):
		pass

	def trigger_dialogue(self, player):
		if self.dialogue and player.rect.colliderect(self.trigger_rect):
			return True

	def damage(self, dmg, proj):
		hit = False
		main_dmg = dmg
		critical = False
		if self.collidable and self.active:
			hit = True
			if time.time()-self.i_frame >= self.i_time:
				dmg *= random.uniform(0.75, 1.25)
				if random.randint(0, 10) == 0:
					dmg *= 1.75
					critical = True
				dmg = round(dmg*dmg/(dmg+self.stats["DP"]))
				if dmg == 0: dmg = 1

				self.stats["HP"][0] -= dmg
				self.i_frame = time.time()


				if dmg < main_dmg:
					c = (211, 142, 23)
					s = 2
				elif dmg >= main_dmg and not critical:
					c = (244, 111, 9)
					s = 2
				elif critical:
					c = (204, 23, 0)
					s = 3
				self.damage_counters.append([Text(os.path.join("assets", "fontsDL", "font.png"), str(dmg), s, c), [list(self.rect.center), 10, False]])

		return self.stats["HP"][0], hit, critical
