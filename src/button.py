"""
This module defines the Button class used in the DuckHunt game for handling UI button design.
"""
import pygame
from pygame.locals import MOUSEBUTTONDOWN

class Button:
    """
    A UI button design for the DuckHunt game.
    This class supports rendering a button with text, handling hover effects,
    and detecting click events.
    """
    def __init__(self, text: str, x: int, y: int, width: int, height: int,
                 font: pygame.font.Font, color: pygame.Color, hover_color: pygame.Color) -> None:
        """
        Initialize a button with text, position, dimensions, and colors.
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color

    def draw(self, screen: pygame.Surface, mouse_pos: tuple[int, int]) -> None:
        """
        Draw the button on the screen with hover effect.
        """
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(screen, color, self.rect)
        text_surface = self.font.render(self.text, True, pygame.Color("white"))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event: pygame.event.Event) -> bool:
        """
        Check if the button has been clicked.
        """
        return event.type == MOUSEBUTTONDOWN and self.rect.collidepoint(pygame.mouse.get_pos())
