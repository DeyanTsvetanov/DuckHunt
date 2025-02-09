import pygame

class UI:
    def __init__(self, screen: pygame.Surface, font: pygame.font.Font) -> None:
        self.screen = screen
        self.font = font

    def draw_standard_ui(self, score: int, lives: int, shots_remaining: int) -> None:
        score_text = self.font.render(f"Score: {score}", True, pygame.Color("white"))
        lives_text = self.font.render(f"Lives: {lives}", True, pygame.Color("white"))
        shots_text = self.font.render(f"Shots: {shots_remaining}", True, pygame.Color("white"))
        self.screen.blit(score_text, (500, 490))
        self.screen.blit(lives_text, (240, 490))
        self.screen.blit(shots_text, (50, 490))

    def draw_time_ui(self, score: int, remaining_time: int) -> None:
        score_text = self.font.render(f"Score: {score}", True, pygame.Color("white"))
        time_text = self.font.render(f"Time: {remaining_time}", True, pygame.Color("white"))
        self.screen.blit(score_text, (50, 490))
        self.screen.blit(time_text, (500, 490))
