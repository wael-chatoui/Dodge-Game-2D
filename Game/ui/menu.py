"""
Main menu and difficulty selection.
"""
import pygame
from ..config import constants as C
from ..utils import colors
from .ui_components import Button, render_text
from ..core.state_manager import GameState


class MainMenu:
    """Main menu screen."""

    def __init__(self):
        self.title_font = pygame.font.SysFont(None, C.MENU_TITLE_SIZE)

        # Buttons centered on screen
        center_x = C.SCREEN_WIDTH // 2 - C.BUTTON_WIDTH // 2
        start_y = C.SCREEN_HEIGHT // 2 - 50

        self.play_button = Button("Play", center_x, start_y)
        self.tutorial_button = Button("Tutorial", center_x, start_y + C.BUTTON_HEIGHT + C.BUTTON_PADDING)
        self.quit_button = Button("Quit", center_x, start_y + 2 * (C.BUTTON_HEIGHT + C.BUTTON_PADDING))

    def update(self, mouse_pos: tuple) -> GameState:
        """
        Update menu, return new state if button clicked.

        Args:
            mouse_pos: Current mouse position

        Returns:
            New game state or current state
        """
        self.play_button.update(mouse_pos)
        self.tutorial_button.update(mouse_pos)
        self.quit_button.update(mouse_pos)

        mouse_pressed = pygame.mouse.get_pressed()[0]

        if self.play_button.is_clicked(mouse_pos, mouse_pressed):
            return GameState.DIFFICULTY_SELECT
        elif self.tutorial_button.is_clicked(mouse_pos, mouse_pressed):
            return GameState.TUTORIAL
        elif self.quit_button.is_clicked(mouse_pos, mouse_pressed):
            return None  # Signal to quit

        return GameState.MENU

    def draw(self, screen: pygame.Surface):
        """
        Draw menu.

        Args:
            screen: Pygame surface to draw on
        """
        # Title
        title = self.title_font.render("Dodge Game 2D", True, colors.white)
        title_rect = title.get_rect(center=(C.SCREEN_WIDTH // 2, 100))
        screen.blit(title, title_rect)

        # Buttons
        self.play_button.draw(screen)
        self.tutorial_button.draw(screen)
        self.quit_button.draw(screen)


class DifficultySelect:
    """Difficulty selection screen."""

    def __init__(self):
        self.title_font = pygame.font.SysFont(None, 36)

        center_x = C.SCREEN_WIDTH // 2 - C.BUTTON_WIDTH // 2
        start_y = 200

        # FIXED: Buttons now have correct labels (was all "Hard" in original)
        self.easy_button = Button("Easy", center_x, start_y)
        self.medium_button = Button("Medium", center_x, start_y + C.BUTTON_HEIGHT + C.BUTTON_PADDING)
        self.hard_button = Button("Hard", center_x, start_y + 2 * (C.BUTTON_HEIGHT + C.BUTTON_PADDING))
        self.back_button = Button("Back", center_x, start_y + 3 * (C.BUTTON_HEIGHT + C.BUTTON_PADDING))

        self.selected_difficulty = None

    def update(self, mouse_pos: tuple) -> tuple:
        """
        Update difficulty select, return (new_state, difficulty).

        Args:
            mouse_pos: Current mouse position

        Returns:
            Tuple of (new_state, difficulty_string)
        """
        self.easy_button.update(mouse_pos)
        self.medium_button.update(mouse_pos)
        self.hard_button.update(mouse_pos)
        self.back_button.update(mouse_pos)

        mouse_pressed = pygame.mouse.get_pressed()[0]

        if self.easy_button.is_clicked(mouse_pos, mouse_pressed):
            return (GameState.COUNTDOWN, 'easy')
        elif self.medium_button.is_clicked(mouse_pos, mouse_pressed):
            return (GameState.COUNTDOWN, 'medium')
        elif self.hard_button.is_clicked(mouse_pos, mouse_pressed):
            return (GameState.COUNTDOWN, 'hard')
        elif self.back_button.is_clicked(mouse_pos, mouse_pressed):
            return (GameState.MENU, None)

        return (GameState.DIFFICULTY_SELECT, None)

    def draw(self, screen: pygame.Surface):
        """
        Draw difficulty selection.

        Args:
            screen: Pygame surface to draw on
        """
        title = self.title_font.render("Select Difficulty", True, colors.white)
        title_rect = title.get_rect(center=(C.SCREEN_WIDTH // 2, 100))
        screen.blit(title, title_rect)

        self.easy_button.draw(screen)
        self.medium_button.draw(screen)
        self.hard_button.draw(screen)
        self.back_button.draw(screen)
