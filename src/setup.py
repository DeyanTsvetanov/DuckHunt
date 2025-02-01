import pygame

class Setup:
    def __init__(self):
        """Initialize Pygame, create the window, and load assets"""
        self.screen_width = 800
        self.screen_height = 600

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Duck Hunt")
        
        self.background = pygame.image.load("assets/forest.png").convert()

    def get_screen(self):
        """Return the Pygame screen surface"""
        return self.screen

    def get_background(self):
        """Return the loaded background image"""
        return self.background
