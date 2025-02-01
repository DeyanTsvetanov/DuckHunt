import pygame
from src.duck import Duck
from src.setup import Setup
import random

class Gameplay:
    def __init__(self):
        """Initialize the game, load assets, and create objects"""
        self.setup = Setup()
        self.screen = self.setup.get_screen()
        self.background = self.setup.get_background()
        self.duck = [
            Duck(self.setup.screen_width, 360, "assets/final_normal_duck.png"),
            Duck(self.setup.screen_width, 360, "assets/final_red_duck.png"),
            Duck(self.setup.screen_width, 360, "assets/final_special_duck.png")
        ]
        self.current_duck = self.duck[0]
        pygame.font.init()
        self.font = pygame.font.SysFont("Arial Black", 30)
        self.score = 0
        self.clock = pygame.time.Clock()
        self.running = True
        self.score = 0
        self.lives = 3
        self.shots_remaining = 3
        self.scope = pygame.image.load("assets/scope.png").convert_alpha()
        self.smaller_scope = pygame.transform.scale(self.scope, (40, 40))
        pygame.mouse.set_visible(False)

    def check_shooting(self, mouse_pos):
        """Check if the duck was shot"""
        if self.current_duck.rect.collidepoint(mouse_pos):
            self.score += 50
            self.current_duck.respawn()
            self.shots_remaining = 3

            # Set a timer for the next duck
            #self.next_duck_timer = pygame.time.get_ticks() + 1000  # 1-second delay
            self.current_duck = random.choice(self.duck)
        else:
            self.shots_remaining -= 1

        if self.shots_remaining == 0:
            self.lives -= 1
            if self.lives > 0:
                self.current_duck.make_duck_fly_off()
                self.shots_remaining = 3
            else:
                self.game_over_screen()

    def game_over_screen(self):
        """Display a 'Game Over' message on the screen"""
        game_over_text = self.font.render("GAME OVER", True, (255, 0, 0))
        text_rect = game_over_text.get_rect(center=(self.setup.screen_width // 2, self.setup.screen_height // 2))
        self.screen.blit(game_over_text, text_rect)
        pygame.display.flip()
        pygame.time.wait(3000)

    def run(self):
        """Main game loop"""
        while self.running:
            self.screen.blit(self.background, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.check_shooting(event.pos)

            if self.lives == 0:
                self.game_over_screen()
                self.running = False

            score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
            lives_text = self.font.render(f"Lives: {self.lives}", True, (255, 255, 255))
            shots_text = self.font.render(f"Shots: {self.shots_remaining}", True, (255, 255, 255))
            
            self.screen.blit(score_text, (500, 490))
            self.screen.blit(lives_text, (240, 490))
            self.screen.blit(shots_text, (50, 490))

            self.current_duck.update_respawn()
            self.current_duck.move()
            self.current_duck.draw(self.screen)

            mouse_x, mouse_y = pygame.mouse.get_pos()
            scope_rect = self.smaller_scope.get_rect(center=(mouse_x, mouse_y))
            self.screen.blit(self.smaller_scope, scope_rect)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
