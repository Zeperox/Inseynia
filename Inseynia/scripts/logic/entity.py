import pygame, os, platform, time
from scripts.custom_collisions.obb import OBB

class Entity:
    def __init__(self, x: int, y: int, animation_dirs: list[str] | pygame.Surface, animation_pause: int = 0, animation_action: str = "idle", end_animation: bool = False):
        self.x = x
        self.y = y
        
        self.img_type = type(animation_dirs)
        if type(animation_dirs) == list:
            if platform.system() == "Windows":
                splitter = "\\"
            else:
                splitter = "/"

            self.orig_animations = {}
            self.animations = {}
            for animation_dir in animation_dirs:
                self.orig_animations[animation_dir.split(splitter)[-1]] = []
                self.animations[animation_dir.split(splitter)[-1]] = []

                imgs = os.listdir(animation_dir)
                for i, img in enumerate(imgs):
                    imgs[i] = int(img[:img.index(".")])
                for img in sorted(imgs):
                    self.orig_animations[animation_dir.split(splitter)[-1]].append(pygame.transform.scale2x(pygame.image.load(os.path.join(animation_dir, f"{img}.png"))))
                    self.animations[animation_dir.split(splitter)[-1]].append(pygame.transform.scale2x(pygame.image.load(os.path.join(animation_dir, f"{img}.png"))))
            

            self.animation_count = [0, animation_pause]
            self.action = animation_action
            self.end_animation = [end_animation, False]
        else:
            self.orig_img = animation_dirs
            self.img = animation_dirs

        self.flip = False

        self.movement = [0, 0]

        self.rect = pygame.Rect(self.x, self.y, self.get_width(), self.get_height())
        self.tile_rect = self.rect.inflate(0, -26)
        self.tile_rect.center = self.rect.center

        self.active = True
        self.collidable = True
        self.animate = True

        self.i_frame = 0
        self.i_time = 0.1

        self.knockback = False
        self.knockback_dir = pygame.Vector2()
        self.knockback_speed = 0
        self.knockback_resist = 0

    def get_width(self):
        if self.img_type == list:
            return self.animations[self.action][self.animation_count[0]//self.animation_count[1]].get_width()
        else:
            return self.img.get_width()

    def get_height(self):
        if self.img_type == list:
            return self.animations[self.action][self.animation_count[0]//self.animation_count[1]].get_height()
        else:
            return self.img.get_height()

    def draw(self, win: pygame.Surface, scroll: list[int, int], dt: float=1):
        if self.active:
            if self.img_type == list:
                if self.animate:
                    if not self.end_animation[1]:
                        self.animation_count[0] += 1*dt
                    if self.animation_count[0] + 1 >= len(self.animations[self.action])*self.animation_count[1]:
                        if self.end_animation[0]:
                            self.end_animation[1] = True
                        else:
                            self.animation_count[0] = 0

                try:            
                    win.blit(pygame.transform.flip(self.animations[self.action][int(self.animation_count[0]//self.animation_count[1])], self.flip, False), (self.x-scroll[0], self.y-scroll[1]))
                except IndexError:
                    win.blit(pygame.transform.flip(self.animations[self.action][len(self.animations[self.action])-1], self.flip, False), (self.x-scroll[0], self.y-scroll[1]))
            else:
                win.blit(pygame.transform.flip(self.img, self.flip, False), (self.x-scroll[0], self.y-scroll[1]))
   
    def collision_test(self, tiles: list[pygame.Rect], return_on_collision: bool = False):
        hit_list = []

        rect = pygame.Rect(self.x-32*2, self.y-32*2, self.x+self.rect.width+32*2, self.y+self.rect.height+32*2)
        close_list = []
        for tile in tiles:
            if rect.colliderect(tile):
                close_list.append(tile)
            
        for tile in close_list:
            if self.tile_rect.colliderect(tile):
                if return_on_collision:
                    return True
                hit_list.append(tile)
        return hit_list

    def movement_collision(self, tiles: list[pygame.Rect], collide=True):
        collision_types = {"top": False, "bottom": False, "left": False, "right": False}
        self.x += self.movement[0]
        self.tile_rect.x = self.x
        hit_list = self.collision_test(tiles)
        for tile in hit_list:
            if self.movement[0] > 0:
                if collide:
                    self.x = tile.left-self.rect.width
                collision_types["right"] = True
            if self.movement[0] < 0:
                if collide:
                    self.x = tile.right
                collision_types["left"] = True
        if type(self.rect) == OBB:
            self.rect.center.x = self.x+self.get_width()*0.5
        else:
            self.tile_rect.x = self.x

        self.y += self.movement[1]
        self.tile_rect.y = self.y+10
        hit_list = self.collision_test(tiles)
        for tile in hit_list:
            if self.movement[1] > 0:
                if collide:
                    self.y = tile.top-self.tile_rect.height-10
                collision_types["bottom"] = True
            if self.movement[1] < 0:
                if collide:
                    self.y = tile.bottom-10
                collision_types["top"] = True
        if type(self.rect) == OBB:
            self.rect.center.y = self.y+self.get_height()*0.5
        else:
            self.tile_rect.y = self.y+10

        self.rect.center = self.tile_rect.center

        return collision_types

    def change_anim(self, anim: str, animation_puase: int = None, end_animation: bool = False):
        self.action = anim
        self.animation_count[0] = 0
        if animation_puase is not None:
            self.animation_count[1] = animation_puase
        self.end_animation = [end_animation, False]

