import pygame

from pygame.sprite import Sprite
from dino_runner.utils.constants import (
    DUCKING,
    RUNNING,
    JUMPING,
    DEFAULT_TYPE
)

class Dinosaur(Sprite):
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5
    DUCK_VEL = 8.5

    def __init__(self):
        self.run_img = {DEFAULT_TYPE: RUNNING}
        self.jump_img = {DEFAULT_TYPE: JUMPING}
        self.duck_img = {DEFAULT_TYPE: DUCKING}
        self.type = DEFAULT_TYPE
        self.image = self.run_img[self.type][0]

        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index = 0
        self.dino_run = True
        self.dino_jump = False
        self.jump_vel = self.JUMP_VEL
        self.duck_vel = self.DUCK_VEL
        self.dino_duck = False

        self.has_lives = False
        self.lives_transition_time = 0

    def update(self, user_input):
        if self.dino_jump:
            self.jump()
            print("jump")
        if self.dino_duck:
            self.duck()
            print("duck")
        if self.dino_run:
            self.run()
            print("run")
        print(self.dino_run, self.dino_jump, self.dino_duck)

        if user_input[pygame.K_UP] and not self.dino_jump:
            self.dino_jump = True
            self.dino_run = False
            self.dino_duck = False
        elif user_input[pygame.K_DOWN] and not self.dino_duck:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not self.dino_jump and not self.dino_duck:
            self.dino_run = True
            self.dino_jump = False
            self.dino_duck = False

        if self.step_index >= 10:
            self.step_index = 0

    def run(self):
        self.image = self.run_img[self.type][self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img[self.type]
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < -self.JUMP_VEL:
            self.dino_rect.y = self.Y_POS
            self.dino_jump = False
            self.dino_duck = False
            self.jump_vel = self.JUMP_VEL

    def duck(self):
        self.image = self.duck_img[self.type][self.step_index // 5]
        if self.dino_duck:
            self.dino_rect.y = self.Y_POS_DUCK
            self.duck_vel -= 0.8
        if self.duck_vel < -self.DUCK_VEL:
            self.dino_rect.y = self.Y_POS
            self.dino_duck = False
            self.dino_jump = False
            self.duck_vel = self.DUCK_VEL


    def draw(self, screen):
        screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

    def check_lives(self):
        if self.has_lives:
            transition_time = round((self.lives_transition_time - pygame.time.get_ticks()) / 1000)
            if transition_time < 0:
                self.has_lives = False
