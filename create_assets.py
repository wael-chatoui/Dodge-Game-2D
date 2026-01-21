"""
Create placeholder assets for the game.
"""
import pygame
import os

pygame.init()

# Create directories
os.makedirs('Game/assets/powerups', exist_ok=True)
os.makedirs('Game/assets/audio/music', exist_ok=True)
os.makedirs('Game/assets/audio/sfx', exist_ok=True)
os.makedirs('Game/assets/data', exist_ok=True)

# Create power-up images
powerups = {
    'shield': (100, 200, 255),      # Blue
    'slowmo': (255, 200, 100),      # Orange
    'multiplier': (255, 255, 100)   # Yellow
}

for name, color in powerups.items():
    surface = pygame.Surface((40, 40), pygame.SRCALPHA)

    # Draw circle
    pygame.draw.circle(surface, color, (20, 20), 18)
    pygame.draw.circle(surface, (255, 255, 255), (20, 20), 18, 2)

    # Add symbol
    font = pygame.font.SysFont(None, 24)
    if name == 'shield':
        text = font.render('S', True, (255, 255, 255))
    elif name == 'slowmo':
        text = font.render('T', True, (255, 255, 255))
    else:
        text = font.render('X2', True, (255, 255, 255))

    text_rect = text.get_rect(center=(20, 20))
    surface.blit(text, text_rect)

    # Save
    pygame.image.save(surface, f'Game/assets/powerups/{name}.png')
    print(f'Created {name}.png')

print('Placeholder assets created successfully!')
print('Note: Audio files are optional - the game will work without them.')
