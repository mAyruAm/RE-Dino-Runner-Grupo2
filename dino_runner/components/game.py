import pygame

from dino_runner.components.player_hearts.player_heart_manager import PlayerHeartManager
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacle_manager import ObstacleManager
from dino_runner.components.text_utils import get_score_element, get_centered_message
from dino_runner.components.power_up.power_up_manager import PowerUpManager
from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, SOUND_BACKGROUND

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.points = 0
        self.best_score = 0
        self.running = True
        self.death_count = 0
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.player_heart_manager = PlayerHeartManager()
        self.power_up_manager = PowerUpManager()
        self.background_round = pygame.mixer.music.load(SOUND_BACKGROUND)


    def run(self):
        # Game loop: events - update - draw
        self.create_comment()
        self.playing = True
        pygame.mixer.music.play(-1)
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.power_up_manager.update(self.points, self.game_speed, self.player)
        self.obstacle_manager.update(self)

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.player_heart_manager.draw(self.screen)
        self.power_up_manager.draw(self.screen)
        self.score()

        self.player.check_lives()
        pygame.display.update()
        pygame.display.flip()


    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def score(self):
        self.points += 1
        if self.points % 100 == 0:
            self.game_speed += 1
        score, score_rect = get_score_element(self.points)
        self.player.check_visibility(self.screen)
        self.screen.blit(score, score_rect)

    def create_comment(self):
        self.power_up_manager.reset_power_ups(self.points)

    def show_menu(self, death_count = 0):
        self.running = True
        white_color = (255,255,255)
        self.screen.fill(white_color)

        self.print_menu_elements(self.death_count if death_count == 0 else death_count)

        pygame.display.update()

        self.handle_key_events_on_menu()

    def print_menu_elements(self, death_count = 0):
        half_screen_height = SCREEN_HEIGHT // 2

        if death_count == 0:
            text, text_rect = get_centered_message("Press any Key to Start")
            self.screen.blit(text, text_rect)
        elif death_count > 0:
            self.update_best_score()
            text, text_rect = get_centered_message("Press any Key to Restart")
            score, score_rect = get_centered_message(f"Your Current Score: {str(self.points)}", height=half_screen_height + 50)
            best_score, best_score_rect = get_centered_message(f"Your Best Score: {str(self.best_score)}", height=half_screen_height + 75)
            death, death_rect = get_centered_message(f"Your Death Count: {str(self.death_count)}", height=half_screen_height + 100)
            self.screen.blit(text, text_rect)
            self.screen.blit(score, score_rect)
            self.screen.blit(death, death_rect)
            self.screen.blit(best_score, best_score_rect)
            self.player_heart_manager = PlayerHeartManager()
            self.obstacle_manager = ObstacleManager()

    def handle_key_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False
                pygame.display.quit()
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                self.points = 0
                self.run()

    def update_best_score(self):
        if self.points > self.best_score:
            self.best_score = self.points
