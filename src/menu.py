"""
This module implements the menu system.
"""
import sys
from collections.abc import Callable
import pygame
from src.music import Music
from src.button import Button


class Menu:
    """
    This class manages the main menu and the mode selection submenu. It displays buttons for 
    starting the game, showing top results, changing the background, and quitting. It 
    also plays the title music.
    """
    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock,
                 background: pygame.Surface, change_background: Callable[[], str]) -> None:
        """
        Initialize the menu with background and buttons.
        """
        self.screen = screen
        self.clock = clock
        self.running = True
        pygame.mouse.set_visible(True)
        self.background = background
        self.change_background = change_background

        # Initialize buttons
        self.main_menu_buttons = [
            Button(
                "Game Start", 250, 150, 300, 60, pygame.font.SysFont("Arial", 30), 
                pygame.Color("steelblue"), pygame.Color("dodgerblue")
            ),
            Button(
                "Top Results", 250, 230, 300, 60, pygame.font.SysFont("Arial", 30), 
                pygame.Color("steelblue"), pygame.Color("dodgerblue")
            ),
            Button(
                "Change Background", 250, 310, 300, 60, pygame.font.SysFont("Arial", 30), 
                pygame.Color("steelblue"), pygame.Color("dodgerblue")
            ),
            Button(
                "Quit", 250, 390, 300, 60, pygame.font.SysFont("Arial", 30), 
                pygame.Color("steelblue"), pygame.Color("dodgerblue")
            )
        ]

        self.mode_menu_buttons = [
            Button(
                "Standard Mode", 250, 150, 300, 60, pygame.font.SysFont("Arial", 30), 
                pygame.Color("steelblue"), pygame.Color("dodgerblue")
            ),
            Button(
                "Time Mode", 250, 230, 300, 60, pygame.font.SysFont("Arial", 30), 
                pygame.Color("steelblue"), pygame.Color("dodgerblue")
            )
        ]

        self.current_menu = "main"
        self.music_manager = Music()
        self.music_manager.play_music(self.music_manager.title_music)

    def display(self) -> None:
        """
        Display the menu screen with buttons and background.
        """
        while self.running:
            self.screen.blit(self.background, (0, 0))
            mouse_x, mouse_y = pygame.mouse.get_pos()

            buttons = self.main_menu_buttons if self.current_menu == "main" else self.mode_menu_buttons

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for button in buttons:
                        if button.is_clicked(event):
                            if button.text == "Change Background":
                                new_background_path = self.change_background()
                                self.background = pygame.image.load(new_background_path).convert()
                            elif button.text == "Quit":
                                sys.exit()
                            elif button.text == "Game Start":
                                self.select_mode()
                            elif button.text == "Top Results":
                                self.show_top_results()
                            elif button.text == "Standard Mode":
                                self.start_game("standard")
                            elif button.text == "Time Mode":
                                self.start_game("time")

            for button in buttons:
                button.draw(self.screen, (mouse_x, mouse_y))

            pygame.display.flip()
            self.clock.tick(60)

    def select_mode(self) -> None:
        """
        Open submenu for game mode selection.
        """
        self.current_menu = "mode"

    def start_game(self, mode: str) -> None:
        """
        Close the menu and start the game in the specified mode.
        """
        self.running = False
        self.chosen_mode = mode

    def load_results(self, filename: str) -> list[tuple[str, int]]:
        """
        Load results from a file, returning a list of (name, score) tuples.
        """
        try:
            with open(filename, "r", encoding="utf-8") as file:
                return [(name, int(score)) for name, score in (line.strip().split(",") for line in file.readlines())]
        except FileNotFoundError:
            return []

    def show_top_results(self) -> None:
        """
        Display the top results screen with a return button.
        """
        font = pygame.font.SysFont("Arial", 30)
        results_running = True

        # Load top results
        standard_results = self.load_results("standard_results.txt")
        time_results = self.load_results("time_results.txt")

        # Create the return button
        return_button = Button(
            "Return to Main Menu",
            self.screen.get_width() // 2 - 150,
            self.screen.get_height() - 100,
            300,
            60,
            font,
            pygame.Color("steelblue"),
            pygame.Color("dodgerblue")
        )

        while results_running:
            self.screen.fill(pygame.Color("black"))

            # Display headers
            self.screen.blit(
                font.render("Standard Mode", True, pygame.Color("white")),
                (50, 100)
            )
            self.screen.blit(
                font.render("Time Mode", True, pygame.Color("white")),
                (self.screen.get_width() // 2 + 20, 100)
            )

            # Display results for both modes
            y_offset = 140
            for i in range(max(len(standard_results), len(time_results))):
                if i < len(standard_results):
                    name, score = standard_results[i]
                    self.screen.blit(
                        font.render(f"{name}: {score}", True, pygame.Color("white")),
                        (50, y_offset)
                    )
                if i < len(time_results):
                    name, score = time_results[i]
                    self.screen.blit(
                        font.render(f"{name}: {score}", True, pygame.Color("white")),
                        (self.screen.get_width() // 2 + 20, y_offset)
                    )
                y_offset += 30

            # Handle events and button interactions
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    results_running = False
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if return_button.is_clicked(event):
                        results_running = False
                        self.current_menu = "main"

            return_button.draw(self.screen, mouse_pos)

            pygame.display.flip()
            self.clock.tick(60)
