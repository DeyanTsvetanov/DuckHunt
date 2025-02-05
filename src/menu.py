import pygame
import sys

class Menu:
    def __init__(self, screen, clock, background, change_background_func):
        """Initialize the menu with background and buttons"""
        self.screen = screen
        self.clock = clock
        self.running = True
        pygame.mouse.set_visible(True)
        self.background = background
        self.change_background_func = change_background_func
        self.main_menu_buttons = [
            {"text": "Game Start", "action": self.select_mode},
            {"text": "Top Results", "action": self.show_top_results},
            {"text": "Change Background", "action": self.change_background_func},
            {"text": "Quit", "action": sys.exit}
        ]
        self.mode_menu_buttons = [
            {"text": "Standard Mode", "action": lambda: self.start_game("standard")},
            {"text": "Time Mode", "action": lambda: self.start_game("time")}
        ]

        self.current_menu = "main"

    def display(self):
        """Display the menu screen with buttons and background"""
        font = pygame.font.SysFont("Arial", 30)

        # Button settings
        button_width, button_height = 300, 60
        button_margin = 20
        button_color = pygame.Color("steelblue")
        button_hover_color = pygame.Color("dodgerblue")

        while self.running:
            self.screen.blit(self.background, (0, 0))
            mouse_x, mouse_y = pygame.mouse.get_pos()

            top_y = 150
            if self.current_menu == "main":
                buttons = self.main_menu_buttons
            elif self.current_menu == "mode":
                buttons = self.mode_menu_buttons
            elif self.current_menu == "top_results":
                self.show_top_results()
                continue

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for i, button in enumerate(buttons):
                        if self.is_mouse_over_button(mouse_x, mouse_y, i, button_width, button_height, button_margin, top_y):
                            if button["text"] == "Change Background":
                                self.change_background_func()
                                self.background = pygame.image.load(self.change_background_func()).convert()
                            else:
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
        """Open submenu for game mode selection"""
        self.current_menu = "mode"

    def start_game(self, mode):
        """Close the menu and start the game in the specified mode"""
        self.running = False
        self.chosen_mode = mode

    def load_results(self, filename):
        """Load results from a file, returning a list of (name, score) tuples."""
        try:
            with open(filename, "r") as file:
                return [(name, int(score)) for name, score in (line.strip().split(",") for line in file.readlines())]
        except FileNotFoundError:
            return []

    def save_new_score(self, filename, new_score):
        """Prompt for player name and save the new score to the file, keeping only the top 10 scores."""
        name = self.prompt_for_name()
        results = self.load_results(filename)
        results.append((name, new_score))
        results = sorted(results, key=lambda x: x[1], reverse=True)[:10]
        with open(filename, "w") as file:
            for name, score in results:
                file.write(f"{name},{score}\n")

    def prompt_for_name(self):
        """Display a window for the player to enter their name."""
        font = pygame.font.SysFont("Arial", 36)
        input_active = True
        player_name = ""

        # Define colors for name window
        input_box_color = pygame.Color("steelblue")
        input_text_color = pygame.Color("white")
        background_color = pygame.Color("black")

        while input_active:
            self.screen.fill(background_color)

            # Display prompt text
            prompt_text = font.render("Enter Your Name:", True, input_text_color)
            prompt_rect = prompt_text.get_rect(center=(self.screen.get_width() // 2, 150))
            self.screen.blit(prompt_text, prompt_rect)

            # Display the input box
            input_box_rect = pygame.Rect((self.screen.get_width() // 2 - 150, 200, 300, 50))
            pygame.draw.rect(self.screen, input_box_color, input_box_rect)

            # Display the player's current input text
            input_text_surface = font.render(player_name, True, input_text_color)
            self.screen.blit(input_text_surface, (input_box_rect.x + 10, input_box_rect.y + 10))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    input_active = False
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    else:
                        player_name += event.unicode

            pygame.display.flip()
            self.clock.tick(60)

        return player_name

    def show_top_results(self):
        font = pygame.font.SysFont("Arial", 30)
        results_running = True

        # Load and display top 10 results from files
        standard_results = self.load_results("standard_results.txt")
        time_results = self.load_results("time_results.txt")

        button_width, button_height = 300, 60
        button_color = pygame.Color("steelblue")
        button_hover_color = pygame.Color("dodgerblue")

        while results_running:
            self.screen.fill(pygame.Color("black"))

            # Display results for both modes
            left_x = 50
            right_x = self.screen.get_width() // 2 + 20
            y_offset = 100

            self.screen.blit(font.render("Standard Mode", True, pygame.Color("white")), (left_x, y_offset))
            self.screen.blit(font.render("Time Mode", True, pygame.Color("white")), (right_x, y_offset))

            y_offset += 40
            for i in range(max(len(standard_results), len(time_results))):
                if i < len(standard_results):
                    name, score = standard_results[i]
                    self.screen.blit(font.render(f"{name}: {score}", True, pygame.Color("white")), (left_x, y_offset))
                if i < len(time_results):
                    name, score = time_results[i]
                    self.screen.blit(font.render(f"{name}: {score}", True, pygame.Color("white")), (right_x, y_offset))
                y_offset += 30

            # Draw the return button
            mouse_x, mouse_y = pygame.mouse.get_pos()
            button_x = (self.screen.get_width() - button_width) // 2
            button_y = self.screen.get_height() - button_height - 50

            button_hovered = button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height
            color = button_hover_color if button_hovered else button_color
            pygame.draw.rect(self.screen, color, (button_x, button_y, button_width, button_height))
            button_text = font.render("Return to Main Menu", True, pygame.Color("white"))
            button_text_rect = button_text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
            self.screen.blit(button_text, button_text_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    results_running = False
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and button_hovered:
                    results_running = False
                    self.current_menu = "main"

            pygame.display.flip()
            self.clock.tick(60)
