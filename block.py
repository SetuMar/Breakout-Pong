import pygame
import random

class Block(pygame.sprite.Sprite):
    def __init__(self, position, dimensions, x_coord = None, y_coord = None, color=(255, 255, 255)):
        super().__init__()
        self.image = pygame.Surface(dimensions)
        self.image.fill(color)
        
        self.rect = self.image.get_rect()
        self.rect.topleft = position

        self.block_width = x_coord
        self.block_height = y_coord
    
    def update(self, move_amt = 0):
        self.rect.topleft += move_amt