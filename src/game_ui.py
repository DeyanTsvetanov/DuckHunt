"""
This module provides the UI class for rendering the user interface elements.
"""
import pygame

class UI:
    """
    It provides methods for drawing the game UI on a specified pygame
    surface. It can display the standard game UI (with score, lives, and shots remaining)
    and the time-based UI (with score and remaining time).
    """
    def __init__(self, screen: pygame.Surface, font: pygame.font.Font) -> None:
        """
        Initialize the UI with a display surface and a font for rendering text.
        """
        self.screen = screen
        self.font = font

    def draw_standard_ui(self, score: int, lives: int, shots_remaining: int) -> None:
        """
        Draw the standard UI elements: score, lives, and shots remaining.
        """
        score_text = self.font.render(f"Score: {score}", True, pygame.Color("white"))
        lives_text = self.font.render(f"Lives: {lives}", True, pygame.Color("white"))
        shots_text = self.font.render(f"Shots: {shots_remaining}", True, pygame.Color("white"))
        self.screen.blit(score_text, (500, 490))
        self.screen.blit(lives_text, (240, 490))
        self.screen.blit(shots_text, (50, 490))

    def draw_time_ui(self, score: int, remaining_time: int) -> None:
        """
        Draw the time-based UI elements: score and remaining time.
        """
        score_text = self.font.render(f"Score: {score}", True, pygame.Color("white"))
        time_text = self.font.render(f"Time: {remaining_time}", True, pygame.Color("white"))
        self.screen.blit(score_text, (50, 490))
        self.screen.blit(time_text, (500, 490))
