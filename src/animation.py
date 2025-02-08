import pygame

class Animation:
    def __init__(self, sprite_sheet, frame_width, frame_height, animation_speed=10):
        """
        Initialize the animation with a sprite sheet and frame dimensions.
        """
        self.frames = self.load_frames(sprite_sheet, frame_width, frame_height)
        self.current_frame_index = 0
        self.image = self.frames[self.current_frame_index]
        self.animation_timer = 0
        self.animation_speed = animation_speed
        self.facing_right = True  # Default direction

    def load_frames(self, sprite_sheet, frame_width, frame_height):
        """
        Extract frames from a sprite sheet.
        """
        frames = []
        sheet_width, sheet_height = sprite_sheet.get_size()
        
        for x in range(0, sheet_width, frame_width):
            if x + frame_width <= sheet_width:
                frame = sprite_sheet.subsurface((x, 0, frame_width, frame_height))
                frames.append(frame)
        return frames

    def update(self):
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

    def set_direction(self, facing_right):
        """
        Set the direction the animation is facing.
        """
        self.facing_right = facing_right

    def get_current_frame(self):
        """
        Get the current frame of the animation.
        """
        return self.image
