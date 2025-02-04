import pygame

class GameOver:
    def __init__(self, screen, clock):
        """Initialize the Game Over screen"""
        self.screen = screen
        self.clock = clock
        self.font_large = pygame.font.SysFont("Arial", 48)
        self.font_small = pygame.font.SysFont("Arial", 36)

    def display(self, final_score):
        """Display the Game Over screen"""
        button_width, button_height = 300, 60
        button_color = pygame.Color("steelblue")
        button_hover_color = pygame.Color("dodgerblue")

        # Enable mouse cursor
        pygame.mouse.set_visible(True)

        running = True
        while running:
            self.screen.fill(pygame.Color("black"))

            # Display Game Over
            game_over_text = self.font_large.render("GAME OVER", True, pygame.Color("red"))
            game_over_rect = game_over_text.get_rect(center=(self.screen.get_width() // 2, 150))
            self.screen.blit(game_over_text, game_over_rect)

            # Display the final score
            score_text = self.font_small.render(f"Your Score: {final_score}", True, pygame.Color("white"))
            score_rect = score_text.get_rect(center=(self.screen.get_width() // 2, 220))
            self.screen.blit(score_text, score_rect)

            mouse_x, mouse_y = pygame.mouse.get_pos()
            button_x = (self.screen.get_width() - button_width) // 2
            button_y = 300

            button_hovered = button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and button_hovered:
                    running = False

            # Draw the button and it's text
            color = button_hover_color if button_hovered else button_color
            pygame.draw.rect(self.screen, color, (button_x, button_y, button_width, button_height))
            button_text = self.font_small.render("Back to Menu", True, pygame.Color("white"))
            button_text_rect = button_text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
            self.screen.blit(button_text, button_text_rect)

            pygame.display.flip()
            self.clock.tick(60)
