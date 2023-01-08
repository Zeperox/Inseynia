import math, pygame, os

from .dialogue import Dialogue
from scripts.logic.entity import Entity
from scripts.loading.json_functions import load_json

entity_based_animations = ["goto", "cameralock", "move"]

class Cutscene:
	def __init__(self, id):
		self.id = id

		self.animation_command = load_json(["scripts", "data", "cutscenes.json"])[id]
		self.animaion_index = 0
		self.triggered = False
		self.pause = 0
		self.dialogue_num = 0
		self.dialogue = False

	def _next_frame(self, curr_animation):
		for other_animation in self.animation_command[self.animaion_index]:
			if other_animation != curr_animation:
				try:
					self.animation_command[self.animaion_index+1].append(other_animation)
				except:
					self.animation_command.append([])
					self.animation_command[self.animaion_index+1].append(other_animation)

		self.animaion_index += 1

	def _command(self, game_map, player, camera, dt):
		if self.animaion_index >= len(self.animation_command):
			self.triggered = True
			return True

		for animation_num, curr_animations in enumerate(self.animation_command[self.animaion_index]):
			curr_animation = curr_animations.split(" ")
			if curr_animation[0] in entity_based_animations:
				if curr_animation[1] == "player":
					entity = player
				elif curr_animation[1] == "camera":
					entity = camera
				else:
					for entity in game_map.cutscene_entities:
						if entity[1] == curr_animation[1]:
							entity = entity[0]
							break

			if curr_animation[0] == "move": # move <entity> <xunits> <yunits> [speed]
				self.animation_command[self.animaion_index][animation_num] = self.animation_command[self.animaion_index][animation_num].split(" ")
				self.animation_command[self.animaion_index][animation_num][0] = "goto"
				self.animation_command[self.animaion_index][animation_num][2] = str(float(curr_animation[2])+entity.x)
				self.animation_command[self.animaion_index][animation_num][3] = str(float(curr_animation[3])+entity.y)
				self.animation_command[self.animaion_index][animation_num] = " ".join(self.animation_command[self.animaion_index][animation_num])
				
			if curr_animation[0] == "goto": # goto <entity> <xloc> <yloc> [speed]
				entity.movement = [0, 0]

				if len(curr_animation) == 5:
					speed = float(curr_animation[4])
				else:
					speed = 3
					
				try:
					vel = (pygame.Vector2(float(curr_animation[2]), float(curr_animation[3])) - pygame.Vector2(entity.x, entity.y)).normalize()*speed
				except:
					vel = (pygame.Vector2(float(curr_animation[2]), float(curr_animation[3])) - pygame.Vector2(entity.x, entity.y))
					vel.x += 1
					vel = vel.normalize()*speed

				if vel.x < 0:
					entity.flip = True
				else:
					entity.flip = False

				entity.movement[0] += vel.x*dt
				entity.movement[1] += vel.y*dt

				entity.movement_collision(game_map.tile_rects)
				
				# next frame
				if math.dist((entity.x, entity.y), (float(curr_animation[2]), float(curr_animation[3]))) <= 5:
					self._next_frame(curr_animations)

			elif curr_animation[0] == "cameralock": # cameralock <entity>
				camera.target = entity
				
				self._next_frame(curr_animations)

			elif curr_animation[0] == "dialogue" and not self.dialogue: # dialogue
				self.dialogue = True
				return Dialogue(str(self.id)+":"+str(self.dialogue_num))

			elif curr_animation[0] == "summon": # summon <entity> <x> <y> ["center"]
				if len(curr_animation) == 5:
					curr_animation[2] = str(float(curr_animation[2])+camera.scroll.x+camera.main_display.get_width()*0.5)
					curr_animation[3] = str(float(curr_animation[3])+camera.scroll.y+camera.main_display.get_height()*0.5)

				game_map.cutscene_entities.append([Entity(float(curr_animation[2]), float(curr_animation[3]), os.path.join("assets", "ANIMATIONSDL", curr_animation[1].replace("_", " "))), curr_animation[1]+str(len([cut_entity for cut_entity in game_map.cutscene_entities if entity[1].startswith(curr_animation[1])]))])

				self._next_frame(curr_animations)

			elif curr_animation[0] == "remove": # remove <entity>
				for cut_entity in game_map.cutscene_entities:
					if cut_entity[1] == curr_animation[1] and cut_entity in game_map.cutscene_entities:
						game_map.cutscene_entities.remove(cut_entity)
						break
				
				self._next_frame(curr_animations)

	def animate(self, game_map, player, camera, dt):
		done = self._command(game_map, player, camera, dt)
		return done
