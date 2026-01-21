"""
Meteorite entity with proper collision detection.
"""
import pygame
import random
import os
from ..config import constants as C
from ..core.asset_loader import AssetLoader


class Meteorite:
    """Falling meteorite obstacle."""

    def __init__(self, world_data: list, velocity: float = None):
        """
        Initialize meteorite.

        Args:
            world_data: World tile data to determine spawn range
            velocity: Fall speed (negative number), uses base if not provided
        """
        self.asset_loader = AssetLoader()

        # FIXED: Proper spawn position calculation (0-based index)
        max_tiles = len(world_data[0])
        spawn_tile = random.randint(0, max_tiles - 1)  # FIXED: was random.randint(1, max_tiles)
        self.pos = pygame.math.Vector2(
            spawn_tile * C.TILE_SIZE,
            -C.METEORITE_SIZE  # Start above screen
        )

        # Load random rock image
        rock_num = random.randint(1, 2)
        rock_path = os.path.join(C.ROCKS_DIR, f'rock{rock_num}.png')
        self.image = self.asset_loader.load_image(rock_path, (C.METEORITE_SIZE, C.METEORITE_SIZE))

        # Visual rect
        self.rect = pygame.Rect(
            int(self.pos.x),
            int(self.pos.y),
            C.METEORITE_SIZE,
            C.METEORITE_SIZE
        )

        # FIXED: Hitbox centered on meteorite
        hitbox_offset_x = (C.METEORITE_SIZE - C.METEORITE_HITBOX_WIDTH) // 2
        hitbox_offset_y = (C.METEORITE_SIZE - C.METEORITE_HITBOX_HEIGHT) // 2
        self.hitbox = pygame.Rect(
            int(self.pos.x) + hitbox_offset_x,
            int(self.pos.y) + hitbox_offset_y,
            C.METEORITE_HITBOX_WIDTH,
            C.METEORITE_HITBOX_HEIGHT
        )

        self.velocity = velocity if velocity is not None else C.METEORITE_BASE_VELOCITY
        self.grounded = False
        self.rotation = random.randint(0, 360)
        self.rotation_speed = random.uniform(-5, 5)

    def update(self, dt: float):
        """
        Update position and rotation.

        Args:
            dt: Delta time in seconds
        """
        if not self.grounded:
            # Fall (velocity is negative, so subtract to move down)
            self.pos.y -= self.velocity * dt * 60

            # Rotate
            self.rotation += self.rotation_speed

            # Update rects - FIXED: Update every frame
            self.rect.x = int(self.pos.x)
            self.rect.y = int(self.pos.y)

            hitbox_offset_x = (C.METEORITE_SIZE - C.METEORITE_HITBOX_WIDTH) // 2
            hitbox_offset_y = (C.METEORITE_SIZE - C.METEORITE_HITBOX_HEIGHT) // 2
            self.hitbox.x = int(self.pos.x) + hitbox_offset_x
            self.hitbox.y = int(self.pos.y) + hitbox_offset_y

            # Check ground collision
            if self.pos.y >= C.GROUND_LEVEL:
                self.grounded = True
                self.pos.y = C.GROUND_LEVEL

    def check_collision(self, player_hitbox: pygame.Rect) -> bool:
        """
        FIXED: Proper hitbox collision detection.

        Args:
            player_hitbox: Player's hitbox rectangle

        Returns:
            True if collision detected
        """
        return self.hitbox.colliderect(player_hitbox) and not self.grounded

    def draw(self, screen: pygame.Surface, debug: bool = False):
        """
        Draw meteorite with rotation.

        Args:
            screen: Pygame surface to draw on
            debug: If True, draw hitbox outline
        """
        if not self.grounded:
            # Rotate image
            rotated_image = pygame.transform.rotate(self.image, self.rotation)
            rotated_rect = rotated_image.get_rect(center=self.rect.center)
            screen.blit(rotated_image, rotated_rect)

            if debug:
                pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)
                pygame.draw.rect(screen, (255, 255, 0), self.rect, 1)
