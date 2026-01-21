"""
Sprite sheet utilities - improved transparency handling.

Note: The main sprite sheet loading is handled by asset_loader.py.
This module provides backward compatibility and standalone utilities.
"""
import pygame
from typing import List


def divide_sprite_sheet(sprite_sheet: pygame.Surface, frame_width: int, frame_height: int) -> List[pygame.Surface]:
    """
    Divide a sprite sheet into individual frames with proper alpha transparency.

    Args:
        sprite_sheet: The sprite sheet image
        frame_width: Width of each frame
        frame_height: Height of each frame

    Returns:
        List of individual frame surfaces with alpha channel
    """
    frames = []
    sheet_width, sheet_height = sprite_sheet.get_size()

    for y in range(0, sheet_height, frame_height):
        for x in range(0, sheet_width, frame_width):
            # Create surface with alpha channel (FIXED: was using colorkey before)
            frame_surface = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
            frame_surface.blit(sprite_sheet, (0, 0), (x, y, frame_width, frame_height))
            frames.append(frame_surface)

    return frames


# Backward compatibility with French function name (from original code)
diviser_sprite_sheet = divide_sprite_sheet
