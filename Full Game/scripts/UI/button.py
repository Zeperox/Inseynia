import pygame
from pygame.locals import *

class Button:
    def __init__(self, x:int, y:int, width:int, height:int, color:tuple=(0,0,0), text:str="", text_color:tuple=(255,255,255)):
        self.x = x
        self.y = y
        self.width = width
        self.width_init = width
        self.height = height
        self.color = color

        self.text = text
        self.text_color = text_color

    def draw(self, window:pygame.Surface, outline:tuple=None, outline_thickness:int=2, font_name:str=None, font_size:int=None, dynamic_width=False):
        if outline:
            pygame.draw.rect(window, outline, (self.x-outline_thickness, self.y-outline_thickness, self.width+outline_thickness*2, self.height+outline_thickness*2), outline_thickness)
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))

        if self.text:
            try:
                button_font = pygame.font.Font(font_name, font_size) if font_size else pygame.font.Font(font_name, int(self.height*0.5))
            except FileNotFoundError():
                button_font = pygame.font.SysFont(font_name, font_size) if font_size else pygame.font.SysFont(font_name, int(self.height*0.5))
            button_label = button_font.render(self.text, 1, self.text_color)
            if button_label.get_width() > self.width_init:
                self.width = button_label.get_width()
            else:
                self.width = self.width_init
            window.blit(button_label, (self.x + (self.width*0.5 - button_label.get_width()*0.5), self.y + (self.height*0.5 - button_label.get_height()*0.5)))

    def isOver(self, pos:list) -> bool:
        collision_test = pygame.Rect(self.x, self.y, self.width, self.height)
        return collision_test.collidepoint(pos)
