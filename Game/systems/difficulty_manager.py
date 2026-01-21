"""
Progressive difficulty scaling system.
"""
import random
from ..config import constants as C


class DifficultyManager:
    """Manages difficulty progression during gameplay."""

    def __init__(self, initial_difficulty: str = 'medium'):
        """
        Initialize difficulty manager.

        Args:
            initial_difficulty: 'easy', 'medium', or 'hard'
        """
        self.difficulty_name = initial_difficulty
        self.settings = self._get_difficulty_settings(initial_difficulty)

        # Current values (will change during game)
        self.spawn_rate = self.settings['spawn_rate']
        self.fall_speed = self.settings['fall_speed']

        # Progression timers
        self.time_elapsed = 0.0
        self.last_spawn_increase = 0.0
        self.last_speed_increase = 0.0

    def _get_difficulty_settings(self, difficulty: str) -> dict:
        """
        Get difficulty preset.

        Args:
            difficulty: Difficulty name

        Returns:
            Dictionary of difficulty settings
        """
        presets = {
            'easy': C.DIFFICULTY_EASY,
            'medium': C.DIFFICULTY_MEDIUM,
            'hard': C.DIFFICULTY_HARD
        }
        return presets.get(difficulty, C.DIFFICULTY_MEDIUM)

    def update(self, dt: float):
        """
        Update difficulty progression.

        Args:
            dt: Delta time in seconds
        """
        self.time_elapsed += dt

        # Increase spawn rate every second
        if self.time_elapsed - self.last_spawn_increase >= 1.0:
            self.last_spawn_increase = self.time_elapsed
            self.spawn_rate *= self.settings['spawn_increase_rate']
            self.spawn_rate = max(5, self.spawn_rate)  # Minimum spawn rate

        # Increase fall speed every 10 seconds
        if self.time_elapsed - self.last_speed_increase >= 10.0:
            self.last_speed_increase = self.time_elapsed
            self.fall_speed -= self.settings['speed_increase_rate']
            self.fall_speed = max(-20, self.fall_speed)  # Maximum fall speed

    def should_spawn_meteorite(self) -> bool:
        """
        Check if a meteorite should spawn this frame.

        Returns:
            True if meteorite should spawn
        """
        return random.randint(1, max(1, int(self.spawn_rate))) == 1

    def get_meteorite_speed(self) -> float:
        """
        Get current meteorite fall speed.

        Returns:
            Fall speed (negative number)
        """
        return self.fall_speed
