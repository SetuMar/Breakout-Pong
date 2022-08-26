import pygame

pygame.init()

start_game = False

class Transition:
    def __init__(self):
        self.items = self.__dict__

    def change_alpha(self, alpha):
        for value in self.items.values():
            if type(value) is pygame.Surface:
                value.set_alpha(alpha)
    
    def place_move(self, position):
        for value in self.items.values():
            if type(value) is pygame.Rect:
                move_amt = pygame.math.Vector2(position.x - value.x, position.y - value.y)
                value.topleft += move_amt
    
    def lerp_move(self, position, time):
        for key, value in self.items.items():
            if type(value) is pygame.Rect:
                rect_center = pygame.math.Vector2(value.topleft)
                rect_center = rect_center.lerp(position, time)

                value.topleft = rect_center

class Text(Transition):
    def __init__(self, text, location, color = (255, 255, 255), font_name = 'dogicapixel.ttf', font_size = 50, txt_opacity = 255):
        Transition.__init__(self)
        self.font = pygame.font.Font(font_name, font_size)
        self.text = text
        self.color = color

        self.shadow = None

        self.font_txt = self.font.render(self.text, True, self.color)

        self.rect = self.font_txt.get_rect()

        self.location_x = location[0]

        self.rect.center = location

        self.font_txt.set_alpha(txt_opacity)
    
    def draw(self, display):
        display.blit(self.font_txt, self.rect.topleft)

    def update_text(self, new_text):
        self.text = new_text
        self.font_txt = self.font.render(self.text, True, self.color)

class Image(Transition):
    def __init__(self, image_name, position):
        Transition.__init__(self)

        self.image_name = image_name
        
        self.image = pygame.image.load(self.image_name)
        self.rect = self.image.get_rect()
        self.rect.center = position
    
    def draw(self, display):
        display.blit(self.image, self.rect.topleft)