"""
World/level tile rendering system.
"""
import pygame
from ..config import constants as C
from ..core.asset_loader import AssetLoader


class World:
    """Manages level tiles and rendering."""

    def __init__(self, data: list = None):
        """
        Initialize world with tile data.

        Args:
            data: 2D list where 0=empty, 1=dirt, 2=grass
        """
        self.asset_loader = AssetLoader()
        self.tile_list = []

        # Default world data if none provided
        if data is None:
            data = self.get_default_world_data()

        self.data = data
        self._load_tiles()

    def _load_tiles(self):
        """Load and position all tiles based on data."""
        # Load tile images
        dirt_img = self.asset_loader.load_image(C.DIRT_IMAGE, (C.TILE_SIZE, C.TILE_SIZE))
        grass_img = self.asset_loader.load_image(C.GRASS_IMAGE, (C.TILE_SIZE, C.TILE_SIZE))

        row_count = 0
        for row in self.data:
            col_count = 0
            for tile in row:
                if tile == 1:  # Dirt tile
                    img_rect = dirt_img.get_rect()
                    img_rect.x = col_count * C.TILE_SIZE
                    img_rect.y = row_count * C.TILE_SIZE
                    self.tile_list.append((dirt_img, img_rect))
                elif tile == 2:  # Grass tile
                    img_rect = grass_img.get_rect()
                    img_rect.x = col_count * C.TILE_SIZE
                    img_rect.y = row_count * C.TILE_SIZE
                    self.tile_list.append((grass_img, img_rect))
                col_count += 1
            row_count += 1

    def draw(self, screen: pygame.Surface):
        """
        Draw all tiles to the screen.

        Args:
            screen: Pygame surface to draw on
        """
        for tile_image, tile_rect in self.tile_list:
            screen.blit(tile_image, tile_rect)

    @staticmethod
    def get_default_world_data() -> list:
        """
        Get the default world tile data.

        Returns:
            2D list of tile data
        """
        return [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],  # Grass row
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]   # Dirt row
        ]
