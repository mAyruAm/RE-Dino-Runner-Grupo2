from pickle import FALSE
import pygame
from dino_runner.components.cactus import Cactus
from dino_runner.components.pterodactilo import Terodactilo

from dino_runner.utils.constants import SMALL_CACTUS, BIRD
import random

class ObstacleManager:

    def __init__(self):
        self.obstacles = []


    def update(self, game):
        random_obstacles = [Cactus(SMALL_CACTUS), Terodactilo(BIRD)]
        if len(self.obstacles) == 0:
            self.obstacles.append(random_obstacles[random.randint(0 , len(random_obstacles) - 1)])
            # self.obstacles.append(Cactus(SMALL_CACTUS))
            # self.obstacles.append(Terodactilo(BIRD))





        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if (game.player.dino_rect.colliderect(obstacle.rect)):
                pygame.time.delay(500)
                game.playing = False
                break


    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)
