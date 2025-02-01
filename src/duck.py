import pygame
import random

class Duck:
    def __init__(self, screen_width, screen_height, sprite_path, duck_type):
        """Initialize the duck with animation and movement"""
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.sprite_sheet = pygame.image.load(sprite_path).convert_alpha()
        self.frames = self.load_frames(self.sprite_sheet, frame_width=85, frame_height=90)
        self.current_frame_index = 0
        self.image = self.frames[self.current_frame_index]
        self.rect = self.image.get_rect()
        self.duck_type = duck_type

        # Define the flying window (800x360)
        self.x_min = 0
        self.x_max = screen_width - self.rect.width
        self.y_min = 0
        self.y_max = 360 - self.rect.height

        # Add movement speed
        self.speed_x = 3
        self.speed_y = -3
        
        self.flying_off_screen = False

        self.facing_right = self.speed_x > 0  # Set direction based on speed

        self.respawn(initial_spawn=True)
        
        # Animation settings
        self.animation_timer = 0
        self.animation_speed = 10
        self.current_frame = 0

        self.waiting_to_respawn = False
        self.respawn_timer_start = None
        self.respawn_delay = 2.0
        self.alive = True

    def load_frames(self, sprite_sheet, frame_width, frame_height):
        """Extract frames from a sprite sheet"""
        frames = []
        sheet_width, sheet_height = sprite_sheet.get_size()
        
        for x in range(0, sheet_width, frame_width):
            if x + frame_width <= sheet_width:
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

    def respawn(self, initial_spawn=False):
        """Respawns the duck at a valid position, either on the first spawn or after a delay."""
        self.waiting_to_respawn = True
        self.respawn_timer_start = pygame.time.get_ticks()

        if initial_spawn:
            # Set the position correctly for the first spawn
            self.rect.x = random.randint(self.x_min, self.x_max)
            self.rect.y = self.y_max
            self.alive = True
            self.waiting_to_respawn = False  # Skip delay for the first appearance
        else:
            # Move the duck off-screen temporarily during the delay
            self.rect.x = -100
            self.rect.y = -100
            self.alive = False

        # Increase speed on every respawn
        self.speed_x *= 1.1
        self.speed_y *= 1.1

        # Ensure the duck keeps moving right and up
        self.speed_x = abs(self.speed_x)
        self.speed_y = -abs(self.speed_y)

    def handle_respawn(self):
        """Respawns the duck after the delay has passed."""
        if self.waiting_to_respawn:
            elapsed_time = (pygame.time.get_ticks() - self.respawn_timer_start) / 1000
            if elapsed_time >= self.respawn_delay:
                self.waiting_to_respawn = False
                self.alive = True

                # Spawn the duck at a random x position and the grass level
                self.rect.x = random.randint(self.x_min, self.x_max)
                self.rect.y = self.y_max

                # Ensure it starts moving right and upwards
                self.speed_x = abs(self.speed_x)  # Start moving right
                self.speed_y = -abs(self.speed_y)  # Start moving upwards
                self.facing_right = True
