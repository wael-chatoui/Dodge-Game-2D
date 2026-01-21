"""
Reusable UI components.
"""
import pygame
from ..config import constants as C
from ..utils import colors


class Button:
    """Clickable button with hover effect."""

    def __init__(self, text: str, x: int, y: int, width: int = None, height: int = None):
        """
        Initialize button.

        Args:
            text: Button text
            x: X position
            y: Y position
            width: Button width (uses constant if not provided)
            height: Button height (uses constant if not provided)
        """
        self.text = text
        self.width = width or C.BUTTON_WIDTH
        self.height = height or C.BUTTON_HEIGHT
        self.rect = pygame.Rect(x, y, self.width, self.height)

        self.normal_color = colors.red
        self.hover_color = (255, 100, 100)
        self.text_color = colors.white

        self.font = pygame.font.SysFont(None, C.MENU_TEXT_SIZE)
        self.hovered = False
        self.clicked_this_frame = False

    def update(self, mouse_pos: tuple):
        """
        Update hover state.

        Args:
            mouse_pos: Current mouse position (x, y)
        """
        self.hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, mouse_pos: tuple, mouse_pressed: bool) -> bool:
        """
        Check if button was clicked this frame.

        Args:
            mouse_pos: Current mouse position
            mouse_pressed: True if mouse button is pressed

        Returns:
            True if button was clicked
        """
        if self.hovered and mouse_pressed and not self.clicked_this_frame:
            self.clicked_this_frame = True
            return True
        elif not mouse_pressed:
            self.clicked_this_frame = False
        return False

    def draw(self, screen: pygame.Surface):
        """
        Draw button.

        Args:
            screen: Pygame surface to draw on
        """
        color = self.hover_color if self.hovered else self.normal_color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, colors.white, self.rect, 3)

        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)


def render_text(screen: pygame.Surface, text: str, x: int, y: int,
                font_size: int = 24, color: tuple = (255, 255, 255),
                center: bool = False):
    """
    Render text to screen.

    Args:
        screen: Pygame surface to draw on
        text: Text to render
        x: X position
        y: Y position
        font_size: Font size
        color: RGB color tuple
        center: If True, center text at (x, y)
    """
    font = pygame.font.SysFont(None, font_size)
    text_surf = font.render(text, True, color)
    if center:
        text_rect = text_surf.get_rect(center=(x, y))
        screen.blit(text_surf, text_rect)
    else:
        screen.blit(text_surf, (x, y))
