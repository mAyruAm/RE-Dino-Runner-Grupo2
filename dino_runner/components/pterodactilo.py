import pygame
from dino_runner.components.obstaculo import Obstacle
import random

class Terodactilo(Obstacle):

    def __init__(self, image):
        self.type = random.randint(0,1)
        super().__init__(image, self.type)
        self.rect.y = 280
