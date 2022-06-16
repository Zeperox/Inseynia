import pygame, math

class View:
    def __init__(self, loc: list[int, int], angle: int, length: int, offset: int=0):
        self.angle = [angle, math.radians(angle)]
        self.offset = [offset, math.radians(offset)]
        self.lines = [
            [loc, [loc[0]+math.cos(-self.angle[1]/2+self.offset[1])*length, loc[1]+math.sin(-self.angle[1]/2+self.offset[1])*length]],
            [loc, [loc[0]+math.cos(self.offset[1])*length, loc[1]+math.sin(self.offset[1])*length]],
            [loc, [loc[0]+math.cos(self.angle[1]/2+self.offset[1])*length, loc[1]+math.sin(self.angle[1]/2+self.offset[1])*length]]
        ]
        self.length = length

        for i, line in enumerate(self.lines):
            self.lines[i].append(math.atan2(line[1][1]-line[0][1], line[1][0]-line[0][0]))

    def collision(self, tiles, rect):
        def colliderect_line(line, rect: pygame.Rect):
            def collideline_line(line1: list[list[int, int], list[int, int]], line2: list[list[int, int], list[int, int]]):
                uA = ((line2[1][0]-line2[0][0])*(line1[0][1]-line2[0][1]) - (line2[1][1]-line2[0][1])*(line1[0][0]-line2[0][0])) / (((line2[1][1]-line2[0][1])*(line1[1][0]-line1[0][0]) - (line2[1][0]-line2[0][0])*(line1[1][1]-line1[0][1]))+1)
                uB = ((line1[1][0]-line1[0][0])*(line1[0][1]-line2[0][1]) - (line1[1][1]-line1[0][1])*(line1[0][0]-line2[0][0])) / (((line2[1][1]-line2[0][1])*(line1[1][0]-line1[0][0]) - (line2[1][0]-line2[0][0])*(line1[1][1]-line1[0][1]))+1)
                return uA >= 0 and uA <= 1 and uB >= 0 and uB <= 1
            
            l = collideline_line(line, (rect.topleft, rect.bottomleft))
            r = collideline_line(line, (rect.topright, rect.bottomright))
            t = collideline_line(line, (rect.topleft, rect.topright))
            b = collideline_line(line, (rect.bottomleft, rect.bottomright))
            return l or r or t or b

        line = self.lines[1]
        
        if math.dist(line[0], rect.center) <= self.length:
            for tile in tiles:
                t_collision = colliderect_line(line, tile)
                if t_collision:
                    if line[0][0] > tile.right:
                        line[1][0] = tile.right
                    elif line[0][0] < tile.left:
                        line[1][0] = tile.left

                    if line[0][1] > tile.bottom:
                        line[1][1] = tile.bottom
                    elif line[0][1] < tile.top:
                        line[1][1] = tile.top
                
            p_collision = colliderect_line(line, rect)

            ang = math.atan2(rect.centery-line[0][1], rect.centerx-line[0][0])

            if p_collision and self.lines[0][2] < ang < self.lines[2][2] and self.lines[0][2] < self.lines[2][2]:
                return True
            elif p_collision and self.lines[0][2] > self.lines[2][2] and (self.lines[0][2] < ang < math.pi or self.lines[2][2] > ang > -math.pi):
                return True

            if not t_collision:
                line[1] = [line[0][0]+math.cos(line[2])*self.length, line[0][1]+math.sin(line[2])*self.length]
            
        return False

    def draw(self, win, c, scroll):
        pygame.draw.lines(win, c, False, (((self.lines[0][1][0]-scroll[0], self.lines[0][1][1]-scroll[1]), (self.lines[1][0][0]-scroll[0], self.lines[1][0][1]-scroll[1]), (self.lines[2][1][0]-scroll[0], self.lines[2][1][1]-scroll[1]))))
        pygame.draw.line(win, c, (self.lines[1][0][0]-scroll[0], self.lines[1][0][1]-scroll[1]), (self.lines[1][1][0]-scroll[0], self.lines[1][1][1]-scroll[1]))

    def update_lines(self, loc):
        self.lines = [
            [loc, [loc[0]+math.cos(-self.angle[1]/2+self.offset[1])*self.length, loc[1]+math.sin(-self.angle[1]/2+self.offset[1])*self.length]],
            [loc, [loc[0]+math.cos(self.offset[1])*self.length, loc[1]+math.sin(self.offset[1])*self.length]],
            [loc, [loc[0]+math.cos(self.angle[1]/2+self.offset[1])*self.length, loc[1]+math.sin(self.angle[1]/2+self.offset[1])*self.length]]
        ]
        for i, line in enumerate(self.lines):
            self.lines[i].append(math.atan2(line[1][1]-line[0][1], line[1][0]-line[0][0]))

if __name__ == "__main__":
    win = pygame.display.set_mode((500, 500))
    
    prect = pygame.Rect(0, 0, 10, 10)
    trects = [pygame.Rect(400, 240, 20, 20), pygame.Rect(350, 300, 20, 20), pygame.Rect(350, 180, 20, 20)]
    view = View([250, 250], 45, 300, 90)

    while 1:
        win.fill((0, 0, 0))
        
        prect.center = pygame.mouse.get_pos()
        if math.dist((250, 250), prect.center) <= 200:
            view.lines[1][1] = list(prect.center)
        else:
            view.lines[1][1] = [250+math.cos(view.lines[1][2])*200, 250+math.sin(view.lines[1][2])*200]

        view.draw(win, (255, 255, 255), (0, 0))
        for trect in trects:
            pygame.draw.rect(win, (255, 0, 0), trect)

        ang = math.degrees(math.atan2(prect.centery-250, prect.centerx-250))
        if view.collision(trects, prect):
            pygame.draw.rect(win, (0, 255, 0), prect)
        else:
            pygame.draw.rect(win, (255, 0, 0), prect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        pygame.display.flip()
