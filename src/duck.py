"""
This module defines the Duck class, which encapsulates the behavior
of a duck, including animation, movement, boundary collision (bouncing),
respawn logic, and state changes (e.g., being shot). It supports different duck types
(e.g., "normal", "red", "special") and uses sprite sheets for animation.
"""
import random
import os
import pygame
from src.animation import Animation

ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
# Constants:
FLYING_WINDOW_WIDTH = 800         # Width of the flying window
FLYING_WINDOW_HEIGHT = 360        # Height of the flying window
DEFAULT_SPEED_X = 3               # Initial horizontal speed
DEFAULT_SPEED_Y = -3              # Initial vertical speed
RESPAWN_DELAY = 1.0               # Delay in seconds before a duck respawns
SHOT_DISPLAY_TIME = 350           # Time in milliseconds to display the shot image before respawn
ZIGZAG_CHANGE_CHANCE = 5          # Percentage chance for a zigzag movement


class Duck:
    """
    This class handles the behavior and state of a duck in the game. It is responsible for:
      - Loading the duck sprite and its animations.
      - Managing movement and updating the duck's position based on speed 
        (which can gradually increase).
      - Handling boundary collisions (bouncing off the edges of the flying window).
      - Managing state transitions, such as when the duck is shot and when it should respawn.
      - Supporting different duck types (e.g., "normal", "red", "special") with 
        corresponding shot images.
    """
    def __init__(self, screen_width: int, screen_height: int,
                 sprite_path: str, duck_type: str) -> None:
        """
        Initialize the duck with animation and movement.
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.sprite_sheet = pygame.image.load(sprite_path).convert_alpha()

        # Initialize animation
        self.animation = Animation(self.sprite_sheet, frame_width=85, frame_height=90)
        self.image = self.animation.get_current_frame()
        self.rect = self.image.get_rect()
        self.duck_type = duck_type

        # Define the flying window (800x360)
        self.x_min = 0
        self.x_max = screen_width - self.rect.width
        self.y_min = 0
        self.y_max = FLYING_WINDOW_HEIGHT - self.rect.height

        # Add movement speed
        self.speed_x: float = float(DEFAULT_SPEED_X)
        self.speed_y: float = float(DEFAULT_SPEED_Y)
        self.flying_off_screen = False
        self.facing_right = self.speed_x > 0  # Set direction based on speed
        self.animation.set_direction(self.facing_right)
        self.spawn_time = 0  # Track duck's time on the screen

        self.respawn(initial_spawn=True)
        self.waiting_to_respawn = False
        self.respawn_timer_start: int | None = None
        self.respawn_delay = RESPAWN_DELAY
        self.alive = True

        if self.duck_type == "normal":
            shot_path = os.path.join(ASSETS_DIR, "normal_duck_shot.png")
            self.shot_image = pygame.image.load(shot_path).convert_alpha()
        elif self.duck_type == "red":
            shot_path = os.path.join(ASSETS_DIR, "red_duck_shot.png")
            self.shot_image = pygame.image.load(shot_path).convert_alpha()
        elif self.duck_type == "special":
            shot_path = os.path.join(ASSETS_DIR, "special_duck_shot.png")
            self.shot_image = pygame.image.load(shot_path).convert_alpha()
        self.shot_time: int | None = None  # To track when the duck was shot
        self.is_shot = False  # Indicator if the duck was recently shot

    def make_duck_fly_off(self) -> None:
        """
        Make the duck fly off the screen.
        """
        self.flying_off_screen = True
        self.speed_y = -abs(self.speed_y) # Makes the duck go upwards

    def move(self) -> None:
        """
        Moves the duck and ensures it bounces correctly.
        """
        if self.is_shot:
            # Check if enough time has passed to respawn the duck
            current_time = pygame.time.get_ticks()
            if self.shot_time is not None and current_time - self.shot_time > SHOT_DISPLAY_TIME:
                self.is_shot = False
                self.respawn()
            return
        if self.alive:
            time_on_screen = (pygame.time.get_ticks() - self.spawn_time) / 1000
            if time_on_screen > 5:
                self.make_duck_fly_off()

            self.rect.x += self.speed_x
            self.rect.y += self.speed_y

            # Update animation
            self.animation.update()
            self.image = self.animation.get_current_frame()

            # Handle flying-off-screen condition
            if self.flying_off_screen:
                if (self.rect.y < -self.rect.height or
                        self.rect.x < -self.rect.width or
                        self.rect.x > self.screen_width):
                    self.flying_off_screen = False
                    self.respawn()
                return  # Skip boundary checks if flying off

            # Chance to move on zigzag
            if random.randint(1, 100) < ZIGZAG_CHANGE_CHANCE:
                self.speed_y = -self.speed_y

            # Bounce off the left and right edges
            if self.rect.x <= self.x_min or self.rect.x >= self.x_max:
                self.speed_x = -self.speed_x  # Reverse direction
                self.facing_right = not self.facing_right  # Flip sprite direction
                self.animation.set_direction(self.facing_right)

            # Bounce off the bottom boundary
            if self.rect.y >= self.y_max:
                self.rect.y = self.y_max
                self.speed_y = -abs(self.speed_y)

            # Bounce off the top boundary
            if self.rect.y <= self.y_min:
                self.speed_y = abs(self.speed_y)

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw the duck on the screen
        """
        screen.blit(self.image, self.rect)

    def respawn(self, mode: str = "standard", initial_spawn: bool = False) -> None:
        """
        Respawns the duck at a valid position, either on the first spawn or after a delay.
        """
        self.waiting_to_respawn = True
        self.respawn_timer_start = pygame.time.get_ticks()
        self.flying_off_screen = False

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

        # Increase speed
        if mode == "standard" and not initial_spawn:
            self.speed_x *= 1.1
            self.speed_y *= 1.1

        # Ensure the duck keeps moving right and up
        self.speed_x = abs(self.speed_x)
        self.speed_y = -abs(self.speed_y)

        # Start the timer for flying
        self.spawn_time = pygame.time.get_ticks()

    def handle_respawn(self) -> None:
        """
        Respawns the duck after the delay has passed.
        """
        if self.waiting_to_respawn and self.respawn_timer_start is not None:
            elapsed_time: float = (pygame.time.get_ticks() - self.respawn_timer_start) / 1000.0
            if elapsed_time >= self.respawn_delay:
                self.waiting_to_respawn = False
                self.alive = True
                # Spawn the duck at a random position on the grass level
                self.rect.x = random.randint(self.x_min, self.x_max)
                self.rect.y = self.y_max

                self.speed_x = abs(self.speed_x)  # Ensure it starts moving right
                self.facing_right = True # Ensure it's facing right
                self.animation.set_direction(self.facing_right)  # Update animation direction
                self.speed_y = -abs(self.speed_y)  # Ensure it starts moving upwards
