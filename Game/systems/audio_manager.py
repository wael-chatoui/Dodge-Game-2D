"""
Audio management for music and sound effects.
"""
import pygame
from typing import Optional, Dict
from ..config import constants as C
from ..core.asset_loader import AssetLoader


class AudioManager:
    """Singleton audio manager."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self._initialized = True
        pygame.mixer.init()
        self.asset_loader = AssetLoader()

        self.sounds: Dict[str, Optional[pygame.mixer.Sound]] = {}
        self.music_playing = False
        self.sfx_enabled = True
        self.music_enabled = True

        self._load_audio()

    def _load_audio(self):
        """Load all audio files."""
        # Sound effects
        sfx_files = {
            'jump': C.SFX_JUMP,
            'collision': C.SFX_COLLISION,
            'menu_click': C.SFX_MENU_CLICK,
            'powerup': C.SFX_POWERUP,
            'game_over': C.SFX_GAME_OVER
        }

        for name, path in sfx_files.items():
            sound = self.asset_loader.load_sound(path)
            if sound:
                sound.set_volume(C.SFX_VOLUME)
            self.sounds[name] = sound

    def play_sfx(self, name: str):
        """
        Play a sound effect.

        Args:
            name: Name of the sound effect
        """
        if self.sfx_enabled and name in self.sounds and self.sounds[name]:
            self.sounds[name].play()

    def play_music(self, loop: bool = True):
        """
        Start background music.

        Args:
            loop: If True, loop the music
        """
        if self.music_enabled and not self.music_playing:
            try:
                import os
                if os.path.exists(C.MUSIC_FILE):
                    pygame.mixer.music.load(C.MUSIC_FILE)
                    pygame.mixer.music.set_volume(C.MUSIC_VOLUME)
                    pygame.mixer.music.play(-1 if loop else 0)
                    self.music_playing = True
            except pygame.error as e:
                print(f"WARNING: Could not play music: {e}")

    def stop_music(self):
        """Stop background music."""
        pygame.mixer.music.stop()
        self.music_playing = False

    def toggle_music(self):
        """Toggle music on/off."""
        self.music_enabled = not self.music_enabled
        if self.music_enabled:
            self.play_music()
        else:
            self.stop_music()

    def toggle_sfx(self):
        """Toggle sound effects on/off."""
        self.sfx_enabled = not self.sfx_enabled
