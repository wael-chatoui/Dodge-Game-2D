"""
Game constants - all magic numbers centralized here.
"""
import os

# Display Settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TILE_SIZE = 50

# Physics
GRAVITY = 1
MAX_FALL_SPEED = 50
JUMP_VELOCITY = -15
PLAYER_SPEED = 6

# Player
PLAYER_SIZE = 70
PLAYER_HITBOX_OFFSET_X = 10
PLAYER_HITBOX_OFFSET_Y = 5
PLAYER_HITBOX_WIDTH = 50
PLAYER_HITBOX_HEIGHT = 60

# Ground
GROUND_LEVEL = SCREEN_HEIGHT - 160

# Meteorite
METEORITE_SIZE = TILE_SIZE
METEORITE_HITBOX_WIDTH = 30
METEORITE_HITBOX_HEIGHT = 30
METEORITE_BASE_VELOCITY = -8

# Animation
WALK_ANIMATION_COOLDOWN = 8
IDLE_ANIMATION_FRAMES = 4
WALK_ANIMATION_FRAMES = 10

# Difficulty Presets
DIFFICULTY_EASY = {
    'spawn_rate': 60,
    'fall_speed': -6,
    'spawn_increase_rate': 0.995,  # Multiply spawn_rate by this each second
    'speed_increase_rate': 0.05    # Add to fall_speed each 10 seconds
}

DIFFICULTY_MEDIUM = {
    'spawn_rate': 40,
    'fall_speed': -8,
    'spawn_increase_rate': 0.99,
    'speed_increase_rate': 0.08
}

DIFFICULTY_HARD = {
    'spawn_rate': 20,
    'fall_speed': -10,
    'spawn_increase_rate': 0.985,
    'speed_increase_rate': 0.12
}

# Power-ups
POWERUP_SPAWN_CHANCE = 0.02  # 2% chance per second
POWERUP_DURATION = 5000  # milliseconds
SHIELD_DURATION = 8000
SLOWMO_DURATION = 5000
SLOWMO_FACTOR = 0.5
MULTIPLIER_DURATION = 10000
SCORE_MULTIPLIER = 2.0

# Score
SCORE_PER_SECOND = 10
METEORITE_DODGE_BONUS = 50

# Audio
MUSIC_VOLUME = 0.3
SFX_VOLUME = 0.5

# Get the base directory (Game folder)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Asset Paths (relative to BASE_DIR)
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
IMG_DIR = os.path.join(ASSETS_DIR, 'img')
SPRITES_DIR = os.path.join(ASSETS_DIR, 'Sprites')
ROCKS_DIR = os.path.join(ASSETS_DIR, 'rocks')
AUDIO_DIR = os.path.join(ASSETS_DIR, 'audio')
POWERUPS_DIR = os.path.join(ASSETS_DIR, 'powerups')
DATA_DIR = os.path.join(ASSETS_DIR, 'data')

# Files
HIGHSCORE_FILE = os.path.join(DATA_DIR, 'highscores.json')
PLAYER_SPRITE_SHEET = os.path.join(SPRITES_DIR, 'doux.png')
SKY_IMAGE = os.path.join(IMG_DIR, 'sky.png')
SUN_IMAGE = os.path.join(IMG_DIR, 'sun.png')
DIRT_IMAGE = os.path.join(IMG_DIR, 'dirt.png')
GRASS_IMAGE = os.path.join(IMG_DIR, 'grass.png')

# Audio files
MUSIC_FILE = os.path.join(AUDIO_DIR, 'music', 'background.ogg')
SFX_JUMP = os.path.join(AUDIO_DIR, 'sfx', 'jump.wav')
SFX_COLLISION = os.path.join(AUDIO_DIR, 'sfx', 'collision.wav')
SFX_MENU_CLICK = os.path.join(AUDIO_DIR, 'sfx', 'menu_click.wav')
SFX_POWERUP = os.path.join(AUDIO_DIR, 'sfx', 'powerup_collect.wav')
SFX_GAME_OVER = os.path.join(AUDIO_DIR, 'sfx', 'game_over.wav')

# UI
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 100
BUTTON_PADDING = 20
MENU_TITLE_SIZE = 48
MENU_TEXT_SIZE = 24
HUD_TEXT_SIZE = 24

# Countdown
COUNTDOWN_DURATION = 3  # seconds
