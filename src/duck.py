import pygame
import random

class Duck:
    def __init__(self, screen_width, screen_height, sprite_path):
        """Initialize the duck with animation and movement"""
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Load the sprite sheet and extract frames
        self.sprite_sheet = pygame.image.load(sprite_path).convert_alpha()
        self.frames = self.load_frames(self.sprite_sheet, frame_width=85, frame_height=90)
        self.current_frame_index = 0
        self.image = self.frames[self.current_frame_index]
        self.rect = self.image.get_rect()

        # Define the flying window (800x360)
        self.x_min = 0
        self.x_max = screen_width - self.rect.width
        self.y_min = 0
        self.y_max = 360 - self.rect.height

        # Add movement speed
        self.speed_x = 3
        self.speed_y = -3

        self.alive = True  # Tracks if the duck is visible or not
        self.flying_off_screen = False

        self.facing_right = self.speed_x > 0  # Set direction based on speed

        self.respawn()  # Set initial position at the grass level
        
        # Animation settings
        self.animation_timer = 0
        self.animation_speed = 10
        self.current_frame = 0

    def load_frames(self, sprite_sheet, frame_width, frame_height):
        """Extract frames from a sprite sheet"""
        frames = []
        sheet_width, sheet_height = sprite_sheet.get_size()
        
        for x in range(0, sheet_width, frame_width):
            if x + frame_width <= sheet_width:  # Prevent out-of-bounds frame extraction
                frame = sprite_sheet.subsurface((x, 0, frame_width, frame_height))
                frames.append(frame)
        return frames

    def make_duck_fly_off(self):
        """Make the duck fly off the screen"""
        self.flying_off_screen = True
        self.speed_y = -abs(self.speed_y) # Makes the duck go upwards

    def move(self):
        """Moves the duck and ensures it bounces correctly"""
        if self.alive:
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y

            # Update animation
            self.animation_timer += 1
            if self.animation_timer >= self.animation_speed:
                self.current_frame_index = (self.current_frame_index + 1) % len(self.frames)
                self.image = self.frames[self.current_frame_index]

                # Flip the image if facing left
                if not self.facing_right:
                    self.image = pygame.transform.flip(self.image, True, False)

                self.animation_timer = 0

            # Handle flying-off-screen condition
            if self.flying_off_screen:
                if (self.rect.y < -self.rect.height or
                        self.rect.x < -self.rect.width or
                        self.rect.x > self.screen_width):
                    self.flying_off_screen = False
                    self.respawn()
                return  # Skip boundary checks if flying off

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
