import pygame
import sys

class Menu:
    def __init__(self, screen, clock):
        """Initialize the menu with background and buttons"""
        self.screen = screen
        self.clock = clock
        self.running = True
        pygame.mouse.set_visible(True)
        self.background = pygame.image.load("assets/forest.png").convert()
        self.main_menu_buttons = [
            {"text": "Game Start", "action": self.select_mode},
            {"text": "Quit", "action": sys.exit}
        ]
        self.mode_menu_buttons = [
            {"text": "Standard Mode", "action": lambda: self.start_game("standard")},
            {"text": "Time Mode", "action": lambda: self.start_game("time")}
        ]

        self.current_menu = "main"

    def display(self):
        """Display the menu screen with buttons and background"""
        font = pygame.font.SysFont("Arial", 36)

        # Button settings
        button_width, button_height = 300, 60
        button_margin = 20
        button_color = pygame.Color("steelblue")
        button_hover_color = pygame.Color("dodgerblue")

        while self.running:
            self.screen.blit(self.background, (0, 0))
            mouse_x, mouse_y = pygame.mouse.get_pos()

            top_y = 150
            buttons = self.main_menu_buttons if self.current_menu == "main" else self.mode_menu_buttons

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for i, button in enumerate(buttons):
                        if self.is_mouse_over_button(mouse_x, mouse_y, i, button_width, button_height, button_margin, top_y):
                            if button["action"]:
                                button["action"]()

            screen_width = self.screen.get_width()
            # Draw buttons
            for i, button in enumerate(buttons):
                button_x = (screen_width - button_width) // 2
                button_y = top_y + i * (button_height + button_margin)
                color = button_hover_color if self.is_mouse_over_button(mouse_x, mouse_y, i, button_width, button_height, button_margin, top_y) else button_color
                pygame.draw.rect(self.screen, color, (button_x, button_y, button_width, button_height))
                text_surface = font.render(button["text"], True, pygame.Color("white"))
                text_rect = text_surface.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
                self.screen.blit(text_surface, text_rect)

            pygame.display.flip()
            self.clock.tick(60)

    def is_mouse_over_button(self, mouse_x, mouse_y, index, button_width, button_height, button_margin, top_y):
        """Check if the mouse is over a specific button"""
        screen_width = self.screen.get_width()
        button_x = (screen_width - button_width) // 2
        button_y = top_y + index * (button_height + button_margin)
        return button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height

    def select_mode(self):
        """Отваря подменю за избор на игра"""
        self.current_menu = "mode"

    def start_game(self, mode):
        """Затваря менюто и стартираме играта в зададения режим"""
        self.running = False
        self.chosen_mode = mode
