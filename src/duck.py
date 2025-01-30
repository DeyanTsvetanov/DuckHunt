import pygame
import random

class Duck:
    def __init__(self, screen_width, screen_height, sprite_path1, sprite_path2):
        """Initialize the duck with animation and movement"""
        self.image1 = pygame.image.load(sprite_path1).convert_alpha()
        self.image2 = pygame.image.load(sprite_path2).convert_alpha()
        self.flipped_image1 = pygame.transform.flip(self.image1, True, False)
        self.flipped_image2 = pygame.transform.flip(self.image2, True, False)
        self.image = self.image1
        self.rect = self.image.get_rect()

        # Define the flying window (800x360)
        self.x_min = 0
        self.x_max = 800 - self.rect.width
        self.y_min = 0
        self.y_max = 360 - self.rect.height

        self.respawn_timer = 0  # Timer for delayed respawn
        self.alive = True  # Tracks if the duck is visible or not

        # Add movement speed
        self.speed_x = 3
        self.speed_y = -3

        self.facing_right = self.speed_x > 0  # Set direction based on speed

        self.respawn()  # Set initial position at the grass level

        # Animation settings
        self.animation_timer = 0
        self.animation_speed = 10
        self.current_frame = 0

    def move(self):
        """Moves the duck and ensures it bounces correctly"""
        if self.alive:
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y

            # Chance to move on zigzag
            if random.randint(1, 100) < 5:  # 5% chance to change vertical direction
                self.speed_y = -self.speed_y

            # Bounce off the left and right edges
            if self.rect.x <= self.x_min or self.rect.x >= self.x_max:
                self.speed_x = -self.speed_x  # Reverse direction
                self.facing_right = not self.facing_right  # Flip sprite direction

            # Bounce off the top boundary
            if self.rect.y >= self.y_max:
                self.rect.y = self.y_max
                self.speed_y = -3

            # Bounce off the top boundary
            if self.rect.y <= self.y_min:
                self.speed_y = 3

    def animate(self):
        """Switch between two images every few frames and apply correct flipping"""
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            if self.facing_right:
                self.image = self.image2 if self.image == self.image1 else self.image1
            else:
                self.image = self.flipped_image2 if self.image == self.flipped_image1 else self.flipped_image1
            self.animation_timer = 0

    def draw(self, screen):
        """Draw the duck on the screen"""
        screen.blit(self.image, self.rect)

    def respawn(self):
        """Hides the duck before respawning after a delay, resets direction, and increases speed"""
        self.alive = False
        self.respawn_timer = pygame.time.get_ticks() + 1000  # 1 second delay

        # Move the duck off-screen
        self.rect.x = -100
        self.rect.y = -100

        # Increase speed after each respawn
        self.speed_x = abs(self.speed_x) * 1.1
        self.speed_y = -abs(self.speed_y) * 1.1

        # Always start facing right after respawning
        self.facing_right = True

    def update_respawn(self):
        """Respawns the duck after a delay with increased speed"""
        if not self.alive and pygame.time.get_ticks() >= self.respawn_timer:
            self.alive = True
            self.respawn_timer = 0
            
            # Duck gets a new position
            self.rect.x = random.randint(self.x_min, self.x_max)
            self.rect.y = self.y_max

            # Duck moves right and up after respawning
            self.speed_x = abs(self.speed_x)
            self.speed_y = -abs(self.speed_y)