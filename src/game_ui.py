import pygame

class UI:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font

    def draw_standard_ui(self, score, lives, shots_remaining):
        score_text = self.font.render(f"Score: {score}", True, pygame.Color("white"))
        lives_text = self.font.render(f"Lives: {lives}", True, pygame.Color("white"))
        shots_text = self.font.render(f"Shots: {shots_remaining}", True, pygame.Color("white"))
        self.screen.blit(score_text, (500, 490))
        self.screen.blit(lives_text, (240, 490))
        self.screen.blit(shots_text, (50, 490))

    def draw_time_ui(self, score, remaining_time):
        score_text = self.font.render(f"Score: {score}", True, pygame.Color("white"))
        time_text = self.font.render(f"Time: {remaining_time}", True, pygame.Color("white"))
        self.screen.blit(score_text, (50, 490))
        self.screen.blit(time_text, (500, 490))
