import unittest
import pygame
import random
from unittest.mock import patch
from src.duck import Duck, FLYING_WINDOW_HEIGHT, ZIGZAG_CHANGE_CHANCE, SHOT_DISPLAY_TIME

def dummy_load(path):
    """
    A dummy image loader function that returns a pygame.Surface of size 250x90.
    """
    # Create a dummy surface with an alpha channel.
    return pygame.Surface((255, 90), pygame.SRCALPHA)

class DuckTest(unittest.TestCase):
    def setUp(self):
        pygame.init()
        pygame.display.set_mode((800, 600))
        
        # Patch pygame.image.load so that any call returns our dummy surface.
        self.patcher = patch("pygame.image.load", side_effect=dummy_load)
        self.mock_load = self.patcher.start()

        # Set screen dimensions
        self.screen_width = 800
        self.screen_height = 600
        self.sprite_path = "dummy_sprite.png"

        self.duck = Duck(self.screen_width, 360, self.sprite_path, "normal")

    def tearDown(self):
        """
        Stops the override of pygame.image.load and cleans up pygame resources after each test.
        """
        self.patcher.stop()
        pygame.quit()

    def test_initial_spawn(self):
        """
        After creation (with initial_spawn), the duck should be alive and positioned correctly.
        """
        self.assertTrue(self.duck.alive)
        self.assertGreaterEqual(self.duck.rect.x, self.duck.x_min)
        self.assertLessEqual(self.duck.rect.x, self.duck.x_max)
        self.assertEqual(self.duck.rect.y, self.duck.y_max)

    def test_move_changes_position(self):
        """
        Calling move() on an alive duck should change its position.
        """
        initial_pos = (self.duck.rect.x, self.duck.rect.y)
        self.duck.move()
        new_pos = (self.duck.rect.x, self.duck.rect.y)
        self.assertNotEqual(initial_pos, new_pos, "Duck position should change after move()")

    def test_make_duck_fly_off(self):
        """
        make_duck_fly_off() should set flying_off_screen True and ensure speed_y is upward.
        """
        self.duck.make_duck_fly_off()
        self.assertTrue(self.duck.flying_off_screen, "Duck should be marked as flying off screen after make_duck_fly_off()")
        self.assertEqual(self.duck.speed_y, -abs(self.duck.speed_y), 
                         "Duck's vertical speed should be set to a negative value after make_duck_fly_off()")

    def test_respawn_non_initial(self):
        """
        Calling respawn() with initial_spawn=False should move the duck off-screen 
        and mark it as waiting to respawn.
        """
        self.duck.respawn(initial_spawn=False)
        self.assertFalse(self.duck.alive, "Duck should not be alive immediately after a non-initial respawn")
        self.assertTrue(self.duck.waiting_to_respawn, "Duck should be waiting to respawn after non-initial respawn")
        self.assertEqual(self.duck.rect.x, -100)
        self.assertEqual(self.duck.rect.y, -100)

    def test_handle_respawn(self):
        """
        When enough time has passed, handle_respawn() should set waiting_to_respawn to False,
        mark the duck as alive, and reposition it on-screen.
        """
        self.duck.waiting_to_respawn = True
        # Simulate that the respawn delay.
        past_time = pygame.time.get_ticks() - int((self.duck.respawn_delay + 0.1) * 1000)
        self.duck.respawn_timer_start = past_time

        self.duck.handle_respawn()
        self.assertFalse(self.duck.waiting_to_respawn, "Duck should no longer be waiting to respawn after delay")
        self.assertTrue(self.duck.alive, "Duck should be alive after handle_respawn()")

        # The new position should be within valid bounds.
        self.assertGreaterEqual(self.duck.rect.x, self.duck.x_min)
        self.assertLessEqual(self.duck.rect.x, self.duck.x_max)
        self.assertEqual(self.duck.rect.y, self.duck.y_max, "After respawn, duck's y should be at y_max")

    def test_move_when_shot(self):
        """
        When the duck is marked as shot and enough time has passed, move() should trigger
        a respawn and reset the is_shot flag.
        """
        self.duck.is_shot = True
        # Simulate that the shot.
        past_shot_time = pygame.time.get_ticks() - (SHOT_DISPLAY_TIME + 10)
        self.duck.shot_time = past_shot_time

        self.duck.move()
        self.assertFalse(self.duck.is_shot, "Duck should not be marked as shot after move() triggers respawn")

    def test_zigzag_changes_speed(self):
        """
        The move() method has a chance to reverse the vertical speed (zigzag). We force this branch
        by patching random.randint to always return a value that triggers the change.
        """
        original_speed_y = self.duck.speed_y
        with patch('random.randint', return_value=1):
            self.duck.rect.x = (self.duck.x_min + self.duck.x_max) // 2
            self.duck.rect.y = self.duck.y_min + 10
            self.duck.move()
        self.assertEqual(self.duck.speed_y, -original_speed_y,
                         "Duck's vertical speed should be reversed due to zigzag change")

    def test_bounce_off_left_edge(self):
        """
        If the duck is at the left edge and moving left, move() should bounce it off so that
        the horizontal speed is reversed and the duck faces right.
        """
        # Simulate the duck moving left.
        self.duck.speed_x = -3
        self.duck.facing_right = False
        self.duck.rect.x = self.duck.x_min  # at the left boundary
        self.duck.move()
        self.assertEqual(self.duck.speed_x, 3,
                         "After bouncing off the left edge, the duck's horizontal speed should be positive")
        self.assertTrue(self.duck.facing_right,
                        "After bouncing off the left edge, the duck should face right")

    def test_bounce_off_right_edge(self):
        """
        If the duck is at the right edge and moving right, move() should bounce it off so that
        the horizontal speed is reversed and the duck faces left.
        """
        # Simulate the duck moving right.
        self.duck.speed_x = 3
        self.duck.facing_right = True
        self.duck.rect.x = self.duck.x_max  # at the right boundary
        self.duck.move()
        self.assertEqual(self.duck.speed_x, -3,
                         "After bouncing off the right edge, the duck's horizontal speed should be negative")
        self.assertFalse(self.duck.facing_right,
                         "After bouncing off the right edge, the duck should face left")

    def test_bounce_off_bottom_edge(self):
        """
        When the duck reaches (or exceeds) the bottom boundary (y_max), move() should set its
        y position to y_max and adjust the vertical speed.
        """
        # Simulate downward motion.
        self.duck.speed_y = 3
        self.duck.rect.y = self.duck.y_max + 10  # force beyond the bottom boundary
        self.duck.move()
        self.assertEqual(self.duck.rect.y, self.duck.y_max,
                         "Duck's y position should be set to y_max when bouncing off the bottom edge")
        self.assertEqual(self.duck.speed_y, -abs(self.duck.speed_y),
                         "Duck's vertical speed should be set to -abs(speed_y) when bouncing off the bottom edge")

    def test_bounce_off_top_edge(self):
        """
        When the duck goes above the top boundary (y_min), move() should set its vertical speed to
        a positive value.
        """
        self.duck.speed_y = -3
        self.duck.rect.y = self.duck.y_min - 10  # force above the top
        self.duck.move()
        self.assertEqual(self.duck.speed_y, abs(self.duck.speed_y),
                         "Duck's vertical speed should be set to abs(speed_y) when bouncing off the top edge")

if __name__ == "__main__":
    unittest.main()