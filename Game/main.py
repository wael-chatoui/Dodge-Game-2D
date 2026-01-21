"""
Dodge Game 2D - Main entry point
Complete refactor with all systems integrated
"""
import pygame
import sys
from .core.game_engine import GameEngine
from .core.state_manager import StateManager, GameState
from .core.asset_loader import AssetLoader
from .config import constants as C
from .utils import colors

# Import all screens and systems
from .ui.menu import MainMenu, DifficultySelect
from .ui.tutorial_screen import TutorialScreen
from .ui.game_over_screen import GameOverScreen
from .ui.hud import HUD
from .entities.player import Player
from .entities.meteorite import Meteorite
from .entities.world import World
from .entities.powerup import PowerUpManager
from .systems.audio_manager import AudioManager
from .systems.score_manager import ScoreManager
from .systems.difficulty_manager import DifficultyManager
from .systems.particle_system import ParticleSystem
from .systems.physics import Ragdoll


class DodgeGame:
    """Main game class."""

    def __init__(self):
        # Core systems
        self.engine = GameEngine()
        self.state_manager = StateManager()
        self.asset_loader = AssetLoader()
        self.audio = AudioManager()

        # Load assets
        self.asset_loader.preload_all_assets()

        # Background
        self.bg_img = self.asset_loader.load_image(C.SKY_IMAGE)
        self.sun_img = self.asset_loader.load_image(C.SUN_IMAGE)

        # UI screens
        self.main_menu = MainMenu()
        self.difficulty_select = DifficultySelect()
        self.tutorial = TutorialScreen()
        self.game_over_screen = GameOverScreen()
        self.hud = HUD()

        # Game objects (initialized when game starts)
        self.world = World()
        self.player = None
        self.meteorites = []
        self.ragdoll = None

        # Systems
        self.score_manager = ScoreManager()
        self.difficulty_manager = None
        self.powerup_manager = PowerUpManager()
        self.particle_system = ParticleSystem()

        # Game state
        self.countdown_timer = C.COUNTDOWN_DURATION
        self.countdown_start = 0
        self.game_start_time = 0
        self.active_powerups = []
        self.last_jump_state = False  # Track jump for particles

        # Start music
        self.audio.play_music()

    def run(self):
        """Main game loop."""
        while self.engine.running:
            self.engine.update()
            dt = self.engine.get_delta_time()

            # Handle events
            self._handle_events()

            # Update current state
            self._update_state(dt)

            # Draw current state
            self._draw_state()

            pygame.display.flip()

        pygame.quit()
        sys.exit()

    def _handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.engine.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p and self.state_manager.is_state(GameState.PLAYING):
                    self.state_manager.transition_to(GameState.PAUSED)
                    self.audio.play_sfx('menu_click')
                elif event.key == pygame.K_p and self.state_manager.is_state(GameState.PAUSED):
                    self.state_manager.return_to_previous()
                    self.audio.play_sfx('menu_click')

    def _update_state(self, dt: float):
        """Update based on current state."""
        if self.state_manager.is_state(GameState.MENU):
            new_state = self.main_menu.update(pygame.mouse.get_pos())
            if new_state != GameState.MENU:
                if new_state is None:
                    self.engine.running = False
                else:
                    self.state_manager.transition_to(new_state)
                    self.audio.play_sfx('menu_click')

        elif self.state_manager.is_state(GameState.DIFFICULTY_SELECT):
            new_state, difficulty = self.difficulty_select.update(pygame.mouse.get_pos())
            if new_state != GameState.DIFFICULTY_SELECT:
                self.state_manager.transition_to(new_state)
                self.audio.play_sfx('menu_click')
                if difficulty:
                    self._start_game(difficulty)

        elif self.state_manager.is_state(GameState.TUTORIAL):
            new_state = self.tutorial.update(pygame.mouse.get_pos())
            if new_state != GameState.TUTORIAL:
                self.state_manager.transition_to(new_state)
                self.audio.play_sfx('menu_click')

        elif self.state_manager.is_state(GameState.COUNTDOWN):
            self._update_countdown()

        elif self.state_manager.is_state(GameState.PLAYING):
            self._update_game(dt)

        elif self.state_manager.is_state(GameState.GAME_OVER):
            new_state = self.game_over_screen.update(pygame.mouse.get_pos())
            if new_state != GameState.GAME_OVER:
                self.state_manager.transition_to(new_state)
                self.audio.play_sfx('menu_click')

    def _draw_state(self):
        """Draw based on current state."""
        # Background
        self.engine.screen.blit(self.bg_img, (0, 0))
        self.engine.screen.blit(self.sun_img, (100, 100))

        if self.state_manager.is_state(GameState.MENU):
            self.main_menu.draw(self.engine.screen)

        elif self.state_manager.is_state(GameState.DIFFICULTY_SELECT):
            self.difficulty_select.draw(self.engine.screen)

        elif self.state_manager.is_state(GameState.TUTORIAL):
            self.tutorial.draw(self.engine.screen)

        elif self.state_manager.is_state(GameState.COUNTDOWN):
            self._draw_countdown()

        elif self.state_manager.is_state(GameState.PLAYING):
            self._draw_game()

        elif self.state_manager.is_state(GameState.PAUSED):
            self._draw_game()
            self._draw_pause_overlay()

        elif self.state_manager.is_state(GameState.GAME_OVER):
            self._draw_game_over()

    def _start_game(self, difficulty: str):
        """Initialize new game."""
        # Reset systems
        self.score_manager.reset()
        self.difficulty_manager = DifficultyManager(difficulty)
        self.meteorites = []
        self.active_powerups = []
        self.particle_system.clear()
        self.powerup_manager.clear()
        self.ragdoll = None

        # Create player
        self.player = Player(100, C.GROUND_LEVEL)

        # Start countdown
        self.countdown_timer = C.COUNTDOWN_DURATION
        self.countdown_start = pygame.time.get_ticks()
        self.state_manager.transition_to(GameState.COUNTDOWN)

    def _update_countdown(self):
        """FIXED: Actual countdown implementation (was empty in original)."""
        elapsed = (pygame.time.get_ticks() - self.countdown_start) / 1000
        self.countdown_timer = C.COUNTDOWN_DURATION - int(elapsed)

        if self.countdown_timer <= 0:
            self.game_start_time = pygame.time.get_ticks()
            self.state_manager.transition_to(GameState.PLAYING)

    def _update_game(self, dt: float):
        """Update game logic."""
        game_time = (pygame.time.get_ticks() - self.game_start_time) // 1000

        # Update systems
        self.difficulty_manager.update(dt)
        self.score_manager.update(dt)
        self.score_manager.check_multiplier_expiry()

        # Update player
        was_grounded = self.player.grounded
        self.player.update(dt)

        # Emit jump particles
        if was_grounded and not self.player.grounded:
            self.particle_system.emit_jump(self.player.rect.x, self.player.rect.y)
            self.audio.play_sfx('jump')

        # Spawn meteorites
        if self.difficulty_manager.should_spawn_meteorite():
            meteorite = Meteorite(self.world.data)
            meteorite.velocity = self.difficulty_manager.get_meteorite_speed()
            self.meteorites.append(meteorite)

        # Update meteorites (FIXED: No list modification during iteration)
        meteorites_to_remove = []
        for meteorite in self.meteorites:
            meteorite.update(dt)

            # Emit trail particles
            if not meteorite.grounded:
                self.particle_system.emit_meteorite_trail(meteorite.rect.x, meteorite.rect.y)

            # Check collision
            if meteorite.check_collision(self.player.hitbox):
                if self.player.has_shield:
                    # Shield absorbs hit
                    self.player.has_shield = False
                    self.active_powerups = [p for p in self.active_powerups if 'Shield' not in p]
                    meteorites_to_remove.append(meteorite)
                    self.particle_system.emit_collision(meteorite.rect.x, meteorite.rect.y)
                    self.audio.play_sfx('collision')
                else:
                    # Game over
                    self._trigger_game_over()
                    return

            if meteorite.grounded:
                meteorites_to_remove.append(meteorite)
                self.score_manager.add_meteorite_dodge()

        for meteorite in meteorites_to_remove:
            self.meteorites.remove(meteorite)

        # Update power-ups
        self.powerup_manager.update(dt, self.world.data)
        collected = self.powerup_manager.check_collisions(self.player.hitbox)
        for powerup_type in collected:
            self._apply_powerup(powerup_type)

        # Update particles
        self.particle_system.update(dt)

    def _apply_powerup(self, powerup_type):
        """Apply collected power-up."""
        self.audio.play_sfx('powerup')
        self.particle_system.emit_powerup_collect(
            self.player.rect.centerx,
            self.player.rect.centery
        )

        if powerup_type.value == 'shield':
            self.player.has_shield = True
            self.active_powerups.append("Shield Active")
        elif powerup_type.value == 'slowmo':
            # Slow down meteorites temporarily
            for meteorite in self.meteorites:
                meteorite.velocity *= C.SLOWMO_FACTOR
            self.active_powerups.append("Slow Motion")
        elif powerup_type.value == 'multiplier':
            self.score_manager.set_multiplier(C.SCORE_MULTIPLIER, C.MULTIPLIER_DURATION)
            self.active_powerups.append("Score x2")

    def _trigger_game_over(self):
        """Handle game over."""
        self.audio.play_sfx('game_over')
        self.ragdoll = Ragdoll(self.player.rect.x, self.player.rect.y)
        self.particle_system.emit_collision(self.player.rect.centerx, self.player.rect.centery)

        # Animate ragdoll
        start_time = pygame.time.get_ticks()
        while not self.ragdoll.finished and pygame.time.get_ticks() - start_time < 3000:
            dt = self.engine.clock.tick(C.FPS) / 1000.0
            self.ragdoll.update(dt)

            # Draw game with ragdoll
            self.engine.screen.blit(self.bg_img, (0, 0))
            self.engine.screen.blit(self.sun_img, (100, 100))
            self.world.draw(self.engine.screen)

            for meteorite in self.meteorites:
                meteorite.draw(self.engine.screen)

            self.ragdoll.draw(self.engine.screen)
            pygame.display.flip()

        # Save score
        if self.score_manager.is_high_score():
            self.score_manager.save_high_score()

        self.state_manager.transition_to(GameState.GAME_OVER)

    def _draw_game(self):
        """Draw game objects."""
        # World
        self.world.draw(self.engine.screen)

        # Meteorites
        for meteorite in self.meteorites:
            meteorite.draw(self.engine.screen)

        # Power-ups
        self.powerup_manager.draw(self.engine.screen)

        # Particles
        self.particle_system.draw(self.engine.screen)

        # Player or ragdoll
        if self.ragdoll and not self.state_manager.is_state(GameState.PLAYING):
            self.ragdoll.draw(self.engine.screen)
        else:
            self.player.draw(self.engine.screen)

        # HUD
        game_time = (pygame.time.get_ticks() - self.game_start_time) // 1000
        self.hud.draw(
            self.engine.screen,
            self.score_manager.current_score,
            game_time,
            self.score_manager.score_multiplier,
            self.active_powerups
        )

    def _draw_countdown(self):
        """Draw countdown."""
        self.world.draw(self.engine.screen)
        if self.player:
            self.player.draw(self.engine.screen)

        font = pygame.font.SysFont(None, 72)
        if self.countdown_timer > 0:
            text = font.render(str(self.countdown_timer), True, colors.white)
        else:
            text = font.render("GO!", True, colors.green)

        text_rect = text.get_rect(center=(C.SCREEN_WIDTH // 2, C.SCREEN_HEIGHT // 2))
        self.engine.screen.blit(text, text_rect)

    def _draw_pause_overlay(self):
        """Draw pause overlay."""
        overlay = pygame.Surface((C.SCREEN_WIDTH, C.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.engine.screen.blit(overlay, (0, 0))

        font = pygame.font.SysFont(None, 48)
        text = font.render("PAUSED", True, colors.white)
        text_rect = text.get_rect(center=(C.SCREEN_WIDTH // 2, C.SCREEN_HEIGHT // 2))
        self.engine.screen.blit(text, text_rect)

        info_font = pygame.font.SysFont(None, 24)
        info = info_font.render("Press P to resume", True, colors.white)
        info_rect = info.get_rect(center=(C.SCREEN_WIDTH // 2, C.SCREEN_HEIGHT // 2 + 50))
        self.engine.screen.blit(info, info_rect)

    def _draw_game_over(self):
        """Draw game over screen."""
        self.engine.screen.blit(self.bg_img, (0, 0))
        self.engine.screen.blit(self.sun_img, (100, 100))

        game_time = (pygame.time.get_ticks() - self.game_start_time) // 1000
        self.game_over_screen.draw(
            self.engine.screen,
            self.score_manager.current_score,
            game_time,
            self.score_manager.is_high_score(),
            self.score_manager.get_rank(),
            self.score_manager.high_scores
        )


if __name__ == '__main__':
    game = DodgeGame()
    game.run()
