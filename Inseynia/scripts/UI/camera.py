import pygame


class Camera:
    def __init__(self, true_scroll, target, immediate=False):
        self.display = pygame.Surface((1280, 720))

        self.true_scroll = true_scroll
        self.target = target

        self.forced_loc = None
        self.immediate = immediate

    def update(self, game_map, screen_size, dt):
        if not self.forced_loc:
            if not self.immediate:
                if game_map.x == 0: self.true_scroll[0] += (self.target.x-self.true_scroll[0]-(screen_size[0]*0.5-self.target.rect.width*0.5))/20*dt
                else: self.true_scroll[0] += -self.true_scroll[0]/20*dt
                
                if game_map.y == 0: self.true_scroll[1] += (self.target.y-self.true_scroll[1]-(screen_size[1]*0.5-self.target.rect.height*0.5))/20*dt
                else: self.true_scroll[1] += -self.true_scroll[1]/20*dt
                
                scroll = self.true_scroll.copy()
                scroll[0] = int(scroll[0]); scroll[1] = int(scroll[1])

                if scroll[0] <= game_map.x and game_map.x == 0:
                    scroll[0] = game_map.x
                elif scroll[0] >= game_map.w-screen_size[0] and game_map.x == 0:
                    scroll[0] = game_map.w-screen_size[0]
                    
                if scroll[1] <= game_map.y and game_map.y == 0:
                    scroll[1] = game_map.y
                elif scroll[1] >= game_map.h-screen_size[1] and game_map.y == 0:
                    scroll[1] = game_map.h-screen_size[1]
            else:
                if game_map.x == 0: self.true_scroll[0] = self.target.x-((screen_size[0]*0.5)-(self.target.rect.width*0.5))
                else: self.true_scroll[0] = 0
                if game_map.y == 0: self.true_scroll[1] = self.target.y-((screen_size[1]*0.5)-(self.target.rect.height*0.5))
                else: self.true_scroll[1] = 0

                scroll = self.true_scroll
                if scroll[0] <= game_map.x and game_map.x == 0:
                    scroll[0] = game_map.x
                elif scroll[0] >= game_map.w-screen_size[0] and game_map.x == 0:
                    scroll[0] = game_map.w-screen_size[0]
                    
                if scroll[1] <= game_map.y and game_map.y == 0:
                    scroll[1] = game_map.y
                elif scroll[1] >= game_map.h-screen_size[1] and game_map.y == 0:
                    scroll[1] = game_map.h-screen_size[1]
        else:
            if not self.immediate:
                self.true_scroll[0] += (self.forced_loc[0]-self.true_scroll[0]-screen_size[0]*0.5)/20*dt
                self.true_scroll[1] += (self.forced_loc[1]-self.true_scroll[1]-screen_size[1]*0.5)/20*dt
                scroll = self.true_scroll.copy()
                scroll[0] = int(scroll[0]); scroll[1] = int(scroll[1])
            else:
                self.true_scroll = [self.forced_loc[0]-screen_size[0]*0.5, self.forced_loc[1]-screen_size[1]*0.5]
                scroll = self.true_scroll

        return scroll