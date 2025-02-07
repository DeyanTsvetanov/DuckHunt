import pygame
from src.button import Button

class GameOver:
    def __init__(self, screen, clock):
        """Initialize the Game Over screen"""
        self.screen = screen
        self.clock = clock
        self.font_large = pygame.font.SysFont("Arial", 48)
        self.font_small = pygame.font.SysFont("Arial", 30)

    def display(self, final_score):
        """Display the Game Over screen"""

        # Creating buttons
        back_to_menu_button = Button("Back to Menu", 250, 300, 300, 60, self.font_small, pygame.Color("steelblue"), pygame.Color("dodgerblue"))

        # Enable mouse cursor
        pygame.mouse.set_visible(True)

        running = True
        while running:
            self.screen.fill(pygame.Color("black"))

            # Display Game Over and Score
            game_over_text = self.font_large.render("GAME OVER", True, pygame.Color("red"))
            score_text = self.font_small.render(f"Your Score: {final_score}", True, pygame.Color("white"))

            self.screen.blit(game_over_text, game_over_text.get_rect(center=(self.screen.get_width() // 2, 150)))
            self.screen.blit(score_text, score_text.get_rect(center=(self.screen.get_width() // 2, 220)))

            # Handle events and button interactions
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if back_to_menu_button.is_clicked(event):
                    print("Back to Menu button clicked")
                    running = False

            # Draw button
            back_to_menu_button.draw(self.screen, mouse_pos)

            pygame.display.flip()
            self.clock.tick(60)
