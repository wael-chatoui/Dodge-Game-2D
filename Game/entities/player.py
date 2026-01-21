"""
Player entity with proper hitbox, animations, and physics.
"""
import pygame
from enum import Enum
from ..config import constants as C
from ..core.asset_loader import AssetLoader


class PlayerState(Enum):
    """Player animation states."""
    IDLE_RIGHT = 0
    IDLE_LEFT = 1
    RUNNING_RIGHT = 2
    RUNNING_LEFT = 3


class Player:
    """Player character with animations and physics."""

    def __init__(self, x: int, y: int):
        self.asset_loader = AssetLoader()

        # Load animations
        self._load_animations()

        # Position and physics
        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(0, 0)

        # Sprite and hitbox
        self.image = self.animations[PlayerState.IDLE_RIGHT][0]
        self.rect = pygame.Rect(int(x), int(y), C.PLAYER_SIZE, C.PLAYER_SIZE)

        # FIXED: Hitbox that updates every frame
        self.hitbox = pygame.Rect(
            int(x) + C.PLAYER_HITBOX_OFFSET_X,
            int(y) + C.PLAYER_HITBOX_OFFSET_Y,
            C.PLAYER_HITBOX_WIDTH,
            C.PLAYER_HITBOX_HEIGHT
        )

        # State
        self.state = PlayerState.IDLE_RIGHT
        self.grounded = False
        self.can_jump = True

        # Animation
        self.frame_index = 0
        self.animation_timer = 0.0

        # Power-ups
        self.has_shield = False
        self.is_invincible = False

    def _load_animations(self):
        """Load all animation frames."""
        frames = self.asset_loader.load_sprite_sheet(C.PLAYER_SPRITE_SHEET, 24, 23)

        self.animations = {
            PlayerState.IDLE_RIGHT: [],
            PlayerState.IDLE_LEFT: [],
            PlayerState.RUNNING_RIGHT: [],
            PlayerState.RUNNING_LEFT: []
        }

        # Idle frames (0-3)
        for i in range(C.IDLE_ANIMATION_FRAMES):
            if i < len(frames):
                img = pygame.transform.scale(frames[i], (C.PLAYER_SIZE, C.PLAYER_SIZE))
                img_left = pygame.transform.flip(img, True, False)
                self.animations[PlayerState.IDLE_RIGHT].append(img)
                self.animations[PlayerState.IDLE_LEFT].append(img_left)

        # Running frames (4-13)
        for i in range(C.WALK_ANIMATION_FRAMES):
            frame_idx = i + 4
            if frame_idx < len(frames):
                img = pygame.transform.scale(frames[frame_idx], (C.PLAYER_SIZE, C.PLAYER_SIZE))
                img_left = pygame.transform.flip(img, True, False)
                self.animations[PlayerState.RUNNING_RIGHT].append(img)
                self.animations[PlayerState.RUNNING_LEFT].append(img_left)

    def update(self, dt: float):
        """
        Update player state, physics, and animation.

        Args:
            dt: Delta time in seconds
        """
        self._handle_input(dt)
        self._apply_physics(dt)
        self._update_animation(dt)
        self._update_hitbox()  # FIXED: Always update hitbox

    def _handle_input(self, dt: float):
        """Process keyboard input."""
        keys = pygame.key.get_pressed()

        # Horizontal movement
        dx = 0
        moving = False

        if keys[pygame.K_LEFT] and self.pos.x > 0:
            dx = -C.PLAYER_SPEED
            moving = True
            if self.grounded:
                self.state = PlayerState.RUNNING_LEFT
        elif keys[pygame.K_RIGHT] and self.pos.x < C.SCREEN_WIDTH - C.PLAYER_SIZE:
            dx = C.PLAYER_SPEED
            moving = True
            if self.grounded:
                self.state = PlayerState.RUNNING_RIGHT

        if not moving and self.grounded:
            # Return to idle when no input
            if self.state == PlayerState.RUNNING_LEFT:
                self.state = PlayerState.IDLE_LEFT
            elif self.state == PlayerState.RUNNING_RIGHT:
                self.state = PlayerState.IDLE_RIGHT

        self.vel.x = dx

        # Jump
        if keys[pygame.K_UP] and self.can_jump and self.grounded:
            self.vel.y = C.JUMP_VELOCITY
            self.grounded = False
            self.can_jump = False

        # Reset jump when key released
        if not keys[pygame.K_UP]:
            self.can_jump = True

    def _apply_physics(self, dt: float):
        """Apply gravity and update position."""
        # Gravity
        self.vel.y += C.GRAVITY * dt * 60
        self.vel.y = min(self.vel.y, C.MAX_FALL_SPEED)

        # Update position
        self.pos.x += self.vel.x * dt * 60
        self.pos.y += self.vel.y * dt * 60

        # Ground collision
        if self.pos.y >= C.GROUND_LEVEL:
            self.pos.y = C.GROUND_LEVEL
            self.vel.y = 0
            self.grounded = True
        else:
            self.grounded = False

        # Update rect
        self.rect.x = int(self.pos.x)
        self.rect.y = int(self.pos.y)

    def _update_animation(self, dt: float):
        """Update animation frame."""
        self.animation_timer += dt

        # FIXED: Proper frame indexing with bounds checking
        if self.animation_timer >= C.WALK_ANIMATION_COOLDOWN / 1000.0:
            self.animation_timer = 0
            frames = self.animations.get(self.state, [])
            if frames:
                self.frame_index = (self.frame_index + 1) % len(frames)
                self.image = frames[self.frame_index]

    def _update_hitbox(self):
        """Update hitbox position to follow player."""
        self.hitbox.x = self.rect.x + C.PLAYER_HITBOX_OFFSET_X
        self.hitbox.y = self.rect.y + C.PLAYER_HITBOX_OFFSET_Y

    def reset_position(self, x: int, y: int):
        """
        Reset player to a specific position.

        Args:
            x: X coordinate
            y: Y coordinate
        """
        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(0, 0)
        self.rect.x = int(x)
        self.rect.y = int(y)
        self._update_hitbox()
        self.grounded = False
        self.state = PlayerState.IDLE_RIGHT
        self.frame_index = 0

    def draw(self, screen: pygame.Surface, debug: bool = False):
        """
        Draw player and optionally hitbox.

        Args:
            screen: Pygame surface to draw on
            debug: If True, draw hitbox outline
        """
        screen.blit(self.image, self.rect)

        # Draw shield effect if active
        if self.has_shield:
            shield_surf = pygame.Surface((C.PLAYER_SIZE + 10, C.PLAYER_SIZE + 10), pygame.SRCALPHA)
            pygame.draw.circle(shield_surf, (100, 200, 255, 100),
                             (C.PLAYER_SIZE // 2 + 5, C.PLAYER_SIZE // 2 + 5),
                             C.PLAYER_SIZE // 2 + 5)
            screen.blit(shield_surf, (self.rect.x - 5, self.rect.y - 5))

        if debug:
            pygame.draw.rect(screen, (0, 255, 0), self.hitbox, 2)
            pygame.draw.rect(screen, (255, 0, 0), self.rect, 1)
