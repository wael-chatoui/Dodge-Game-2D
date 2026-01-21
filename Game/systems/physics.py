"""
Physics system for ragdoll and particles.
"""
import pygame
import random
from typing import List
from ..config import constants as C


class RagdollLimb:
    """Individual limb with physics."""

    def __init__(self, x: int, y: int, width: int, height: int, color: tuple):
        """
        Initialize a ragdoll limb.

        Args:
            x: Initial X position
            y: Initial Y position
            width: Limb width
            height: Limb height
            color: RGB color tuple
        """
        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(
            random.uniform(-5, 5),
            random.uniform(-10, -5)
        )
        self.angular_vel = random.uniform(-20, 20)
        self.angle = 0
        self.width = width
        self.height = height
        self.color = color
        self.grounded = False

    def update(self, dt: float):
        """
        Update limb physics.

        Args:
            dt: Delta time in seconds
        """
        if not self.grounded:
            # Gravity
            self.vel.y += C.GRAVITY * dt * 60

            # Update position
            self.pos += self.vel * dt * 60

            # Rotation
            self.angle += self.angular_vel * dt * 10

            # Ground collision
            if self.pos.y >= C.GROUND_LEVEL:
                self.pos.y = C.GROUND_LEVEL
                self.vel.y *= -0.3  # Bounce
                self.vel.x *= 0.8  # Friction
                self.angular_vel *= 0.8

                if abs(self.vel.y) < 1 and abs(self.vel.x) < 0.5:
                    self.grounded = True
                    self.vel.x = 0
                    self.vel.y = 0

    def draw(self, screen: pygame.Surface):
        """
        Draw rotated rectangle.

        Args:
            screen: Pygame surface to draw on
        """
        surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        surf.fill(self.color)
        rotated = pygame.transform.rotate(surf, self.angle)
        rect = rotated.get_rect(center=(int(self.pos.x), int(self.pos.y)))
        screen.blit(rotated, rect)


class Ragdoll:
    """Ragdoll death animation."""

    def __init__(self, player_x: int, player_y: int):
        """
        Initialize ragdoll at player position.

        Args:
            player_x: Player X position
            player_y: Player Y position
        """
        self.limbs: List[RagdollLimb] = []
        self.finished = False

        # Create limbs (simplified character)
        # Head
        self.limbs.append(RagdollLimb(
            player_x + 25, player_y + 10,
            20, 20,
            (255, 220, 177)  # Skin color
        ))

        # Body
        self.limbs.append(RagdollLimb(
            player_x + 25, player_y + 35,
            15, 30,
            (100, 100, 255)  # Blue shirt
        ))

        # Left arm
        self.limbs.append(RagdollLimb(
            player_x + 15, player_y + 30,
            8, 20,
            (255, 220, 177)  # Skin color
        ))

        # Right arm
        self.limbs.append(RagdollLimb(
            player_x + 35, player_y + 30,
            8, 20,
            (255, 220, 177)  # Skin color
        ))

        # Left leg
        self.limbs.append(RagdollLimb(
            player_x + 20, player_y + 55,
            8, 25,
            (100, 100, 255)  # Blue pants
        ))

        # Right leg
        self.limbs.append(RagdollLimb(
            player_x + 30, player_y + 55,
            8, 25,
            (100, 100, 255)  # Blue pants
        ))

    def update(self, dt: float):
        """
        Update all limbs.

        Args:
            dt: Delta time in seconds
        """
        all_grounded = True
        for limb in self.limbs:
            limb.update(dt)
            if not limb.grounded:
                all_grounded = False

        if all_grounded:
            self.finished = True

    def draw(self, screen: pygame.Surface):
        """
        Draw all limbs.

        Args:
            screen: Pygame surface to draw on
        """
        for limb in self.limbs:
            limb.draw(screen)
