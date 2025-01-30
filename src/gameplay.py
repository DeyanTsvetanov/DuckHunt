import pygame
from src.duck import Duck
from src.setup import Setup

class Gameplay:
    def __init__(self):
        """Initialize the game, load assets, and create objects"""
        self.setup = Setup()
        self.screen = self.setup.get_screen()
        self.background = self.setup.get_background()
        self.duck = Duck(self.setup.screen_width, self.setup.screen_height, "assets/duck1.png", "assets/duck2.png")
        pygame.font.init()
        self.font = pygame.font.SysFont("Arial Black", 30)
        self.score = 0
        self.clock = pygame.time.Clock()
        self.running = True
        self.score = 0
        self.lives = 3
        self.shots_remaining = 3

    def check_shooting(self, mouse_pos):
        """Check if the duck was shot"""
        if self.duck.rect.collidepoint(mouse_pos):
            self.score += 50
            self.duck.respawn()
            self.shots_remaining = 3
        else:
            self.shots_remaining -= 1

        if self.shots_remaining == 0:
            self.lives -= 1
            if self.lives > 0:
                self.duck.make_duck_fly_off()
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
            self.screen.blit(lives_text, (300, 490))
            self.screen.blit(shots_text, (100, 490))

            self.duck.update_respawn()
            self.duck.move()
            self.duck.animate()
            self.duck.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()