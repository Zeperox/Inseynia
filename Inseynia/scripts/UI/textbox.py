import pygame
from pygame.locals import *

class TextBox:
    def __init__(self, color, x, y, width, height, pre_text="", text_color=(255,255,255), clear_text_when_click=False, numeric=False, alpha=False, alnum=False):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.text = pre_text
        self.text_color = text_color
        self.clear_text_when_click = clear_text_when_click
        self.clicked = False

        self.numeric = numeric
        self.alpha = alpha
        self.alnum = alnum

        self.selected = False
        
    def draw(self, window:pygame.Surface, outline:tuple=None, outline_thickness:int=2, font_name:str=None, font_size:int=None):
        if outline:
            pygame.draw.rect(window, outline, (self.x-outline_thickness, self.y-outline_thickness, self.width+outline_thickness*2, self.height+outline_thickness*2), outline_thickness)
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))

        if self.text:
            try:
                button_font = pygame.font.Font(font_name, font_size) if font_size else pygame.font.Font(font_name, int(self.height*0.5))
            except FileNotFoundError():
                button_font = pygame.font.SysFont(font_name, font_size) if font_size else pygame.font.SysFont(font_name, int(self.height*0.5))
            button_label = button_font.render(self.text, 1, self.text_color)
            window.blit(button_label, (self.x + (self.width*0.5 - button_label.get_width()*0.5), self.y + (self.height*0.5 - button_label.get_height()*0.5)))

    def isOver(self, pos):
        collision_test = pygame.Rect(self.x, self.y, self.width, self.height)
        if collision_test.collidepoint(pos):
            self.selected = True
            if self.clear_text_when_click and not self.clicked:
                self.text = ""
                self.clicked = True
        else:
            self.selected = False

    def update_text(self, event) -> str:
        if self.selected:
            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key == K_RETURN:
                    return self.text
                else:
                    if self.alnum or (self.numeric and self.alpha):
                        if event.unicode.isalnum():
                            self.text += event.unicode
                    elif self.numeric:
                        if event.unicode.isnumeric():
                            if self.text == "0":
                                self.text = ""
                            self.text += event.unicode
                    elif self.alpha:
                        if event.unicode.isalpha():
                            self.text += event.unicode
                    else:
                        self.text += event.unicode

                if self.text == "" and self.numeric:
                    self.text = "0"
