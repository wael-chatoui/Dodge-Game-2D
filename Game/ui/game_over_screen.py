"""
Game over screen with scores and replay option.
"""
import pygame
from ..config import constants as C
from ..utils import colors
from .ui_components import Button
from ..core.state_manager import GameState


class GameOverScreen:
    """Game over screen."""

    def __init__(self):
        self.title_font = pygame.font.SysFont(None, 48)
        self.text_font = pygame.font.SysFont(None, 24)

        center_x = C.SCREEN_WIDTH // 2 - C.BUTTON_WIDTH // 2

        self.replay_button = Button("Play Again", center_x, C.SCREEN_HEIGHT // 2 + 50)
        self.menu_button = Button("Main Menu", center_x, C.SCREEN_HEIGHT // 2 + 170)

    def update(self, mouse_pos: tuple) -> GameState:
        """
        Update game over screen.

        Args:
            mouse_pos: Current mouse position

        Returns:
            New game state
        """
        self.replay_button.update(mouse_pos)
        self.menu_button.update(mouse_pos)

        mouse_pressed = pygame.mouse.get_pressed()[0]

        if self.replay_button.is_clicked(mouse_pos, mouse_pressed):
            return GameState.DIFFICULTY_SELECT
        elif self.menu_button.is_clicked(mouse_pos, mouse_pressed):
            return GameState.MENU

        return GameState.GAME_OVER

    def draw(self, screen: pygame.Surface, score: int, time: int,
             is_high_score: bool, rank: int, high_scores: list):
        """
        Draw game over screen.

        Args:
            screen: Pygame surface to draw on
            score: Final score
            time: Time survived in seconds
            is_high_score: True if this is a high score
            rank: Rank in high scores (1-10)
            high_scores: List of high score entries
        """
        # Title
        title = self.title_font.render("Game Over", True, colors.red)
        title_rect = title.get_rect(center=(C.SCREEN_WIDTH // 2, 100))
        screen.blit(title, title_rect)

        # Score
        score_text = self.text_font.render(f"Final Score: {score}", True, colors.white)
        score_rect = score_text.get_rect(center=(C.SCREEN_WIDTH // 2, 180))
        screen.blit(score_text, score_rect)

        # Time
        time_text = self.text_font.render(f"Time Survived: {time}s", True, colors.white)
        time_rect = time_text.get_rect(center=(C.SCREEN_WIDTH // 2, 210))
        screen.blit(time_text, time_rect)

        # High score notification
        if is_high_score and rank > 0:
            hs_text = self.title_font.render(f"NEW HIGH SCORE! Rank #{rank}", True, colors.green)
            hs_rect = hs_text.get_rect(center=(C.SCREEN_WIDTH // 2, 260))
            screen.blit(hs_text, hs_rect)

        # Buttons
        self.replay_button.draw(screen)
        self.menu_button.draw(screen)

        # High scores list (right side)
        if high_scores:
            hs_title = self.text_font.render("High Scores", True, colors.white)
            screen.blit(hs_title, (C.SCREEN_WIDTH - 200, 50))

            y = 80
            for i, entry in enumerate(high_scores[:5]):
                text = f"{i+1}. {entry['score']} - {entry['time']}s"
                hs_text = self.text_font.render(text, True, colors.white)
                screen.blit(hs_text, (C.SCREEN_WIDTH - 200, y))
                y += 25
