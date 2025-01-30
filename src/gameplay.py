import pygame
from src.duck import Duck
from src.setup import Setup

class Gameplay:
    def __init__(self):
        """Initialize the game, load assets, and create objects"""
        self.setup = Setup()
        self.screen = self.setup.get_screen()
        self.background = self.setup.get_background()
        self.duck = Duck(self.setup.screen_width, 360, "assets/duck1.png", "assets/duck2.png")
        pygame.font.init()
        self.font = pygame.font.SysFont("Arial Black", 30)
        self.score = 0
        self.clock = pygame.time.Clock()
        self.running = True
        self.score = 0

    def check_shooting(self, mouse_pos):
        """Check if the duck was shot"""
        if self.duck.rect.collidepoint(mouse_pos):
            self.score += 50
            self.duck.respawn()

    def run(self):
        """Main game loop"""
        while self.running:
            self.screen.blit(self.background, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.check_shooting(event.pos)

            score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
            self.screen.blit(score_text, (500, 490))

            self.duck.update_respawn()
            self.duck.move()
            self.duck.animate()
            self.duck.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()