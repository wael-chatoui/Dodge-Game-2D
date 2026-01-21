"""
Collectible power-ups with different effects.
"""
import pygame
import random
import os
from enum import Enum
from typing import List
from ..config import constants as C
from ..core.asset_loader import AssetLoader


class PowerUpType(Enum):
    """Types of power-ups."""
    SHIELD = "shield"
    SLOW_MOTION = "slowmo"
    SCORE_MULTIPLIER = "multiplier"


class PowerUp:
    """Base power-up class."""

    def __init__(self, x: int, y: int, powerup_type: PowerUpType):
        """
        Initialize power-up.

        Args:
            x: X position
            y: Y position
            powerup_type: Type of power-up
        """
        self.type = powerup_type
        self.pos = pygame.math.Vector2(x, y)
        self.asset_loader = AssetLoader()

        # Load image (with fallback to colored circles)
        powerup_path = os.path.join(C.POWERUPS_DIR, f'{powerup_type.value}.png')
        if os.path.exists(powerup_path):
            self.image = self.asset_loader.load_image(powerup_path, (40, 40))
        else:
            # Create simple colored circle as fallback
            self.image = self._create_fallback_image(powerup_type)

        self.rect = self.image.get_rect(center=(int(x), int(y)))
        self.collected = False
        self.lifetime = 10.0  # Despawn after 10 seconds
        self.bob_offset = 0
        self.bob_speed = 3

    def _create_fallback_image(self, powerup_type: PowerUpType) -> pygame.Surface:
        """Create a simple colored circle as fallback image."""
        size = 40
        surface = pygame.Surface((size, size), pygame.SRCALPHA)

        # Different colors for different power-ups
        colors = {
            PowerUpType.SHIELD: (100, 200, 255),      # Blue
            PowerUpType.SLOW_MOTION: (255, 200, 100), # Orange
            PowerUpType.SCORE_MULTIPLIER: (255, 255, 100)  # Yellow
        }
        color = colors.get(powerup_type, (255, 255, 255))

        pygame.draw.circle(surface, color, (size // 2, size // 2), size // 2)
        pygame.draw.circle(surface, (255, 255, 255), (size // 2, size // 2), size // 2, 2)

        return surface

    def update(self, dt: float):
        """
        Update power-up animation.

        Args:
            dt: Delta time in seconds
        """
        self.lifetime -= dt

        # Bobbing animation
        self.bob_offset += self.bob_speed * dt
        bob_y = 5 * pygame.math.Vector2(0, 1).rotate(self.bob_offset * 50).y
        self.rect.centery = int(self.pos.y + bob_y)

    def check_collision(self, player_hitbox: pygame.Rect) -> bool:
        """
        Check if player collected this power-up.

        Args:
            player_hitbox: Player's hitbox

        Returns:
            True if collected
        """
        if not self.collected and self.rect.colliderect(player_hitbox):
            self.collected = True
            return True
        return False

    def is_expired(self) -> bool:
        """Check if power-up should despawn."""
        return self.lifetime <= 0 or self.collected

    def draw(self, screen: pygame.Surface):
        """
        Draw power-up with glow effect.

        Args:
            screen: Pygame surface to draw on
        """
        if not self.collected:
            # Glow effect
            glow_surf = pygame.Surface((60, 60), pygame.SRCALPHA)
            glow_alpha = int(100 + 50 * pygame.math.Vector2(0, 1).rotate(self.bob_offset * 100).y)
            pygame.draw.circle(glow_surf, (255, 255, 0, max(0, min(255, glow_alpha))), (30, 30), 25)
            screen.blit(glow_surf, (self.rect.centerx - 30, self.rect.centery - 30))

            # Power-up sprite
            screen.blit(self.image, self.rect)


class PowerUpManager:
    """Manages spawning and updating power-ups."""

    def __init__(self):
        self.powerups: List[PowerUp] = []
        self.spawn_timer = 0.0

    def update(self, dt: float, world_data: list):
        """
        Update all power-ups and spawn new ones.

        Args:
            dt: Delta time in seconds
            world_data: World tile data for spawn positioning
        """
        self.spawn_timer += dt

        # Spawn new power-up
        if self.spawn_timer >= 1.0:
            self.spawn_timer = 0.0
            if random.random() < C.POWERUP_SPAWN_CHANCE:
                self._spawn_random_powerup(world_data)

        # Update existing power-ups
        for powerup in self.powerups[:]:
            powerup.update(dt)
            if powerup.is_expired():
                self.powerups.remove(powerup)

    def _spawn_random_powerup(self, world_data: list):
        """Spawn a random power-up at a random location."""
        max_tiles = len(world_data[0])
        spawn_x = random.randint(1, max_tiles - 1) * C.TILE_SIZE + C.TILE_SIZE // 2
        spawn_y = C.GROUND_LEVEL - 100

        powerup_type = random.choice(list(PowerUpType))
        powerup = PowerUp(spawn_x, spawn_y, powerup_type)
        self.powerups.append(powerup)

    def check_collisions(self, player_hitbox: pygame.Rect) -> List[PowerUpType]:
        """
        Check if player collected any power-ups.

        Args:
            player_hitbox: Player's hitbox

        Returns:
            List of collected power-up types
        """
        collected = []
        for powerup in self.powerups:
            if powerup.check_collision(player_hitbox):
                collected.append(powerup.type)
        return collected

    def clear(self):
        """Remove all power-ups."""
        self.powerups.clear()

    def draw(self, screen: pygame.Surface):
        """
        Draw all active power-ups.

        Args:
            screen: Pygame surface to draw on
        """
        for powerup in self.powerups:
            powerup.draw(screen)
