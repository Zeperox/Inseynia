class Quest:
	def __init__(self):
		self.file_name = "alice_letter"

		self.completed = False
		self.type = "deliver"
		self.data = {
			"title": ["Important Letter"],
			"desc": ["You've got a letter from Alice and she wants you to send the letter to a guy named Bob"],
			"requirements_text": [["Deliver the letter to bob"], ["Return to Alice"]],
			"requirements": ["bob_deliver", "confirm"]
		}
		self.current_req = self.data["requirements"][0]
		self.reward = {
			"items": [["blood meat", 1]],
			"money": 1,
			"XP": 1
		}
		self.rewarded = False

	def start(self, player, dialogue):
		if len(player.inventory) < player.inv_size:
			player.inventory.append("Alice's Letter")
			dialogue.quest = "progress"
		else:
			return True

	def check(self, game_map, current_dialogue, player, last_enemy_killed):
		if not self.completed:
			if current_dialogue:
				if self.current_req == "bob_deliver":
					if current_dialogue.id.startswith("npc:NPC_bob:0") and "Alice's Letter" in player.inventory:
						current_dialogue.previous_id.append([current_dialogue.id, current_dialogue.text_index+1])
						current_dialogue.id = "npc:NPC_bob:0.alice_quest"
						current_dialogue.text_index = 0

						player.inventory.remove("Alice's Letter")
						self.current_req = self.data["requirements"][self.data["requirements"].index(self.current_req)+1]

				elif self.current_req == "confirm":
					if current_dialogue.id.startswith("npc:NPC_alice:0"):
						current_dialogue.quest = "end"
						current_dialogue.text_index = 0
						self.current_req = None

						if not self.completed:
							for item in self.reward["items"]:
								for _ in range(item[1]):
									player.inventory.append(item[0])
							player.stats["M"] += self.reward["money"]
							player.stats["XP"][0] += self.reward["XP"]

						self.completed = True
						