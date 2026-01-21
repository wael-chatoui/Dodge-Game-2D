"""
Main game engine with delta time support.
"""
import pygame
from ..config import constants as C


class GameEngine:
    """Core game engine managing the main loop."""

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Dodge Game 2D")

        self.screen = pygame.display.set_mode((C.SCREEN_WIDTH, C.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.delta_time = 0.0  # seconds since last frame
        self.running = True

    def update(self):
        """Update delta time - call once per frame."""
        # Convert milliseconds to seconds and cap at 0.05 (20 FPS minimum)
        dt_ms = self.clock.tick(C.FPS)
        self.delta_time = min(dt_ms / 1000.0, 0.05)

    def get_delta_time(self) -> float:
        """
        Get time elapsed since last frame in seconds.

        Returns:
            Delta time in seconds
        """
        return self.delta_time

    def quit(self):
        """Clean up and quit the game."""
        pygame.quit()
        self.running = False
