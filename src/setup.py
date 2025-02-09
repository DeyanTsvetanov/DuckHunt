"""
This module initializes the game environment for the DuckHunt game.
"""
import pygame
from src.duck import Duck
from src.music import Music

class Setup:
    """
    This class creates the main display window, loads and cycles through background images,
    initializes fonts and scope images, and instantiates game objects like ducks and
    the music manager. The class provides several getter methods to retrieve these assets
    for use by other parts of the game.
"""
    def __init__(self) -> None:
        """
        Initialize Pygame, create the window, and load assets.
        """
        self.screen_width = 800
        self.screen_height = 600

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Duck Hunt")

        # Load backgrounds
        self.backgrounds = [
            "assets/forest.png",
            "assets/mountain.png",
            "assets/field.png"
        ]
        self.current_background_index = 0
        self.background = pygame.image.load(self.backgrounds[self.current_background_index]).convert()

        pygame.font.init()
        self.font = pygame.font.SysFont("Arial Black", 30)

        self.scope = pygame.image.load("assets/scope.png").convert_alpha()
        self.smaller_scope = pygame.transform.scale(self.scope, (40, 40))

        self.music_manager = Music()

        self.ducks = [
            Duck(self.screen_width, 360, "assets/final_normal_duck.png", "normal"),
            Duck(self.screen_width, 360, "assets/final_red_duck.png", "red"),
            Duck(self.screen_width, 360, "assets/final_special_duck.png", "special")
        ]

    def get_screen(self) -> pygame.Surface:
        """
        Return the Pygame screen surface.
        """
        return self.screen

    def get_background(self) -> pygame.Surface:
        """
        Return the loaded background image.
        """
        return self.background

    def change_background(self) -> str:
        """
        Cycle through the backgrounds and return the new path.
        """
        self.current_background_index = (self.current_background_index + 1) % len(self.backgrounds)
        new_background_path = self.backgrounds[self.current_background_index]
        self.background = pygame.image.load(new_background_path).convert()
        return new_background_path

    def get_font(self) -> pygame.font.Font:
        """
        Return the font object.
        """
        return self.font

    def get_scope(self) -> pygame.Surface:
        """
        Return the scope image.
        """
        return self.smaller_scope

    def get_music_manager(self) -> Music:
        """
        Return the music manager.
        """
        return self.music_manager

    def get_ducks(self) -> list[Duck]:
        """
        Return the list of duck objects.
        """
        return self.ducks
