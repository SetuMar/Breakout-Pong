import block
import pygame

class Ball(block.Block):
    direction = None
    speed = 5

    def __init__(self, position, dimensions, start_dir, screen_dimensions, center=False):
        super().__init__(position, dimensions)
        Ball.direction = start_dir

        self.screen_dimensions = pygame.math.Vector2(screen_dimensions)

        if center == True:
            self.rect.center = position

    def collision_check(self):
        if self.rect.right >= self.screen_dimensions.x or self.rect.left <= 0:
            Ball.direction.x *= -1

        if self.rect.bottom >= self.screen_dimensions.y or self.rect.top <= 0:
            Ball.direction.y *= -1