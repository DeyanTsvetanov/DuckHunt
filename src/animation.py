"""
This module provides an Animation class for handling sprite sheet animations in the DuckHunt game.
"""
import pygame

class Animation:
    """
    This class handles the extraction and updating of frames from a sprite sheet.
    It loads the frames, updates the current frame based on a timer, and allows flipping
    the image based on the direction.
    """
    def __init__(self, sprite_sheet: pygame.Surface, frame_width: int,
                 frame_height: int, animation_speed: int = 10) -> None:
        """
        Initialize the animation with a sprite sheet and frame dimensions.
        """
        self.frames = self.load_frames(sprite_sheet, frame_width, frame_height)
        self.current_frame_index = 0
        self.image = self.frames[self.current_frame_index]
        self.animation_timer = 0
        self.animation_speed = animation_speed
        self.facing_right = True  # Default direction

    def load_frames(self, sprite_sheet: pygame.Surface,
                    frame_width: int, frame_height: int) -> list[pygame.Surface]:
        """
        Extract frames from a sprite sheet.
        """
        frames = []
        sheet_width, _ = sprite_sheet.get_size()

        for x in range(0, sheet_width, frame_width):
            if x + frame_width <= sheet_width:
                frame = sprite_sheet.subsurface((x, 0, frame_width, frame_height))
                frames.append(frame)
        return frames

    def update(self) -> None:
        """
        Update the animation by advancing to the next frame if enough time has passed.
        """
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.current_frame_index = (self.current_frame_index + 1) % len(self.frames)
            self.image = self.frames[self.current_frame_index]
            # Flip the image if facing left
            if not self.facing_right:
                self.image = pygame.transform.flip(self.image, True, False)
            self.animation_timer = 0

    def set_direction(self, facing_right: bool) -> None:
        """
        Set the direction the animation is facing.
        """
        self.facing_right = facing_right

    def get_current_frame(self) -> pygame.Surface:
        """
        Get the current frame of the animation.
        """
        return self.image
