"""
Tutorial/instructions screen.
"""
import pygame
from ..config import constants as C
from ..utils import colors
from .ui_components import Button
from ..core.state_manager import GameState


class TutorialScreen:
    """Tutorial screen explaining controls."""

    def __init__(self):
        self.title_font = pygame.font.SysFont(None, 36)
        self.text_font = pygame.font.SysFont(None, 24)

        self.back_button = Button("Back", C.SCREEN_WIDTH // 2 - C.BUTTON_WIDTH // 2,
                                 C.SCREEN_HEIGHT - 150)

    def update(self, mouse_pos: tuple) -> GameState:
        """
        Update tutorial screen.

        Args:
            mouse_pos: Current mouse position

        Returns:
            New game state
        """
        self.back_button.update(mouse_pos)

        if self.back_button.is_clicked(mouse_pos, pygame.mouse.get_pressed()[0]):
            return GameState.MENU

        return GameState.TUTORIAL

    def draw(self, screen: pygame.Surface):
        """
        Draw tutorial.

        Args:
            screen: Pygame surface to draw on
        """
        # Title
        title = self.title_font.render("How to Play", True, colors.white)
        screen.blit(title, (C.SCREEN_WIDTH // 2 - 100, 50))

        # Instructions (all in English as per user preference)
        instructions = [
            "Controls:",
            "  UP ARROW - Jump",
            "  LEFT ARROW - Move Left",
            "  RIGHT ARROW - Move Right",
            "  P - Pause Game",
            "",
            "Objective:",
            "  Dodge falling meteorites for as long as possible!",
            "",
            "Power-ups:",
            "  Shield - Protects you from one hit",
            "  Slow Motion - Slows down meteorites",
            "  Score Multiplier - Doubles your score",
            "",
            "Difficulty increases over time - good luck!"
        ]

        y = 120
        for line in instructions:
            text = self.text_font.render(line, True, colors.white)
            screen.blit(text, (100, y))
            y += 30

        self.back_button.draw(screen)
