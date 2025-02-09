import unittest
import pygame
from unittest.mock import patch
from src.gameplay import Gameplay

class DummyDuck:
    def __init__(self, duck_type="normal"):
        self.duck_type = duck_type
        self.alive = True
        self.facing_right = True
        self.image = None
        # Creating a dummy shot image
        self.shot_image = pygame.Surface((85, 90))
        self.rect = pygame.Rect(100, 100, 85, 90)
        self.speed_x = 3
        self.speed_y = -3
        self.waiting_to_respawn = False
        self.shot_time = None
        self.is_shot = False

    def respawn(self, mode="standard"):
        self.alive = True
        self.rect.topleft = (100, 100)

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def handle_respawn(self):
        pass

    def make_duck_fly_off(self):
        self.alive = False

class DummyMusicManager:
    def __init__(self):
        self.gunshot_sound = "gunshot"
        self.combo_sound = "combo"
        self.game_over_sound = "game_over"
        self.last_sound = None

    def play_sound(self, sound):
        self.last_sound = sound

class DummyUI:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font

    def draw_standard_ui(self, score, lives, shots_remaining):
        pass

    def draw_time_ui(self, score, remaining_time):
        pass

class DummySetup:
    def __init__(self):
        self.screen = pygame.Surface((800, 600))
        self.background = pygame.Surface((800, 600))
        self.font = pygame.font.SysFont("Arial", 30)
        self.scope = pygame.Surface((40, 40))
        self.ducks = [DummyDuck(), DummyDuck()]
        self.music_manager = DummyMusicManager()

    def get_screen(self):
        return self.screen

    def get_background(self):
        return self.background

    def get_font(self):
        return self.font

    def get_scope(self):
        return self.scope

    def get_ducks(self):
        return self.ducks

    def get_music_manager(self):
        return self.music_manager

    def change_background(self):
        return "dummy_background.png"

class DummyMenu:
    def __init__(self, screen, clock, background, change_background):
        self.background = background
        self.chosen_mode = "standard"

    def display(self):
        pass

class DummyGameOver:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock

    def display(self, score):
        return "TestPlayer"

    def save_new_score(self, filename, score, player_name):
        self.saved = True

class TestGameplay(unittest.TestCase):
    def setUp(self):
        pygame.init()
        pygame.display.set_mode((800, 600))
        # Patching Setup, Menu, GameOver, and UI so that Gameplay uses our dummy classes
        patcher_setup = patch("src.gameplay.Setup", new=DummySetup)
        self.addCleanup(patcher_setup.stop)
        patcher_setup.start()

        patcher_menu = patch("src.gameplay.Menu", new=DummyMenu)
        self.addCleanup(patcher_menu.stop)
        patcher_menu.start()

        patcher_gameover = patch("src.gameplay.GameOver", new=DummyGameOver)
        self.addCleanup(patcher_gameover.stop)
        patcher_gameover.start()

        patcher_ui = patch("src.gameplay.UI", new=DummyUI)
        self.addCleanup(patcher_ui.stop)
        patcher_ui.start()

        # Create a Gameplay object in standard mode
        self.gameplay = Gameplay(mode="standard")

    def tearDown(self):
        pygame.quit()

    def test_award_milestone_bonus(self):
        """
        Test that a bonus is awarded correctly after reaching a hit milestone.
        """
        self.gameplay.duck_hits = 5
        initial_score = self.gameplay.score
        self.gameplay.award_milestone_bonus()
        # Bonus must be 105
        self.assertEqual(self.gameplay.score, initial_score + 105)

    def test_switch_duck_with_delay(self):
        """
        Test that after the delay expires, the duck is switched.
        """
        self.gameplay.new_duck_timer_start = pygame.time.get_ticks() - 3000  # 3 seconds ago
        old_duck = self.gameplay.current_duck
        self.gameplay.switch_duck_with_delay()
        self.assertIsNone(self.gameplay.new_duck_timer_start)
        # Check that the new duck is respawned.
        self.assertTrue(self.gameplay.current_duck.alive)
        self.assertEqual(self.gameplay.current_duck.rect.topleft, (100, 100))

    def test_reset_game(self):
        """
        Test that reset_game resets the score, hit count, and initializes lives and shots.
        """
        self.gameplay.score = 500
        self.gameplay.duck_hits = 10
        self.gameplay.lives = 1
        self.gameplay.reset_game()
        self.assertEqual(self.gameplay.score, 0)
        self.assertEqual(self.gameplay.duck_hits, 0)
        self.assertEqual(self.gameplay.current_duck.speed_x, 3)
        self.assertEqual(self.gameplay.current_duck.speed_y, -3)
        self.assertTrue(self.gameplay.running)
        if self.gameplay.mode == "standard":
            self.assertEqual(self.gameplay.lives, 3)
            self.assertEqual(self.gameplay.shots_remaining, 3)

    def test_process_hit(self):
        """
        Test that when a hit occurs, points are awarded and the duck is marked as shot.
        """
        self.gameplay.current_duck.duck_type = "normal"
        initial_score = self.gameplay.score
        self.gameplay.duck_hits = 4  # After the hit, duck_hits becomes 5 and than the bonus is awarded
        self.gameplay.process_hit(play_combo_sound=True)
        # For a normal duck: base points (50) + bonus (105) = 155 points
        self.assertEqual(self.gameplay.score, initial_score + 155)
        self.assertTrue(self.gameplay.current_duck.is_shot)
        self.assertIsNotNone(self.gameplay.current_duck.shot_time)
        self.assertEqual(self.gameplay.shots_remaining, 3)

    def test_check_shooting_hit(self):
        """
        Test that clicking on the duck is processed correctly.
        """
        self.gameplay.current_duck.rect = pygame.Rect(100, 100, 85, 90)
        self.gameplay.check_shooting((110, 110))
        # In standard mode, on a hit the shots are reseted to 3 and points are awarded
        self.assertEqual(self.gameplay.shots_remaining, 3)
        self.assertEqual(self.gameplay.score, 50)

    def test_check_shooting_miss(self):
        """
        Test that on a miss, shots are reduced and, when they reach zero, a life is lost and shots reset.
        """
        self.gameplay.current_duck.rect = pygame.Rect(100, 100, 85, 90)
        self.gameplay.shots_remaining = 1
        self.gameplay.lives = 3
        self.gameplay.check_shooting((10, 10))
        # Expected lives to drop from 3 to 2 and shots to be reset to 3.
        self.assertEqual(self.gameplay.lives, 2)
        self.assertEqual(self.gameplay.shots_remaining, 3)

    def test_update_standard_game_over(self):
        """
        Test that in standard mode, when lives reach 0, handle_game_over() is called.
        """
        self.gameplay.lives = 0
        self.gameplay.game_over_flag = False
        with patch.object(self.gameplay, "handle_game_over") as mock_handle_game_over:
            self.gameplay.update()
            mock_handle_game_over.assert_called_once()

    def test_update_time_mode_game_over(self):
        """
        Test that in time mode, when time runs out, handle_game_over() is called.
        """
        self.gameplay.mode = "time"
        self.gameplay.start_time = pygame.time.get_ticks() - 61000  # 61 seconds have passed
        self.gameplay.total_time = 60
        self.gameplay.game_over_flag = False
        with patch.object(self.gameplay, "handle_game_over") as mock_handle_game_over:
            self.gameplay.update()
            mock_handle_game_over.assert_called_once()

if __name__ == "__main__":
    unittest.main()