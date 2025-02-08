import pygame
from src.button import Button

class GameOver:
    def __init__(self, screen, clock):
        """
        Initialize the Game Over screen.
        """
        self.screen = screen
        self.clock = clock
        self.font_large = pygame.font.SysFont("Arial", 48)
        self.font_small = pygame.font.SysFont("Arial", 30)

    def display(self, final_score):
        """
        Display the Game Over screen with the final score and a "Back to Menu" button. 
        When the button is clicked, prompt for the player's name.
        """
        # Creating "Back to Menu" button.
        button_width = 300
        button_height = 60
        button_x = self.screen.get_width() // 2 - button_width // 2
        button_y = 300
        back_to_menu_button = Button(
            "Back to Menu", 
            button_x, button_y, button_width, button_height,
            self.font_small, pygame.Color("steelblue"), pygame.Color("dodgerblue")
        )
        pygame.mouse.set_visible(True)

        running = True
        while running:
            self.screen.fill(pygame.Color("black"))
            
            # Display game over and final score.
            game_over_text = self.font_large.render("GAME OVER", True, pygame.Color("red"))
            score_text = self.font_small.render(f"Your Score: {final_score}", True, pygame.Color("white"))
            self.screen.blit(game_over_text, game_over_text.get_rect(center=(self.screen.get_width() // 2, 150)))
            self.screen.blit(score_text, score_text.get_rect(center=(self.screen.get_width() // 2, 220)))
            
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    return ""  # Return empty name if quitting
                if back_to_menu_button.is_clicked(event):
                    running = False

            back_to_menu_button.draw(self.screen, mouse_pos)
            pygame.display.flip()
            self.clock.tick(60)
        
        player_name = self.prompt_for_name()
        return player_name

    def prompt_for_name(self):
        """
        Display a prompt for the player to enter their name.
        """
        input_active = True
        player_name = ""
        pygame.mouse.set_visible(False)
        font = self.font_small
        input_box_color = pygame.Color("steelblue")
        input_text_color = pygame.Color("white")
        background_color = pygame.Color("black")

        while input_active:
            self.screen.fill(background_color)
            
            prompt_text = font.render("Enter Your Name:", True, input_text_color)
            prompt_rect = prompt_text.get_rect(center=(self.screen.get_width() // 2, 150))
            self.screen.blit(prompt_text, prompt_rect)

            input_box_rect = pygame.Rect(self.screen.get_width() // 2 - 150, 200, 300, 50)
            pygame.draw.rect(self.screen, input_box_color, input_box_rect)
            
            name_text = font.render(player_name, True, input_text_color)
            self.screen.blit(name_text, (input_box_rect.x + 10, input_box_rect.y + 10))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    input_active = False
                    return ""
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    else:
                        player_name += event.unicode
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.mouse.set_visible(True)
        return player_name

    def load_results(self, filename):
        """
        Load existing results from the given file.
        """
        results = []
        try:
            with open(filename, "r") as file:
                for line in file:
                    parts = line.strip().split(",")
                    if len(parts) == 2:
                        name, score = parts
                        results.append((name, int(score)))
        except FileNotFoundError:
            pass
        return results

    def save_new_score(self, filename, score, player_name):
        """
        Save the new score along with the player's name to the given file,
        keeping only the top 10 scores.
        """
        results = self.load_results(filename)
        results.append((player_name, score))
        results = sorted(results, key=lambda x: x[1], reverse=True)[:10]
        with open(filename, "w") as file:
            for name, s in results:
                file.write(f"{name},{s}\n")
