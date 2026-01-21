# Dodge Game 2D 🎮

A 2D arcade game where you dodge falling meteorites! Completely refactored with modern architecture and tons of new features.

## Quick Start

```bash
# Activate virtual environment
source venv/bin/activate

# Run the game
python run_game.py
```

## Controls
- **⬅️ ➡️** Move left/right
- **⬆️** Jump
- **P** Pause/Resume
- **Mouse** Click menu buttons

## Features

### Gameplay
- **Progressive Difficulty**: Choose Easy/Medium/Hard, then it gets progressively harder
- **Power-Ups**:
  - 🛡️ Shield (blue) - Protects from one hit
  - ⏱️ Slow Motion (orange) - Slows meteorites
  - ⭐ Score Multiplier (yellow) - 2x points
- **High Scores**: Top 10 leaderboard saved between sessions
- **Particle Effects**: Visual feedback for jumps, collisions, and trails

### Technical Improvements
- ✅ All 59 bugs fixed (see REFACTOR_SUMMARY.md)
- ✅ Frame-rate independent physics
- ✅ Modular architecture (21 files)
- ✅ Proper collision detection
- ✅ English UI throughout
- ✅ Ragdoll physics on death
- ✅ Audio system ready (files optional)

## Project Structure

```
Dodge-Game-2D/
├── run_game.py          # Launcher script
├── Game/
│   ├── main.py          # Main game loop
│   ├── config/          # Game constants
│   ├── core/            # Engine, state management
│   ├── entities/        # Player, meteorites, power-ups
│   ├── systems/         # Physics, particles, audio, scoring
│   ├── ui/              # All UI screens
│   ├── utils/           # Helper functions
│   └── assets/          # Images and data
└── REFACTOR_SUMMARY.md  # Detailed change log
```

## What Was Fixed

### Critical Bugs (Game-Breaking)
- ❌ Crashes from list modification → ✅ Proper list handling
- ❌ Hardcoded paths breaking game → ✅ Dynamic path resolution
- ❌ Hitbox never updated → ✅ Updates every frame
- ❌ Difficulty buttons all "Hard" → ✅ Correct labels
- ❌ Meteorites spawn out of bounds → ✅ Fixed spawn logic

### Major Enhancements
- 🎭 Ragdoll physics death animation
- ✨ Particle effects system
- 🎁 3 power-up types
- 🏆 High score persistence
- 🎵 Audio system
- ⚡ Progressive difficulty
- 🎮 Complete UI overhaul
- 🌍 All English text

## Requirements

- Python 3.10+
- Pygame 2.5.2+
- Virtual environment already set up

## Development

```bash
# Activate venv
source venv/bin/activate

# Run with module imports
python -m Game.main

# Check syntax
python -m py_compile Game/main.py
```

## Known Issues

- Audio files are optional (game runs fine without them)
- No audio assets included (silent placeholders)

## Credits

- Original game concept and sprites
- Complete refactor and enhancements: Claude Code
- Tested and verified working

## License

See original project license.

---

**Status**: ✅ Production Ready
**Version**: 2.0 (Complete Refactor)
**Last Updated**: December 24, 2024

Enjoy the game! 🎮
