import math
import pygame
import sys
import random
import time
# import neccesary libraries
import paddle
import ball
import ui
# import custom scripts

pygame.init()
# initialize pygame
screen_size = [800, 800]
display = pygame.display.set_mode((screen_size))
# used for screen

clock = pygame.time.Clock()
frame_rate = 60

paddle_attributes = {(100, 300):[[pygame.K_s, pygame.K_w], [(74, 222, 208), (38, 207, 191), (30, 164, 151)]], (670, 300):[[pygame.K_DOWN, pygame.K_UP], [(30, 164, 151), (38, 207, 191), (74, 222, 208)]]}
# position, controls for paddles
paddles = []
# list of all paddles

for pos, attributes in paddle_attributes.items():
    paddles.append(paddle.Paddle(pos, (14, 14), attributes[0], screen_size, attributes[1]))
# adding paddles to paddles list

ball_sprite = pygame.sprite.GroupSingle(ball.Ball((400, 600), (7, 7), pygame.math.Vector2(random.choice([-1, 1]), random.choice([-1, 1])), screen_size, center=True))
# creating the ball

# MENU STUFF
title = ui.Text("Breakout-Pong", (400, 100))

controls = {'w.png':pygame.math.Vector2(100, 500), 's.png':pygame.math.Vector2(100, 530), 'up.png':pygame.math.Vector2(700, 500), 'down.png':pygame.math.Vector2(700, 530)}
controls_list = []

controls_p1 = ui.Text("Player 1 Controls", (100, 470), font_size=10)
controls_p2 = ui.Text("Player 2 Controls", (700, 470), font_size=10)

start_inst = ui.Text("[To Start, Press Any Key]", (400, 520), font_size=20)
start_inst_alpha = 0

frame_count = 0
start_game_time = 3

timer_text = ['3', '2', '1']
start_timer_text = ui.Text(timer_text[0], pygame.math.Vector2(400, 900), font_size=20)

for name, start_pos in controls.items():
    controls_list.append(ui.Image(name, start_pos))

round_text = ui.Text("30", pygame.math.Vector2(400, 400), (30, 164, 151), font_size=200)
round_frame_count = 0
start_round_timer = 3
round_timer = start_round_timer

while True:
    display.fill((22, 121, 111))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()    

        if event.type == pygame.KEYDOWN and ui.start_game == False:
            ui.start_game = True

    for pad in paddles:
        pad.update_paddle(display, ball_sprite, ui.start_game and start_timer_text.text == timer_text[-1])

    # updating paddles
    # updating and drawing ball

    ball_sprite.sprite.collision_check()
    # checking for ball collisions

    title.draw(display)

    controls_p1.draw(display)
    controls_p2.draw(display)

    for inst in controls_list:
        inst.draw(display)
    
    start_inst.draw(display)

    if ui.start_game:
        title.lerp_move(pygame.math.Vector2(title.rect.x, -200), 0.05)
        controls_p1.lerp_move(pygame.math.Vector2(-300, controls_p1.rect.y), 0.05)
        controls_p2.lerp_move(pygame.math.Vector2(900, controls_p2.rect.y), 0.05)
        start_inst.lerp_move(pygame.math.Vector2(start_inst.rect.x, 900), 0.05)
        
        for control in controls_list:
            if len(control.image_name.split('.')[0]) == 1:
                control.lerp_move(pygame.math.Vector2(-100, control.rect.y), 0.05)
            else:
                control.lerp_move(pygame.math.Vector2(900, control.rect.y), 0.05)

        try:
            start_timer_text.lerp_move(pygame.math.Vector2(400, 600), 0.1)
            frame_count += 1
            seconds_passed = int(math.floor(frame_count / 60))
            start_timer_text.update_text(timer_text[seconds_passed])

        except:
            start_timer_text.place_move(pygame.math.Vector2(400, 900))

            round_frame_count += 1
            if round_timer - int(round_frame_count/frame_rate) >= 0:
                round_time = str(round_timer - int(round_frame_count/frame_rate))

            if len(round_time) == 1:
                round_time = "0" + round_time

            if round_time == "00":
                round_timer = start_round_timer
                round_frame_count = 0
                frame_count = 0

                ball_sprite.sprite.rect.center = pygame.math.Vector2(400, 600)

                paddles.clear()

                for pos, attributes in paddle_attributes.items():
                    paddles.append(paddle.Paddle(pos, (14, 14), attributes[0], screen_size, attributes[1]))

                pygame.time.wait(250)

            round_text.update_text(round_time)
            round_text.draw(display)

            ball_sprite.update(ball.Ball.direction * ball.Ball.speed)
            ball_sprite.draw(display)


        start_timer_text.draw(display)

    pygame.display.update()
    clock.tick(frame_rate)
    # update display at 60 frames/second

# To Do For Game To Be Done (MVP Pipeline):

# add restart ability and winner

# Sound effects

# To Do For a Better Product:
# add a health systems (health bar?)
# pause menu
# control remapping