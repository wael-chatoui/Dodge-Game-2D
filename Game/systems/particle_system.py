"""
Particle effects for jumps, collisions, and meteorite trails.
"""
import pygame
import random
from typing import List
from ..config import constants as C


class Particle:
    """Single particle with lifetime."""

    def __init__(self, x: int, y: int, color: tuple, vel_x: float, vel_y: float, lifetime: float):
        """
        Initialize a particle.

        Args:
            x: Initial X position
            y: Initial Y position
            color: RGB color tuple
            vel_x: X velocity
            vel_y: Y velocity
            lifetime: Lifetime in seconds
        """
        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(vel_x, vel_y)
        self.color = color
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.size = random.randint(2, 5)

    def update(self, dt: float) -> bool:
        """
        Update particle, return True if alive.

        Args:
            dt: Delta time in seconds

        Returns:
            True if particle is still alive
        """
        self.lifetime -= dt
        if self.lifetime <= 0:
            return False

        self.pos += self.vel * dt * 60
        self.vel.y += 0.2  # Gravity
        return True

    def draw(self, screen: pygame.Surface):
        """
        Draw particle with fade-out.

        Args:
            screen: Pygame surface to draw on
        """
        alpha = int(255 * (self.lifetime / self.max_lifetime))
        alpha = max(0, min(255, alpha))  # Clamp to 0-255
        color_with_alpha = (*self.color[:3], alpha)

        surf = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(surf, color_with_alpha, (self.size, self.size), self.size)
        screen.blit(surf, (int(self.pos.x) - self.size, int(self.pos.y) - self.size))


class ParticleSystem:
    """Manages all particle effects."""

    def __init__(self):
        self.particles: List[Particle] = []

    def emit_jump(self, x: int, y: int):
        """
        Emit particles when player jumps.

        Args:
            x: Player X position
            y: Player Y position
        """
        for _ in range(10):
            particle = Particle(
                x + random.randint(-20, 20),
                y + C.PLAYER_SIZE,
                (200, 200, 200),
                random.uniform(-2, 2),
                random.uniform(-1, 1),
                random.uniform(0.2, 0.5)
            )
            self.particles.append(particle)

    def emit_collision(self, x: int, y: int):
        """
        Emit particles on collision.

        Args:
            x: Collision X position
            y: Collision Y position
        """
        for _ in range(30):
            particle = Particle(
                x,
                y,
                (255, random.randint(100, 200), 0),
                random.uniform(-5, 5),
                random.uniform(-8, -2),
                random.uniform(0.5, 1.5)
            )
            self.particles.append(particle)

    def emit_meteorite_trail(self, x: int, y: int):
        """
        Emit trail behind falling meteorites.

        Args:
            x: Meteorite X position
            y: Meteorite Y position
        """
        particle = Particle(
            x + C.METEORITE_SIZE // 2 + random.randint(-5, 5),
            y + C.METEORITE_SIZE // 2 + random.randint(-5, 5),
            (255, random.randint(150, 200), 0),
            random.uniform(-0.5, 0.5),
            random.uniform(-1, 1),
            random.uniform(0.3, 0.8)
        )
        self.particles.append(particle)

    def emit_powerup_collect(self, x: int, y: int, color: tuple = (255, 255, 100)):
        """
        Emit particles when power-up is collected.

        Args:
            x: Power-up X position
            y: Power-up Y position
            color: Particle color
        """
        for _ in range(20):
            particle = Particle(
                x,
                y,
                color,
                random.uniform(-4, 4),
                random.uniform(-6, -1),
                random.uniform(0.4, 1.0)
            )
            self.particles.append(particle)

    def update(self, dt: float):
        """
        Update all particles and remove dead ones.

        Args:
            dt: Delta time in seconds
        """
        self.particles = [p for p in self.particles if p.update(dt)]

    def clear(self):
        """Remove all particles."""
        self.particles.clear()

    def draw(self, screen: pygame.Surface):
        """
        Draw all particles.

        Args:
            screen: Pygame surface to draw on
        """
        for particle in self.particles:
            particle.draw(screen)
