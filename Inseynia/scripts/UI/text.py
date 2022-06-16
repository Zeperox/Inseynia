import pygame

class Text:
    def __init__(self, font_path: str, text: str, size: int, color: list[int, int, int]):
        self._font = font_path
        self._content = text
        self._size = size//7
        self.given_size = size
        self._color = list(color)
        self.spacing = 1*self._size
        
        self.font_img = pygame.image.load(self._font).convert()
        if self._color[0] == 128:
            self._color[0] = 127
        elif self._color[0] == 255:
            self._color[0] = 254
        elif self._color[0] == 0:
            self._color[0] = 1

        f_copy = pygame.Surface(self.font_img.get_size())
        f_copy.fill(self._color)
        self.font_img.set_colorkey((0, 0, 0))
        f_copy.blit(self.font_img, (0, 0))
        self.font_img = f_copy
        self.font_img.set_colorkey((255, 255, 255))
        
        self.character_order = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '.', '-', ',', ':', '+', "'", '!', '?', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '(', ')', '/', '_', '=', '\\', '[', ']', '*', '"', '<', '>', ';']
        current_char_width = 0
        self.characters = {}
        self.unchanged_characters = {}
        character_count = 0

        for x in range(self.font_img.get_width()):
            c = self.font_img.get_at((x, 0))
            if c[0] == 128:
                self.characters[self.character_order[character_count]] = self._clip(self.font_img, x-current_char_width, 0, current_char_width, self.font_img.get_height())
                self.unchanged_characters[self.character_order[character_count]] = self._clip(self.font_img, x-current_char_width, 0, current_char_width, self.font_img.get_height(), False)
                character_count += 1
                current_char_width = 0
            else:
                current_char_width += 1
        self.space_width = self.characters["A"].get_width()

        data = []
        x_offset = [0]
        y_offset = 0
        for char in self._content:
            if char == " ":
                x_offset[-1] += self.space_width+self.spacing
            elif char == "\n":
                x_offset.append(0)
                y_offset += self.characters["A"].get_height()+self.spacing
            else:
                data.append([self.characters[char], x_offset[-1], y_offset])
                x_offset[-1] += self.characters[char].get_width()+self.spacing

        self.surf = pygame.Surface((max(x_offset), y_offset+self.characters["A"].get_height()))
        self.surf.set_colorkey((0, 0, 0))
        for char in data:
            self.surf.blit(char[0], (char[1], char[2]))

    def _clip(self, surf: pygame.Surface, x: int, y: int, width: int, height: int, size_affect=True):
        handle_surf = surf.copy()
        clip_rect = pygame.Rect(x, y, width, height)

        handle_surf.set_clip(clip_rect)
        img = surf.subsurface(handle_surf.get_clip())
        if size_affect:
            return pygame.transform.scale(img, (img.get_width()*self._size, img.get_height()*self._size))
        else:
            return img

    def render(self, surf: pygame.Surface, loc: tuple[int, int], scroll: list[int, int]=[0, 0]):
        surf.blit(self.surf, (loc[0]-scroll[0], loc[1]-scroll[1]))

    @property
    def width(self):
        return self.surf.get_width()
    
    @property
    def height(self):
        return self.surf.get_height()
    

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, new_text):
        self._content = new_text
        data = []
        x_offset = [0]
        y_offset = 0
        for char in self._content:
            if char == " ":
                x_offset[-1] += self.space_width+self.spacing
            elif char == "\n":
                x_offset.append(0)
                y_offset += self.characters["A"].get_height()+self.spacing
            else:
                data.append([self.characters[char], x_offset[-1], y_offset])
                x_offset[-1] += self.characters[char].get_width()+self.spacing

        self.surf = pygame.Surface((max(x_offset), y_offset+self.characters["A"].get_height()))
        self.surf.set_colorkey((0, 0, 0))
        for char in data:
            self.surf.blit(char[0], (char[1], char[2]))

    @property
    def size(self):
        return self.given_size

    @size.setter
    def size(self, new_size):
        self._size = new_size//7
        self.given_size = new_size
        self.spacing = 1*self._size

        self.characters = self.unchanged_characters.copy()
        for char in self.characters.keys():
            self.characters[char] = pygame.transform.scale(self.characters[char], (self.characters[char].get_width()*self._size, self.characters[char].get_height()*self._size))
        self.space_width = self.characters["A"].get_width()

        data = []
        x_offset = [0]
        y_offset = 0
        for char in self._content:
            if char == " ":
                x_offset[-1] += self.space_width+self.spacing
            elif char == "\n":
                x_offset.append(0)
                y_offset += self.characters["A"].get_height()+self.spacing
            else:
                data.append([self.characters[char], x_offset[-1], y_offset])
                x_offset[-1] += self.characters[char].get_width()+self.spacing

        self.surf = pygame.Surface((max(x_offset), y_offset+self.characters["A"].get_height()))
        self.surf.set_colorkey((0, 0, 0))
        for char in data:
            self.surf.blit(char[0], (char[1], char[2]))

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, new_color):
        self._color = list(new_color)

        self.font_img = pygame.image.load(self._font).convert()
        if self._color[0] == 128:
            self._color[0] = 127
        elif self._color[0] == 255:
            self._color[0] = 254
        elif self._color[0] == 0:
            self._color[0] = 1
        
        f_copy = pygame.Surface(self.font_img.get_size())
        f_copy.fill(self._color)
        self.font_img.set_colorkey((0, 0, 0))
        f_copy.blit(self.font_img, (0, 0))
        self.font_img = f_copy
        self.font_img.set_colorkey((255, 255, 255))
        
        self.character_order = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '.', '-', ',', ':', '+', "'", '!', '?', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '(', ')', '/', '_', '=', '\\', '[', ']', '*', '"', '<', '>', ';']
        current_char_width = 0
        self.characters = {}
        self.unchanged_characters = {}
        character_count = 0

        for x in range(self.font_img.get_width()):
            c = self.font_img.get_at((x, 0))
            if c[0] == 128:
                self.characters[self.character_order[character_count]] = self._clip(self.font_img, x-current_char_width, 0, current_char_width, self.font_img.get_height())
                self.unchanged_characters[self.character_order[character_count]] = self._clip(self.font_img, x-current_char_width, 0, current_char_width, self.font_img.get_height(), False)
                character_count += 1
                current_char_width = 0
            else:
                current_char_width += 1
        self.space_width = self.characters["A"].get_width()

        data = []
        x_offset = [0]
        y_offset = 0
        for char in self._content:
            if char == " ":
                x_offset[-1] += self.space_width+self.spacing
            elif char == "\n":
                x_offset.append(0)
                y_offset += self.characters["A"].get_height()+self.spacing
            else:
                data.append([self.characters[char], x_offset[-1], y_offset])
                x_offset[-1] += self.characters[char].get_width()+self.spacing

        self.surf = pygame.Surface((max(x_offset), y_offset+self.characters["A"].get_height()))
        self.surf.set_colorkey((0, 0, 0))
        for char in data:
            self.surf.blit(char[0], (char[1], char[2]))

    @property
    def font(self):
        return self._font

    @font.setter
    def font(self, new_font):
        self._font = new_font

        self.font_img = pygame.image.load(self._font).convert()
        
        f_copy = pygame.Surface(self.font_img.get_size())
        f_copy.fill(self._color)
        self.font_img.set_colorkey((0, 0, 0))
        f_copy.blit(self.font_img, (0, 0))
        self.font_img = f_copy
        self.font_img.set_colorkey((255, 255, 255))
        
        self.character_order = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '.', '-', ',', ':', '+', "'", '!', '?', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '(', ')', '/', '_', '=', '\\', '[', ']', '*', '"', '<', '>', ';']
        current_char_width = 0
        self.characters = {}
        self.unchanged_characters = {}
        character_count = 0

        for x in range(self.font_img.get_width()):
            c = self.font_img.get_at((x, 0))
            if c[0] == 128:
                self.characters[self.character_order[character_count]] = self._clip(self.font_img, x-current_char_width, 0, current_char_width, self.font_img.get_height())
                self.unchanged_characters[self.character_order[character_count]] = self._clip(self.font_img, x-current_char_width, 0, current_char_width, self.font_img.get_height(), False)
                character_count += 1
                current_char_width = 0
            else:
                current_char_width += 1
        self.space_width = self.characters["A"].get_width()

        data = []
        x_offset = [0]
        y_offset = 0
        for char in self._content:
            if char == " ":
                x_offset[-1] += self.space_width+self.spacing
            elif char == "\n":
                x_offset.append(0)
                y_offset += self.characters["A"].get_height()+self.spacing
            else:
                data.append([self.characters[char], x_offset[-1], y_offset])
                x_offset[-1] += self.characters[char].get_width()+self.spacing

        self.surf = pygame.Surface((max(x_offset), y_offset+self.characters["A"].get_height()))
        self.surf.set_colorkey((0, 0, 0))
        for char in data:
            self.surf.blit(char[0], (char[1], char[2]))

if __name__ == "__main__":
    win = pygame.display.set_mode((800, 600))

    font = Text("assets/fontsDL/Font.png", "hello\nwo", 16, (0, 0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    print(font.font)
                
                if event.key == pygame.K_w:
                    print(font.content)
                
                if event.key == pygame.K_e:
                    print(font.size)
                
                if event.key == pygame.K_r:
                    print(font.color)
                
                if event.key == pygame.K_a:
                    font.font = ("assets/fontsDL/Font.png", "assets/fontsDL/Font2.png")[font.font == "assets/fontsDL/Font.png"]
                
                if event.key == pygame.K_s:
                    font.content = ("hello\nwo", "hello\nworld")[font.content == "hello\nwo"]
                
                if event.key == pygame.K_d:
                    font.size = (16, 25)[font.size == 16]
                
                if event.key == pygame.K_f:
                    font.color = ((255, 255, 255), (0, 0, 0))[font.color == [254, 255, 255]]
                
        win.fill((128,128,128))
        font.render(win, (100, 100))

        pygame.display.flip()
