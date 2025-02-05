import pygame

class Music:
    def __init__(self):
        pygame.mixer.init()

        self.title_music = "assets/new_title_screen.mp3"
        self.combo_sound = pygame.mixer.Sound("assets/combo.mp3")
        self.duck_flapping_sound = pygame.mixer.Sound("assets/duck_flapping.mp3")
        self.game_over_sound = pygame.mixer.Sound("assets/game_over.mp3")
        self.gunshot_sound = pygame.mixer.Sound("assets/gunshot.mp3")

        self.combo_sound.set_volume(0.7)
        self.duck_flapping_sound.set_volume(0.5)
        self.gunshot_sound.set_volume(0.8)

    def play_music(self, music_file, loop=True):
        """Play background music."""
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.set_volume(0.5)
        if loop:
            pygame.mixer.music.play(-1)  # Loop the music
        else:
            pygame.mixer.music.play()

    def stop_music(self):
        """Stop the background music."""
        pygame.mixer.music.stop()

    def play_sound(self, sound):
        """Play a sound effect."""
        sound.play()

    def stop_all_sounds(self):
        """Stop all playing sounds."""
        pygame.mixer.stop()