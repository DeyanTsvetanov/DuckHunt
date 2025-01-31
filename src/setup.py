import pygame

class Setup:
    def __init__(self, screen_width=800, screen_height=600):
        """Initialize Pygame, create the window, and load assets"""
        pygame.init()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Duck Hunt")
        self.background = pygame.image.load("assets/forest.png").convert()

    def get_screen(self):
        """Return the Pygame screen surface"""
        return self.screen

    def get_background(self):
        """Return the loaded background image"""
        return self.background
