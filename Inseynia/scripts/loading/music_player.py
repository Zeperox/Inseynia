import pygame, os

class Music:
    def __init__(self, path, loops=-1, start_ms=0, fade=[0, 0], volume=1):
        self.path = path[0]
        for location_entry in path[1:]:
            self.path = os.path.join(self.path, location_entry)
        
        self.loops = loops
        self.start_ms = start_ms
        self.fade = fade
        self.volume = volume
        
        self.playing = False
        self.paused = False

    def set_volume(self, volume=None, _set=False):
        if volume == None:
            pygame.mixer.music.set_volume(self.volume)
        else:
            pygame.mixer.music.set_volume(volume)
            if _set:
                self.volume = volume

    def start(self):
        pygame.mixer.music.unload()
        pygame.mixer.music.load(self.path)
        self.set_volume()
        pygame.mixer.music.play(self.loops, self.start_ms, self.fade[0])
        self.playing = True

    def end(self, fade=False):
        if not fade:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
        else:
            pygame.mixer.music.fadeout(self.fade[1])
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.unload()
        self.playing = False

    def set_pos(self, pos):
        pygame.mixer.music.set_pos(pos)

    def restart(self, full_restart=False):
        if full_restart:
            self.end()
            self.start()
        else:
            pygame.mixer.music.rewind()

    def toggle_pause(self, always_action=[False, False]):
        if always_action[0]:
            pygame.mixer.music.pause()
            self.paused = True
        elif always_action[1]:
            pygame.mixer.music.unpause()
            self.paused = False
        else:
            if self.paused:
                pygame.mixer.music.unpause()
                self.paused = False
            else:
                pygame.mixer.music.pause()
                self.paused = True

    def get_pos(self):
        return pygame.mixer.music.get_pos()

    def get_busy(self):
        return pygame.mixer.music.get_busy()


musics: dict[Music] = {}
for music in os.scandir(os.path.join("assets", "SOUND", "songs")):
    if music.is_file():
        musics[music.name[:-4]] = Music(["assets", "SOUND", "songs", music.name])

for mod in os.scandir(os.path.join("mods")):
    if mod.is_dir():
        try:
            for music in os.scandir(os.path.join("mods", mod.name, "assets", "SOUND", "songs")):
                if music.is_file():
                    musics[music.name[:-4]] = Music(["mods", mod.name, "assets", "SOUND", "songs", music.name])
        except:
            continue

if __name__ == "__main__":
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()
    while True:
        for music in musics.values():
            music.loops = 0
            music.start()
            while music.get_busy():
                pass