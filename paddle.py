import pygame
import block
import ball

class Paddle():
    def __init__(self, position, dimensions, inputs, screen_size, paddle_colors_order):
        self.paddle_blocks = pygame.sprite.Group()
        self.speed = 5
        self.inputs = inputs

        self.axis_loop_amt = [3, 10]
        self.rect = pygame.Rect(position[0], position[1], dimensions[0] * self.axis_loop_amt[0], dimensions[1] * self.axis_loop_amt[1])
        self.last_rect_top = 0

        self.h_dim = dimensions[1]

        self.start_height = self.rect.height/self.h_dim

        self.screen_size = screen_size

        for x in range(self.axis_loop_amt[0]):
            for y in range(self.axis_loop_amt[1]):
                self.paddle_blocks.add(block.Block(self.rect.topleft + pygame.math.Vector2(x * dimensions[0], y * dimensions[1]), dimensions, x, y, (paddle_colors_order[x])))

        self.start_height_pixel = self.rect.width

    def update_paddle(self, display, ball_sprite_group, game_has_started):
        keys = pygame.key.get_pressed()
        key_input = pygame.math.Vector2(0, keys[self.inputs[0]] - keys[self.inputs[1]]) * self.speed

        topleft = pygame.math.Vector2(0, 0)
        bottomleft = pygame.math.Vector2(float('inf'), float('inf'))

        max_topleft_pos = float('inf')
        bottom_pos = float('-inf')

        for block in self.paddle_blocks.sprites():
            if block.rect.colliderect(ball_sprite_group.sprite.rect):
                inverse_dir = ball.Ball.direction * -1
                ball_sprite_group.sprite.rect.topleft += inverse_dir * ball.Ball.speed

                self.paddle_blocks.remove(block)
                ball.Ball.direction.x *= -1

            if block.block_height < max_topleft_pos:
                topleft.y = block.rect.y
                max_topleft_pos = block.block_height

                if block.block_width == 0:
                    topleft.x = block.rect.x
            
            if block.block_height > bottom_pos:
                bottomleft.y = block.rect.y
                bottom_pos = block.block_height

                if block.block_width == 0:
                    bottomleft.x = block.rect.x

        if (key_input.y > 0 and self.rect.bottom >= self.screen_size[1] or key_input.y < 0 and self.rect.top <= 0) or game_has_started != True:
            key_input = pygame.math.Vector2(0, 0)

        self.rect.topleft = topleft

        try:
            if self.rect.bottom != int(bottomleft.y + self.h_dim):
                self.rect.height -= (self.rect.bottom - int(bottomleft.y + self.h_dim))
        except:
            pass

        self.rect.topleft += key_input
        self.paddle_blocks.update(key_input)
        self.paddle_blocks.draw(display)

    def __len__(self):
        return len(self.paddle_blocks)