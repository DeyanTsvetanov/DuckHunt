import pygame
from src.duck import Duck
from src.setup import Setup
from src.menu import Menu
from src.game_over import GameOver
from src.music import Music
import random

class Gameplay:
    def __init__(self, mode="standard"):
        """Initialize the game, load assets, and create objects"""
        self.mode = mode
        self.setup = Setup()
        self.screen = self.setup.get_screen()
        self.background = self.setup.get_background()
        self.music_manager = self.setup.get_music_manager()
        self.ducks = self.setup.get_ducks()
        self.current_duck = self.ducks[0]
        self.new_duck_timer_start = None
        self.duck_switch_delay = 2.0
        self.duck_hits = 0

        self.font = self.setup.get_font()
        self.score = 0
        self.clock = pygame.time.Clock()
        self.running = True

        self.total_time = None
        self.lives = 3 if mode == "standard" else None
        self.shots_remaining = 3 if mode == "standard" else None
        self.start_time = None

        self.smaller_scope = self.setup.get_scope()

    def switch_duck_with_delay(self):
        """Switch to a new duck after the specified delay"""
        if self.new_duck_timer_start is None:
            # Start the timer when switching is triggered
            self.new_duck_timer_start = pygame.time.get_ticks()

        elapsed_time = (pygame.time.get_ticks() - self.new_duck_timer_start) / 1000
        if elapsed_time >= self.duck_switch_delay:
            # Delay has passed, switch to a new duck and reset the timer
            self.new_duck_timer_start = None
            self.current_duck = random.choice(self.ducks)
            self.current_duck.respawn(mode=self.mode)

    def award_milestone_bonus(self):
        """Award bonus points for reaching a milestone"""
        milestone_bonus = 100 + (self.duck_hits // 5) * 5
        self.score += milestone_bonus

    def check_shooting(self, mouse_pos):
        """Check if the duck was shot"""
        if self.mode == "standard":
            if self.current_duck.alive and self.current_duck.rect.collidepoint(mouse_pos):
                self.music_manager.play_sound(self.music_manager.gunshot_sound)
                points = {"special": 100, "normal": 50, "red": -25}
                self.score += points.get(self.current_duck.duck_type, 0)
                if self.score < 0:
                    self.score = 0

                self.duck_hits += 1
                if self.duck_hits % 5 == 0:
                    self.music_manager.play_sound(self.music_manager.combo_sound)
                    self.award_milestone_bonus()

                if not self.current_duck.facing_right:
                    self.current_duck.image = pygame.transform.flip(self.current_duck.shot_image, True, False)
                else:
                    self.current_duck.image = self.current_duck.shot_image

                self.current_duck.is_shot = True
                self.current_duck.shot_time = pygame.time.get_ticks()
                self.shots_remaining = 3

            else:
                self.shots_remaining -= 1

            if self.shots_remaining == 0:
                self.lives -= 1
                if self.lives > 0:
                    self.current_duck.make_duck_fly_off()
                    self.shots_remaining = 3
                else:
                    self.music_manager.play_sound(self.music_manager.game_over_sound)
                    game_over = GameOver(self.screen, self.clock)
                    game_over.display(self.score)
                    self.running = False
        else:
            if self.current_duck.alive and self.current_duck.rect.collidepoint(mouse_pos):
                self.music_manager.play_sound(self.music_manager.gunshot_sound)
                points = {"special": 100, "normal": 50, "red": -25}
                self.score += points.get(self.current_duck.duck_type, 0)
                if self.score < 0:
                    self.score = 0

                self.duck_hits += 1
                if self.duck_hits % 5 == 0:
                    self.award_milestone_bonus()

                if not self.current_duck.facing_right:
                    self.current_duck.image = pygame.transform.flip(self.current_duck.shot_image, True, False)
                else:
                    self.current_duck.image = self.current_duck.shot_image

                self.current_duck.is_shot = True
                self.current_duck.shot_time = pygame.time.get_ticks()

    def reset_game(self):
        """Reset the game state to start a new game"""
        self.score = 0
        self.current_duck = random.choice(self.ducks)
        self.current_duck.respawn(mode=self.mode)
        self.running = True
        self.current_duck.speed_x = 3
        self.current_duck.speed_y = -3
        self.duck_hits = 0

        if self.mode == "standard":
            self.lives = 3
            self.shots_remaining = 3
        else:
            self.start_time = pygame.time.get_ticks()

    def handle_game_over(self):
        """Handle game over and save the score."""
        game_over = GameOver(self.screen, self.clock)
        game_over.display(self.score)

        menu = Menu(self.screen, self.clock, self.background, self.setup.change_background)
        if self.mode == "standard":
            menu.save_new_score("standard_results.txt", self.score)
        else:
            menu.save_new_score("time_results.txt", self.score)

        self.running = False

    def run(self):
        """Main game loop"""
        pygame.mouse.set_visible(False)
        self.reset_game()

        if self.mode == "time":
            self.start_time = pygame.time.get_ticks()
            self.total_time = 60

        while self.running:
            self.screen.blit(self.background, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.check_shooting(event.pos)

            if self.mode == "standard":
                if self.lives == 0:
                    self.handle_game_over()

                score_text = self.font.render(f"Score: {self.score}", True, pygame.Color("white"))
                lives_text = self.font.render(f"Lives: {self.lives}", True, pygame.Color("white"))
                shots_text = self.font.render(f"Shots: {self.shots_remaining}", True, pygame.Color("white"))

                self.screen.blit(score_text, (500, 490))
                self.screen.blit(lives_text, (240, 490))
                self.screen.blit(shots_text, (50, 490))
            else:
                elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000
                if self.total_time and elapsed_time >= self.total_time:
                    self.handle_game_over()

                score_text = self.font.render(f"Score: {self.score}", True, pygame.Color("white"))
                elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000
                remaining_time = max(int(self.total_time - elapsed_time), 0)
                time_text = self.font.render(f"Time: {remaining_time}", True, pygame.Color("white"))

                self.screen.blit(score_text, (50, 490))
                self.screen.blit(time_text, (500, 490))

            self.current_duck.handle_respawn()
            if self.current_duck.alive:
                self.current_duck.move()
                self.current_duck.draw(self.screen)

            mouse_x, mouse_y = pygame.mouse.get_pos()
            scope_rect = self.smaller_scope.get_rect(center=(mouse_x, mouse_y))
            self.screen.blit(self.smaller_scope, scope_rect)

            pygame.display.flip()
            self.clock.tick(60)

    def start(self):
        """Start the game by displaying the menu and handling transitions"""
        menu = Menu(self.screen, self.clock, self.background, self.setup.change_background)
        menu.display()
        chosen_mode = getattr(menu, "chosen_mode", "standard")
        self.mode = chosen_mode
        print(f"Chosen mode: {self.mode}")
        self.run()
        game_over = GameOver(self.screen, self.clock)
        game_over.display(self.score)
        self.start()
