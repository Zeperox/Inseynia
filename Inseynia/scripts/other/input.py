import pygame
import pygame._sdl2.controller as sdl2_controller
sdl2_controller.init()

class Input:
    def __init__(self):
        self.keys = []

    def press(self, input, method, controller: sdl2_controller.Controller = None):
        if method == "keys":
            if input <= 5:
                mouse = pygame.mouse.get_pressed(num_buttons=5)
                if mouse[input-1] and input-1 not in self.keys:
                    self.keys.append(input-1)
                    return True
                elif not mouse[input-1] and input-1 in self.keys:
                    self.keys.remove(input-1)
                    return False
            else:
                if pygame.key.get_pressed()[input] and input not in self.keys:
                    self.keys.append(input)
                    return True
                elif not pygame.key.get_pressed()[input] and input in self.keys:
                    self.keys.remove(input)
                    return False
        elif method == "cons" and controller:
            if input <= 14:
                if controller.get_button(input) and f"c{input}" not in self.keys:
                    self.keys.append(f"c{input}")
                    return True
                elif not controller.get_button(input) and f"c{input}" in self.keys:
                    self.keys.remove(f"c{input}")
                    return False
            else:
                if controller.get_axis(input-11) and f"c{input}" not in self.keys:
                    self.keys.append(f"c{input}")
                    return True
                elif not controller.get_axis(input-11) and f"c{input}" in self.keys:
                    self.keys.remove(f"c{input}")
                    return False
        return False

    def hold(self, input, method, controller: sdl2_controller.Controller):
        if method == "keys":
            if input <= 5:
                return pygame.mouse.get_pressed(num_buttons=5)[input-1]
            else:
                return pygame.key.get_pressed()[input]
        else:
            if input <= 14:
                return controller.get_button(input)
            else:
                return controller.get_axis(input-11)/32767 >= 0.5
            
game_input = Input()
if __name__ == "__main__":
    controller = sdl2_controller.Controller(0)

    pygame.display.set_mode((500, 500))
    clock = pygame.time.Clock()
    while 1:
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.CONTROLLERAXISMOTION:
                print(event)

        print(game_input.press(16, "c", controller))

