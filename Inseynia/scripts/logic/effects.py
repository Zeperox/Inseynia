import time, os

from scripts.loadingDL.files import files

Text = files["text"].Text

class DefaultEffect:
    def __init__(self, entity, seconds, amplify):
        self.entity = entity
        self.seconds = seconds
        self.amplify = amplify

        self.start_time = time.time()
        self.per_time = 0
        self.pause_time = 0
        self.paused = False

    def affect(self):
        if time.time()-self.start_time >= self.seconds and self in self.entity.effects:
            self.entity.effects.remove(self)

    def pause(self):
        if not self.paused:
            self.pause_time = self.start_time
        self.paused = True

    def unpause(self):
        if self.paused:
            self.start_time = time.time()-(time.time()-self.pause_time)
        self.paused = False

class AddHealth(DefaultEffect):
    def affect(self):
        if time.time()-self.per_time >= 0.5 and self.entity.stats["HP"][0] < self.entity.stats["HP"][1]:
            health_added = self.amplify
            self.entity.stats["HP"][0] += self.amplify
            if self.entity.stats["HP"][0] > self.entity.stats["HP"][1]:
                health_added -= self.player.stats["HP"][0] - self.player.stats["HP"][1]
                self.entity.stats["HP"][0] = self.entity.stats["HP"][1]
            self.entity.damage_counters.append([Text(os.path.join("assets", "fontsDL", "font.ttf"), str(health_added), 16, (32, 140, 24), bold=True), list(self.entity.rect.center)])
            
            self.per_time = time.time()

        super().affect()

class AddStamina(DefaultEffect):
    def affect(self):
        super().affect()

        if isinstance(self.entity, files["player"].Player):
            if time.time()-self.per_time >= 0.5 and self.entity.stats["SP"][0] < self.entity.stats["SP"][1]:
                self.entity.stats["SP"][0] += self.amplify
                if self.entity.stats["SP"][0] > self.entity.stats["SP"][1]:
                    self.entity.stats["SP"][0] = self.entity.stats["SP"][1]
                
                self.per_time = time.time()

class AddMana(DefaultEffect):
    def affect(self):
        super().affect()

        if isinstance(self.entity, files["player"].Player) and "Mage" in self.entity.classes:
            mana = self.entity.classes.index("Mage")
            if time.time()-self.per_time >= 0.5 and self.entity.stats["EP"][mana][0] < self.entity.stats["EP"][mana][1]:
                self.entity.stats["EP"][mana][0] += self.amplify
                if self.entity.stats["EP"][mana][0] > self.entity.stats["EP"][mana][1]:
                    self.entity.stats["EP"][mana][0] = self.entity.stats["EP"][mana][1]

                self.per_time = time.time()

class AddQuiver(DefaultEffect):
    def affect(self):
        super().affect()

        if isinstance(self.entity, files["player"].Player) and "Archer" in self.entity.classes:
            projs = self.entity.classes.index("Archer")
            if time.time()-self.per_time >= 0.5 and self.entity.stats["EP"][projs][0] < self.entity.stats["EP"][projs][1]:
                self.entity.stats["EP"][projs][0] += self.amplify
                if self.entity.stats["EP"][projs][0] > self.entity.stats["EP"][projs][1]:
                    self.entity.stats["EP"][projs][0] = self.entity.stats["EP"][projs][1]

                self.per_time = time.time()

class Poison(DefaultEffect):
    def affect(self):
        if time.time()-self.per_time >= 0.5 and self.entity.stats["HP"][0] > 0:
            health_added = self.amplify
            self.entity.stats["HP"][0] -= self.amplify
            self.entity.damage_counters.append([Text(os.path.join("assets", "fontsDL", "font.ttf"), str(health_added), 16, (244, 111, 9), bold=True), list(self.entity.rect.center)])
            
            self.per_time = time.time()

        super().affect()


effects = {
    "AddHealth": AddHealth,
    "AddStamina": AddStamina,
    "AddMana": AddMana,
    "AddQuiver": AddQuiver,
    "Poison": Poison,
}
