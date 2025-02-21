"""
This module implements the main game logic.
"""
import random
import pygame
from src.setup import Setup
from src.menu import Menu
from src.game_over import GameOver
from src.game_ui import UI

class Gameplay:
    """
    This class is responsible for initializing the game environment,
    managing game states, processing user input, updating game objects
    (such as ducks), and rendering the game UI. It supports both standard
    and time-based game modes.
    """
    def __init__(self, mode: str = "standard") -> None:
        """
        Initialize the game, load assets, and create objects.
        """
        self.mode = mode
        self.setup = Setup()
        self.screen = self.setup.get_screen()
        self.background = self.setup.get_background()
        self.music_manager = self.setup.get_music_manager()
        self.ducks = self.setup.get_ducks()
        self.current_duck = self.ducks[0]
        self.new_duck_timer_start: int | None = None
        self.duck_switch_delay = 2.0
        self.duck_hits = 0

        self.font = self.setup.get_font()
        self.score = 0
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over_flag = False

        self.total_time: int | None = None
        self.lives = 3 if mode == "standard" else None
        self.shots_remaining = 3 if mode == "standard" else None
        self.start_time: int | None = None

        self.smaller_scope = self.setup.get_scope()
        self.ui_manager = UI(self.screen, self.font)

    def switch_duck_with_delay(self) -> None:
        """
        Switch to a new duck after the specified delay.
        """
        if self.new_duck_timer_start is None:
            # Start the timer when switching is triggered
            self.new_duck_timer_start = pygame.time.get_ticks()

        elapsed_time = (pygame.time.get_ticks() - self.new_duck_timer_start) / 1000
        if elapsed_time >= self.duck_switch_delay:
            # Delay has passed, switch to a new duck and reset the timer
            self.new_duck_timer_start = None
            self.current_duck = random.choice(self.ducks)
            self.current_duck.respawn(mode=self.mode)

    def award_milestone_bonus(self) -> None:
        """
        Award bonus points for reaching a milestone.
        """
        milestone_bonus = 100 + (self.duck_hits // 5) * 5
        self.score += milestone_bonus

    def process_hit(self, play_combo_sound: bool = False) -> None:
        """
        Handle a successful duck hit.
        """
        self.music_manager.play_sound(self.music_manager.gunshot_sound)
        points = {"special": 100, "normal": 50, "red": -25}
        self.score += points.get(self.current_duck.duck_type, 0)
        self.score = max(self.score, 0)

        self.duck_hits += 1
        if self.duck_hits % 5 == 0:
            if play_combo_sound:
                self.music_manager.play_sound(self.music_manager.combo_sound)
            self.award_milestone_bonus()

        # Set the appropriate shot image depending on duck direction.
        if not self.current_duck.facing_right:
            self.current_duck.image = pygame.transform.flip(
                self.current_duck.shot_image, True, False
            )
        else:
            self.current_duck.image = self.current_duck.shot_image

        self.current_duck.is_shot = True
        self.current_duck.shot_time = pygame.time.get_ticks()

    def check_shooting(self, mouse_pos: tuple) -> None:
        """
        Check if the duck was shot and update game state accordingly.
        """
        hit = self.current_duck.alive and self.current_duck.rect.collidepoint(mouse_pos)

        if hit:
            if self.mode == "standard":
                self.process_hit(play_combo_sound=True)
                self.shots_remaining = 3
            else:
                self.process_hit()
        elif self.mode == "standard":
            assert self.shots_remaining is not None
            self.shots_remaining -= 1
            if self.shots_remaining == 0:
                assert self.lives is not None
                self.lives -= 1
                if self.lives > 0:
                    self.current_duck.make_duck_fly_off()
                    self.shots_remaining = 3
                else:
                    self.running = False

    def reset_game(self) -> None:
        """
        Reset the game state to start a new game.
        """
        self.score = 0
        self.current_duck = random.choice(self.ducks)
        self.current_duck.respawn(mode=self.mode)
        self.running = True
        self.game_over_flag = False
        self.current_duck.speed_x = 3
        self.current_duck.speed_y = -3
        self.duck_hits = 0

        if self.mode == "standard":
            self.lives = 3
            self.shots_remaining = 3
        else:
            self.start_time = pygame.time.get_ticks()

    def handle_game_over(self) -> None:
        """
        Execute the game-over sequence.
        """
        self.music_manager.play_sound(self.music_manager.game_over_sound)
        game_over = GameOver(self.screen, self.clock)
        player_name = game_over.display(self.score)
        print(f"Returned from game over; player name: {player_name}")
        if player_name.strip() != "":
            if self.mode == "standard":
                game_over.save_new_score("standard_results.txt", self.score, player_name)
            else:
                game_over.save_new_score("time_results.txt", self.score, player_name)
        else:
            print("No valid name entered! Score wasn't saved.")
        pygame.time.delay(500)
        pygame.event.clear()
        self.running = False
        print("Exiting handle_game_over(), game loop stopped.")

    def process_events(self) -> None:
        """
        Process user input.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.check_shooting(event.pos)

    def update(self) -> None:
        """
        Update game logic for duck status and game over conditions.
        """
        if not self.current_duck.alive:
            self.switch_duck_with_delay()

        if self.mode == "standard":
            if self.lives == 0 and not self.game_over_flag:
                self.game_over_flag = True
                self.handle_game_over()
        else:
            assert self.start_time is not None
            elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000
            if self.total_time and elapsed_time >= self.total_time and not self.game_over_flag:
                self.game_over_flag = True
                self.handle_game_over()

        self.current_duck.handle_respawn()
        if self.current_duck.alive:
            self.current_duck.move()

    def render(self) -> None:
        """
        Render all game elements.
        """
        self.screen.blit(self.background, (0, 0))

        # Drawing of UI elements
        if self.mode == "standard":
            assert self.lives is not None
            assert self.shots_remaining is not None
            self.ui_manager.draw_standard_ui(self.score, self.lives, self.shots_remaining)
        else:
            assert self.start_time is not None
            assert self.total_time is not None
            elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000
            remaining_time = max(int(self.total_time - elapsed_time), 0)
            self.ui_manager.draw_time_ui(self.score, remaining_time)

        if self.current_duck.alive:
            self.current_duck.draw(self.screen)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        scope_rect = self.smaller_scope.get_rect(center=(mouse_x, mouse_y))
        self.screen.blit(self.smaller_scope, scope_rect)
        pygame.display.flip()

    def run(self) -> None:
        """
        Main game loop.
        """
        pygame.mouse.set_visible(False)
        self.reset_game()

        if self.mode == "time":
            self.start_time = pygame.time.get_ticks()
            self.total_time = 60

        while self.running:
            self.process_events()
            self.update()
            self.render()
            self.clock.tick(60)

    def start(self) -> None:
        """
        Manage transitions between the menu, gameplay, and game-over screens.
        """
        while True:
            menu = Menu(self.screen, self.clock, self.background, self.setup.change_background)
            menu.display()
            self.background = menu.background
            self.mode = getattr(menu, "chosen_mode", "standard")
            print(f"Chosen mode: {self.mode}")
            pygame.mixer.music.stop()
            self.run()
            self.reset_game()
