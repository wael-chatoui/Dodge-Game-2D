"""
In-game HUD displaying score, time, power-ups.
"""
import pygame
from ..config import constants as C
from ..utils import colors


class HUD:
    """Heads-up display during gameplay."""

    def __init__(self):
        self.font = pygame.font.SysFont(None, C.HUD_TEXT_SIZE)

    def draw(self, screen: pygame.Surface, score: int, time: int,
             multiplier: float, active_powerups: list):
        """
        Draw HUD elements.

        Args:
            screen: Pygame surface to draw on
            score: Current score
            time: Time survived in seconds
            multiplier: Score multiplier
            active_powerups: List of active power-up names
        """
        # Score (top left)
        score_text = self.font.render(f"Score: {score}", True, colors.white)
        screen.blit(score_text, (10, 10))

        # Time (top right) - FIXED: Now resets properly between games
        time_text = self.font.render(f"Time: {time}s", True, colors.white)
        time_rect = time_text.get_rect(topright=(C.SCREEN_WIDTH - 10, 10))
        screen.blit(time_text, time_rect)

        # Multiplier (if active)
        if multiplier > 1.0:
            mult_text = self.font.render(f"x{multiplier:.1f}", True, colors.yellow)
            screen.blit(mult_text, (10, 40))

        # Active power-ups (bottom left)
        y_offset = C.SCREEN_HEIGHT - 40
        for powerup in active_powerups:
            powerup_text = self.font.render(powerup, True, colors.green)
            screen.blit(powerup_text, (10, y_offset))
            y_offset -= 25
