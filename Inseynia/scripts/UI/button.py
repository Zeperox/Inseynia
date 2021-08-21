import pygame
from pygame.locals import *

class Button:
    def __init__(self, x:int, y:int, width:int, height:int, color:tuple[int, int, int]=(0,0,0), text:str="", text_color:tuple[int, int, int]=(255,255,255),
        outline:tuple[int, int, int]=None, outline_thickness:int=2, font_path:str=None, font_size:int=None
    ):
        self.x = x
        self.y = y
        self.width = width
        self.width_init = width
        self.height = height
        self.color = color

        self.text = text
        self.text_color = text_color

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.surf = pygame.Surface((width+1, height+1))
        self.outline = outline
        self.outline_thickness = outline_thickness
        self.font_path = font_path
        self.font_size = font_size

        self.update_surf()
        
    def update_surf(self):
        self.surf.fill(self.color)
        if self.outline:
            pygame.draw.rect(self.surf, self.outline, (0, 0, self.width, self.height), self.outline_thickness)

        if self.text:
            try:
                button_font = pygame.font.Font(self.font_path, self.font_size) if self.font_size else pygame.font.Font(self.font_path, int(self.height*0.5))
            except FileNotFoundError:
                button_font = pygame.font.SysFont(self.font_path, self.font_size) if self.font_size else pygame.font.SysFont(self.font_path, int(self.height*0.5))
            button_label = button_font.render(self.text, 1, self.text_color)
            if button_label.get_width() > self.width_init:
                self.width = button_label.get_width()
            else:
                self.width = self.width_init
            self.surf.blit(button_label, (self.width*0.5 - button_label.get_width()*0.5, self.height*0.5 - button_label.get_height()*0.5))

    def draw(self, window:pygame.Surface):
        window.blit(self.surf, (self.x, self.y))

    def isOver(self, pos:list) -> bool:
        return self.rect.collidepoint(pos)

    def change_color(self, color=None, text_color=None):
        if color != self.color and color is not None:
            self.color = color
            self.update_surf()
        if text_color != self.text_color and text_color is not None:
            self.text_color = text_color
            self.update_surf()

    def change_text(self, text):
        if text != self.text:
            self.text = text
            self.update_surf()
            