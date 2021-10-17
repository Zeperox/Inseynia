import pygame
from pygame.constants import QUIT

class Polygon:
    def __init__(self, vertices):
        self.vertices = vertices

    def collidepoint(self, point):
        collide = False

        next = 0
        for current in range(len(self.vertices)):
            next = current+1
            if next == len(self.vertices): next = 0

            vc = self.vertices[current]
            vn = self.vertices[next]
            
            if (((vc[1] >= point[1] and vn[1] < point[1]) or (vc[1] < point[1] and vn[1] >= point[1])) and (point[0] < (vn[0]-vc[0])*(point[1]-vc[1]) / (vn[1]-vc[1])+vc[0])):
                collide = not collide

        return collide

def draw_poly(win, color, poly, scroll=[0, 0]):
    points = []
    for v in poly.vertices:
        points.append((v[0]-scroll[0], v[1]-scroll[1]))

    pygame.draw.polygon(win, color, points, 1)

if __name__ == "__main__":
    c = (0, 0, 0)
    poly = Polygon([(100, 100), (300, 100), (150, 300)])
    win = pygame.display.set_mode((500, 500))
    while True:
        win.fill((255,255,255))
        draw_poly(win, c, poly)

        for event in pygame.event.get():
            if event.type == QUIT: quit()

        if poly.collidepoint(pygame.mouse.get_pos()):
            c = (255, 0, 0)
        else:
            c = (0, 0, 0)
        pygame.display.update()
