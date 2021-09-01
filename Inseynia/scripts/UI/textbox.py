import pygame, time
from pygame.locals import *

class TextBox:
    def __init__(self, color, x, y, width, height, pre_text="", text_color=(255,255,255), text_pos="left", clear_text_when_click=False, numeric=False, alpha=False, alnum=False):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.text = pre_text
        self.text_color = text_color
        self.text_pos = text_pos

        self.clear_text_when_click = clear_text_when_click
        self.clicked = False

        self.numeric = numeric
        self.alpha = alpha
        self.alnum = alnum

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.selected = False
        self.blink_timer = time.time()
        
    def draw(self, window, outline=None, outline_thickness=2, font_name=None, font_size=None):
        if outline:
            pygame.draw.rect(window, outline, (self.x-outline_thickness, self.y-outline_thickness, self.width+outline_thickness*2, self.height+outline_thickness*2), outline_thickness)
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))

        try:
            button_font = pygame.font.Font(font_name, font_size) if font_size else pygame.font.Font(font_name, int(self.height*0.5))
        except FileNotFoundError:
            button_font = pygame.font.SysFont(font_name, font_size) if font_size else pygame.font.SysFont(font_name, int(self.height*0.5))
        button_label = button_font.render(self.text, 1, self.text_color)
        
        if self.text_pos == "left":
            text_x = self.x + 10
        elif self.text_pos == "center" or self.text_pos == "middle":
            text_x = self.x + (self.width*0.5 - button_label.get_width()*0.5)
        elif self.text_pos == "right":
            text_x = (self.x+self.width)-(button_label.get_width()-15)
        window.blit(button_label, (text_x, self.y + (self.height*0.5 - button_label.get_height()*0.5)))

        if self.selected:
            if time.time() - self.blink_timer >= 0.75:
                pygame.draw.line(window, (255,255,255), (text_x+button_label.get_width()+5, self.y+15), (text_x+button_label.get_width()+5, self.y+(self.height-15)))
            if time.time() - self.blink_timer >= 1:
                self.blink_timer = time.time()

    def isOver(self, pos):
        self.selected = self.rect.collidepoint(pos)

        if self.selected and self.clear_text_when_click and not self.clicked:
            self.text = ""
            self.clicked = True

    def update_text(self, event):
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
        else:
            return self.text
