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
        self.buttons = [
            {"text": "Game Start", "action": self.start_game},
            {"text": "Quit", "action": sys.exit}
        ]

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

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for i, button in enumerate(self.buttons):
                        if self.is_mouse_over_button(mouse_x, mouse_y, i, button_width, button_height, button_margin):
                            if button["action"]:
                                button["action"]()

            screen_width = self.screen.get_width()
            # Draw buttons
            for i, button in enumerate(self.buttons):
                button_x = (screen_width - button_width) // 2
                button_y = 150 + i * (button_height + button_margin)
                color = button_hover_color if self.is_mouse_over_button(mouse_x, mouse_y, i, button_width, button_height, button_margin) else button_color
                pygame.draw.rect(self.screen, color, (button_x, button_y, button_width, button_height))
                text_surface = font.render(button["text"], True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
                self.screen.blit(text_surface, text_rect)

            pygame.display.flip()
            self.clock.tick(60)

    def is_mouse_over_button(self, mouse_x, mouse_y, index, button_width, button_height, button_margin):
        """Check if the mouse is over a specific button"""
        screen_width = self.screen.get_width()
        button_x = (screen_width - button_width) // 2
        button_y = 150 + index * (button_height + button_margin)
        return button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height

    def start_game(self):
        """Start the game (for now, just print a message)"""
        self.running = False
