"""
Centralized asset loading with error handling and caching.
"""
import pygame
import os
from typing import Dict, Optional, List
from ..config import constants as C


def divide_sprite_sheet(sprite_sheet: pygame.Surface, frame_width: int, frame_height: int) -> List[pygame.Surface]:
    """
    Divide a sprite sheet into individual frames.

    Args:
        sprite_sheet: The sprite sheet image
        frame_width: Width of each frame
        frame_height: Height of each frame

    Returns:
        List of individual frame surfaces
    """
    frames = []
    sheet_width, sheet_height = sprite_sheet.get_size()

    for y in range(0, sheet_height, frame_height):
        for x in range(0, sheet_width, frame_width):
            # Create surface with alpha channel
            frame_surface = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
            frame_surface.blit(sprite_sheet, (0, 0), (x, y, frame_width, frame_height))
            frames.append(frame_surface)

    return frames


class AssetLoader:
    """Singleton asset loader with caching and error handling."""

    _instance = None
    _images: Dict[str, pygame.Surface] = {}
    _sounds: Dict[str, pygame.mixer.Sound] = {}
    _sprite_sheets: Dict[str, List[pygame.Surface]] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def load_image(self, path: str, scale: Optional[tuple] = None) -> pygame.Surface:
        """
        Load image with caching and error handling.

        Args:
            path: Path to the image file
            scale: Optional (width, height) tuple to scale the image

        Returns:
            Loaded image surface or magenta placeholder if failed
        """
        cache_key = f"{path}_{scale}" if scale else path

        if cache_key in self._images:
            return self._images[cache_key]

        try:
            if not os.path.exists(path):
                raise FileNotFoundError(f"Image not found: {path}")

            image = pygame.image.load(path).convert_alpha()

            if scale:
                image = pygame.transform.scale(image, scale)

            self._images[cache_key] = image
            return image

        except (pygame.error, FileNotFoundError) as e:
            print(f"ERROR: Failed to load image {path}: {e}")
            # Return magenta placeholder surface
            size = scale if scale else (C.TILE_SIZE, C.TILE_SIZE)
            placeholder = pygame.Surface(size)
            placeholder.fill((255, 0, 255))  # Magenta for missing assets
            self._images[cache_key] = placeholder
            return placeholder

    def load_sprite_sheet(self, path: str, frame_width: int, frame_height: int) -> List[pygame.Surface]:
        """
        Load and cache sprite sheet.

        Args:
            path: Path to the sprite sheet image
            frame_width: Width of each frame
            frame_height: Height of each frame

        Returns:
            List of frame surfaces
        """
        cache_key = f"{path}_{frame_width}_{frame_height}"

        if cache_key in self._sprite_sheets:
            return self._sprite_sheets[cache_key]

        try:
            sheet_image = self.load_image(path)
            frames = divide_sprite_sheet(sheet_image, frame_width, frame_height)
            self._sprite_sheets[cache_key] = frames
            return frames
        except Exception as e:
            print(f"ERROR: Failed to load sprite sheet {path}: {e}")
            return []

    def load_sound(self, path: str) -> Optional[pygame.mixer.Sound]:
        """
        Load sound with caching and error handling.

        Args:
            path: Path to the sound file

        Returns:
            Sound object or None if failed
        """
        if path in self._sounds:
            return self._sounds[path]

        try:
            if not os.path.exists(path):
                print(f"WARNING: Sound not found: {path}")
                return None

            sound = pygame.mixer.Sound(path)
            self._sounds[path] = sound
            return sound

        except pygame.error as e:
            print(f"WARNING: Failed to load sound {path}: {e}")
            return None

    def preload_all_assets(self):
        """Preload all game assets at startup."""
        print("Loading assets...")

        # Images
        self.load_image(C.SKY_IMAGE)
        self.load_image(C.SUN_IMAGE)
        self.load_image(C.DIRT_IMAGE, (C.TILE_SIZE, C.TILE_SIZE))
        self.load_image(C.GRASS_IMAGE, (C.TILE_SIZE, C.TILE_SIZE))

        # Sprite sheets
        self.load_sprite_sheet(C.PLAYER_SPRITE_SHEET, 24, 23)

        # Rocks
        for i in range(1, 3):
            rock_path = os.path.join(C.ROCKS_DIR, f'rock{i}.png')
            self.load_image(rock_path, (C.METEORITE_SIZE, C.METEORITE_SIZE))

        # Create directories if they don't exist
        os.makedirs(C.POWERUPS_DIR, exist_ok=True)
        os.makedirs(C.AUDIO_DIR, exist_ok=True)
        os.makedirs(C.DATA_DIR, exist_ok=True)

        # Try to load power-up images (optional)
        for powerup in ['shield', 'slowmo', 'multiplier']:
            powerup_path = os.path.join(C.POWERUPS_DIR, f'{powerup}.png')
            if os.path.exists(powerup_path):
                self.load_image(powerup_path, (40, 40))

        print("Assets loaded successfully!")

    def clear_cache(self):
        """Clear all cached assets (useful for testing)."""
        self._images.clear()
        self._sounds.clear()
        self._sprite_sheets.clear()
