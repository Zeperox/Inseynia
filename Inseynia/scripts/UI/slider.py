import pygame
from pygame.locals import SRCALPHA

from .text import Text

class Slider:
    def __init__(self, x: int, y: int, width: int, height: int, color: tuple[int, int, int]=None, min_val=0, max_val=100, is_list: list=[], choppy: bool=False, width_fill: int=40, color_fill: tuple[int, int, int]=None,
        text: str="", text_color: tuple[int, int, int]=(255,255,255), outline: tuple[int, int, int]=None, outline_thickness: int=2, font_path: str=None, font_size: int=None,
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self._color = color

        self.min_val = min_val
        self.max_val = max_val
        self.list = is_list
        self.choppy = choppy

        self.surf = pygame.Surface((width+1, height+1), SRCALPHA)
        self._outline = outline
        self._outline_thickness = outline_thickness

        self.width_fill = width_fill
        self._color_fill = color_fill
        self.selected = False

        font_size = self.height*0.5 if not font_size else font_size
        if text:
            self.text = Text(font_path, text, font_size, text_color)
        else:
            self.text = None

        self.selector_rect_x = self.width_fill-40
        self.selector_rect_height = self.height

        self.update_surf()
    
    def update_surf(self):
        self.surf = pygame.Surface((self.width+1, self.height+1), SRCALPHA)
        self.selector_rect_x = self.width_fill-40
        self.selector_rect_height = self.height

        if self._color:
            self.surf.fill(self._color)
        if self._color_fill:
            pygame.draw.rect(self.surf, self._color_fill, (0, 0, self.width_fill, self.height))
        if self._outline:
            pygame.draw.rect(self.surf, self._outline, (0, 0, self.width, self.height), self._outline_thickness)
        pygame.draw.rect(self.surf, (195, 197, 202), (self.selector_rect_x, 0, 40, self.selector_rect_height))

        if self.text:
            self.text.render(self.surf, (self.width*0.5 - self.text.width*0.5, self.height*0.5 - self.text.height*0.5))

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, win: pygame.Surface, scroll: list[int, int]=[0, 0]):
        win.blit(self.surf, (self.x-scroll[0], self.y-scroll[1]))

    def is_over(self, pos):
        self.selected = self.rect.collidepoint(pos)
        
        return self.selected
    
    def update_value(self, pos=None, slide_data=[None, 10]):
        if pos:
            if pos[0] < self.x+40:
                self.width_fill = 40
            elif pos[0] > self.x+self.width:
                self.width_fill = self.width
            else:
                '''if self.choppy:
                    self.width_fill = '''
                self.width_fill = pos[0]-self.x
        else:
            if slide_data[0] == 4:
                self.width_fill += slide_data[1]
            if slide_data[0] == 5:
                self.width_fill -= slide_data[1]
            
        self.update_surf()

        if self.width_fill <= 40:
            val = self.min_val
        elif self.width_fill >= self.width:
            val = self.max_val
        else:
            if len(self.list) == 0:
                val = ((self.max_val-self.min_val)/100)*((self.width_fill-40)/(self.width-40)*100)+self.min_val
            else:
                val = self.list[int((len(self.list)/100)*((self.width_fill-40)/(self.width-40)*100))]

        return val


    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = color if color != "None" else None
        self.update_surf()

    @property
    def color_fill(self):
        return self._color_fill

    @color.setter
    def color_fill(self, color):
        self._color_fill = color if color != "None" else None
        self.update_surf()

    @property
    def outline(self):
        return self._outline

    @outline.setter
    def outline(self, outline_color):
        self._outline = outline_color if outline_color != "None" else None
        self.update_surf()

    @property
    def text_content(self):
        return self.text.content

    @text_content.setter
    def text_content(self, text):
        self.text.content = text
        self.update_surf()
