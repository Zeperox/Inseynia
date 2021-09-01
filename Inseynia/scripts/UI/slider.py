import pygame
from pygame.locals import *

class SliderX:
    def __init__(self, x, y, width, height, color1=(0,0,0),  width2=40, color2=(0,0,0), text="", text_color=(255,255,255)):
        self.color1 = color1
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.color2 = color2
        self.selected = False
        self.width2 = width2

        self.text = text
        self.text_color = text_color

        self.selector_rect_x = self.x+self.width2-40
        self.selector_rect_y = self.y
        self.selector_rect_width = 40
        self.selector_rect_height = self.height

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def set_value(self, min_value, max_value, set_value, value_type="int", new_value_per_pix=1, list_of_values_not_int_type=[]):
        if value_type == "int":
            if self.width2 <= 40:
                new_value = int(min_value)
            elif self.width2 >= self.width:
                new_value = int(max_value)
            else:
                new_value = int(self.width2*new_value_per_pix)
        if value_type == "float":
            if self.width2 <= 40:
                new_value = float(min_value)
            elif self.width2 >= self.width:
                new_value = float(max_value)
            else:
                new_value = float(self.width2*new_value_per_pix)
        else:
            if self.width2 <= 40:
                new_value = min_value
            elif self.width2 >= self.width:
                new_value = max_value
            else:
                if round(self.width2*new_value_per_pix) > len(list_of_values_not_int_type):
                    new_value = max_value
                elif round(self.width2*new_value_per_pix) < 0:
                    new_value = min_value
                else:
                    new_value = list_of_values_not_int_type[round(self.width2*new_value_per_pix)]

        return new_value

    def draw(self, window, outline=None, outline_thickness=2, font_name=None, font_size=None):
        self.selector_rect_y = self.y
        self.selector_rect_x = self.x+self.width2-40

        if outline:
            pygame.draw.rect(window, outline, (self.x-outline_thickness, self.y-outline_thickness, self.width+outline_thickness*2, self.height+outline_thickness*2), outline_thickness)
        pygame.draw.rect(window, self.color1, (self.x, self.y, self.width, self.height))

        pygame.draw.rect(window, self.color2, (self.x, self.y, self.width2, self.height))
        pygame.draw.rect(window, (195, 197, 202), (self.selector_rect_x, self.selector_rect_y, self.selector_rect_width, self.selector_rect_height))

        if self.text:
            try:
                button_font = pygame.font.Font(font_name, font_size) if font_size else pygame.font.Font(font_name, int(self.height*0.5))
            except FileNotFoundError:
                button_font = pygame.font.SysFont(font_name, font_size) if font_size else pygame.font.SysFont(font_name, int(self.height*0.5))
            button_label = button_font.render(self.text, 1, self.text_color)
            window.blit(button_label, (self.x + (self.width*0.5 - button_label.get_width()*0.5), self.y + (self.height*0.5 - button_label.get_height()*0.5)))

    def isOver(self, pos):
        self.selected = self.rect.collidepoint(pos)
        
        return self.selected
            
    def move(self, pos):
        if self.selected:
            if pos[0] < self.x+40:
                self.width2 = 40
            elif pos[0] > self.x+self.width:
                self.width2 = self.width
                self.selector_rect_x = self.x+self.width-40
            else:
                self.width2 = pos[0]-self.x
                self.selector_rect_x = self.x+self.width2-40

    def scroll(self, button, val_diff=4):
        if button == 4:
            self.width2 += val_diff
            if self.width2 < 40:
                self.width2 = 40
            elif self.width2 > self.width:
                self.width2 = self.width
                self.selector_rect_x = self.width-40
            else:
                self.selector_rect_x = self.width2-40

        if button == 5:
            self.width2 -= val_diff
            if self.width2 <= 40:
                self.width2 = 40
            elif self.width2 > self.width:
                self.width2 = self.width
                self.selector_rect_x = self.width-40
            else:
                self.selector_rect_x = self.width2-40

class SliderY:
    def __init__(self, x, y, width, height, color1=(0,0,0),  height2=0, color2=(0,0,0), text="", text_color=(255,255,255)):
        self.color1 = color1
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.color2 = color2
        self.selected = False
        self.height2 = height2

        self.text = text
        self.text_color = text_color

        self.selector_rect_x = self.x
        self.selector_rect_y = self.y+self.height2-40
        self.selector_rect_width = self.width
        self.selector_rect_height = 40

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def set_value(self, min_value, max_value, set_value, value_type="int", new_value_per_pix=1, list_of_values_not_int_type=[]):
        if value_type == "int":
            if self.height2 <= 40:
                new_value = int(min_value)
            elif self.height2 >= self.width:
                new_value = int(max_value)
            else:
                new_value = int(self.height2*new_value_per_pix)
        if value_type == "float":
            if self.height2 <= 40:
                new_value = float(min_value)
            elif self.height2 >= self.width:
                new_value = float(max_value)
            else:
                new_value = float(self.height2*new_value_per_pix)
        else:
            if self.height2 <= 40:
                new_value = min_value
            elif self.height2 >= self.width:
                new_value = max_value
            else:
                if round(self.height2*new_value_per_pix) > len(list_of_values_not_int_type):
                    new_value = max_value
                elif round(self.height2*new_value_per_pix) < 0:
                    new_value = min_value
                else:
                    new_value = list_of_values_not_int_type[round(self.height2*new_value_per_pix)]

        return new_value

    def draw(self, window, outline=None, outline_thickness=2, font_name=None, font_size=None):
        self.selector_rect_y = self.y+self.height2-40
        self.selector_rect_x = self.x

        if outline:
            pygame.draw.rect(window, outline, (self.x-outline_thickness, self.y-outline_thickness, self.width+outline_thickness*2, self.height+outline_thickness*2), outline_thickness)
        pygame.draw.rect(window, self.color1, (self.x, self.y, self.width, self.height))

        pygame.draw.rect(window, self.color2, (self.x, self.y, self.width, self.height2))
        pygame.draw.rect(window, (195, 197, 202), (self.selector_rect_x, self.selector_rect_y, self.selector_rect_width, self.selector_rect_height))

        if self.text:
            try:
                button_font = pygame.font.Font(font_name, font_size) if font_size else pygame.font.Font(font_name, int(self.height*0.5))
            except FileNotFoundError:
                button_font = pygame.font.SysFont(font_name, font_size) if font_size else pygame.font.SysFont(font_name, int(self.height*0.5))
            button_label = button_font.render(self.text, 1, self.text_color)
            window.blit(button_label, (self.x + (self.width*0.5 - button_label.get_width()*0.5), self.y + (self.height*0.5 - button_label.get_height()*0.5)))

    def isOver(self, pos):
        self.selected = self.rect.collidepoint(pos)
        
        return self.selected
            
    def move(self, pos):
        if self.selected:
            if pos[0] < self.y+40:
                self.height2 = 40
            elif pos[0] > self.y+self.height:
                self.height2 = self.height
                self.selector_rect_y = self.y+self.height-40
            else:
                self.height2 = pos[0]-self.y
                self.selector_rect_x = self.y+self.height2-40
